# Reporting

## Final Report Requirements

The final runtime response must include:

- selected unit,
- readiness verdict,
- validation report path,
- validation result,
- blockers or gaps,
- extra sources used outside the handoff pack,
- next route.

## Extra-Source Reporting

If any source outside `handoff-pack.md` and `handoff-index.json` is used, report:

| Field | Required |
| --- | --- |
| Source path | yes |
| Justifying gap | yes |
| Effect on result | yes |

## Completion Rule

Do not mark the native goal complete unless the validation report or equivalent
receipt exists and states pass, flag, or block for `SWU-GOAL-001`.
