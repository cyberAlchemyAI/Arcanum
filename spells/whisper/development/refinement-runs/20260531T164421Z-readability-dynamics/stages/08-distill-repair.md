# Stage 08: Distill Repair

Status: `pass`

## Repaired Unit

`readability_dynamics_layer` becomes:

A transport-aware, source-stable, validator-backed layer that annotates prose with rhythm units and discourse moves so review HTML can render readable beats without losing agent-addressable anchors.

## Final Shape

```text
text_intent_substrate
  -> composition_parts
  -> composition_plan
  -> draft_artifact
  -> readability_dynamics
  -> review_html
  -> review_payload
  -> revision_plan
  -> learning_residue
```

## Pareto Comparison

| Route | Readability Effect | Governance Fit | Cost | Review Utility | Verdict |
| --- | --- | --- | --- | --- | --- |
| CSS-only | medium | low | low | low | reject |
| Validator-only | medium | high | low | medium | viable but incomplete |
| Schema plus renderer plus validator | high | high | medium | high | select |
| Full academic metric engine | uncertain | medium | high | medium | defer |

Selected route: schema plus renderer plus validator.

Reason: it is non-dominated for the current Whisper problem. It improves the visible reading experience, preserves governance, and gives agents better anchors for revision.

