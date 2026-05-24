# TechniqueSpec: Set-Based Tournament

```text
technique_id: set_based_tournament
display_name: Set-Based Tournament
type: mode mechanic
phase: pitch-off
hook: before_pitch_off
activation: Tournament mode
```

## Allowed Inputs

- `ModeProfile.proposal_tracks`
- `TrackState[]`
- `Technique pack traces`
- `Tension ledger`
- `RunFrame.constraints`

## Questions

- What assumption makes each track attractive?
- What option value does each track preserve?
- What evidence would eliminate each track?
- Which track should converge now, and why?
- Is no winner justified yet?

## Emits

```text
technique_id
track_id
track_assumption
option_value
elimination_condition
comparison_scores
winner_or_preserved_options
convergence_rationale
decision: pass | flag | block
```

## Comparison Criteria

- context fit
- closure
- recomposition
- evolution fit
- cognitive load
- validation cost
- risk of brittle minimalism
- risk of premature generality

## Verdict Rules

- Pass: a winner or preserved option set is justified by explicit criteria.
- Flag: more than one viable option remains, but the next evidence needed is clear.
- Block: no winner can be selected and the user must decide a blocker tradeoff.

## Failure Behavior

Ask a human gate, preserve alternatives, or route to Decision-Gate.

## Anti-Patterns

- Making proposals compete by style or confidence.
- Keeping all options alive after elimination evidence is already clear.
- Collapsing to one track because of budget pressure without recording the tradeoff.
