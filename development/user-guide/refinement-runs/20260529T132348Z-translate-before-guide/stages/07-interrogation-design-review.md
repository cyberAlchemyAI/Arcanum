# Stage 07: Interrogation Design Review

Status: `flag`

## Findings

| Severity | Finding | Repair |
| --- | --- | --- |
| P1 | Translate could overstep by changing the target concept to fit the source domain. | Require target-domain definition and mapping limits in every output. |
| P1 | Guide dispatching subagents can become unbounded. | Guide needs budget, route, and evidence gates before subagent/research dispatch. |
| P2 | Translate needs User data but should not own User memory. | Translate reads preference handles and returns receipts; User owns ledger writes. |
| P2 | Translate output may be mistaken for canonical glossary. | Mark it as user-facing bridge output unless promoted separately. |

## Verdict

The split is good. Proceed with `Translate` first, but keep Guide dispatch governance as a separate later design.
