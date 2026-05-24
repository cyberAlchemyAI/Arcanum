# TechniqueSpec: Navigable Result Check

```text
technique_id: navigable_result_check
display_name: Navigable Result Check
type: closeout
phase: final synthesis
hook: before_verdict
activation: always
```

## Allowed Inputs

- `RunFrame.objective`
- `RunFrame.output_artifact`
- `ResultEnvelope`
- `Concept layer map`
- `Tension ledger`
- `Next-route recommendation`

## Questions

- Can a human or future agent tell what this result is for?
- Can they tell where to start reading or acting?
- Does the result name what changed during the run?
- Does it separate decided, deferred, and unresolved items?
- Does it explain how to use the selected concept unit in the expected output artifact?
- Does it name the next route and owner clearly enough to continue work?

## Emits

```text
technique_id
start_here
artifact_use
changed_in_this_run
decided_items
unresolved_items
next_action
decision: pass | flag | block
```

## Verdict Rules

- Pass: the result has a clear reading path, artifact use, unresolved gap summary, and next action.
- Flag: the result is usable but needs a short navigation note before handoff.
- Block: the result is too dense or ambiguous for a user or future agent to act on responsibly.

## Failure Behavior

Add a navigation guide before claiming pass. Downgrade to flag when the guide is partial but usable. Downgrade to block when the missing navigation hides a blocker decision, route, or artifact purpose.

## Anti-Patterns

- Returning a technically complete concept map without explaining how to use it.
- Hiding unresolved decisions inside the reduction trace.
- Treating "next route" as optional when downstream work is expected.
- Forcing the reader to reconstruct the objective-output artifact pair from conversation context.
