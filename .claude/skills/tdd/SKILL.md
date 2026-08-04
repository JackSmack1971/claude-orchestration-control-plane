---
name: tdd
description: Execute one selected atomic task through the enforced TDD state machine with real RED, GREEN, refactor, and related-verification evidence.
user-invocable: false
---

# Atomic TDD execution

Work on exactly the active task from `.workflow/state.json` and `task-graph.json`.

State sequence:

`SELECTED -> UNDERSTAND_EXISTING_BEHAVIOR -> TEST_WRITTEN -> RED_CONFIRMED -> IMPLEMENT_MINIMAL -> GREEN_CONFIRMED -> REFACTOR -> RELATED_VERIFIED -> COMPLETE`

Use `python3 scripts/workflow.py task-state <STATE>` for state transitions and `python3 scripts/workflow.py check` to record real command evidence.

## RED
Write or identify the smallest test that demonstrates the missing/incorrect behavior. Run it. Confirm it fails for the expected behavioral reason. A syntax error, broken fixture, missing dependency, or unrelated failure is not acceptable RED evidence.

## GREEN
Implement the minimum change required. Run the targeted test through `check --kind green --expect pass`.

## REFACTOR
Improve structure without changing the new behavior. Rerun the targeted test if code changed.

## RELATED VERIFICATION
Run relevant surrounding tests/checks through `check --kind related --expect pass`.

Read `${CLAUDE_SKILL_DIR}/references/transition-rules.md`. Never jump directly from implementation to completion.
