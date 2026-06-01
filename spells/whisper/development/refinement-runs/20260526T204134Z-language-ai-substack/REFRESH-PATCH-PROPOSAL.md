# Refresh Patch Proposal: Whisper Pareto Dynamics

## Scope

Proposal-only patch plan for making Whisper's Pareto-aware dynamic operational.

## Recommended Decision

Use a `two_tier` Pareto dynamic:

1. Global tournament selects the composition strategy.
2. Part-level mini-tournament runs only when a part is delegated, revised, or fails validation.

This keeps the schema expressive without making every paragraph run a full tournament.

## Decision Record

- Decision: `two_tier`
- Status: approved
- Approval source: `/invoke lets go with two tier`
- Recorded at: `2026-05-29T10:04:53Z`

## Proposed Schema Shape

```yaml
pareto_tournament:
  tiering: two_tier
  objectives:
    - id: resonance
      question: "Does this create the intended emotional residue?"
    - id: relevance
      question: "Does this fit the target public and transport?"
    - id: trajectory
      question: "Does this move the narrative cleanly?"
  hard_gates:
    - opening_contract_compliance
    - citation_integrity
    - audience_legibility
  candidate_protocol:
    each_candidate_must_define:
      - technique_stack
      - target_reader_effect
      - expected_strengths
      - known_tradeoffs
      - failure_modes
      - part_sequence
      - objective_scores
  dominance_rule: "Reject a candidate only when another candidate is equal or better on all objectives and strictly better on at least one while passing the same hard gates."
  consensus_rule: "Select a non-dominated candidate that best matches author_objective; preserve rejected candidates as reusable alternatives."
```

## Proposed Validator Additions

- `validate_pareto_tournament(schema)`
- fail if `pareto_tournament.objectives` omits `resonance`, `relevance`, or `trajectory`
- fail if fewer than two candidates are compared
- fail if selected candidate lacks consensus rationale
- fail if rejected alternatives lack trade-off notes
- fail if `composition_plan.source_candidate_set` does not match the selected candidate

## Proposed Work-Pack Addition

Add follow-up SWU after approval:

```markdown
| SWU-WHISPER-PARETO-001 | TASK-WHISPER-SCHEMA-REFRESH | Add Pareto tournament schema and validator checks. | Decision on Pareto tiering. | `text-intent-substrate.yaml`; `spells/whisper/tools/validate-whisper-draft.py`; refresh report artifacts. | Schema validates, draft validator still passes, Pareto completeness checks fail on incomplete tournament fixtures and pass on accepted schema. |
```

## Apply Gate

Decision/work-pack apply gate is satisfied:

- The operator approved `two_tier`.
- `WORK-PACK.md` can now carry `SWU-WHISPER-PARETO-001` as a ready Task Session unit.

Remaining apply boundary:

- Do not patch `text-intent-substrate.yaml` or `validate-whisper-draft.py` inside Invoke.
- Execute those changes through `task-session` using `SWU-WHISPER-PARETO-001`.
