---
paths:
  - ".claude/**"
  - "orchestration/**"
  - "scripts/workflow.py"
  - "scripts/audit.py"
  - "tests/test_audit.py"
  - "tests/test_workflow.py"
---

# Control-plane maintenance rules

When changing the control plane itself:

- Preserve the layer split: policy -> orchestration -> procedure -> worker -> enforcement.
- Every new skill, agent, rule, hook, command, or enforcement script must have a singular purpose and an observable verification path.
- Add every control-plane component to `orchestration/manifest.json` or make the audit explicitly classify it as support material.
- Workflow stage names and transition behavior must remain synchronized between `orchestration/workflow.json`, `scripts/workflow.py`, and workflow skill documentation.
- If a requirement is objectively detectable, prefer a deterministic hook/script/test over another prompt instruction.
- Run `make verify` after control-plane changes.
