# Claude Code Audited Engineering Control Plane

A complete project-level Claude Code control plane implementing this pipeline:

**Ideate -> Problem Definition -> Research -> Evidence Synthesis -> Plan V1 -> Architecture Critique -> Targeted Re-research -> Plan V2 -> Implementation-Readiness Critique -> Final Plan -> Phase/Task DAG -> Atomic TDD Execution -> Phase Review -> Final Verification**

This is not a collection of example prompts. The repository contains the actual Claude Code project configuration plus deterministic Python gates that make the workflow observable and testable.

## The actual control plane

```text
.claude/
├── agents/
│   ├── researcher.md
│   ├── architecture-critic.md
│   ├── implementation-critic.md
│   ├── implementer.md
│   └── verifier.md
├── commands/
│   ├── workflow-status.md
│   ├── workflow-validate.md
│   └── control-plane-doctor.md
├── hooks/
│   ├── session_context.py
│   ├── guard_write.py
│   ├── guard_bash.py
│   ├── invalidate_evidence.py
│   └── stop_gate.py
├── rules/
│   ├── 00-control-plane.md
│   ├── 10-engineering.md
│   ├── 20-testing.md
│   ├── 30-security.md
│   ├── 40-git-safety.md
│   └── 90-control-plane-files.md
├── skills/
│   ├── workflow/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── ideate/SKILL.md
│   ├── research/SKILL.md + references/
│   ├── planning/SKILL.md + references/
│   ├── plan-repair/SKILL.md
│   ├── phase-decomposition/SKILL.md + references/
│   ├── tdd/SKILL.md + references/
│   ├── verification/SKILL.md + references/
│   └── audit/SKILL.md
├── project-checks.json
├── settings.json
└── settings.local.example.json
```

See `CONTROL_PLANE_TREE.txt` for the complete control-plane inventory.

## Layer model

| Layer | Files | Responsibility |
|---|---|---|
| Policy | `CLAUDE.md`, `.claude/rules/*.md`, settings | Permanent truths and constraints |
| Orchestration | `.claude/skills/workflow/SKILL.md`, `orchestration/workflow.json`, `scripts/workflow.py` | Own stage order and transitions |
| Procedures | `.claude/skills/*/SKILL.md` | Reusable methodology loaded only when needed |
| Workers | `.claude/agents/*.md` | Bounded isolated research, critique, implementation, verification |
| Enforcement | `.claude/hooks/*.py`, workflow CLI, tests, CI | Deterministic gates and evidence |

The main Claude session remains the conductor. No worker owns end-to-end flow.

## Quick start in this repository

Requirements: Python 3.11+ and Claude Code.

```bash
make verify
```

Then start Claude Code in the repository and invoke:

```text
/workflow Add organization-scoped API keys
```

The workflow skill creates/resumes `.workflow/`, follows the current stage, delegates bounded worker jobs, and calls the deterministic workflow CLI for transitions.

Useful operator entry points:

```text
/workflow-status
/workflow-validate
/control-plane-doctor
```

## Install into an existing project

From this repository:

```bash
python3 scripts/install_into.py /path/to/your/project
```

The installer copies the actual `.claude/` directory, `CLAUDE.md`, orchestration definitions, and enforcement scripts. It refuses to overwrite existing files unless `--force` is supplied.

After installing, edit `.claude/project-checks.json` so final verification runs the target project's real commands. Example:

```json
{
  "format": ["npm run format:check"],
  "lint": ["npm run lint"],
  "typecheck": ["npm run typecheck"],
  "test": ["npm test"],
  "audit": [],
  "build": ["npm run build"]
}
```

Review `CLAUDE.md` and the permanent rules for repo-specific invariants before committing.

## Workflow artifacts

An active run creates:

```text
.workflow/
├── state.json
├── events.jsonl
└── artifacts/
    ├── ideation.md
    ├── problem.md
    ├── research.md
    ├── synthesis.md
    ├── plan-v1.md
    ├── critique-v1.md
    ├── research-delta.md
    ├── plan-v2.md
    ├── critique-v2.md
    ├── plan-final.md
    ├── task-graph.json
    ├── phases/
    ├── phase-review-*.md
    └── final-verification.json
```

`.workflow/` is intentionally ignored by Git: it is per-run execution state/evidence, not permanent configuration.

## Deterministic workflow CLI

```bash
python3 scripts/workflow.py init --goal "..."
python3 scripts/workflow.py status
python3 scripts/workflow.py validate
python3 scripts/workflow.py advance
python3 scripts/workflow.py task-start TASK-1.1
python3 scripts/workflow.py task-state UNDERSTAND_EXISTING_BEHAVIOR
python3 scripts/workflow.py task-state TEST_WRITTEN
python3 scripts/workflow.py check --kind red --expect fail -- <command...>
python3 scripts/workflow.py task-state IMPLEMENT_MINIMAL
python3 scripts/workflow.py check --kind green --expect pass -- <command...>
python3 scripts/workflow.py task-state REFACTOR
python3 scripts/workflow.py check --kind related --expect pass -- <command...>
python3 scripts/workflow.py task-complete TASK-1.1
python3 scripts/workflow.py final-verify
```

The CLI rejects missing artifact contracts, invalid DAGs, illegal TDD transitions, task completion without evidence, incomplete phases, and failed final checks.

## Hooks

`settings.json` wires these lifecycle gates:

- **SessionStart** -> `session_context.py`: restores active workflow stage/task context on startup/resume/compaction.
- **PreToolUse Write|Edit** -> `guard_write.py`: blocks outside-root, secret/private-key, dependency, build-output, and protected writes.
- **PreToolUse Bash** -> `guard_bash.py`: blocks high-risk destructive commands such as hard reset, forced clean, and force push.
- **PostToolUse Write|Edit** -> `invalidate_evidence.py`: invalidates stale final/related verification evidence after later edits.
- **Stop** -> `stop_gate.py`: prevents a FINAL_VERIFICATION turn from being presented as complete before deterministic final verification exists and passes.

## Audit and test suite

```bash
python3 scripts/audit.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/smoke_test.py
```

`make verify` runs all three. GitHub Actions runs the same verification on pushes and pull requests.

The audit checks, among other things:

- all 5 required worker definitions exist;
- all 9 project skills exist;
- all 6 rule files and 3 operator commands exist;
- read-only worker roles do not receive Edit/Write tools;
- both critics explicitly forbid repair;
- project settings wire SessionStart, PreToolUse, PostToolUse, and Stop hooks;
- built-in Explore/Plan are denied for the project-aware workflow;
- the canonical workflow and TDD state machines are complete;
- the machine-readable component dependency graph is acyclic;
- rules, skills, agents, commands, hooks, and support files are inventoried;
- each inventory component clears the audit score threshold.

## Benchmarks

`orchestration/benchmarks/cases.json` contains representative task categories. `scripts/benchmark.py` records real measured results for current/candidate architectures. No fabricated benchmark numbers ship with the project.

## Files to read first

1. `CLAUDE.md`
2. `.claude/skills/workflow/SKILL.md`
3. `.claude/rules/00-control-plane.md`
4. `.claude/agents/researcher.md`
5. `.claude/agents/architecture-critic.md`
6. `.claude/agents/implementation-critic.md`
7. `.claude/skills/tdd/SKILL.md`
8. `orchestration/workflow.json`
9. `scripts/workflow.py`
10. `docs/AUDIT-COMPLIANCE.md`

## License

MIT.
