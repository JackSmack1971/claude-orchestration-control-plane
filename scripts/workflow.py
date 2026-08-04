#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".workflow"
ARTIFACTS = RUNTIME / "artifacts"
STATE_PATH = RUNTIME / "state.json"
EVENTS_PATH = RUNTIME / "events.jsonl"
WORKFLOW_PATH = ROOT / "orchestration" / "workflow.json"
TEMPLATES = ROOT / "orchestration" / "templates"
CHECKS_PATH = ROOT / ".claude" / "project-checks.json"


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def event(kind: str, **data: Any) -> None:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    row = {"time": now(), "event": kind, **data}
    with EVENTS_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")


def workflow() -> dict[str, Any]:
    return load_json(WORKFLOW_PATH)


def state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        fail("No active workflow. Run `python3 scripts/workflow.py init --goal ...` first.")
    return load_json(STATE_PATH)


def save_state(s: dict[str, Any]) -> None:
    s["updated_at"] = now()
    write_json(STATE_PATH, s)


def fail(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def copy_template(src_name: str, dst_name: str) -> None:
    src = TEMPLATES / src_name
    dst = ARTIFACTS / dst_name
    if not dst.exists():
        shutil.copyfile(src, dst)


def init_run(goal: str, force: bool = False) -> None:
    if STATE_PATH.exists() and not force:
        fail("A workflow is already active. Use `status`, or pass --force to replace it.")
    if force and RUNTIME.exists():
        shutil.rmtree(RUNTIME)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    copy_template("ideation.md", "ideation.md")
    s = {
        "version": 1,
        "goal": goal,
        "state": workflow()["initial_state"],
        "current_phase_index": 0,
        "created_at": now(),
        "updated_at": now(),
        "active_task": None,
        "completed_tasks": [],
        "task_evidence": {},
    }
    write_json(STATE_PATH, s)
    event("workflow_initialized", goal=goal, state=s["state"])
    print(f"Initialized workflow in {RUNTIME} at state {s['state']}.")


def heading_exists(text: str, heading: str) -> bool:
    needle = heading.strip().lower()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip().lower()
            if title == needle:
                return True
    return False


def validate_markdown(path: Path, headings: list[str]) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing artifact: {path.name}"]
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    found: dict[str, int] = {}
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            found[stripped.lstrip("#").strip().lower()] = i
    for heading in headings:
        key = heading.strip().lower()
        if key not in found:
            errors.append(f"{path.name}: missing heading `{heading}`")
            continue
        start = found[key] + 1
        end = len(lines)
        for j in range(start, len(lines)):
            if lines[j].strip().startswith("#"):
                end = j
                break
        content = [line.strip() for line in lines[start:end] if line.strip() and not line.strip().startswith("<!--")]
        if not content:
            errors.append(f"{path.name}: section `{heading}` is empty")
    if len(text.strip()) < 40:
        errors.append(f"{path.name}: artifact is effectively empty")
    return errors


def validate_task_graph(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return ["missing artifact: task-graph.json"]
    try:
        data = load_json(path)
    except Exception as exc:
        return [f"task-graph.json: invalid JSON: {exc}"]
    phases = data.get("phases")
    tasks = data.get("tasks")
    if not isinstance(phases, list) or not phases:
        errors.append("task-graph.json: `phases` must be a non-empty list")
    if not isinstance(tasks, list) or not tasks:
        errors.append("task-graph.json: `tasks` must be a non-empty list")
        return errors
    phase_ids = {p.get("id") for p in phases if isinstance(p, dict)}
    phase_order = {p.get("id"): i for i, p in enumerate(phases) if isinstance(p, dict)}
    phase_graph: dict[str, list[str]] = {}
    for phase in phases:
        if not isinstance(phase, dict) or not phase.get("id"):
            errors.append("task-graph.json: every phase requires a non-empty id")
            continue
        deps = phase.get("depends_on", [])
        if not isinstance(deps, list):
            errors.append(f"phase {phase.get('id')}: depends_on must be a list")
            deps = []
        phase_graph[phase["id"]] = deps
    for pid, deps in phase_graph.items():
        for dep in deps:
            if dep not in phase_ids:
                errors.append(f"phase {pid}: unknown dependency {dep}")
            elif phase_order.get(dep, -1) >= phase_order.get(pid, 0):
                errors.append(f"phase {pid}: dependency {dep} must precede it")
    phase_visiting: set[str] = set()
    phase_visited: set[str] = set()
    def phase_dfs(node: str) -> None:
        if node in phase_visiting:
            errors.append(f"phase dependency cycle detected at {node}")
            return
        if node in phase_visited:
            return
        phase_visiting.add(node)
        for dep in phase_graph.get(node, []):
            if dep in phase_graph:
                phase_dfs(dep)
        phase_visiting.remove(node)
        phase_visited.add(node)
    for pid in phase_graph:
        phase_dfs(pid)
    ids: set[str] = set()
    required = {
        "id", "phase", "objective", "dependencies", "files_likely_affected", "test_first",
        "implementation", "verification", "acceptance_criteria", "non_goals"
    }
    graph: dict[str, list[str]] = {}
    for task in tasks:
        if not isinstance(task, dict):
            errors.append("task-graph.json: every task must be an object")
            continue
        missing = sorted(required - set(task))
        if missing:
            errors.append(f"task {task.get('id', '<unknown>')}: missing {', '.join(missing)}")
        tid = task.get("id")
        if not isinstance(tid, str) or not tid:
            errors.append("task-graph.json: task id must be non-empty string")
            continue
        if tid in ids:
            errors.append(f"duplicate task id: {tid}")
        ids.add(tid)
        if task.get("phase") not in phase_ids:
            errors.append(f"task {tid}: unknown phase {task.get('phase')}")
        deps = task.get("dependencies", [])
        if not isinstance(deps, list):
            errors.append(f"task {tid}: dependencies must be a list")
            deps = []
        graph[tid] = deps
        if not str(task.get("objective", "")).strip():
            errors.append(f"task {tid}: objective must be non-empty")
        if not task.get("verification"):
            errors.append(f"task {tid}: verification must be non-empty")
        if not task.get("acceptance_criteria"):
            errors.append(f"task {tid}: acceptance_criteria must be non-empty")
        if not str(task.get("test_first", "")).strip() and not str(task.get("tdd_exception", "")).strip():
            errors.append(f"task {tid}: test_first required unless tdd_exception is documented")
    task_map = {t.get("id"): t for t in tasks if isinstance(t, dict) and t.get("id")}
    for tid, deps in graph.items():
        for dep in deps:
            if dep not in ids:
                errors.append(f"task {tid}: unknown dependency {dep}")
                continue
            task_phase = task_map.get(tid, {}).get("phase")
            dep_phase = task_map.get(dep, {}).get("phase")
            if task_phase in phase_order and dep_phase in phase_order and phase_order[dep_phase] > phase_order[task_phase]:
                errors.append(f"task {tid}: dependency {dep} belongs to a later phase")
    visiting: set[str] = set()
    visited: set[str] = set()
    def dfs(node: str) -> None:
        if node in visiting:
            errors.append(f"task dependency cycle detected at {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for dep in graph.get(node, []):
            if dep in graph:
                dfs(dep)
        visiting.remove(node)
        visited.add(node)
    for tid in graph:
        dfs(tid)
    return sorted(set(errors))


def validate_current(s: dict[str, Any]) -> list[str]:
    wf = workflow()
    st = s["state"]
    errors: list[str] = []
    for name in wf.get("artifact_requirements", {}).get(st, []):
        path = ARTIFACTS / name
        if name == "task-graph.json":
            errors.extend(validate_task_graph(path))
        else:
            errors.extend(validate_markdown(path, wf.get("artifact_headings", {}).get(name, [])))
    if st == "PHASE_DECOMPOSITION" and (ARTIFACTS / "task-graph.json").exists():
        try:
            graph = load_json(ARTIFACTS / "task-graph.json")
            phase_files = sorted((ARTIFACTS / "phases").glob("*.md")) if (ARTIFACTS / "phases").exists() else []
            if len(phase_files) < len(graph.get("phases", [])):
                errors.append("phase decomposition: fewer phase artifacts than phases in task graph")
            for phase_file in phase_files[:len(graph.get("phases", []))]:
                errors.extend(validate_markdown(phase_file, ["Objective", "Dependencies", "System state after this phase", "Tasks", "Exit Criteria"]))
        except Exception as exc:
            errors.append(f"phase decomposition validation failed: {exc}")
    return errors


def prepare_for_state(st: str, s: dict[str, Any]) -> None:
    mapping = {
        "PROBLEM_DEFINITION": ("problem.md", "problem.md"),
        "RESEARCH": ("research.md", "research.md"),
        "EVIDENCE_SYNTHESIS": ("synthesis.md", "synthesis.md"),
        "PLAN_V1": ("plan.md", "plan-v1.md"),
        "CRITIQUE_1": ("critique-v1.md", "critique-v1.md"),
        "TARGETED_RESEARCH": ("research-delta.md", "research-delta.md"),
        "PLAN_V2": ("plan.md", "plan-v2.md"),
        "CRITIQUE_2": ("critique-v2.md", "critique-v2.md"),
        "PLAN_FINAL": ("plan.md", "plan-final.md"),
        "PHASE_DECOMPOSITION": ("task-graph.json", "task-graph.json"),
    }
    if st in mapping:
        copy_template(*mapping[st])
    if st == "PHASE_DECOMPOSITION":
        phases = ARTIFACTS / "phases"
        phases.mkdir(exist_ok=True)
        phase_path = phases / "phase-01.md"
        if not phase_path.exists():
            shutil.copyfile(TEMPLATES / "phase.md", phase_path)


def get_graph() -> dict[str, Any]:
    path = ARTIFACTS / "task-graph.json"
    errors = validate_task_graph(path)
    if errors:
        fail("Task graph invalid:\n- " + "\n- ".join(errors))
    return load_json(path)


def phase_tasks(graph: dict[str, Any], phase_id: str) -> list[dict[str, Any]]:
    return [t for t in graph["tasks"] if t["phase"] == phase_id]


def current_phase_id(s: dict[str, Any], graph: dict[str, Any]) -> str:
    phases = graph["phases"]
    idx = int(s.get("current_phase_index", 0))
    if idx >= len(phases):
        fail("Current phase index is outside task graph.")
    return phases[idx]["id"]


def phase_complete(s: dict[str, Any], graph: dict[str, Any], phase_id: str) -> bool:
    required = {t["id"] for t in phase_tasks(graph, phase_id)}
    return required.issubset(set(s.get("completed_tasks", [])))


def advance() -> None:
    s = state()
    st = s["state"]
    wf = workflow()
    errors = validate_current(s)
    if errors:
        fail("Current stage is not ready:\n- " + "\n- ".join(errors))

    if st in wf["linear_transitions"]:
        nxt = wf["linear_transitions"][st]
        s["state"] = nxt
        if nxt == "EXECUTION":
            graph = get_graph()
            s["current_phase_index"] = 0
            s["active_task"] = None
            s["completed_tasks"] = []
            s["task_evidence"] = {}
            event("entered_execution", phase=current_phase_id(s, graph))
        save_state(s)
        prepare_for_state(nxt, s)
        event("state_transition", from_state=st, to_state=nxt)
        print(f"Advanced: {st} → {nxt}")
        return

    if st == "EXECUTION":
        graph = get_graph()
        phase = current_phase_id(s, graph)
        if s.get("active_task"):
            fail(f"Cannot leave EXECUTION while task {s['active_task']} is active.")
        if not phase_complete(s, graph, phase):
            incomplete = [t["id"] for t in phase_tasks(graph, phase) if t["id"] not in s.get("completed_tasks", [])]
            fail("Current phase is incomplete: " + ", ".join(incomplete))
        review_name = f"phase-review-{phase.lower()}.md"
        review_path = ARTIFACTS / review_name
        if not review_path.exists():
            shutil.copyfile(TEMPLATES / "phase-review.md", review_path)
        s["state"] = "PHASE_REVIEW"
        save_state(s)
        event("state_transition", from_state="EXECUTION", to_state="PHASE_REVIEW", phase=phase)
        print(f"Advanced: EXECUTION → PHASE_REVIEW ({phase})")
        return

    if st == "PHASE_REVIEW":
        graph = get_graph()
        phase = current_phase_id(s, graph)
        review_name = f"phase-review-{phase.lower()}.md"
        review_errors = validate_markdown(
            ARTIFACTS / review_name,
            ["Phase", "Exit criteria evidence", "Verification commands and outcomes", "Residual risks", "Verdict"],
        )
        if review_errors:
            fail("Phase review is not ready:\n- " + "\n- ".join(review_errors))
        idx = int(s.get("current_phase_index", 0))
        if idx + 1 < len(graph["phases"]):
            s["current_phase_index"] = idx + 1
            s["state"] = "EXECUTION"
            save_state(s)
            next_phase = current_phase_id(s, graph)
            event("state_transition", from_state="PHASE_REVIEW", to_state="EXECUTION", phase=next_phase)
            print(f"Advanced: PHASE_REVIEW → EXECUTION ({next_phase})")
        else:
            s["state"] = "FINAL_VERIFICATION"
            save_state(s)
            event("state_transition", from_state="PHASE_REVIEW", to_state="FINAL_VERIFICATION")
            print("Advanced: PHASE_REVIEW → FINAL_VERIFICATION")
        return

    if st == "FINAL_VERIFICATION":
        path = ARTIFACTS / "final-verification.json"
        if not path.exists():
            fail("Run `python3 scripts/workflow.py final-verify` first.")
        data = load_json(path)
        if not data.get("passed"):
            fail("Final verification contains failed required checks.")
        s["state"] = "COMPLETE"
        save_state(s)
        event("state_transition", from_state="FINAL_VERIFICATION", to_state="COMPLETE")
        print("Advanced: FINAL_VERIFICATION → COMPLETE")
        return

    if st == "COMPLETE":
        print("Workflow is already COMPLETE.")
        return

    fail(f"No transition rule for state {st}.")



def validate_stage() -> None:
    s = state()
    errors = validate_current(s)
    if errors:
        fail("Current stage is not ready:\n- " + "\n- ".join(errors))
    print(f"Current stage {s['state']} is valid.")

def print_status() -> None:
    s = state()
    print(json.dumps(s, indent=2))
    errors = validate_current(s)
    if errors:
        print("\nCurrent gate issues:")
        for err in errors:
            print(f"- {err}")


def task_by_id(graph: dict[str, Any], task_id: str) -> dict[str, Any]:
    for task in graph["tasks"]:
        if task["id"] == task_id:
            return task
    fail(f"Unknown task: {task_id}")
    raise AssertionError


def task_start(task_id: str) -> None:
    s = state()
    if s["state"] != "EXECUTION":
        fail("Tasks can only start in EXECUTION state.")
    if s.get("active_task"):
        fail(f"Task {s['active_task']} is already active.")
    graph = get_graph()
    task = task_by_id(graph, task_id)
    phase = current_phase_id(s, graph)
    if task["phase"] != phase:
        fail(f"Task {task_id} belongs to {task['phase']}; current phase is {phase}.")
    completed = set(s.get("completed_tasks", []))
    missing = [d for d in task.get("dependencies", []) if d not in completed]
    if missing:
        fail("Task dependencies incomplete: " + ", ".join(missing))
    if task_id in completed:
        fail(f"Task {task_id} is already complete.")
    s["active_task"] = task_id
    s["task_state"] = "SELECTED"
    s.setdefault("task_evidence", {})[task_id] = {"checks": []}
    save_state(s)
    event("task_started", task=task_id, phase=phase)
    print(f"Started {task_id} in SELECTED state.")


def task_state(target: str) -> None:
    s = state()
    task_id = s.get("active_task")
    if not task_id:
        fail("No active task.")
    sequence = workflow()["tdd_states"]
    current = s.get("task_state")
    if target not in sequence:
        fail(f"Unknown TDD state {target}.")
    if target == "COMPLETE":
        fail("Use task-complete to enforce completion evidence.")
    ci = sequence.index(current)
    ti = sequence.index(target)
    allowed_exception_skip = False
    if current == "TEST_WRITTEN" and target == "IMPLEMENT_MINIMAL":
        graph = get_graph()
        task = task_by_id(graph, task_id)
        allowed_exception_skip = bool(str(task.get("tdd_exception", "")).strip())
    if ti != ci + 1 and not allowed_exception_skip:
        fail(f"Invalid TDD transition {current} → {target}; expected {sequence[ci + 1] if ci + 1 < len(sequence) else 'none'}.")
    if target == "RED_CONFIRMED":
        fail("Use `check --kind red --expect fail -- <command>` to enter RED_CONFIRMED.")
    if target == "GREEN_CONFIRMED":
        fail("Use `check --kind green --expect pass -- <command>` to enter GREEN_CONFIRMED.")
    if target == "RELATED_VERIFIED":
        fail("Use `check --kind related --expect pass -- <command>` to enter RELATED_VERIFIED.")
    s["task_state"] = target
    save_state(s)
    event("task_state", task=task_id, from_state=current, to_state=target)
    print(f"Task {task_id}: {current} → {target}")


def run_shell(command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, shell=True, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def check(kind: str, expect: str, command_parts: list[str]) -> None:
    s = state()
    task_id = s.get("active_task")
    if not task_id:
        fail("No active task.")
    if not command_parts:
        fail("A command is required after `--`.")
    command = shlex.join(command_parts)
    current = s.get("task_state")
    expected_from = {"red": "TEST_WRITTEN", "green": "IMPLEMENT_MINIMAL", "related": "REFACTOR"}
    next_state = {"red": "RED_CONFIRMED", "green": "GREEN_CONFIRMED", "related": "RELATED_VERIFIED"}
    if current != expected_from[kind]:
        fail(f"{kind} check requires task state {expected_from[kind]}; current state is {current}.")
    proc = subprocess.run(command_parts, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    passed_expectation = (proc.returncode == 0) if expect == "pass" else (proc.returncode != 0)
    record = {
        "kind": kind,
        "expect": expect,
        "command": command,
        "exit_code": proc.returncode,
        "matched_expectation": passed_expectation,
        "time": now(),
        "output_tail": proc.stdout[-4000:],
    }
    s.setdefault("task_evidence", {}).setdefault(task_id, {"checks": []})["checks"].append(record)
    if passed_expectation:
        s["task_state"] = next_state[kind]
    save_state(s)
    event(
        "task_check",
        task=task_id,
        check_kind=kind,
        expect=expect,
        command=command,
        exit_code=proc.returncode,
        matched_expectation=passed_expectation,
    )
    print(proc.stdout, end="")
    if not passed_expectation:
        fail(f"Check did not match expectation `{expect}`; exit code was {proc.returncode}.")
    print(f"Recorded {kind} evidence; task state is now {s['task_state']}.")


def task_complete(task_id: str) -> None:
    s = state()
    if s.get("active_task") != task_id:
        fail(f"Active task is {s.get('active_task')!r}, not {task_id}.")
    graph = get_graph()
    task = task_by_id(graph, task_id)
    checks = s.get("task_evidence", {}).get(task_id, {}).get("checks", [])
    kinds = {c.get("kind") for c in checks if c.get("matched_expectation")}
    exception = str(task.get("tdd_exception", "")).strip()
    required = {"green", "related"} | (set() if exception else {"red"})
    missing = sorted(required - kinds)
    if missing:
        fail("Task cannot complete; missing evidence: " + ", ".join(missing))
    if s.get("task_state") != "RELATED_VERIFIED":
        fail(f"Task cannot complete from TDD state {s.get('task_state')}; expected RELATED_VERIFIED.")
    s.setdefault("completed_tasks", []).append(task_id)
    s["active_task"] = None
    s["task_state"] = None
    save_state(s)
    event("task_completed", task=task_id)
    print(f"Completed {task_id} with required evidence.")


def final_verify() -> None:
    s = state()
    if s["state"] != "FINAL_VERIFICATION":
        fail("final-verify can only run in FINAL_VERIFICATION state.")
    checks = load_json(CHECKS_PATH)
    results: list[dict[str, Any]] = []
    all_pass = True
    for category, commands in checks.items():
        for command in commands:
            proc = run_shell(command)
            ok = proc.returncode == 0
            all_pass = all_pass and ok
            results.append({
                "category": category,
                "command": command,
                "exit_code": proc.returncode,
                "passed": ok,
                "time": now(),
                "output_tail": proc.stdout[-5000:],
            })
            status = "PASS" if ok else "FAIL"
            print(f"[{status}] {category}: {command}")
    data = {"passed": all_pass, "time": now(), "results": results}
    write_json(ARTIFACTS / "final-verification.json", data)
    event("final_verification", passed=all_pass, checks=len(results))
    if not all_pass:
        fail("Final verification failed.")
    print("Final verification passed.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic workflow state and evidence manager")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("--goal", required=True)
    p.add_argument("--force", action="store_true")

    sub.add_parser("status")
    sub.add_parser("validate")
    sub.add_parser("advance")

    p = sub.add_parser("task-start")
    p.add_argument("task_id")

    p = sub.add_parser("task-state")
    p.add_argument("target")

    p = sub.add_parser("check")
    p.add_argument("--kind", required=True, choices=["red", "green", "related"])
    p.add_argument("--expect", required=True, choices=["pass", "fail"])
    p.add_argument("command", nargs=argparse.REMAINDER)

    p = sub.add_parser("task-complete")
    p.add_argument("task_id")

    sub.add_parser("final-verify")

    args = parser.parse_args()
    if args.cmd == "init":
        init_run(args.goal, args.force)
    elif args.cmd == "status":
        print_status()
    elif args.cmd == "validate":
        validate_stage()
    elif args.cmd == "advance":
        advance()
    elif args.cmd == "task-start":
        task_start(args.task_id)
    elif args.cmd == "task-state":
        task_state(args.target)
    elif args.cmd == "check":
        command = list(args.command)
        if command and command[0] == "--":
            command = command[1:]
        check(args.kind, args.expect, command)
    elif args.cmd == "task-complete":
        task_complete(args.task_id)
    elif args.cmd == "final-verify":
        final_verify()


if __name__ == "__main__":
    main()
