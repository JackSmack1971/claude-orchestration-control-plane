---
name: verification
description: Evaluate phase or final implementation evidence against acceptance criteria without silently repairing failures.
user-invocable: false
---

# Verification procedure

Verification is evidence review, not implementation.

For the requested scope:

1. Read acceptance criteria, task graph, current state, and recorded command evidence.
2. Confirm the changed behavior itself, not merely lint/typecheck success.
3. Distinguish `PASS`, `FAIL`, and `INSUFFICIENT EVIDENCE`.
4. Identify stale evidence produced before later edits.
5. Check for unverified migration, rollback, compatibility, security, and observability claims where they are part of the plan.
6. Do not edit code to make findings disappear.
7. Return exactly what must be repaired or rerun.

Read `${CLAUDE_SKILL_DIR}/references/review-contract.md`.
