---
name: audit
description: Audit this Claude Code control plane for missing components, invalid layer boundaries, hidden cycles, weak contracts, incomplete state machines, absent deterministic enforcement, and untracked configuration.
disable-model-invocation: true
allowed-tools: Read Glob Grep Bash(python3 scripts/audit.py)
---

# Control-plane audit

Run `python3 scripts/audit.py` first. Treat a failure as a control-plane defect, not a suggestion to waive the checker.

Then review the machine result against these semantic questions:

- Does every always-true instruction live in policy/rules rather than a procedure?
- Does each skill represent one reusable procedure or bounded knowledge unit?
- Does each subagent have a distinct objective, explicit contract, and least-privilege tools?
- Is the main session still the conductor?
- Are critics independent from repair?
- Are objective invariants enforced by hooks/scripts/tests instead of prompts where practical?
- Are both workflow and TDD state machines complete and non-bypassable through supported commands?
- Does every control-plane component appear in the machine-readable inventory?
- Can complexity be justified by benchmark evidence rather than aesthetics?

Report failures before recommendations.
