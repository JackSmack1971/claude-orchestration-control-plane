# Audit compliance map

This document maps the target architecture to concrete project files.

| Audit requirement | Concrete implementation |
|---|---|
| `CLAUDE.md` contains always-true policy, not the entire procedure | `CLAUDE.md`; modular permanent rules in `.claude/rules/` |
| Main agent remains conductor | `.claude/skills/workflow/SKILL.md`; `.claude/rules/00-control-plane.md` |
| Reusable methodology lives in skills | `.claude/skills/ideate`, `research`, `planning`, `plan-repair`, `phase-decomposition`, `tdd`, `verification` |
| Human workflow entry point | project skill `/workflow`; read-only admin commands in `.claude/commands/` |
| Bounded project-aware research | `.claude/agents/researcher.md`, preloaded `research` skill |
| Critique 1 is adversarial/architectural | `.claude/agents/architecture-critic.md` |
| Critique 2 is implementation-readiness focused | `.claude/agents/implementation-critic.md` |
| Critics do not repair | explicit agent hard boundaries; repair is separate `plan-repair` skill |
| Targeted re-research after critique | workflow stage `TARGETED_RESEARCH`; `research-delta.md` contract |
| Phase decomposition produces task DAG | `phase-decomposition` skill; task graph validator; `task-graph.schema.json` |
| Task is too large if implementer must re-plan | `phase-decomposition` skill and task DAG contract |
| TDD is a state machine | `orchestration/workflow.json`; `scripts/workflow.py`; `.claude/skills/tdd/` |
| RED/GREEN/related checks are real evidence | `workflow.py check` records command, exit, output tail, timestamp |
| Phase review is independent | `.claude/agents/verifier.md`; `PHASE_REVIEW` state |
| Final verification is deterministic | `.claude/project-checks.json`; `workflow.py final-verify`; Stop hook |
| Prompts do not carry objectively detectable invariants alone | Pre/Post/Stop hooks plus CLI/test gates |
| Workflow state survives session restart/resume | SessionStart `session_context.py` hook |
| Destructive/sensitive operations are blocked | `guard_bash.py`, `guard_write.py`, permission deny rules |
| Stale verification is invalidated after edits | `invalidate_evidence.py` |
| Component inventory/dependency graph | `orchestration/manifest.json` |
| Architecture scorecard | `orchestration/scorecard.json`; `scripts/audit.py` |
| Benchmark current vs simplified architecture | `orchestration/benchmarks/cases.json`; `scripts/benchmark.py` |
| CI continuously audits the control plane | `.github/workflows/ci.yml` |

## Current shipped counts

- 5 subagents
- 9 project skills
- 6 project rule files
- 3 operator commands
- 5 lifecycle/tool hooks
- 15-state canonical engineering workflow
- 9-state atomic TDD workflow

Run `make verify` to verify the shipped control plane.
