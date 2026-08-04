#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
ITEMS = [".claude", "CLAUDE.md", "orchestration", "scripts/workflow.py", "scripts/audit.py", "scripts/benchmark.py", "scripts/smoke_test.py"]


def main() -> None:
    p = argparse.ArgumentParser(description="Install this project-level orchestration system into another repository")
    p.add_argument("target", type=Path)
    p.add_argument("--force", action="store_true")
    args = p.parse_args()
    target = args.target.resolve()
    target.mkdir(parents=True, exist_ok=True)
    for rel in ITEMS:
        src = ROOT / rel
        dst = target / rel
        if dst.exists() and not args.force:
            raise SystemExit(f"Refusing to overwrite {dst}; use --force after reviewing differences.")
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    print(f"Installed orchestration system into {target}")
    print("Review CLAUDE.md and .claude/project-checks.json before use.")


if __name__ == "__main__":
    main()
