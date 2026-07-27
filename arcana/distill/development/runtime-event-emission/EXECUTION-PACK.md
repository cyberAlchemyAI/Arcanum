# Execution Pack: Distill Runtime-Event Emission

## Wave Order

| Wave | Layer | Units | Entry Gate | Exit Evidence |
| --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | L0 | DRE-001 | Sigil Development accepts owner/path design | one accepted event append and fail-closed negatives |
| [W1](work-pack/waves/W1.md) | L1 | DRE-002, then DRE-003 | W0 pass | both complete paths resolve and preserve identity policy |
| [W2](work-pack/waves/W2.md) | L2 | DRE-004, DRE-005, DRE-006 | W1 pass | direct telemetry/status/docs agree |
| [W3](work-pack/waves/W3.md) | L3 | DRE-007, then VERIFY | W2 pass | generated parity and integrated closeout pass |

## Scheduling Rules

- Execute one SWU at a time.
- DRE-002 and DRE-003 share emitter/fixture surfaces and are sequential.
- Generated files are never edited before canonical validation.
- Verification cannot repair implementation; it returns residue to the owning
  SWU.

## Result Contract

Every SWU returns:

```yaml
swu_id: SWU-DRE-NNN
result: pass | flag | block | interrupted
capability_ref: sigil-development | bootstrap | verification
receipt_kind: lifecycle | local-fallback | blocked
receipt_artifact: work-pack/results/SWU-DRE-NNN-RESULT.md
files_touched: []
validation: []
blockers: []
residue: []
reroute: next SWU id or none
handoff_note: exact successor gate
```
