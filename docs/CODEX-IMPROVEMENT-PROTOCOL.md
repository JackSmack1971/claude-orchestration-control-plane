# Codex Control-Plane Improvement Protocol

## Purpose

This document defines the repository-specific method for using Codex as an independent improvement, research, and evaluation agent for the Claude Code orchestration control plane.

Codex is not another worker inside the Claude orchestration graph. Its improvement role is external to that graph: inspect the control plane, challenge its assumptions, discover overlooked weaknesses or opportunities, propose the smallest credible intervention, and determine whether the intervention produces measurable value.

The objective is not to make the control plane more elaborate. The objective is to make representative Claude Code engineering work more correct, reliable, evidence-driven, deterministic where practical, auditable, maintainable, and efficient in tokens, tool calls, context, latency, rework, and human intervention.

`AGENTS.md` remains the repository-wide Codex policy. This document is the deeper procedure for open-ended control-plane improvement work.

---

## Role boundary

Treat these as the system under evaluation, not as instructions that automatically govern Codex behavior:

- `CLAUDE.md`;
- `.claude/agents/`;
- `.claude/skills/`;
- `.claude/rules/`;
- `.claude/hooks/`;
- `.claude/settings.json`;
- `.claude/commands/`;
- `orchestration/`;
- workflow schemas and templates;
- audit, smoke-test, benchmark, and workflow scripts;
- tests and benchmark cases.

Claude-side role boundaries remain part of the product architecture. Do not solve a Claude orchestration weakness by casually making Codex part of Claude's runtime control flow.

When the user requests only research, audit, or recommendations, do not silently implement a candidate change. When the user requests improvement or implementation, follow the evidence and experiment loop below before claiming success, using proportional judgment for very small changes.

---

# Improvement loop

Use this loop for open-ended requests such as "improve the control plane", "find overlooked weaknesses", "make Claude more reliable", "reduce orchestration cost", or "audit this architecture for the next high-value change".

## 1. Establish the current system

Before generating changes:

1. read the applicable `AGENTS.md`;
2. inspect `docs/ARCHITECTURE.md`, `orchestration/workflow.json`, and relevant contracts;
3. inspect the executable implementation and tests rather than trusting prose alone;
4. inspect `docs/AUDIT-COMPLIANCE.md` and `docs/CLAUDE-CODE-COMPATIBILITY.md` when relevant;
5. for Claude Code platform semantics, follow the first-party documentation lookup procedure in `AGENTS.md`;
6. identify the existing benchmark and audit coverage related to the area being investigated.

Produce a compact mental model of what the control plane currently guarantees, what remains model judgment, and where evidence for those claims lives.

## 2. Search the improvement space

Do not wait for a pre-existing defect report. Generate candidate hypotheses across the discovery lanes below.

For each lane, ask whether the current design contains a concrete failure mode, unnecessary cost, unverified assumption, unused platform capability, or measurement blind spot.

Do not force a finding in every lane. A lane with no material evidence should remain empty.

## 3. Prove novelty relative to the repository

Before calling an idea new or overlooked, search for an existing mechanism that already addresses it.

Check at least the relevant portions of:

- `CLAUDE.md` and `.claude/rules/`;
- agents and skills;
- hooks and settings;
- `orchestration/workflow.json`;
- `orchestration/manifest.json`;
- schemas and templates;
- audit rules;
- tests and smoke tests;
- architecture, audit-compliance, and compatibility documentation;
- benchmark cases and recorded metrics.

Classify the candidate as one of:

- `NEW` — no adequate existing mechanism was found;
- `PARTIAL` — an existing mechanism addresses the issue incompletely or through a bypassable/weak path;
- `DUPLICATE` — the repository already handles the issue adequately;
- `OBSOLETE` — the candidate depends on an outdated Claude Code assumption.

Discard `DUPLICATE` and `OBSOLETE` candidates unless the task is specifically to simplify or remove the redundant mechanism.

## 4. Define the failure and hypothesis

A candidate is not actionable until it states:

- the current failure mode or wasted resource;
- evidence that the failure is real or plausibly reachable;
- why existing controls do not adequately address it;
- the smallest intervention likely to help;
- the observable behavior or metric expected to change;
- the important guarantees that must not regress.

Prefer falsifiable hypotheses.

Weak:

> Add a planning agent to improve planning.

Stronger:

> Cross-cutting tasks lose verified requirements between evidence synthesis and phase decomposition. Adding a second agent is not justified yet; first test whether strengthening the plan artifact contract reduces missed acceptance criteria without increasing context or tool calls materially.

## 5. Rank candidates before implementation

Prefer candidates with high expected value and low mechanism complexity.

Consider:

- severity and frequency of the failure mode;
- correctness or safety impact;
- expected reduction in rework or human intervention;
- expected token, context, tool-call, subagent-call, or latency savings;
- ease of obtaining credible evidence;
- regression risk;
- implementation and maintenance complexity;
- whether a simpler deletion, validation, contract, or test can solve the same issue.

