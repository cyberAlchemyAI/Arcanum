# Execution Pack: Craft Missing Work

## Wave W0

| Field | Value |
| --- | --- |
| Goal | Prove or block the `Interrogation refine-review` owner-stage receipt path. |
| Task | CRAFT-MISSING-INTERROGATION-001 |
| Entry Gate | Context Builder and Invoke Define receipts exist and pass. |
| Exit Evidence | `receipts/03-interrogation-refine-review.json`, owner artifact, and synced run/package state. |

## Stop Conditions

- Stop if Interrogation cannot produce owner-stage evidence; write a block receipt.
- Stop if a command-surface route is required as execution authority.
- Stop if Distill would be evaluated without a completed Interrogation receipt.
- Stop if any task tries to promote Craft.
