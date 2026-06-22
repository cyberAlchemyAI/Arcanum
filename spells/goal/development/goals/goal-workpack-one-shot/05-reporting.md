# Reporting

## Final Report Requirements

The final runtime report must include:

- selected stream: `GOAL-WORKPACK-ONE-SHOT`,
- wave/SWU status table,
- receipt artifact paths,
- files touched,
- validation commands or review checks and results,
- blockers and residue,
- extra sources used outside the handoff pack,
- public/private boundary result,
- generated-surface boundary result,
- next route.

## Extra-Source Reporting

For every source outside `handoff-pack.md` and `handoff-index.json`, report:

| Field | Required |
| --- | --- |
| Source path | yes |
| Justifying gap | yes |
| Effect on result | yes |

## Completion Rule

Do not mark the native goal complete unless each attempted SWU has a receipt and
the final stream report states pass, flag, or block.
