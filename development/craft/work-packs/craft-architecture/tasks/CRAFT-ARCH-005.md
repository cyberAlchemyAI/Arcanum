# Task CRAFT-ARCH-005: Sync Craft Package State

## Objective

Synchronize the Craft package entrypoint and durable session ledger after architecture-hardening evidence exists.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L3 |
| Slice | S-ARCH-004 |
| Wave | W3 |
| Complexity | low |

## Source Contracts

- `development/craft/CRAFT-ARCHITECTURE-WORK-PACK.md`
- `development/craft/CRAFT-VALIDATION-EXAMPLES.yml`
- `development/craft/CRAFT-VALIDATION.md`
- `development/craft/CRAFT-PROMOTION-READINESS.md`
- `development/craft/README.md`
- `development/craft/SESSION-LEDGER.md`

## Dependencies

- CRAFT-ARCH-004 must pass.

## Implementation Detail

Update only package-state artifacts:

- `development/craft/README.md`
- `development/craft/SESSION-LEDGER.md`

The sync should add completed architecture-hardening artifacts and name the next route from the readiness review.

## Smallest Working Units

### SWU-CRAFT-ARCH-007

Goal: sync README and session ledger after readiness review.

Dependencies: SWU-CRAFT-ARCH-006.

Write scope:

- `development/craft/README.md`
- `development/craft/SESSION-LEDGER.md`

Done criteria:

- README and session ledger list the validation examples, validation guide, and readiness review.
- Current verdict reflects the readiness review, not a stronger promotion claim.
- Next route is explicit.
- Runtime/interface and automation deferrals remain visible.

Acceptance evidence:

- README and SESSION-LEDGER agree on verdict, artifacts, and next route.

Validation surface:

- Manual entrypoint review from README to session ledger to readiness report.

Execution owner: manual.

Handoff note:

This is the only task in this work-pack allowed to update package state. It must wait for readiness evidence.

## Synchronization Rules

Do not update package state before CRAFT-ARCH-004. Do not claim promotion unless a separate explicit promotion route has already happened.
