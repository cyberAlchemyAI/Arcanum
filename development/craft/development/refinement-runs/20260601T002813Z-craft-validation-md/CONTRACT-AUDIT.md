# Refine Contract Audit

## Verdict

`flag`

The native Refine wrapper reported `pass`, but this run does not satisfy the canonical Refine contract strongly enough to treat it as a completed Craft validation pass.

## What Passed

| Check | Result |
| --- | --- |
| Refine command resolved | pass |
| Required stage commands resolved | pass: `context-builder`, `invoke`, `interrogation`, `distill`, `dispatch-spec`, `runtime-handoff`, and `refine` all resolve |
| Wrapper run completed | pass |
| Observability signal recorded | pass: refine ledger line `307` |
| Research mode | pass: `no-research`, no external research used |

## Contract Drift

| Required Contract | Observed State | Severity |
| --- | --- | --- |
| Materialized run must include `REFINE-DISPATCH.json` before runtime-backed stage execution. | Missing from the run folder. | high |
| Stage artifacts must be owned outputs or explicit blocked reasons. | Most stage files are `local-skill` runtime-native handoff stubs with `STATUS: flag`. | high |
| `pass` stages must reference actual owner artifacts. | The evidence index marks handoff stubs as `pass` because files exist. | high |
| Final synthesis must be produced from stage artifacts. | Final stage is also a handoff stub, not a final interrogation/synthesis artifact. | high |

## Interpretation

The original missing-command blocker is cleared. The new blocker is runtime evidence semantics:

```text
local-skill handoff stubs are being counted as passed stage artifacts.
```

This means the command surface can now route Refine, but the native Refine wrapper still needs to distinguish:

- handoff prepared,
- owner stage actually executed,
- owner stage returned a receipt,
- owner stage blocked or flagged.

## Recommended Next Route

```text
invoke plan development/craft/CRAFT-REFINE-RUNTIME-STAGE-RECEIPTS
```

Purpose: create a bounded work-pack that repairs native Refine stage evidence classification so `local-skill` handoff stubs cannot be marked as completed owner-stage artifacts.

## Non-Goals Preserved

- Craft is not promoted.
- No external research was used.
- No registry, sigil, spell, scoring, generated index, or role delegation surface was promoted.
