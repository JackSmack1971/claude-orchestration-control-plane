---
name: workflow
description: Run the audited end-to-end engineering control plane for a non-trivial build, repair, migration, refactor, or cross-cutting feature. Orchestrates ideation, evidence research, two distinct critiques, repair, task-DAG decomposition, atomic TDD execution, phase review, and final verification.
disable-model-invocation: true
allowed-tools: Read Glob Grep Bash(python3 scripts/workflow.py *)
---

# Audited engineering workflow

You are the conductor. The goal supplied after `/workflow` is `$ARGUMENTS`.

## Start or resume

1. Run `python3 scripts/workflow.py status`.
2. If no workflow exists, run `python3 scripts/workflow.py init --goal "$ARGUMENTS"`.
3. If a workflow already exists, do not replace it automatically. Continue the active run unless the user explicitly asked to restart.
4. Before every stage, read current status and the stage contract in `${CLAUDE_SKILL_DIR}/references/stage-contracts.md`.
5. Never manually mutate state to skip a failed gate.

## Control-flow rule

The main session owns the sequence. Invoke workers only for bounded jobs and consume their returned result in the main session. Do not delegate orchestration itself.

## Canonical sequence

`IDEATION -> PROBLEM_DEFINITION -> RESEARCH -> EVIDENCE_SYNTHESIS -> PLAN_V1 -> CRITIQUE_1 -> TARGETED_RESEARCH -> PLAN_V2 -> CRITIQUE_2 -> PLAN_FINAL -> PHASE_DECOMPOSITION -> EXECUTION <-> PHASE_REVIEW -> FINAL_VERIFICATION -> COMPLETE`

Use the corresponding project skills for procedures:

- ideation/problem definition: `ideate`
- research methodology: `research`
- plan construction: `planning`
- repair after critique: `plan-repair`
- task DAG: `phase-decomposition`
- task execution: `tdd`
- phase/final validation: `verification`

## Worker routing

- `researcher`: one explicit factual question per invocation; independent questions may run concurrently.
- `architecture-critic`: first critique; attacks assumptions, evidence, architecture, security, feasibility, failure modes, and unnecessary complexity.
- `implementation-critic`: second critique; attacks task ambiguity, sequencing, dependency ordering, acceptance criteria, tests, migration/rollback/observability gaps, and hidden cross-phase coupling.
- `implementer`: one selected atomic task only, under the task graph and TDD state machine.
- `verifier`: phase or final evidence review; no repairs.

The conductor performs synthesis, planning, plan repair, and workflow transitions.

## Transition protocol

At the end of each stage:

1. Write the required artifact under `.workflow/artifacts/` using the exact contract.
2. Run `python3 scripts/workflow.py validate`.
3. If validation fails, repair the artifact. Do not waive the error.
4. Run `python3 scripts/workflow.py advance`.
5. Read status again before beginning the next stage.

## Execution protocol

At `EXECUTION`, select exactly one ready task from `task-graph.json`.

1. `python3 scripts/workflow.py task-start <TASK-ID>`
2. Follow the `tdd` skill and its state machine.
3. Record actual commands through `python3 scripts/workflow.py check ...`; do not invent evidence.
4. `python3 scripts/workflow.py task-complete <TASK-ID>` only after its acceptance criteria and required evidence are satisfied.
5. Repeat until the current phase is complete, then advance to `PHASE_REVIEW`.

## Completion protocol

At `FINAL_VERIFICATION`:

1. Run `python3 scripts/workflow.py final-verify`.
2. Delegate an acceptance-level evidence review to `verifier`.
3. If either deterministic checks or evidence review fails, repair by returning to the appropriate task/stage; do not present the run as complete.
4. Run `python3 scripts/workflow.py advance` only when deterministic final verification passes.

Read `${CLAUDE_SKILL_DIR}/references/transition-table.md` for transition ownership and `${CLAUDE_SKILL_DIR}/references/delegation-contracts.md` before invoking a worker.
