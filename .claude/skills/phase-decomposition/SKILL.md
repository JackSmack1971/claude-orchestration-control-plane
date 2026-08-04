---
name: phase-decomposition
description: Convert the final plan into meaningful phases and an acyclic DAG of atomic implementation tasks with test-first and verification contracts.
user-invocable: false
---

# Phase decomposition

Each phase must leave the system in a meaningful, reviewable state. Prefer dependency layers such as primitives, persistence, application behavior, integration, migration/compatibility, and hardening when they match the design; do not force those labels onto an unrelated architecture.

Each task must contain:
- id;
- phase;
- objective: exactly one meaningful change;
- dependencies;
- files likely affected;
- test first: the failing behavior to demonstrate;
- implementation: minimum intended change;
- verification: exact command(s) or observable checks;
- acceptance criteria;
- non-goals;
- optional `tdd_exception` only when test-first is genuinely inappropriate.

A task is too large if the implementer must re-plan it before coding.

Read `${CLAUDE_SKILL_DIR}/references/task-dag-contract.md`. Produce `.workflow/artifacts/task-graph.json` plus one phase markdown artifact per phase.