A sophisticated mechanism with weak expected value should rank below a simple mechanism with a clear measurable effect.

## 6. Establish a baseline

For a meaningful architectural or orchestration change, record the current behavior before changing it when feasible.

Use the most direct evidence available:

- deterministic regression test;
- audit or smoke-test result;
- capability/bypass test;
- representative benchmark case;
- repeated benchmark runs when model variability matters;
- concrete token/tool/context/rework measurements.

Do not fabricate a baseline after the candidate has already changed the behavior.

If a credible baseline cannot be obtained, state that limitation and prefer a change whose value can still be demonstrated through a strong behavioral test.

## 7. Apply the smallest coherent intervention

Prefer this order unless evidence supports another choice:

1. delete unnecessary machinery;
2. correct an invalid platform assumption;
3. strengthen an existing contract;
4. add or strengthen a deterministic test or validator;
5. close an alternate-path bypass;
6. improve evidence provenance or freshness;
7. reduce model discretion or permanent context;
8. improve failure recovery or observability;
9. add new prompt/orchestration machinery only when simpler mechanisms are inadequate.

Do not add a new agent, skill, rule, hook, state, or abstraction merely because it gives the candidate a visible architectural home.

## 8. Compare candidate against baseline

Use the repository's benchmark dimensions where applicable:

- correctness;
- tests introduced;
- rework;
- critique findings caught;
- findings ignored;
- tool calls;
- subagent calls;
- research duplication;
- context consumed;
- latency;
- human interventions;
- unnecessary files changed.

Also measure the direct property targeted by the candidate when the generic benchmark dimensions are insufficient.

For stochastic Claude behavior, prefer repeated comparable runs over a single favorable example when practical. Keep prompts, fixtures, environment, and scoring criteria as stable as possible between baseline and candidate variants.

An efficiency win does not count if required correctness, safety, or enforcement guarantees regress.

## 9. Attack the candidate

Before accepting an improvement, look for ways its claimed benefit can fail.

Include, as applicable:

- equivalent tool or shell paths;
- stale evidence after edits;
- external or human modifications;
- unsupported Claude Code assumptions;
- prompt compliance failures;
- invalid workflow transitions;
- false-positive and false-success cases;
- context loading or scoping mistakes;
- degraded behavior on small/simple tasks;
- extra orchestration that costs more than it prevents;
- benchmark overfitting.

Add regression coverage for realistic failures when feasible.

## 10. Retain, revise, reject, or defer

Finish each candidate with one decision:

### RETAIN

Use when evidence shows the candidate improves the targeted behavior while preserving required guarantees and avoiding disproportionate new complexity.

### REVISE

Use when the hypothesis remains credible but the mechanism or measurement is inadequate.

### REJECT

Use when the candidate does not improve the target, creates regressions, duplicates existing behavior, depends on a false assumption, or adds unjustified complexity.

### DEFER

Use when the potential value is credible but required evidence cannot currently be obtained.

Do not preserve a candidate merely because implementation effort has already been spent.

---

# Discovery lanes

Use these as prompts for systematic exploration, not as a checklist that requires a finding.

## Platform semantic drift

Look for Claude Code assumptions that are stale, incomplete, or contradicted by current first-party documentation.

Examples:

- changed hook semantics;
- new or removed frontmatter fields;
- changed permission behavior;
- context-loading changes;
- subagent/tool restrictions;
- new platform capabilities that can replace custom machinery.

A newer native capability is especially interesting when it can delete custom orchestration while preserving guarantees.

## Determinism opportunities

Find important requirements currently expressed only as instructions, conventions, or model expectations that can be validated or prevented mechanically.

Do not mechanize subjective judgment merely for the sake of determinism.

## Alternate-path bypasses

Search for ordinary equivalent paths around claimed enforcement, including shell and subprocess equivalents, stale evidence, externally modified files, and semantically equivalent Claude Code capabilities.

## Evidence integrity

Inspect whether evidence proves the property it claims to prove.

Look for:

- commands unrelated to the acceptance criterion;
- evidence recorded without provenance;
- evidence surviving relevant changes;
- RED results failing for the wrong reason;
- GREEN results proving too little;
- final verification that can be satisfied by stale or partial state.

## Workflow state-machine quality

Look for:

- unreachable states;
- transitions that bypass required work;
- duplicated representations that can drift;
- stages whose output contract is too weak for the next stage;
- recovery paths that require manual state manipulation;
- unnecessary stages whose value is not measurable.

## Contract and boundary leakage

Check whether workers, skills, conductor responsibilities, artifacts, and deterministic enforcement have clear non-overlapping ownership.

Look for workers that silently plan, critics that repair, verifiers that implement, or skills that duplicate policy.

## Context and instruction efficiency

Identify instructions loaded permanently even though they are needed only conditionally.

Look for:

- duplicated policy across `CLAUDE.md`, rules, skills, and agents;
- large reference material loaded eagerly;
- verbose output contracts that do not improve downstream behavior;
- repeated repository research that could be represented once as an artifact;
- unnecessary subagent context.

