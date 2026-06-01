# Task CRAFT-ARCH-004: Create Promotion Readiness Review

## Objective

Create a promotion readiness review that evaluates whether Craft should move toward promotion review, remain local, narrow scope, or defer.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L3 |
| Slice | S-ARCH-004 |
| Wave | W3 |
| Complexity | low |

## Source Contracts

- `development/craft/CRAFT-ARCHITECTURE.md#Promotion Decision Path`
- `development/craft/CRAFT-VALIDATION-EXAMPLES.yml`
- `development/craft/CRAFT-VALIDATION.md`
- `development/craft/CRAFT-ARCHITECTURE-GLOSSARY-CONSISTENCY.md`
- `development/craft/CRAFT-ARCHITECTURE-INPUTS.md`

## Dependencies

- CRAFT-ARCH-003 must pass.

## Implementation Detail

Create `development/craft/CRAFT-PROMOTION-READINESS.md`.

The review should not promote Craft. It should report evidence and recommend one of:

- `promote-review`,
- `defer`,
- `narrow`,
- `stay-local`.

## Smallest Working Units

### SWU-CRAFT-ARCH-006

Goal: produce the readiness review.

Dependencies: SWU-CRAFT-ARCH-005.

Write scope:

- `development/craft/CRAFT-PROMOTION-READINESS.md`

Done criteria:

- Review lists required promotion evidence from architecture.
- Review maps current evidence to each requirement.
- Review names remaining blockers, flags, and deferred side-thread dependencies.
- Review gives one explicit recommendation without mutating canonical surfaces.

Acceptance evidence:

- Recommendation is present and supported by evidence.

Validation surface:

- Manual review against `CRAFT-ARCHITECTURE.md#Promotion Decision Path`.

Execution owner: manual.

Handoff note:

Err on the side of candidate/local if evidence is incomplete. Promotion is a later explicit route.

## Synchronization Rules

Do not edit registry, spell, sigil, or runtime files. This task is a review artifact only.
