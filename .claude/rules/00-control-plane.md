# Control-plane invariants

- Keep policy, orchestration, procedures, workers, and enforcement separate.
- The main session owns workflow state and stage transitions.
- Use subagents for bounded investigations, adversarial reviews, isolated implementation tasks, and verification where disposable intermediate context is useful.
- Do not create nested orchestration chains. A worker must return to the conductor rather than spawning a replacement conductor.
- `.workflow/state.json` and `.workflow/events.jsonl` are runtime evidence, not narrative suggestions.
- Never claim a stage, task, phase, test, build, or final verification passed unless the corresponding evidence was actually produced.
- Do not manually edit `.workflow/state.json` to force progress. Use `scripts/workflow.py`.
