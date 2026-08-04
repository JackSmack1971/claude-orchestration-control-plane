---
description: Validate the current workflow stage artifact and state without advancing it.
allowed-tools: Bash(python3 scripts/workflow.py validate)
---

Run `python3 scripts/workflow.py validate`. Report every failure and the artifact that must be repaired. Do not bypass or advance the state.
