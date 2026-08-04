# Transition table

| From | Owner | Required artifact/evidence | Next |
|---|---|---|---|
| IDEATION | conductor | ideation.md | PROBLEM_DEFINITION |
| PROBLEM_DEFINITION | conductor | problem.md | RESEARCH |
| RESEARCH | researcher(s) + conductor | research.md | EVIDENCE_SYNTHESIS |
| EVIDENCE_SYNTHESIS | conductor | synthesis.md | PLAN_V1 |
| PLAN_V1 | conductor | plan-v1.md | CRITIQUE_1 |
| CRITIQUE_1 | architecture-critic | critique-v1.md | TARGETED_RESEARCH |
| TARGETED_RESEARCH | researcher(s) + conductor | research-delta.md | PLAN_V2 |
| PLAN_V2 | conductor | plan-v2.md | CRITIQUE_2 |
| CRITIQUE_2 | implementation-critic | critique-v2.md | PLAN_FINAL |
| PLAN_FINAL | conductor | plan-final.md | PHASE_DECOMPOSITION |
| PHASE_DECOMPOSITION | conductor | task-graph.json + phase files | EXECUTION |
| EXECUTION | implementer + conductor | completed atomic tasks with evidence | PHASE_REVIEW |
| PHASE_REVIEW | verifier + conductor | phase review | EXECUTION or FINAL_VERIFICATION |
| FINAL_VERIFICATION | deterministic checks + verifier | final-verification.json | COMPLETE |
