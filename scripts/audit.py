#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_AGENTS = {
    "researcher", "architecture-critic", "implementation-critic", "implementer", "verifier"
}
REQUIRED_SKILLS = {
    "workflow", "ideate", "research", "planning", "plan-repair",
    "phase-decomposition", "tdd", "verification", "audit"
}
REQUIRED_RULE_FILES = {
    "00-control-plane.md", "10-engineering.md", "20-testing.md",
    "30-security.md", "40-git-safety.md", "90-control-plane-files.md"
}
REQUIRED_COMMAND_FILES = {
    "workflow-status.md", "workflow-validate.md", "control-plane-doctor.md"
}
SCORE_DIMS = [
    "purpose", "trigger", "input_contract", "output_contract", "scope", "context_efficiency",
    "tool_permissions", "failure_behavior", "verification", "composability", "observability", "value"
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    block = text[4:end]
    data: dict[str, Any] = {}
    current_list: str | None = None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") and current_list:
            data.setdefault(current_list, []).append(raw[4:].strip())
            continue
        if ":" in raw and not raw.startswith(" "):
            key, value = raw.split(":", 1)
            key, value = key.strip(), value.strip()
            current_list = None
            if value == "":
                data[key] = []
                current_list = key
            elif value.lower() in {"true", "false"}:
                data[key] = value.lower() == "true"
            else:
                data[key] = value
    return data


def is_dag(components: list[dict[str, Any]]) -> tuple[bool, str]:
    names = {c["component"] for c in components}
    graph = {c["component"]: [d for d in c.get("depends_on", []) if d in names] for c in components}
    visiting: set[str] = set()
    visited: set[str] = set()
    def dfs(node: str) -> str | None:
        if node in visiting:
            return node
        if node in visited:
            return None
        visiting.add(node)
        for dep in graph[node]:
            cyc = dfs(dep)
            if cyc:
                return cyc
        visiting.remove(node)
        visited.add(node)
        return None
    for node in graph:
        cyc = dfs(node)
        if cyc:
            return False, cyc
    return True, ""


def score_component(c: dict[str, Any]) -> dict[str, int]:
    # Deterministic proxy score for auditability of design metadata. It does not
    # claim semantic quality; it checks whether the system makes quality claims explicit.
    explicit_tools = "tools" in c and c.get("tools") is not None
    scores = {
        "purpose": 3 if str(c.get("purpose", "")).strip() else 0,
        "trigger": 3 if str(c.get("trigger", "")).strip() else 0,
        "input_contract": 3 if c.get("inputs") else 0,
        "output_contract": 3 if c.get("outputs") else 0,
        "scope": 3 if str(c.get("purpose", "")).strip() else 0,
        "context_efficiency": 3 if c.get("type") in {"procedure", "subagent", "enforcement", "evaluation"} or c.get("component") == "CLAUDE.md" else 2,
        "tool_permissions": 3 if explicit_tools else 0,
        "failure_behavior": 3 if str(c.get("failure_behavior", "")).strip() else 0,
        "verification": 3 if c.get("verification") else 0,
        "composability": 3 if "depends_on" in c and "called_by" in c else 0,
        "observability": 3 if str(c.get("observability", "")).strip() else 0,
        "value": 3 if str(c.get("benchmark_evidence", "")).strip() else (2 if str(c.get("value_evidence", "")).strip() else 0),
    }
    return scores


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    for rel in ["CLAUDE.md", ".claude/settings.json", "orchestration/manifest.json", "orchestration/workflow.json", "orchestration/scorecard.json"]:
        if not (ROOT / rel).exists():
            failures.append(f"missing required file: {rel}")

    try:
        settings = load_json(ROOT / ".claude/settings.json")
    except Exception as exc:
        failures.append(f"settings.json invalid: {exc}")
        settings = {}

    agents = {}
    for path in (ROOT / ".claude/agents").glob("*.md"):
        fm = frontmatter(path)
        if fm.get("name"):
            agents[fm["name"]] = (path, fm)
    missing_agents = REQUIRED_AGENTS - set(agents)
    if missing_agents:
        failures.append("missing agents: " + ", ".join(sorted(missing_agents)))

    for name, (path, fm) in agents.items():
        for key in ["name", "description", "tools"]:
            if not fm.get(key):
                failures.append(f"agent {name}: missing frontmatter `{key}`")
        tools = str(fm.get("tools", ""))
        if name in {"researcher", "architecture-critic", "implementation-critic", "verifier"} and re.search(r"\b(Edit|Write)\b", tools):
            failures.append(f"agent {name}: read-only role includes write tool")
        body = path.read_text(encoding="utf-8").lower()
        if name in {"architecture-critic", "implementation-critic"} and "do not" not in body and "must not" not in body:
            failures.append(f"agent {name}: critic lacks explicit non-repair boundary")

    skills = {}
    for path in (ROOT / ".claude/skills").glob("*/SKILL.md"):
        fm = frontmatter(path)
        name = fm.get("name") or path.parent.name
        skills[name] = (path, fm)
    missing_skills = REQUIRED_SKILLS - set(skills)
    if missing_skills:
        failures.append("missing skills: " + ", ".join(sorted(missing_skills)))
    if skills.get("workflow") and not skills["workflow"][1].get("disable-model-invocation"):
        failures.append("workflow skill must be human-invoked to keep workflow start explicit")

    rules_dir = ROOT / ".claude/rules"
    rule_files = {p.name for p in rules_dir.glob("*.md")} if rules_dir.exists() else set()
    missing_rules = REQUIRED_RULE_FILES - rule_files
    if missing_rules:
        failures.append("missing rules: " + ", ".join(sorted(missing_rules)))

    commands_dir = ROOT / ".claude/commands"
    command_files = {p.name for p in commands_dir.glob("*.md")} if commands_dir.exists() else set()
    missing_commands = REQUIRED_COMMAND_FILES - command_files
    if missing_commands:
        failures.append("missing operator commands: " + ", ".join(sorted(missing_commands)))

    scoped_rule = rules_dir / "90-control-plane-files.md"
    if scoped_rule.exists() and not frontmatter(scoped_rule).get("paths"):
        failures.append("90-control-plane-files.md must use paths frontmatter")

    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8") if (ROOT / "CLAUDE.md").exists() else ""
    if len(claude.splitlines()) > 120:
        warnings.append("CLAUDE.md is growing large; keep procedures in skills")
    if "IDEATION\n" in claude and "CRITIQUE_1" in claude:
        failures.append("CLAUDE.md appears to contain the full workflow procedure")

    session_start = settings.get("hooks", {}).get("SessionStart", [])
    pre = settings.get("hooks", {}).get("PreToolUse", [])
    post = settings.get("hooks", {}).get("PostToolUse", [])
    stop = settings.get("hooks", {}).get("Stop", [])
    if not session_start:
        failures.append("settings.json: no SessionStart workflow context hook")
    if not pre:
        failures.append("settings.json: no PreToolUse enforcement hooks")
    if not post:
        failures.append("settings.json: no PostToolUse evidence invalidation hook")
    if not stop:
        failures.append("settings.json: no Stop final verification gate")
    denied = set(settings.get("permissions", {}).get("deny", []))
    for required in {"Agent(Explore)", "Agent(Plan)"}:
        if required not in denied:
            failures.append(f"settings.json: expected project-aware workflow to deny built-in {required}")

    try:
        wf = load_json(ROOT / "orchestration/workflow.json")
        required_states = {
            "IDEATION", "PROBLEM_DEFINITION", "RESEARCH", "EVIDENCE_SYNTHESIS", "PLAN_V1", "CRITIQUE_1",
            "TARGETED_RESEARCH", "PLAN_V2", "CRITIQUE_2", "PLAN_FINAL", "PHASE_DECOMPOSITION", "EXECUTION",
            "PHASE_REVIEW", "FINAL_VERIFICATION", "COMPLETE"
        }
        if not required_states.issubset(set(wf.get("states", []))):
            failures.append("workflow.json: canonical state machine is incomplete")
        tdd_required = {"RED_CONFIRMED", "GREEN_CONFIRMED", "REFACTOR", "RELATED_VERIFIED", "COMPLETE"}
        if not tdd_required.issubset(set(wf.get("tdd_states", []))):
            failures.append("workflow.json: TDD state machine is incomplete")
    except Exception as exc:
        failures.append(f"workflow.json invalid: {exc}")

    try:
        manifest = load_json(ROOT / "orchestration/manifest.json")
        comps = manifest.get("components", [])
        ok, cycle = is_dag(comps)
        if not ok:
            failures.append(f"component dependency cycle detected at {cycle}")
        required_fields = {"component", "type", "source", "trigger", "purpose", "inputs", "outputs", "tools", "depends_on", "called_by", "failure_behavior", "verification", "observability", "value_evidence"}
        for c in comps:
            missing = required_fields - set(c)
            if missing:
                failures.append(f"manifest component {c.get('component')}: missing {', '.join(sorted(missing))}")
            source = c.get("source")
            if source and not (ROOT / source).exists():
                failures.append(f"manifest component {c.get('component')}: source does not exist: {source}")
        manifest_sources = {c.get("source") for c in comps}
        for path, _fm in agents.values():
            rel = path.relative_to(ROOT).as_posix()
            if rel not in manifest_sources:
                failures.append(f"agent missing from manifest inventory: {rel}")
        for path, _fm in skills.values():
            rel = path.relative_to(ROOT).as_posix()
            if rel not in manifest_sources:
                failures.append(f"skill missing from manifest inventory: {rel}")
        for path in rules_dir.glob("*.md"):
            rel = path.relative_to(ROOT).as_posix()
            if rel not in manifest_sources:
                failures.append(f"rule missing from manifest inventory: {rel}")
        for path in commands_dir.glob("*.md"):
            rel = path.relative_to(ROOT).as_posix()
            if rel not in manifest_sources:
                failures.append(f"command missing from manifest inventory: {rel}")
        for c in comps:
            for rel in c.get("supporting_files", []):
                if not (ROOT / rel).exists():
                    failures.append(f"manifest component {c.get('component')}: supporting file missing: {rel}")
        scorecfg = load_json(ROOT / "orchestration/scorecard.json")
        min_score = int(scorecfg.get("minimum_component_score", 28))
        for c in comps:
            scores = score_component(c)
            total = sum(scores.values())
            if total < min_score:
                failures.append(f"component {c['component']}: score {total}/36 below {min_score}")
    except Exception as exc:
        failures.append(f"manifest/scorecard invalid: {exc}")

    # Ensure hook scripts referenced by settings exist.
    blob = json.dumps(settings)
    for hook in ["session_context.py", "guard_write.py", "guard_bash.py", "invalidate_evidence.py", "stop_gate.py"]:
        if hook not in blob:
            failures.append(f"settings.json does not reference {hook}")
        if not (ROOT / ".claude/hooks" / hook).exists():
            failures.append(f"missing hook script: {hook}")

    if warnings:
        print("WARNINGS")
        for item in warnings:
            print(f"- {item}")
    if failures:
        print("AUDIT FAILED")
        for item in failures:
            print(f"- {item}")
        return 1

    print("AUDIT PASSED")
    print(f"- agents: {len(agents)}")
    print(f"- skills: {len(skills)}")
    print(f"- rules: {len(rule_files)}")
    print(f"- operator commands: {len(command_files)}")
    print("- component dependency graph: acyclic")
    print("- workflow state machine: complete")
    print("- TDD state machine: complete")
    print("- deterministic hooks: configured")
    print("- scorecard metadata: above threshold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
