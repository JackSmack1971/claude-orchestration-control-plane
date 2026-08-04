# Delegation contracts

Every delegation message must include:

- exact objective/question/task id;
- relevant artifact paths;
- constraints and non-goals;
- expected output structure;
- instruction not to broaden scope;
- instruction to return evidence rather than orchestration decisions.

## Researcher
One factual question. Return conclusion, confidence, evidence, contradictions, unknowns, implications.

## Architecture critic
Attack plan-v1. Return severity-classified findings and targeted research questions. No repair.

## Implementation critic
Attack plan-v2 for execution readiness. Return blockers/gaps and explicit acceptance/test/ordering deficiencies. No repair.

## Implementer
One atomic task from the DAG. Follow existing task objective, dependencies, test-first description, verification, acceptance criteria, non-goals. No architecture redesign.

## Verifier
Assess actual evidence against acceptance criteria. Report pass/fail/insufficient evidence. No fixes.
