import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AuditTests(unittest.TestCase):
    def test_audit_passes(self):
        proc = subprocess.run([sys.executable, "scripts/audit.py"], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("AUDIT PASSED", proc.stdout)

    def test_settings_json_is_valid(self):
        data = json.loads((ROOT / ".claude/settings.json").read_text())
        self.assertIn("hooks", data)
        self.assertIn("permissions", data)

    def test_control_plane_tree_is_present(self):
        self.assertEqual(len(list((ROOT / ".claude/agents").glob("*.md"))), 5)
        self.assertEqual(len(list((ROOT / ".claude/skills").glob("*/SKILL.md"))), 9)
        self.assertEqual(len(list((ROOT / ".claude/rules").glob("*.md"))), 6)
        self.assertEqual(len(list((ROOT / ".claude/commands").glob("*.md"))), 3)
        self.assertEqual(len(list((ROOT / ".claude/hooks").glob("*.py"))), 5)

    def test_research_and_critics_are_read_only(self):
        for name in ["researcher.md", "architecture-critic.md", "implementation-critic.md", "verifier.md"]:
            text = (ROOT / ".claude/agents" / name).read_text()
            first = text.split("---", 2)[1]
            self.assertNotIn("Edit", first)
            self.assertNotIn("Write", first)


if __name__ == "__main__":
    unittest.main()
