---
stage: 2
name: Invoke Define
capability: invoke
mode: define
status: pass
dispatch_id: refine-scu-entropy-experiment-20260608
---

# Invoke Define — SCU Entropy Measurement Experiment

## Objective

Define an experiment that turns two currently-unfalsifiable Craft claims into testable ones:

- **H1 (minimum):** translation entropy, measured by a proxy, is a non-monotone (U-shaped) function of work-unit size with an interior minimum.
- **H2 (control):** the interior minimum co-locates with the independently-judged SCU, so that choosing unit size near the minimum is the "pre-translation control on E."

## Measurable axis (the missing vertical axis)

`E` is not directly observable. Define it operationally as a **proxy** `Ê(u)` of unit `u`. Three proxy families are admissible (compared in the design tournament):

- `Ê_A` — semantic-entropy / self-consistency dispersion over N stochastic generations of the same unit.
- `Ê_B` — two-part description length: `bits(schema|context) + bits(residue|repair)`.
- `Ê_C` — post-hoc residue / validation-failure rate after one translation attempt.

## Independent variable

`u` = work-unit size for a **fixed objective on a fixed corpus**, swept across a granularity ladder (e.g. one SWU = k relations/obligations, k increasing). Difficulty held constant so the only thing that changes is how much the unit asks the translator to hold at once.

## Controls and confounds (named now, hardened in design review)

- Corpus difficulty must not co-vary with `u` (else a monotone curve is a difficulty artifact, not entropy).
- SCU "quality" must be judged **independently** of the proxy (blind rubric) to test H2 without circularity.
- Proxy `Ê_C` measures the `E_energy`/residue trace, not `H_spread`; it tests a different sub-mechanism (see definition card) and is included as a contrast, not as ground truth.

## Falsifiability statement

The design is only valid if it can fail. **Failure = all admissible proxies monotone in `u` (no interior minimum), or the minimum does not track independent SCU quality.** Either outcome refutes "SCU is the local minimum of entropy" as written.

## Closure

The define names what is built (a falsifiable measurement experiment), why (R3 unfalsifiability), the axis, the variable, the prediction, and the failure condition. Ready for refine-review.
