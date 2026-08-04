# AGENTS.md

## Purpose

This repository is the source code for a **Claude Code orchestration control plane**.

The goal when working here is to improve that control plane so non-trivial Claude Code engineering work becomes more correct, evidence-driven, deterministic where possible, auditable, maintainable, and efficient in tokens, tool calls, context, and human intervention.

Prefer simpler mechanisms with stronger guarantees.

Do not add agents, skills, rules, hooks, workflow states, or abstractions merely because they make the system appear more sophisticated.

Every meaningful increase in orchestration complexity should address a concrete failure mode or provide measurable value.

## Scope and precedence

This `AGENTS.md` applies to the entire repository.

If a directory contains a more deeply nested `AGENTS.md`, the closer file takes precedence for files in that subtree.

Explicit instructions from the user take precedence over repository `AGENTS.md` instructions.

Do not assume that instructions intended for Claude Code are instructions for Codex. In particular, `.claude/` is part of the product being engineered and audited.

---

## Repository map

Use this file as a navigation map. Do not expect it to duplicate the detailed documentation referenced below.

### Control-plane architecture

* `CLAUDE.md` — persistent Claude Code project policy and always-true invariants.
* `docs/ARCHITECTURE.md` — intended architecture, responsibility boundaries, workflows, and rationale.
* `docs/AUDIT-COMPLIANCE.md` — mapping between architectural requirements and concrete implementation.
* `docs/CLAUDE-CODE-COMPATIBILITY.md` — this project's conclusions and assumptions about Claude Code compatibility.

### Official-platform documentation namespace

`docs-control-plane/` is a namespace for vendored first-party documentation collections used to reason about the platforms this control plane interacts with.

Do not treat the namespace itself as one documentation source.

The current Claude Code documentation collection is:

`docs-control-plane/claude-code-docs/`

Other documentation collections may be added under `docs-control-plane/` in the future.

### Claude Code documentation collection

Important entry points:

* `docs-control-plane/claude-code-docs/README.md` — pack provenance, source policy, generation metadata, and agent usage instructions.
* `docs-control-plane/claude-code-docs/AGENT_INDEX.md` — primary navigation index.
* `docs-control-plane/claude-code-docs/index/chunks.jsonl` — searchable documentation chunk index.
* `docs-control-plane/claude-code-docs/docs/` — captured full first-party documentation pages.
* `docs-control-plane/claude-code-docs/manifest.json` — generated-document inventory and metadata.
* `docs-control-plane/claude-code-docs/sources.csv` — source inventory.

### Claude Code configuration under test

* `.claude/agents/` — bounded Claude Code worker definitions.
* `.claude/skills/` — reusable Claude Code procedures.
* `.claude/rules/` — modular standing Claude Code instructions.
* `.claude/hooks/` — deterministic lifecycle and tool enforcement.
* `.claude/settings.json` — project permissions and hook registration.
* `.claude/commands/` — intentionally retained operator/legacy-compatible commands.

### Deterministic control plane

* `orchestration/workflow.json` — canonical workflow and TDD state definitions.
* `orchestration/manifest.json` — control-plane component inventory and dependency metadata.
* `orchestration/scorecard.json` — architecture audit scoring model.
* `orchestration/schemas/` — machine-readable workflow artifact contracts.
* `orchestration/templates/` — workflow artifact templates.
* `orchestration/benchmarks/` — representative evaluation cases.
* `scripts/workflow.py` — deterministic workflow, task, TDD, and evidence authority.
* `scripts/audit.py` — control-plane architecture/configuration audit.
* `scripts/smoke_test.py` — deterministic end-to-end smoke test.
* `scripts/benchmark.py` — benchmark result recording and comparison.
* `tests/` — automated behavioral and regression tests.

---

# Sources of truth

Different sources answer different kinds of questions. Do not collapse them into a single undifferentiated precedence hierarchy.

## Claude Code platform truth

Question:

> What does Claude Code officially support, load, allow, restrict, or mean?

Use:

`docs-control-plane/claude-code-docs/`

This applies especially to questions involving:

* `CLAUDE.md`;
* `.claude/`;
* rules;
* skills;
* slash commands;
* subagents;
* agent teams;
* hooks;
* settings;
* permission modes;
* tool permissions;
* frontmatter fields;
* invocation behavior;
* context loading;
* memory;
* MCP;
* workflow features;
* Claude Code CLI behavior.

Do not rely on model memory for version-sensitive Claude Code behavior when this documentation is available.

### Required documentation lookup procedure

For material Claude Code platform claims:

1. Open `docs-control-plane/claude-code-docs/AGENT_INDEX.md`.
2. Locate the relevant documentation topic.
3. If navigation is insufficient, search `docs-control-plane/claude-code-docs/index/chunks.jsonl`.
4. Open the matching complete page under `docs-control-plane/claude-code-docs/docs/`.
5. Read sufficient surrounding context rather than relying on an isolated chunk.
6. Use the page's `source_url` frontmatter as the authoritative first-party origin for the claim.
7. Base implementation decisions on the documented semantics rather than on existing repository assumptions alone.

The documentation pack's own `README.md` defines its source-policy guarantees and should be consulted if provenance is relevant.

## Documentation freshness

The Claude Code documentation collection is a **versioned local snapshot**.

It is authoritative evidence for what its captured first-party sources stated when the collection was generated, but it does not prove that Claude Code has not changed since then.

Check:

* `docs-control-plane/claude-code-docs/README.md`;
* `docs-control-plane/claude-code-docs/manifest.json`;

for generation and provenance information.

When a task materially depends on the latest Claude Code semantics and current first-party documentation is accessible:

1. find the corresponding local captured page;
2. obtain its `source_url`;
3. compare against the current first-party page;
4. prefer newer official documentation when it explicitly changes or supersedes the bundled snapshot;
5. update this project's compatibility conclusions if necessary.

Do not use unofficial tutorials, forum answers, copied documentation, or community examples to override first-party documentation.

If current external verification is unavailable, use the bundled first-party snapshot and identify any material freshness uncertainty.

## Control-plane implementation truth

Question:

> What does this repository actually do right now?

Inspect executable behavior.

Primary evidence includes:

* `scripts/workflow.py`;
* `.claude/hooks/`;
* `.claude/settings.json`;
* schemas;
* actual agent and skill definitions;
* automated tests;
* smoke tests.

Tests and executable behavior outrank prose that merely claims an enforcement property exists.

A configuration field is not proof that the intended capability is actually enforced.

## Control-plane design truth

Question:

> What is this system intended to do?

Use:

1. the explicit user requirement;
2. `docs/ARCHITECTURE.md`;
3. `orchestration/workflow.json`;
4. relevant workflow/stage/delegation contracts;
5. `docs/AUDIT-COMPLIANCE.md`.

If implementation and intended architecture disagree, surface and resolve the discrepancy rather than silently choosing whichever source is convenient.

## Compatibility conclusions

`docs/CLAUDE-CODE-COMPATIBILITY.md` records **this project's conclusions** about Claude Code compatibility.

It is not itself the upstream platform specification.

Material platform claims in that file should be supportable by evidence from:

`docs-control-plane/claude-code-docs/`

When upstream documentation changes, update compatibility conclusions rather than changing the captured first-party documentation to match existing code.

---

# Documentation collection policy

`docs-control-plane/` may contain multiple first-party documentation collections.

Each collection is independent.

Do not assume that instructions, provenance, indexing conventions, or source policy from one collection automatically apply to another.

For `docs-control-plane/claude-code-docs/`, follow its own `README.md`.

The captured documentation is generated reference material.

Do not manually edit captured pages merely to make them agree with this control plane.

Do not alter generated documentation during an unrelated implementation task.

If refreshing a documentation collection is explicitly required, preserve consistency among its documentation pages, index, manifest, source inventory, and provenance metadata.

