---
name: ideate
description: Convert a raw engineering request into a precise problem definition without prematurely choosing an implementation. Used by the audited workflow during IDEATION and PROBLEM_DEFINITION.
user-invocable: false
---

# Ideation and problem definition

## IDEATION
Capture:
- the raw request in neutral language;
- the observable outcome the user wants;
- explicit assumptions, each labeled as validated or unvalidated;
- concrete open questions that would materially change scope or design.

Do not select libraries, schemas, architecture, or implementation sequence yet.

## PROBLEM_DEFINITION
Produce:
- Problem: current undesirable state or missing capability;
- Goals: observable outcomes;
- Non-goals: explicit exclusions;
- Constraints: compatibility, security, performance, delivery, repository, or operational constraints;
- Acceptance Criteria: externally observable conditions that can later be verified.

A requirement is not validated merely because it seems reasonable.
