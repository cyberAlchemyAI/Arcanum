---
profile: autobayes-research
name: Invoke Plan - AutoBayes Research Closure
description: Whole closure plan for the remaining AutoBayes learning research.
type: invoke-plan
mode: plan
status: pass
last_updated: 2026-06-07
---

# Invoke Plan

## Target

Close the AutoBayes research tower into a final, source-backed learning pack for the Arcanum developer.

## Complexity

Medium-high research closure. The work is bounded to local research artifacts, but it spans paper claims, related-paper gaps, definition cards, examples, distillation, and bridge decisions.

## Layering

### L0 - Source Closure

Goal: make the paper's actual claims visible before any Arcanum translation.

Outputs:

- `tracks/paper-claim-ledger.md`
- source-kind markers across generated cards
- updated `residue/open-residue.md`

Validation:

- every major paper layer has a claim ledger entry;
- unsupported claims are marked `open-question`.

### L1 - Definition Closure

Goal: stabilize local definitions and glossary entries.

Outputs:

- `tracks/bayesian-lens-definition-card.md`
- `tracks/parameter-exposure-card.md`
- `tracks/cups-caps-boundary-shift-card.md`
- updates to `GLOSSARY.md` and `DEFINITIONS.md`

Validation:

- each card has source meaning, Arcanum reading, misuse warning, confidence, and promotion status.

### L2 - Example And Loss Closure

Goal: make local loss composition and examples concrete enough to teach from.

Outputs:

- `tracks/two-step-symbolic-loss-calculation.md`
- appendix/example updates in `tracks/appendix-examples-distill.md`

Validation:

- the worked calculation distinguishes energy, entropy, divergence, open free energy, and closed VFE/EUBO without collapsing signs or layers.

### L3 - Bridge And Distill Closure

Goal: produce the final Arcanum-facing synthesis and bridge decision.

Outputs:

- `tracks/implementation-residue-note.md`
- updates to `tracks/arcanum-bridge-decision.md`
- updates to `DISTILLED-KNOWLEDGE.md`
- optional `FINAL-LEARNING-PACK.md`

Validation:

- borrow/block/analogy-only decisions are explicit;
- no canonical Arcanum promotion occurs;
- final distill is usable without rereading the full paper.

## Smallest Working Units

| SWU | Objective | Outputs | Validation |
| --- | --- | --- | --- |
| `SWU-AB-LEARN-001A` | Close paper source ledger. | `tracks/paper-claim-ledger.md` | major paper layers covered |
| `SWU-AB-LEARN-001B` | Close definition cards. | Bayesian lens, parameter exposure, cups/caps cards | source meaning + Arcanum reading + misuse warning |
| `SWU-AB-LEARN-001C` | Close worked loss/example understanding. | symbolic loss calculation and appendix updates | layer/sign/source audit |
| `SWU-AB-LEARN-001D` | Close bridge and final distill. | implementation residue note, bridge update, final learning pack | no promotion drift; residue explicit |

## Subagent Strategy

Subagents are useful but optional. If used, lanes should be:

- `paper-ledger-steward`
- `definition-card-steward`
- `example-loss-steward`
- `bridge-decision-steward`
- `distill-steward`

Each lane must return:

```text
agent_id
role_id
spawn_status
join_status
close_status
artifact_paths
source_gap_addressed
residue
reroute
validation_result
```

The parent may report `PASS` only after every spawned lane is joined and closed, or explicitly blocked/timed out/handed off with residue and reroute.

## Execution Order

1. Read the context handoff pack and JSON index.
2. Validate the dispatch route.
3. Refresh the source/version record for arXiv `2503.18608` only if needed.
4. Produce `paper-claim-ledger.md`.
5. Produce the three definition cards.
6. Produce the two-step symbolic loss calculation.
7. Update glossary, definitions, and distilled knowledge.
8. Produce implementation residue note and bridge decision updates.
9. Update `NEXT.md` and `residue/open-residue.md`.
10. Produce `FINAL-LEARNING-PACK.md` when the tower is coherent.
11. Run read-back validation.

## Stop Conditions

Block if:

- source meaning cannot be separated from Arcanum analogy;
- related-paper work expands beyond named gaps;
- any subagent remains open or hidden;
- the task would require canonical Arcanum mutation;
- final artifacts cannot pass read-back source/promotion/residue checks.