Project-owned documents should record **our architecture, decisions, compatibility conclusions, and constraints**.

They should not reproduce large portions of upstream platform manuals.

---

# Architectural invariants

The control plane has five conceptual layers:

1. policy;
2. orchestration;
3. reusable procedures;
4. bounded workers;
5. deterministic enforcement.

Preserve the responsibility boundaries documented in `docs/ARCHITECTURE.md` unless the task intentionally changes them.

Key invariants:

* The main Claude session owns end-to-end workflow control.
* Subagents perform bounded jobs and return results to the conductor.
* Worker agents do not recursively orchestrate the workflow.
* Researchers collect and assess evidence; they do not own implementation planning.
* Critics diagnose defects; they do not repair plans.
* Implementers execute one approved atomic task at a time.
* Verifiers assess evidence independently; they do not silently fix failures.
* `scripts/workflow.py` is the deterministic workflow-state authority.
* `.workflow/` is runtime state and evidence, not source configuration.
* A deterministic gate that rejects a transition is repaired rather than bypassed.
* Evidence must correspond to commands that actually ran.
* Evidence that becomes stale after relevant changes must not remain valid.
* Task and phase dependency graphs must remain acyclic.
* TDD exceptions must be explicit rather than silently bypassing RED.
* Completion requires observable evidence rather than a model assertion.

---

# Claude Code configuration changes

Before modifying a Claude Code primitive, verify its current documented semantics using `docs-control-plane/claude-code-docs/`.

Do this for changes involving:

* agent frontmatter;
* skill frontmatter;
* skill invocation;
* command compatibility;
* hooks or hook payloads;
* permission configuration;
* settings;
* rule scoping;
* subagent behavior;
* background execution;
* tool controls;
* model or effort configuration;
* context loading;
* MCP.

Distinguish carefully between:

* an instruction;
* a convention;
* a recommendation;
* a permission rule;
* a pre-approval mechanism;
* a capability restriction;
* detection;
* validation;
* deterministic prevention.

Use words such as `enforces`, `prevents`, `guarantees`, `requires`, and `cannot` only when the corresponding property is actually supported by deterministic repository behavior or documented platform behavior.

Prefer capability tests over metadata-presence tests.

---

# Canonical workflow

The canonical engineering state machine lives in:

`orchestration/workflow.json`

Do not introduce an independent competing representation of the workflow.

At the time of writing, its high-level shape is:

```text
IDEATION
→ PROBLEM_DEFINITION
→ RESEARCH
→ EVIDENCE_SYNTHESIS
→ PLAN_V1
→ CRITIQUE_1
→ TARGETED_RESEARCH
→ PLAN_V2
→ CRITIQUE_2
→ PLAN_FINAL
→ PHASE_DECOMPOSITION
→ EXECUTION
↔ PHASE_REVIEW
→ FINAL_VERIFICATION
→ COMPLETE
```

Treat `orchestration/workflow.json` as the state-name and transition-model source of truth rather than relying on this summary if they differ.

When workflow states or contracts change, inspect every dependent implementation, test, skill, schema, template, and document.

---

# TDD

The atomic TDD state machine is defined in `orchestration/workflow.json` and implemented by `scripts/workflow.py`.

Its current conceptual sequence is:

```text
SELECTED
→ UNDERSTAND_EXISTING_BEHAVIOR
→ TEST_WRITTEN
→ RED_CONFIRMED
→ IMPLEMENT_MINIMAL
→ GREEN_CONFIRMED
→ REFACTOR
→ RELATED_VERIFIED
→ COMPLETE
```

A RED result is meaningful only when the test fails for the expected behavioral reason.

A passing command is useful evidence only if it actually proves the property it is being used to support.

Prefer evidence tied to declared verification requirements and acceptance criteria over arbitrary successful commands.

---

# Working method

For a non-trivial change:

