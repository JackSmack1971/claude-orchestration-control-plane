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

    # Avoid loops when Claude is already continuing because of this hook.
    if payload.get("stop_hook_active"):
        return

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", payload.get("cwd", "."))).resolve()
    state_path = project / ".workflow" / "state.json"
    if not state_path.exists():
        return

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:
        return

    # Do not block ordinary stage boundaries or user interaction. Only guard a
    # turn that is already in the deterministic final-verification stage.
    if state.get("state") != "FINAL_VERIFICATION":
        return

    verification = project / ".workflow" / "artifacts" / "final-verification.json"
    if not verification.exists():
        print(
            "Final verification is pending. Run `python3 scripts/workflow.py final-verify` "
            "before presenting the work as complete.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    try:
        data = json.loads(verification.read_text(encoding="utf-8"))
    except Exception:
        print("Final verification evidence is invalid JSON.", file=sys.stderr)
        raise SystemExit(2)

    if not data.get("passed"):
        print("Final verification has failed required checks; completion is blocked.", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
