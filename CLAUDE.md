# Project control-plane policy

This repository uses a project-level Claude Code control plane. Keep this file intentionally small: it contains only facts and invariants that are always true. Procedures live in `.claude/skills/`; worker roles live in `.claude/agents/`; deterministic enforcement lives in `.claude/hooks/`; modular standing rules live in `.claude/rules/`.

## Always true

- The main Claude session is the conductor for non-trivial engineering work.
- Never delegate end-to-end control flow to a subagent. Subagents perform bounded work and return a result to the conductor.
- The canonical state machine is `orchestration/workflow.json`; `scripts/workflow.py` is the deterministic transition authority.
- Active-run state and evidence live under `.workflow/` and must reflect commands that actually ran.
- Use `/workflow <goal>` for non-trivial build, migration, refactor, repair, or cross-cutting feature work when the full audited pipeline is desired.
- Critics diagnose; they do not repair. Researchers establish evidence; they do not plan. Implementers execute one atomic task; they do not redesign the whole plan. Verifiers evaluate evidence; they do not silently fix failures.
- A workflow transition that the CLI rejects must be repaired, not bypassed.

## Repository verification

- Control-plane audit: `python3 scripts/audit.py`
- Unit tests: `python3 -m unittest discover -s tests -p 'test_*.py'`
- Full verification: `make verify`

## Definition of done

A change is complete only when requested observable behavior exists, relevant verification was actually run, failures are not concealed, required workflow evidence is current, and no deterministic gate is bypassed.
