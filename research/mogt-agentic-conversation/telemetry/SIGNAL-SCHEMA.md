# MOGT Telemetry Schema

Append-only run signals for multi-objective game-theory conversation experiments.

## Envelope

- id
- timestamp
- project_id
- experiment_id
- run_id
- claim_id
- type
- severity
- decision_id
- policy_regime
- data

## Required Decision Fields

- active_objectives
- selected_action
- candidate_actions
- turn_count
- model
- operator

## Required Types

- stage-verdict
- gate-decision
- objective-frontier
- negotiation-turn
- convergence-outcome
- overhead-measurement
- evidence-update

## Notes

1. Signal streams must be append-only.
2. Gate outcomes for G1-G4 must be emitted when applicable.
3. Any evidence-update signal must reference both a claim ID and the supporting artifact path.
