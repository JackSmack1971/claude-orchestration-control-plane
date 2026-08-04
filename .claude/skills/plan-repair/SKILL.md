---
name: plan-repair
description: Repair a plan using critique findings and new evidence while preserving adversarial independence. Used after each critic; never invents evidence to close a finding.
user-invocable: false
---

# Plan repair

Inputs are the previous plan, critic findings, and any new evidence.

For every BLOCKER, MAJOR, or QUESTION:

1. Identify the exact challenged claim.
2. Identify the evidence now available.
3. If evidence resolves it, change the plan explicitly.
4. If evidence does not resolve it, keep it visible as a blocker/question rather than fabricating certainty.
5. Preserve unaffected parts of the plan unless the repair changes their dependencies.

Do not erase critique history. Do not let plan repair retroactively rewrite what the critic found.
