---
stage: 2
name: Invoke Define
capability: invoke
mode: define
status: pass
dispatch_id: refine-coherence-metric-20260608
---

# Invoke Define — DCI + Craft redefinition

## Objective A — DCI metric

Define a Decomposition Coherence Index computable from the observability envelope
(`arcanum/framework/observability/templates/invocation-envelope.json`), measuring how well
the agentic system breaks work into coherent units.

- **Unit of measure:** one sigil invocation.
- **Residue signals (emitted):** `execution.status`, `observer.quality_bar_status`,
  `observer.workflow_gaps[]` (category, severity), `observer.output_contract_drift`.
- **Unit-size proxy:** `len(execution.files_changed)`.
- **Validation label (not an input):** `observer.reflection_trigger`, `recommendation`.
- **Boundary:** DCI measures **realized residue** (the trace of entropy after validation),
  **not** pre-translation entropy `H_spread`. It must name a gaming-resistance.

## Objective B — Craft definition redefinition (candidate)

Define the redline target for CRAFT-INITIAL-DEFINITION.md, grounded in the prior-art verdict
and the entropy definition card:

- **SCU:** correct "local minimum of entropy" / "pre-translation control on `E`" to "minimum
  of measured residue density per obligation (DCI-optimal), a post-hoc-located coherence
  optimum; entropy `E` is not directly measurable and is proxied by residue."
- **Entropy:** reserve the word for `H_spread`; rename the schema↔data gap to
  residue-pressure/divergence `E_energy`; keep `R_rel`, `A_att` as named separate terms.
- **DCI↔Craft model:** DCI is an estimator of `R` (residue) per unit — the post-translation
  operationalization of the pre-translation SCU criterion. Same optimum, two sides.
- Cite prior art (bias-variance, MDL, rate-distortion, semantic entropy, functorial
  inversion); claim no novelty. Produce a candidate redline + decision-gate, not an edit.

## Closure

Both objectives have named, emitted/locatable signals and an explicit honesty boundary.
Ready for refine-review.
