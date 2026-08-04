---
name: planning
description: Construct an evidence-backed implementation plan from validated requirements and synthesis. Used after research; does not execute code.
user-invocable: false
---

# Evidence-backed planning

Plan only from validated requirements and supported evidence.

Required sections:
- Validated Requirements
- Architecture
- Ordered Implementation Strategy
- Test Strategy
- Verification

For each architectural choice, identify the evidence or constraint that justifies it. Mark material uncertainty instead of pretending it is resolved. Prefer the least complex design that satisfies acceptance criteria and known constraints.

The plan must define meaningful intermediate system states, migration/compatibility needs where relevant, and how observable behavior will be verified.

Read `${CLAUDE_SKILL_DIR}/references/quality-gates.md` before finalizing.
