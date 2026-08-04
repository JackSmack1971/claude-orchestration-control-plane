#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("workflow_module", ROOT / "scripts" / "workflow.py")
wf = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(wf)


def md(title: str, headings: list[str]) -> str:
    lines = [f"# {title}", ""]
    for h in headings:
        lines += [f"## {h}", "", f"Substantive smoke-test evidence for {h}.", ""]
    return "\n".join(lines)


def write_required(name: str) -> None:
    headings = wf.workflow().get("artifact_headings", {}).get(name, [])
    (wf.ARTIFACTS / name).write_text(md(name, headings), encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="claude-orchestration-smoke-") as td:
        runtime = Path(td) / ".workflow"
        wf.RUNTIME = runtime
        wf.ARTIFACTS = runtime / "artifacts"
        wf.STATE_PATH = runtime / "state.json"
        wf.EVENTS_PATH = runtime / "events.jsonl"

        wf.init_run("Smoke-test the deterministic workflow")
        for current_artifact in [
            "ideation.md",
            "problem.md",
            "research.md",
            "synthesis.md",
            "plan-v1.md",
            "critique-v1.md",
            "research-delta.md",
            "plan-v2.md",
            "critique-v2.md",
            "plan-final.md",
        ]:
            write_required(current_artifact)
            wf.advance()

        phase_dir = wf.ARTIFACTS / "phases"
        phase_dir.mkdir(parents=True, exist_ok=True)
        (phase_dir / "phase-01.md").write_text(
            md(
                "Phase",
                ["Objective", "Dependencies", "System state after this phase", "Tasks", "Exit Criteria"],
            ),
            encoding="utf-8",
        )
        graph = {
            "phases": [{"id": "PHASE-1", "name": "Smoke phase", "depends_on": []}],
            "tasks": [
                {
                    "id": "TASK-1.1",
                    "phase": "PHASE-1",
                    "objective": "Exercise one atomic TDD task",
                    "dependencies": [],
                    "files_likely_affected": [],
                    "test_first": "Run an intentional failing command",
                    "implementation": "Advance through the deterministic task states",
                    "verification": ["Run intentional passing commands"],
                    "acceptance_criteria": ["Task completion gate accepts complete evidence"],
                    "non_goals": ["Application behavior"],
                    "tdd_exception": "",
                }
            ],
        }
        wf.write_json(wf.ARTIFACTS / "task-graph.json", graph)
        wf.advance()

        wf.task_start("TASK-1.1")
        wf.task_state("UNDERSTAND_EXISTING_BEHAVIOR")
        wf.task_state("TEST_WRITTEN")
        wf.check("red", "fail", ["python3", "-c", "import sys; sys.exit(1)"])
        wf.task_state("IMPLEMENT_MINIMAL")
        wf.check("green", "pass", ["python3", "-c", "import sys; sys.exit(0)"])
        wf.task_state("REFACTOR")
        wf.check("related", "pass", ["python3", "-c", "import sys; sys.exit(0)"])
        wf.task_complete("TASK-1.1")
        wf.advance()

        phase_review = wf.ARTIFACTS / "phase-review-phase-1.md"
        phase_review.write_text(
            md(
                "Phase Review",
                [
                    "Phase",
                    "Exit criteria evidence",
                    "Verification commands and outcomes",
                    "Residual risks",
                    "Verdict",
                ],
            ),
            encoding="utf-8",
        )
        wf.advance()
        wf.final_verify()
        wf.advance()
        final_state = wf.state()
        if final_state.get("state") != "COMPLETE":
            raise SystemExit("Smoke test did not reach COMPLETE")
        print("WORKFLOW SMOKE PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
