# TechniqueSpec: Frame-Expiry Note

```text
technique_id: frame_expiry_note
display_name: Frame-Expiry Note
type: closeout
phase: final synthesis
hook: before_verdict
activation: always
```

## Allowed Inputs

- `RunFrame.target_context`
- `CandidateUnit`
- `Evolution profile trace`
- `Tension ledger`

## Questions

- Under what context change would this optimization point stop being responsible?
- What new evidence would require rerunning the sigil?
- Which deferred complexity would become active first?

## Emits

```text
technique_id
expiry_condition
rerun_trigger
first_deferred_complexity_to_revisit
decision: pass | flag | block
```

## Verdict Rules

- Pass: the result names a plausible expiry condition or says why the frame is stable enough for now.
- Flag: the expiry condition is broad but still useful.
- Block: the run claims finality for an obviously unstable frame.

## Failure Behavior

Downgrade readiness to flag or block, depending on how much the missing expiry condition affects the verdict.

## Anti-Patterns

- Claiming the selected unit is universally optimal.
- Hiding uncertainty by saying "future work" without a trigger.
