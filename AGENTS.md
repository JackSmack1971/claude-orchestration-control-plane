AGENTS.md
=========

Scope
-----

This file applies to the entire repository.

A more deeply nested `AGENTS.md` or `AGENTS.override.md` takes precedence for files within its scope.

Direct user instructions take precedence over this file.
Mission
-------

This repository is the source code for a **Claude Code orchestration control plane**.

When working here, improve the control plane so non-trivial Claude Code engineering work becomes more:

* correct;

* evidence-driven;

* deterministic where determinism is possible;

* resistant to orchestration, context, and stale-evidence failures;

* efficient in tokens, tool calls, and context switches;

* auditable;

* testable;

* maintainable.

Prefer simpler mechanisms with stronger guarantees.

Do not add agents, skills, rules, hooks, workflow states, or abstractions merely to make the system appear more sophisticated.
Important distinction
---------------------

`.claude/` is part of the product being engineered.

It is **Claude Code configuration and behavior under test**, not configuration for Codex itself.

Codex should inspect, test, critique, and improve `.claude/` like any other source-controlled subsystem.

* * *

Repository map
==============

Use this section as a navigation index rather than expecting this file to duplicate repository documentation.
Control-plane design
--------------------

* `CLAUDE.md`  
  Persistent Claude Code project policy and always-true invariants.

* `docs/ARCHITECTURE.md`  
  Intended architecture, responsibility boundaries, state-machine design, and rationale.

* `docs/AUDIT-COMPLIANCE.md`  
  Mapping between architectural requirements and their concrete implementation.

* `docs/CLAUDE-CODE-COMPATIBILITY.md`  
  Repository-specific claims and assumptions about Claude Code behavior.

Local official Claude Code documentation
----------------------------------------

* `docs-control-plane/README.md`  
  Provenance, generation metadata, source policy, and instructions for using the documentation pack.

* `docs-control-plane/AGENT_INDEX.md`  
  Primary navigation map for the bundled official documentation.

* `docs-control-plane/index/chunks.jsonl`  
  Searchable chunk index for locating relevant documentation.

* `docs-control-plane/docs/`  
  Full captured first-party Claude Code, Anthropic, and MCP documentation pages.

* `docs-control-plane/manifest.json`  
  Documentation-pack generation metadata and included-source inventory.

* `docs-control-plane/sources.csv`  
  Source inventory.

Claude Code configuration under test
------------------------------------

* `.claude/agents/` — bounded subagent definitions.

* `.claude/skills/` — reusable procedures and workflow methodology.

* `.claude/rules/` — standing modular instructions.

* `.claude/hooks/` — deterministic lifecycle/tool enforcement.

* `.claude/settings.json` — project permissions and hook registration.

* `.claude/commands/` — legacy-compatible/operator command entry points.

Deterministic orchestration
---------------------------

* `orchestration/workflow.json` — canonical engineering and TDD state definitions.

* `orchestration/manifest.json` — control-plane component inventory and dependencies.

* `orchestration/scorecard.json` — architecture audit scoring model.

* `orchestration/schemas/` — machine-readable artifact contracts.

* `orchestration/templates/` — workflow artifact templates.

* `orchestration/benchmarks/` — representative evaluation cases.

* `scripts/workflow.py` — deterministic state, task, TDD, and evidence authority.

* `scripts/audit.py` — architecture/configuration audit.

* `scripts/smoke_test.py` — deterministic workflow smoke test.

* `scripts/benchmark.py` — benchmark result recording/comparison.

* `tests/` — automated regression and behavioral tests.

* * *

Sources of truth
================

Different sources answer different questions. Do not collapse them into one precedence list without considering the type of claim.
What does Claude Code officially support?
-----------------------------------------

For claims about Claude Code itself, including:

* `.claude/` structure;

* `CLAUDE.md`;

* rules;

* skills;

* commands;

* subagents;

* hooks;

* settings;

* permissions;

* tool restrictions;

* invocation semantics;

* frontmatter fields;

* dynamic workflows;

* agent teams;

* context behavior;

* MCP integration;

use the bundled official documentation under `docs-control-plane/`.

### Documentation lookup procedure

1. Start with `docs-control-plane/AGENT_INDEX.md`.

2. If necessary, search `docs-control-plane/index/chunks.jsonl`.

3. Open the matching full page under `docs-control-plane/docs/`.

4. Read enough surrounding context to understand the documented behavior.

5. Treat the page's `source_url` frontmatter as the authoritative origin of the claim.