1. Determine the applicable `AGENTS.md` scope.
2. Read the relevant architecture and contracts.
3. If the work depends on Claude Code semantics, consult the appropriate first-party documentation under `docs-control-plane/claude-code-docs/`.
4. Inspect the actual implementation and existing tests.
5. Identify the invariant, failure mode, or observable behavior being changed.
6. Add or update regression coverage where behavior changes.
7. Make the smallest coherent implementation change.
8. Run focused tests while iterating.
9. Run repository-level verification after the final code change.
10. Inspect the final diff and working-tree status.
11. Update affected architecture, compliance, or compatibility documentation when their truth changed.

Do not refactor unrelated code merely to satisfy stylistic preference.

For small documentation-only changes, use proportional judgment rather than unnecessary workflow ceremony.

---

# Improving the control plane

When deciding how to improve the architecture, prefer this order:

1. remove unnecessary complexity;
2. correct invalid assumptions about Claude Code;
3. make boundaries and contracts explicit;
4. replace prompt-only requirements with deterministic validation where feasible;
5. strengthen evidence provenance and freshness;
6. reduce ambiguous model discretion;
7. improve failure behavior;
8. improve observability;
9. improve context efficiency;
10. add new orchestration machinery only when simpler mechanisms cannot solve the problem.

For any proposed architectural addition, answer:

> What concrete failure does this prevent, detect, or make measurably less likely?

and:

> How will we demonstrate that improvement?

Do not treat architectural sophistication as evidence of architectural quality.

---

# Alternate-path analysis

Whenever a safety or enforcement mechanism is changed, inspect equivalent ways the same action can occur.

Examples include:

* `Write` versus shell redirection;
* `Edit` versus `sed`, Python, Perl, or another subprocess;
* direct file-reading tools versus shell-based reads;
* a declared verification command versus an unrelated command that merely exits successfully;
* edits made after verification evidence was recorded;
* edits made by external tools or humans;
* one Claude Code capability versus another capability with equivalent effects.

A control is incomplete if an ordinary alternate path bypasses the guarantee it claims to provide.

Add regression tests for realistic bypass paths when practical.

---

# Synchronization requirements

## Workflow changes

Changes to `orchestration/workflow.json` require review of relevant:

* `scripts/workflow.py`;
* `tests/`;
* `scripts/smoke_test.py`;
* `.claude/skills/workflow/`;
* `.claude/skills/tdd/`;
* stage/delegation contracts;
* schemas;
* templates;
* `docs/ARCHITECTURE.md`;
* `docs/AUDIT-COMPLIANCE.md`;
* `orchestration/manifest.json`.

Not every file must change, but every affected representation must be considered.

## Claude component changes

When adding, removing, renaming, or materially changing an agent, skill, rule, command, hook, or settings entry, inspect whether the following require corresponding changes:

* `orchestration/manifest.json`;
* `scripts/audit.py`;
* `.claude/settings.json`;
* relevant tests;
* smoke tests;
* `docs/AUDIT-COMPLIANCE.md`;
* `docs/CLAUDE-CODE-COMPATIBILITY.md`.

Validate platform-facing syntax and semantics against `docs-control-plane/claude-code-docs/`.

## Upstream Claude Code semantic changes

If bundled or current first-party documentation demonstrates that a Claude Code assumption has changed:

1. identify every affected control-plane component;
2. update the implementation;
3. add capability/regression tests where feasible;
4. update `docs/CLAUDE-CODE-COMPATIBILITY.md`;
5. update architectural or compliance documentation when materially affected.

Do not edit the captured upstream documentation merely to reflect our implementation.

---

# Runtime and generated data

Treat `.workflow/` as runtime state.

Do not manually alter state or evidence to make a failing gate pass.

Do not commit transient runtime files unless a task explicitly requires them as fixtures or examples.

Treat benchmark outputs as experimental data unless the task explicitly requires committing them.

Treat documentation collections under `docs-control-plane/` according to each collection's own provenance and generation policy.

