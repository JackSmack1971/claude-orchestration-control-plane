# Usage

## 1. Configure your real project checks

Edit `.claude/project-checks.json`. Each key contains shell commands that must pass for final verification.

Example:

```json
{
  "format": ["npm run format:check"],
  "lint": ["npm run lint"],
  "typecheck": ["npm run typecheck"],
  "test": ["npm test"],
  "audit": ["python3 scripts/audit.py"],
  "build": ["npm run build"]
}
```

## 2. Start a workflow

```bash
python3 scripts/workflow.py init --goal "Add organization-scoped API keys"
```

Or, from Claude Code:

```text
/workflow Add organization-scoped API keys
```

The CLI creates `.workflow/state.json`, `.workflow/events.jsonl`, and stage artifact templates.

## 3. Complete one stage at a time

Write the artifact required by the current state, then:

```bash
python3 scripts/workflow.py advance
```

The transition fails if required files/headings are missing.

## 4. Phase decomposition

Create `.workflow/artifacts/task-graph.json` from the template. It must contain an acyclic phase/task graph. Each task must be atomic.

The transition into `EXECUTION` validates the graph.

## 5. Atomic task execution

```bash
python3 scripts/workflow.py task-start TASK-1.1
python3 scripts/workflow.py task-state UNDERSTAND_EXISTING_BEHAVIOR
python3 scripts/workflow.py task-state TEST_WRITTEN
python3 scripts/workflow.py check --kind red --expect fail -- <targeted test command>
python3 scripts/workflow.py task-state IMPLEMENT_MINIMAL
python3 scripts/workflow.py check --kind green --expect pass -- <targeted test command>
python3 scripts/workflow.py task-state REFACTOR
python3 scripts/workflow.py check --kind related --expect pass -- <related checks>
python3 scripts/workflow.py task-complete TASK-1.1
```

`task-complete` refuses completion without RED/GREEN/related evidence unless the selected task has a non-empty `tdd_exception`.

## 6. Phase review

When all tasks in the current phase are complete, `advance` moves from `EXECUTION` to `PHASE_REVIEW`. Write `.workflow/artifacts/phase-review-<phase-id>.md` with the required headings, then `advance` either returns to `EXECUTION` for the next phase or moves to `FINAL_VERIFICATION`.

## 7. Final verification

```bash
python3 scripts/workflow.py final-verify
python3 scripts/workflow.py advance
```

`final-verify` executes every configured command and records command, exit code, output tail, and timestamp. Any failed command prevents completion.

## 8. Audit the architecture itself

```bash
python3 scripts/audit.py
```

CI runs the same audit and unit tests.

## Benchmarking architecture changes

The repository intentionally does not invent benchmark results. Record observed runs:

```bash
python3 scripts/benchmark.py record --case small-bug --variant current --metrics metrics.json
python3 scripts/benchmark.py record --case small-bug --variant candidate --metrics metrics-candidate.json
python3 scripts/benchmark.py summary
```

Use the same cases and metric definitions for both variants.