6. Prefer first-party Claude Code/Anthropic documentation over memory, inference, tutorials, blog posts, or community examples.

Do not infer current Claude Code behavior solely from this repository's existing implementation.
Documentation freshness
-----------------------

The bundled documentation is a **versioned local snapshot**, not proof that Claude Code has never changed afterward.

Check `docs-control-plane/README.md` or `manifest.json` for its generation date.

If a task materially depends on the **latest** Claude Code behavior and network access is available:

1. identify the relevant bundled page;

2. use its `source_url`;

3. verify the corresponding current first-party documentation;

4. prefer newer official documentation when it explicitly supersedes the bundled snapshot;

5. update repository compatibility documentation when the control plane's assumptions change.

Do not use unofficial sources to override first-party documentation.

If current external documentation cannot be checked, use the bundled pack and state any material freshness uncertainty.
What does this repository currently do?
---------------------------------------

Executable implementation and tests are authoritative for existing behavior.

For runtime questions, inspect:

1. `scripts/workflow.py`;

2. hooks under `.claude/hooks/`;

3. `.claude/settings.json`;

4. schemas;

5. tests and smoke tests;

6. the actual Claude configuration being evaluated.

Documentation describing an enforcement mechanism does not prove that the mechanism works.
What is this repository intended to do?
---------------------------------------

Use:

1. the explicit user task;

2. `docs/ARCHITECTURE.md`;

3. `orchestration/workflow.json`;

4. relevant contracts under `.claude/skills/workflow/references/`;

5. `docs/AUDIT-COMPLIANCE.md`.

If implementation and intended architecture disagree, surface the discrepancy rather than silently choosing one.
What assumptions has this project made about Claude Code?
---------------------------------------------------------

Use `docs/CLAUDE-CODE-COMPATIBILITY.md`, but validate material platform claims against `docs-control-plane/`.

That file records **our compatibility conclusions**.

The bundled official documentation supplies the evidence those conclusions should be based on.

* * *

Documentation pack policy
=========================

`docs-control-plane/` is a generated first-party documentation corpus.

Treat it as **reference evidence**, not ordinary project prose.

Do not manually rewrite captured pages to make them agree with the implementation.

Do not modify generated documentation files as part of an unrelated control-plane change.

If the documentation pack itself needs refreshing, treat that as an explicit documentation-ingestion task and preserve its provenance/index/manifest consistency.

Prefer linking repository documentation to authoritative pages in the pack rather than copying large portions of Claude Code documentation into:

* `AGENTS.md`;

* `CLAUDE.md`;

* `.claude/rules/`;

* skill files;

* compatibility documentation.

Project files should describe **our decisions and constraints**, not reproduce the platform manual.

* * *

Core architecture
=================

The control plane has five conceptual layers:

1. **Policy** — persistent project facts and invariants.

2. **Orchestration** — workflow sequencing and state ownership.

3. **Procedures** — reusable methodology encoded as skills.

4. **Workers** — bounded subagents.

5. **Enforcement** — deterministic Python, hooks, schemas, tests, and gates.

Preserve these boundaries unless the task explicitly changes the architecture.
Invariants
----------

* The main Claude session owns end-to-end control flow.

* Subagents perform bounded work and return results to the conductor.

* Worker agents do not recursively orchestrate other workers.

* Researchers establish evidence; they do not own planning.

* Critics diagnose; they do not repair.

* Implementers execute one approved atomic task at a time.

* Verifiers assess evidence; they do not silently fix failures.

* `scripts/workflow.py` is the deterministic transition authority.

* `.workflow/` is runtime state/evidence, not source configuration.

* Rejected workflow transitions are repaired rather than bypassed.

* Recorded evidence must correspond to commands that actually ran.

* Stale evidence must not remain valid after relevant changes.

* Task and phase dependencies must remain acyclic.

* TDD exceptions must be explicit.

* Completion requires observable verification rather than an assertion of success.

* * *

Claude Code design rules
========================

When changing Claude-specific configuration, first determine what primitive the behavior belongs to.

Use official documentation from `docs-control-plane/` to validate that choice.

As a default architectural heuristic:

* **CLAUDE.md / rules** — stable context and project instructions.

* **skills** — reusable procedures or specialized on-demand context.

* **subagents** — bounded isolated work where context separation is useful.

* **hooks / scripts** — deterministic enforcement of detectable invariants.

* **settings / permissions** — platform-supported capability and permission policy.

* **commands** — retain only where their operator-entry-point role is intentional.

