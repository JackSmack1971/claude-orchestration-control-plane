#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys

SENSITIVE_NAMES = {".env", ".env.local", ".env.production", ".env.development"}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
PROTECTED_DIRS = {".git", "node_modules", "vendor", "dist", "build", "coverage"}


def deny(reason: str) -> None:
    print(reason, file=sys.stderr)
    raise SystemExit(2)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        deny("Write blocked: hook input was not valid JSON.")

    raw = payload.get("tool_input", {}).get("file_path")
    if not raw:
        return

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", payload.get("cwd", "."))).resolve()
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = project / path
    resolved = path.resolve(strict=False)

    try:
        rel = resolved.relative_to(project)
    except ValueError:
        deny(f"Write blocked outside project root: {resolved}")

    if ".." in Path(raw).parts:
        deny("Write blocked: path traversal is not allowed.")

    if rel.name in SENSITIVE_NAMES or rel.name.startswith(".env.") or rel.suffix.lower() in SENSITIVE_SUFFIXES:
        deny(f"Write blocked to sensitive file: {rel}")

    if any(part in PROTECTED_DIRS for part in rel.parts):
        deny(f"Write blocked to protected/generated directory: {rel}")

    if rel.as_posix().startswith(".claude/agent-memory"):
        deny("Write blocked to shared agent memory; this template does not use persistent agent memory.")


if __name__ == "__main__":
    main()
