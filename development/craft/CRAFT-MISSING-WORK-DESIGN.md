# Craft Missing Work Design

## Purpose

Design the smallest missing-work path after the approved subagent strategy run.

## Selected Unit

The smallest coherent completion unit is:

```text
Produce or block the Interrogation refine-review owner-stage receipt for the current Refine run.
```

This unit recomposes into the broader Craft validation path because Distill and every later stage depend on Interrogation refine-review.

## Inputs

| Input | Role |
| --- | --- |
| `CRAFT-REFINE-MISSING-APPROVED-RUN.md` | Joined subagent findings and parent decision. |
| `CRAFT-MISSING-BLOCKERS-AND-GAPS.md` | Blocker/gap ledger. |
| `evidence-index.json` | Current stage evidence authority. |
| `stages/03-interrogation-refine-review.md` | Stale stage handoff to repair or supersede. |
| `invoke-define/RESULT.md` | Owner-stage Define output to review. |

## Design

The missing-work package should have one first live-test task:

1. Build a context pack from the current run evidence.
2. Repair or supersede stale Interrogation blocked reason.
3. Produce a local Interrogation `refine-review` owner artifact.
4. Write `receipts/03-interrogation-refine-review.json`.
5. Sync evidence so Interrogation is either `pass` with receipt or `block` with an actionable receipt.
6. Keep Distill blocked unless Interrogation passes.

## Guardrails

- Use local skill surfaces and local artifacts only.
- Treat command-surface text as historical evidence unless a current work-pack reopens it.
- Do not promote Craft.
- Do not evaluate Distill in the same task unless the Interrogation receipt is already pass and a separate task authorizes it.
