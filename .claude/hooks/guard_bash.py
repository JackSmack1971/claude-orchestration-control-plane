#!/usr/bin/env python3
import json
import re
import sys

BLOCK_PATTERNS = [
    (r"(^|[;&|]\s*)rm\s+-[^\n]*r[^\n]*f[^\n]*\s+/(\s|$)", "recursive deletion of filesystem root"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard"),
    (r"\bgit\s+clean\s+-[^\n]*f", "git clean with force"),
    (r"\bgit\s+push\b[^\n]*(--force|-f)(\s|$)", "force push"),
    (r"\bchmod\s+-R\s+777\b", "recursive world-writable permissions"),
]


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print("Command blocked: hook input was not valid JSON.", file=sys.stderr)
        raise SystemExit(2)
    command = payload.get("tool_input", {}).get("command", "")
    for pattern, label in BLOCK_PATTERNS:
        if re.search(pattern, command, flags=re.IGNORECASE):
            print(f"Command blocked by project policy: {label}.", file=sys.stderr)
            raise SystemExit(2)


if __name__ == "__main__":
    main()
