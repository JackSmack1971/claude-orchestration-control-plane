#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", payload.get("cwd", "."))).resolve()
    state_path = project / ".workflow" / "state.json"
    if not state_path.exists():
        return
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:
        return
    changed = payload.get("tool_input", {}).get("file_path", "")
    # Edits after final verification make that evidence stale.
    if state.get("state") == "FINAL_VERIFICATION":
        verification = project / ".workflow" / "artifacts" / "final-verification.json"
        if verification.exists() and str(verification.resolve()) != str(Path(changed).resolve()):
            verification.unlink()
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "Final verification evidence was invalidated because files changed after it ran. Run final verification again before completion."}}))
            return
    # A code edit after related verification invalidates the last related check.
    if state.get("state") == "EXECUTION" and state.get("active_task") and state.get("task_state") == "RELATED_VERIFIED":
        task = state["active_task"]
        checks = state.get("task_evidence", {}).get(task, {}).get("checks", [])
        for i in range(len(checks) - 1, -1, -1):
            if checks[i].get("kind") == "related":
                checks.pop(i)
                break
        state["task_state"] = "REFACTOR"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "Related verification was invalidated because the active task changed after verification. Re-run the related check."}}))


if __name__ == "__main__":
    main()