---

# Testing and verification

Python 3.11 or newer is required.

Useful commands:

```bash
python3 scripts/audit.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/smoke_test.py
make verify
```

Run focused tests during development.

After the final behavior-changing edit, run:

```bash
make verify
```

If verification fails:

* diagnose the failure;
* repair failures caused by the current change;
* do not weaken a valid test or gate merely to obtain green status;
* distinguish unrelated pre-existing failures from regressions introduced by the task.

If an environmental limitation prevents verification, report the exact limitation instead of claiming success.

---

# Test expectations

Add regression coverage for bugs.

For state-machine changes, test both the newly allowed behavior and nearby transitions that must remain forbidden.

For enforcement changes, include negative tests showing that prohibited or stale behavior is actually rejected.

For safety mechanisms, test plausible alternate/bypass paths rather than only the obvious form.

For evidence logic, test provenance, freshness, invalidation, expected failure behavior, and false-success cases.

Prefer behavioral tests over tests that merely assert that configuration text or metadata exists.

---

# Python conventions

The project targets Python 3.11+.

Follow existing style and `pyproject.toml`.

Prefer straightforward standard-library implementations, explicit state/data flow, small deterministic functions, clear failure behavior, and type annotations where they improve clarity.

Avoid introducing dependencies unless they provide clear value that cannot reasonably be obtained from the project's existing standard-library approach.

---

# Security and change safety

Preserve unrelated working-tree changes.

Do not use destructive Git operations to solve local development problems.

Do not expose secrets or weaken protections around environment files, keys, credentials, or protected paths.

Do not weaken an enforcement boundary merely to make a test pass.

If a security or safety boundary is intentionally changed, document the reason and add tests defining the new expected boundary.

---

# Documentation standards

Repository-owned documentation should explain:

* what this control plane chooses to do;
* why it chooses that design;
* what is deterministically guaranteed;
* what remains model judgment;
* which Claude Code platform behavior the design depends upon.

Do not duplicate substantial upstream Claude Code documentation into project-owned instructions.

Point readers and agents to the corresponding collection under:

`docs-control-plane/claude-code-docs/`

Update `docs/ARCHITECTURE.md` when architecture changes.

Update `docs/AUDIT-COMPLIANCE.md` when control/enforcement mappings change.

Update `docs/CLAUDE-CODE-COMPATIBILITY.md` when Claude Code assumptions or compatibility conclusions change.

---

# Benchmarking

Do not assume additional orchestration is beneficial.

Use representative cases under `orchestration/benchmarks/` when evaluating meaningful architectural complexity.

Measure correctness alongside costs such as rework, critique effectiveness, ignored findings, tool calls, subagent calls, research duplication, context consumption, latency, human intervention, and unnecessary file changes.

An efficiency improvement counts only when required correctness and guarantees are preserved.

Prefer measured simplification to speculative sophistication.

---

# Git hygiene

Before finishing a repository change, inspect:

```bash
git diff
git status
```

Confirm that intended files changed, unrelated files did not, runtime/generated data was not accidentally added, and project documentation still agrees with implementation.

Do not force-push, hard-reset, rewrite history, or delete unrelated work unless explicitly instructed by the user.

---

# Definition of done

A change is complete when:

* the requested behavior or improvement exists;
* relevant Claude Code semantics were checked against `docs-control-plane/claude-code-docs/` when applicable;
* architecture invariants remain valid or were intentionally updated;
* relevant regression tests cover behavioral changes;
* deterministic gates still represent the guarantees they claim to provide;
* evidence used to justify completion is current;
* affected implementation, contracts, architecture docs, audit mappings, and compatibility conclusions agree;
* `make verify` was run after the final behavior-changing edits, or the exact reason it could not run is reported;
* the final diff contains no unintended changes.

For improvements to the control plane itself, finish with this question:

> Did this change make the system demonstrably more correct, enforceable, observable, or efficient, or did it merely add machinery?
