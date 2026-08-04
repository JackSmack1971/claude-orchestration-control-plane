# Architecture

## Design goal

Make the end-to-end engineering workflow more reliable per token, tool call, and context switch without turning orchestration itself into an intelligent maze.

## Five layers

### Policy

`CLAUDE.md` contains only persistent facts and engineering invariants. It deliberately does not encode the stage-by-stage workflow.

### Orchestration

The main Claude session owns control flow. `.claude/skills/workflow/SKILL.md` defines stage responsibilities; `scripts/workflow.py` is the deterministic state authority.

### Procedures

Skills contain reusable methodology: ideation, research, planning, repair, phase decomposition, TDD, verification, and architecture audit.

### Workers

Custom subagents isolate bounded contexts. No worker owns the overall workflow. Research and both critiques are read-only. Implementation is the only code-writing worker. Verification is read-only.

### Enforcement

Python hooks and CLI checks handle objectively detectable invariants: protected paths, obviously destructive commands, workflow transitions, artifact contracts, task DAG validity, TDD evidence, and final verification.

## Canonical state machine

```text
IDEATION
  ↓
PROBLEM_DEFINITION
  ↓
RESEARCH
  ↓
EVIDENCE_SYNTHESIS
  ↓
PLAN_V1
  ↓
CRITIQUE_1                  architecture / epistemic
  ↓
TARGETED_RESEARCH
  ↓
PLAN_V2
  ↓
CRITIQUE_2                  implementation readiness
  ↓
PLAN_FINAL
  ↓
PHASE_DECOMPOSITION
  ↓
EXECUTION ←─────────────┐
  ↓                     │
PHASE_REVIEW ─ next ────┘
  ↓ no next phase
FINAL_VERIFICATION
  ↓
COMPLETE
```

The state machine itself contains no Claude-specific concept. Claude primitives are mapped onto it separately.

## Contract boundaries

### Plan → first critique

Input: validated requirements, research synthesis, architecture context, `plan-v1.md`.

Output: severity findings, questionable assumptions, missing evidence, failure modes, unnecessary complexity, and targeted research questions.

The critic must not rewrite the plan or implement code.

### Critique → targeted research

The conductor converts `QUESTION`, evidence gaps, and disputed assumptions into bounded questions. The researcher answers those questions only.

### Final plan → phase decomposition

The approved plan becomes meaningful system-state phases and an acyclic task DAG. Tasks must be small enough to execute without re-planning.

### Task → execution

Each task explicitly identifies its objective, dependencies, likely files, failing test/check, implementation intent, verification, acceptance criteria, and non-goals.

## TDD state machine

```text
SELECTED
  ↓
UNDERSTAND_EXISTING_BEHAVIOR
  ↓
TEST_WRITTEN
  ↓
RED_CONFIRMED
  ↓
IMPLEMENT_MINIMAL
  ↓
GREEN_CONFIRMED
  ↓
REFACTOR
  ↓
RELATED_VERIFIED
  ↓
COMPLETE
```

The deterministic CLI records actual command evidence for RED, GREEN, and related verification. A task with a documented `tdd_exception` can omit RED, but it cannot omit passing verification.

## Why built-in Explore/Plan agents are denied

This project deliberately uses a custom `researcher` because project-aware research must receive the project policy and preloaded research methodology consistently. The conductor can still inspect the repository directly.

## Dependency rule

The architecture dependency graph must be acyclic. Worker agents do not call other workers. Procedures are reusable knowledge; the conductor invokes them. Enforcement never delegates to Claude.
