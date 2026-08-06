# Stage 03 — Interrogation refine-review

## Question 1

- Context: the existing audit treats absent future material as a global readiness failure even when the immutable plan contract passes.
- Question: should readiness be reusable until plan drift, while selected-unit material remains a live Task Session condition?
- Why it matters: this selects between removing duplicated orchestration and weakening admission.
- Recommended default: yes, only with a separate non-authoritative receipt and live drift checks.
- Operator answer: confirmed in the approved Refine strategy.
- Decision: adopt the plan-then-admit split; retain strict legacy behavior.

## Critique ledger

| Challenge | Required response | Define status |
| --- | --- | --- |
| A material package is produced from a semantically different plan revision. | Task Session recomputes selected semantic components and compares package sources; block. | covered |
| A user selects a unit outside the ready frontier. | Selected unit must be present exactly once in the receipt frontier; block. | covered |
| Commands or write scope change after readiness. | Selected-value component digest differs; block and require new audit. | covered |
| Closeout updates task status or handoff bookkeeping after one SWU. | Status/lifecycle receipts change, but unchanged semantic component digests preserve the plan epoch. | covered |
| Material is absent. | No mutation; produce package through its owner, then retry Task Session admission without re-auditing unchanged plan. | covered |
| A legacy caller expects missing material to block audit. | Default remains strict `1.0.0`; opt-in additive profile only. | covered |
| Plan defects are mislabeled runtime-pending. | Only absence of execution-epoch material may be pending; every other category remains blocking. | covered |
| Audit pass is mistaken for execution approval. | Receipt fixes `selected_unit=null`, `authority_effect=none`, `mutation_ready=false`. | covered |

## Verdict

`pass`, pending the independent admission-boundary critic. No additional operator question is required because the only consequential architecture choice was explicitly confirmed.