These are heuristics for this control plane, not substitutes for the official platform documentation.
Enforcement terminology
-----------------------

Distinguish carefully between:

* instruction;

* convention;

* permission rule;

* pre-approval;

* capability restriction;

* validation;

* detection;

* deterministic prevention.

Do not write that something is "enforced", "prevented", "guaranteed", or "impossible" unless the implementation or Claude Code platform actually provides that guarantee.

When possible, test the claimed capability rather than checking only for configuration metadata.

* * *

Canonical workflow
==================

The source of truth for workflow states is:

`orchestration/workflow.json`

Current high-level flow:
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

Do not create competing copies of the state machine in prompts or documentation.

When the canonical workflow changes, inspect every dependent:

* transition in `scripts/workflow.py`;

* test;

* smoke test;

* skill;

* stage contract;

* template;

* schema;

* manifest entry;

* architecture/compliance document.

* * *

TDD
===

The TDD state machine is defined in `orchestration/workflow.json` and enforced by `scripts/workflow.py`.

Current conceptual flow:
    SELECTED
    → UNDERSTAND_EXISTING_BEHAVIOR
    → TEST_WRITTEN
    → RED_CONFIRMED
    → IMPLEMENT_MINIMAL
    → GREEN_CONFIRMED
    → REFACTOR
    → RELATED_VERIFIED
    → COMPLETE

A RED result is useful only when it fails for the expected behavioral reason.

A passing command is useful evidence only when it actually demonstrates the property it claims to verify.

Prefer evidence tied to explicit verification requirements and acceptance criteria over generic successful commands.

* * *

Working method
==============

For non-trivial work:

1. Read the applicable `AGENTS.md` instructions.

2. Read the relevant project architecture/contracts.

3. For Claude Code semantics, consult `docs-control-plane/` before relying on memory.

4. Inspect the existing implementation and tests.

5. Define the invariant, failure mode, or behavior being changed.

6. Add or update regression coverage where behavior changes.

7. Make the smallest coherent implementation change.

8. Run focused checks while iterating.

9. Run the repository verification suite after the final change.

10. Inspect the resulting diff and status.

11. Update affected contracts/documentation when their truth changed.

Do not refactor unrelated code for stylistic preference.

* * *

Improving the control plane
===========================

When evaluating an improvement, prefer this order:

1. remove unnecessary complexity;

2. correct an invalid assumption about Claude Code;

3. make contracts explicit;

4. replace prompt-only requirements with deterministic checks when feasible;

5. strengthen evidence provenance and freshness;

6. reduce ambiguous agent discretion;

7. improve failure behavior;

8. improve observability;

9. improve context efficiency;

10. add orchestration machinery only when simpler options are insufficient.

Ask of every architectural addition:

> What failure does this prevent or detect, and how can we demonstrate that?

Prefer negative/capability tests over configuration-presence tests.

For example, proving that a forbidden transition cannot occur is stronger than checking that a rule describing the prohibition exists.

* * *

Alternate-path analysis
=======================

When reviewing safeguards, consider equivalent ways the same action can occur.

Examples:

* `Write` versus shell redirection;

* `Edit` versus `sed`, Python, or another subprocess;

* direct file reads versus shell commands;

* declared verification versus arbitrary passing commands;

* file changes after evidence was captured;

* manual/human changes to the working tree;

* one Claude Code tool versus another tool with equivalent capability.

A control is incomplete if an ordinary alternate path bypasses the guarantee it claims to provide.

* * *

Synchronization requirements
============================

Workflow changes
----------------

Changes to `orchestration/workflow.json` require review of at least:

* `scripts/workflow.py`;

* `tests/`;

* `scripts/smoke_test.py`;

* `.claude/skills/workflow/`;

* `.claude/skills/tdd/` when applicable;

* templates;

* schemas;

* `docs/ARCHITECTURE.md`;

* `docs/AUDIT-COMPLIANCE.md`.

Claude component changes
------------------------

When adding, removing, renaming, or materially changing an agent, skill, rule, command, or hook, inspect:

* `orchestration/manifest.json`;

* `scripts/audit.py`;

* `.claude/settings.json`;

* relevant tests;

* `docs/AUDIT-COMPLIANCE.md`;

* `docs/CLAUDE-CODE-COMPATIBILITY.md`.

For any claim about whether the new configuration is valid Claude Code behavior, consult `docs-control-plane/`.
Platform-semantics changes
--------------------------

When the bundled/live official documentation shows that a Claude Code assumption has changed:

1. identify affected control-plane components;

