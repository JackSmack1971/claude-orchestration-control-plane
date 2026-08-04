# Stage contracts

## IDEATION
Input: raw goal and known project context.
Output: `.workflow/artifacts/ideation.md` with Raw request, Desired outcome, Assumptions, Open questions.
Must not: choose architecture or implementation details prematurely.

## PROBLEM_DEFINITION
Input: ideation artifact.
Output: `problem.md` with Problem, Goals, Non-goals, Constraints, Acceptance Criteria.
Must not: hide unresolved product ambiguity as technical assumptions.

## RESEARCH
Input: validated problem plus explicit factual questions.
Output: `research.md` containing questions, evidence, contradictions, unknowns, implications.
Workers: `researcher`, one bounded question each.
Must not: turn evidence collection into plan advocacy.

## EVIDENCE_SYNTHESIS
Input: all researcher returns and repository evidence.
Output: `synthesis.md` separating validated facts, supported inferences, remaining unknowns, and constraints on the plan.
Owner: conductor.

## PLAN_V1
Input: problem + synthesis.
Output: `plan-v1.md` with validated requirements, architecture, ordered strategy, test strategy, verification.
Owner: conductor using planning procedure.

## CRITIQUE_1
Input: problem, synthesis, plan-v1.
Output: `critique-v1.md` grouped by severity plus required targeted research and verdict.
Worker: architecture-critic.
Must not: repair the plan.

## TARGETED_RESEARCH
Input: only questions/blockers raised by critique 1.
Output: `research-delta.md` with new evidence and required plan changes.
Must not: repeat broad research already settled unless evidence was contradicted.

## PLAN_V2
Input: plan-v1 + critique-v1 + research-delta.
Output: `plan-v2.md` repairing only evidence-supported defects.
Owner: conductor.

## CRITIQUE_2
Input: plan-v2 and current evidence.
Output: `critique-v2.md` focused on implementation readiness.
Worker: implementation-critic.
Must not: duplicate critique 1 unless an architectural blocker remains unresolved.

## PLAN_FINAL
Input: plan-v2 + critique-v2.
Output: `plan-final.md` resolving blockers or explicitly surfacing any remaining stop condition.
Owner: conductor.

## PHASE_DECOMPOSITION
Input: plan-final.
Output: `task-graph.json` plus one phase artifact per phase.
Must: be acyclic; each task must be independently executable without re-planning.

## EXECUTION
Input: one ready task.
Output: code/test changes plus recorded RED/GREEN/related evidence.
Worker: implementer, one task at a time.

## PHASE_REVIEW
Input: completed tasks and their evidence for one phase.
Output: `phase-review-<phase-id>.md` with pass/fail evidence and unresolved issues.
Worker: verifier.

## FINAL_VERIFICATION
Input: complete implementation and all phase evidence.
Output: deterministic `final-verification.json` plus verifier acceptance review.

## COMPLETE
Only valid after final verification passes. No further implementation work belongs to the completed run.
