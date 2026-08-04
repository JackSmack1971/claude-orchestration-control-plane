import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("wf", ROOT / "scripts/workflow.py")
wf = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(wf)


class WorkflowValidationTests(unittest.TestCase):
    def test_template_task_graph_valid(self):
        errors = wf.validate_task_graph(ROOT / "orchestration/templates/task-graph.json")
        self.assertEqual(errors, [])

    def test_cycle_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "graph.json"
            graph = json.loads((ROOT / "orchestration/templates/task-graph.json").read_text())
            a = graph["tasks"][0]
            a["dependencies"] = ["TASK-1.2"]
            b = dict(a)
            b["id"] = "TASK-1.2"
            b["dependencies"] = ["TASK-1.1"]
            graph["tasks"].append(b)
            path.write_text(json.dumps(graph))
            errors = wf.validate_task_graph(path)
            self.assertTrue(any("cycle" in e for e in errors))

    def test_markdown_heading_contract(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.md"
            p.write_text("# X\n\n## Required\n\nThis artifact contains enough substantive content to satisfy the minimum contract.\n")
            self.assertEqual(wf.validate_markdown(p, ["Required"]), [])
            self.assertTrue(wf.validate_markdown(p, ["Missing"]))


class StageValidationTests(unittest.TestCase):
    def test_validate_stage_passes_current_valid_artifact(self):
        fake_state = {"state": "IDEATION"}
        with mock.patch.object(wf, "state", return_value=fake_state), \
             mock.patch.object(wf, "validate_current", return_value=[]):
            wf.validate_stage()

    def test_validate_stage_rejects_gate_errors(self):
        fake_state = {"state": "PLAN_V1"}
        with mock.patch.object(wf, "state", return_value=fake_state), \
             mock.patch.object(wf, "validate_current", return_value=["plan-v1.md: missing heading `Architecture`"]):
            with self.assertRaises(SystemExit):
                wf.validate_stage()


class TaskEvidenceTests(unittest.TestCase):
    def test_check_records_evidence_without_event_field_collision(self):
        fake_state = {
            "state": "EXECUTION",
            "active_task": "TASK-1.1",
            "task_state": "TEST_WRITTEN",
            "task_evidence": {"TASK-1.1": {"checks": []}},
        }
        completed = subprocess.CompletedProcess(["dummy"], 1, stdout="expected failure")
        with mock.patch.object(wf, "state", return_value=fake_state), \
             mock.patch.object(wf, "save_state") as save, \
             mock.patch.object(wf, "event") as log, \
             mock.patch.object(wf.subprocess, "run", return_value=completed):
            wf.check("red", "fail", ["dummy"])
        self.assertEqual(fake_state["task_state"], "RED_CONFIRMED")
        self.assertEqual(fake_state["task_evidence"]["TASK-1.1"]["checks"][0]["kind"], "red")
        save.assert_called_once()
        log.assert_called_once()
        self.assertEqual(log.call_args.kwargs["check_kind"], "red")


class HookTests(unittest.TestCase):
    def run_hook(self, name, payload):
        return subprocess.run(
            [sys.executable, str(ROOT / ".claude/hooks" / name)],
            cwd=ROOT,
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            env={**__import__("os").environ, "CLAUDE_PROJECT_DIR": str(ROOT)},
        )

    def test_sensitive_write_blocked(self):
        proc = self.run_hook("guard_write.py", {"cwd": str(ROOT), "tool_input": {"file_path": str(ROOT / ".env")}})
        self.assertEqual(proc.returncode, 2)

    def test_arbitrary_env_variant_write_blocked(self):
        proc = self.run_hook("guard_write.py", {"cwd": str(ROOT), "tool_input": {"file_path": str(ROOT / ".env.staging")}})
        self.assertEqual(proc.returncode, 2)

    def test_session_context_reports_active_state(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            (project / ".workflow").mkdir()
            (project / ".workflow/state.json").write_text(json.dumps({"state": "PLAN_V1", "active_task": None}))
            proc = subprocess.run(
                [sys.executable, str(ROOT / ".claude/hooks/session_context.py")],
                input=json.dumps({"cwd": str(project), "source": "resume"}),
                text=True, capture_output=True,
                env={**__import__("os").environ, "CLAUDE_PROJECT_DIR": str(project)},
            )
            self.assertEqual(proc.returncode, 0)
            data = json.loads(proc.stdout)
            ctx = data["hookSpecificOutput"]["additionalContext"]
            self.assertIn("State=PLAN_V1", ctx)

    def test_normal_write_allowed(self):
        proc = self.run_hook("guard_write.py", {"cwd": str(ROOT), "tool_input": {"file_path": str(ROOT / "src/example.py")}})
        self.assertEqual(proc.returncode, 0)

    def test_force_push_blocked(self):
        proc = self.run_hook("guard_bash.py", {"tool_input": {"command": "git push --force origin main"}})
        self.assertEqual(proc.returncode, 2)

    def test_post_edit_invalidates_final_verification(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            (project / ".workflow/artifacts").mkdir(parents=True)
            (project / ".workflow/state.json").write_text(json.dumps({"state": "FINAL_VERIFICATION"}))
            verification = project / ".workflow/artifacts/final-verification.json"
            verification.write_text(json.dumps({"passed": True}))
            proc = subprocess.run(
                [sys.executable, str(ROOT / ".claude/hooks/invalidate_evidence.py")],
                input=json.dumps({"cwd": str(project), "tool_input": {"file_path": str(project / "src.py")}}),
                text=True, capture_output=True,
                env={**__import__("os").environ, "CLAUDE_PROJECT_DIR": str(project)},
            )
            self.assertEqual(proc.returncode, 0)
            self.assertFalse(verification.exists())


if __name__ == "__main__":
    unittest.main()