2. update implementation;

3. add regression/capability tests where practical;

4. update `docs/CLAUDE-CODE-COMPATIBILITY.md`;

5. update architecture/compliance docs if the design implication is material;

6. do not modify the official captured documentation merely to reflect our change.

* * *

Runtime and generated data
==========================

Treat `.workflow/` as runtime state.

Do not manually edit workflow state or evidence to force a gate to pass.

Do not commit transient runtime artifacts unless explicitly required as fixtures/examples.

Treat benchmark output as experimental data unless the task explicitly calls for committing it.

Treat `docs-control-plane/` as generated reference material as described above.

* * *

Testing
=======

Python 3.11+ is required.

Available validation commands:
    python3 scripts/audit.py
    python3 -m unittest discover -s tests -p 'test_*.py'
    python3 scripts/smoke_test.py
    make verify

After repository changes, run:
    make verify

Make a best effort to leave it passing.

If verification cannot run because of an environmental limitation, report the exact limitation rather than claiming success.

If verification fails:

* diagnose the failure;

* fix failures caused by the change;

* do not weaken a valid test or gate merely to obtain green status;

* distinguish unrelated pre-existing failures from regressions caused by the current change.

* * *

Test expectations
=================

Add regression coverage for bugs.

For state-machine changes, test both:

* the newly allowed behavior;

* nearby transitions that must remain forbidden.

For enforcement changes, include negative tests demonstrating that prohibited or stale behavior is actually rejected.

For safety hooks, test plausible bypass paths.

For evidence logic, test:

* provenance;

* freshness;

* invalidation;

* expected failures;

* false-positive success paths.

Prefer behavioral tests over tests that merely search configuration text.

* * *

Python conventions
==================

The project targets Python 3.11+.

Follow existing style and `pyproject.toml`.

Prefer:

* standard-library solutions;

* explicit data and state flow;

* small deterministic functions;

* clear failure behavior;

* type annotations where useful;

* minimal dependencies.

Do not add a dependency unless its value clearly exceeds the maintenance and supply-chain cost.

* * *

Security and change safety
==========================

Preserve unrelated working-tree changes.

Do not use destructive Git operations to solve local problems.

Do not expose secrets or weaken protections around environment files, credentials, keys, or protected paths.

Do not weaken an enforcement boundary merely to make tests easier.

If intentionally changing a security boundary:

* document the reason;

* update relevant compatibility/architecture documentation;

* add tests defining the new boundary.

* * *

Documentation standards
=======================

Repository documentation should explain:

* what this control plane chooses;

* why it chooses it;

* what it guarantees;

* what remains model judgment;

* which official Claude Code behavior the choice depends upon.

Do not copy lengthy first-party Claude Code documentation into project files.

Link or point to the corresponding material under `docs-control-plane/`.

Update:

* `docs/ARCHITECTURE.md` when architecture changes;

* `docs/AUDIT-COMPLIANCE.md` when enforcement/control mappings change;

* `docs/CLAUDE-CODE-COMPATIBILITY.md` when Claude Code assumptions or compatibility conclusions change.

* * *

Benchmarking
============

Do not assume more orchestration is better.

Use `orchestration/benchmarks/` for meaningful architecture comparisons.

Important dimensions include:

* correctness;

* rework;

* critique effectiveness;

* ignored findings;

* tool calls;

* subagent calls;

* research duplication;

* context consumption;

* latency;

* human intervention;

* unnecessary file changes.

An efficiency improvement counts only when correctness and required guarantees are preserved.

* * *

Git hygiene
===========

Before finishing:
    git diff
    git status

Confirm:

* intended files changed;

* unrelated files did not;

* runtime/generated artifacts were not accidentally added;

* documentation and implementation agree;

* required verification was run.

Do not force-push, hard-reset, rewrite history, or delete unrelated work unless explicitly instructed.

* * *

Definition of done
==================

A change is complete when:

* the requested behavior or improvement exists;

* relevant official Claude Code semantics were verified from `docs-control-plane/` when applicable;

* architecture invariants are preserved or intentionally updated;

* relevant tests cover the change;

* deterministic gates still express the intended guarantees;

* evidence is current;

* affected implementation, contracts, compatibility notes, and architecture documentation agree;

* `make verify` has been run after the final changes, or an exact reason it could not run is reported;

* the final diff contains no unintended changes.

For changes intended to improve the control plane itself, finish by asking:

> Did this make the system demonstrably more correct, enforceable, observable, or efficient — or did it merely add machinery?