## Failure behavior and recovery

Test what happens when assumptions fail, tools error, evidence is missing, a gate rejects a transition, a worker returns malformed output, or the environment prevents verification.

Prefer failures that are explicit, diagnosable, and repairable without bypassing the control plane.

## Observability

Ask whether a human or verifier can reconstruct:

- what state the workflow is in;
- why it entered that state;
- what evidence supports completion;
- which component made a decision;
- what changed after evidence was recorded;
- why a gate rejected an action.

Observability should serve debugging or assurance, not merely produce more logs.

## Security and permissions

Compare intended least privilege with actual available capabilities. Test whether nominal restrictions remain meaningful through ordinary alternate paths.

## Complexity deletion

Actively look for agents, skills, rules, hooks, states, schemas, or duplicated documents that can be removed or merged without reducing measured quality.

Deletion is a first-class improvement candidate.

## Benchmark blind spots

Challenge the evaluation system itself.

Ask whether current cases and metrics can detect the failure mode being optimized, whether metrics have clear scoring semantics, whether cases are concrete and reproducible enough, and whether the benchmark can distinguish a genuine gain from a lucky run or an overfit prompt.

## Representative-task regressions

A mechanism that helps complex work may impose needless cost on small work. Check whether the control plane scales ceremony and context proportionally to task complexity.

---

# Candidate record

For substantial open-ended improvement work, record each serious candidate in this shape:

```text
Candidate:
Classification: NEW | PARTIAL | DUPLICATE | OBSOLETE
Failure mode:
Current evidence:
Existing control and gap:
Platform evidence, if applicable:
Hypothesis:
Smallest intervention:
Baseline:
Target metric/behavior:
Non-regression requirements:
Alternate paths / attack cases:
Result:
Decision: RETAIN | REVISE | REJECT | DEFER
Confidence:
```

The record may live in the task response, a temporary research artifact, or a repository artifact when the user explicitly requests one. Do not create permanent process files for every investigation by default.

---

# Evidence standards

Prefer evidence in this order when applicable:

1. executable behavior and deterministic tests;
2. current first-party Claude Code documentation for platform claims;
3. the repository's captured first-party documentation snapshot;
4. repository architecture/contracts for intended behavior;
5. direct controlled experiments;
6. reasoned inference clearly labeled as inference.

Do not use model confidence as a substitute for evidence.

Separate:

- observed fact;
- interpretation;
- hypothesis;
- measured result.

If evidence conflicts, surface the conflict rather than selecting whichever source supports the preferred candidate.

---

# Benchmark discipline

The benchmark system is evidence infrastructure, not proof by itself.

A benchmark comparison is credible only when the compared variants are meaningfully comparable.

When feasible:

- use the same case, prompt, fixture, scoring rubric, and environment for baseline and candidate;
- record enough repeated runs to expose high variance when model behavior is stochastic;
- report both quality and cost dimensions;
- preserve raw observations needed to explain the score;
- distinguish an architecture-wide improvement from a case-specific optimization;
- add a regression case when a newly discovered failure mode was previously invisible.

Do not tune only to the current benchmark cases if doing so weakens general behavior.

A useful improvement to the benchmark system itself is valid when it makes future architectural claims more falsifiable.

---

# Reporting an improvement investigation

For an open-ended improvement task, prefer a concise report with:

1. `Current weakness` — the concrete failure or cost discovered;
2. `Why it was overlooked` — which existing mechanism or assumption made it non-obvious;
3. `Evidence` — repository, platform, and experiment evidence;
4. `Candidate` — the smallest proposed or implemented intervention;
5. `Measurement` — baseline versus candidate behavior;
6. `Regression/attack results` — what was tested to disprove the candidate;
7. `Decision` — retain, revise, reject, or defer;
8. `Next-best hypothesis` — only when another materially supported candidate remains.

Do not produce a long catalog of speculative ideas when one or two candidates have materially stronger evidence.

---

# Anti-patterns

Avoid these behaviors:

- treating every Claude-side instruction as a Codex instruction;
- assuming documented architecture equals actual enforcement;
- proposing a new agent before identifying the failure it solves;
- calling an idea novel without checking existing controls;
- counting configuration presence as capability proof;
- using one successful run as proof of a stochastic improvement when repetition is practical;
- optimizing tool calls or tokens while correctness declines;
- preserving complexity because it already exists;
- adding permanent context to solve a conditional problem;
- weakening tests or gates to validate a preferred design;
- measuring only what is easy rather than what the candidate claims to improve;
- turning Codex into a runtime dependency of the Claude control plane without an explicit architectural requirement.

---

# Completion question

Before declaring an open-ended control-plane improvement successful, answer:

> What measurable or behaviorally demonstrated property is better than the baseline, what important guarantees stayed intact, and why is this the simplest mechanism that achieved that result?

If that question cannot be answered with evidence, the investigation may still have produced a useful hypothesis, but it has not yet demonstrated an improvement.
