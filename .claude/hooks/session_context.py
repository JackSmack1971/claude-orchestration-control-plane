#!/usr/bin/env python3
from __future__ import annotations
import json
import os
from pathlib import Path
import sys


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR", payload.get("cwd", "."))).resolve()
    state_path = root / ".workflow" / "state.json"
    if not state_path.exists():
        return
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:
        return
    task = state.get("active_task") or "none"
    msg = (
        "Audited workflow is active. "
        f"State={state.get('state')}; active_task={task}; "
        "use scripts/workflow.py for transitions and do not bypass failed gates."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": msg,
        }
    }))


if __name__ == "__main__":
    main()
