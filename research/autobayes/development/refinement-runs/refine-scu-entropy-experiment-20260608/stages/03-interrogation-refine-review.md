---
stage: 3
name: Interrogation (refine-review)
capability: interrogation
mode: refine-review
status: flag
verdict: proceed-with-repairs
dispatch_id: refine-scu-entropy-experiment-20260608
---

# Interrogation refine-review — Define critique

One question at a time; answers folded back into the define before design.

## Q1. Does the define claim falsifiability without naming a failing condition?

No — H1/H2 have an explicit failure condition (all proxies monotone, or minimum does not track SCU quality). **Pass.**

## Q2. Is entropy conflated with residue?

Partially flagged. `Ê_C` (residue rate) measures `E_energy` (the energy/divergence trace), while `Ê_A` measures `H_spread`. The define correctly flags this but must **not** average them into one curve — they may have different shapes. **Repair:** keep proxy curves separate; H1 is satisfied if *any* spread-type proxy (A) or constructive proxy (B) is U-shaped, with C reported as a contrast only.

## Q3. Circularity risk in H2?

High risk: if SCU quality is judged by the same signal as the proxy, co-location is tautological. **Repair:** SCU quality must come from a blind, independent rubric (e.g. human/3rd-model review of one-responsibility, recomposition success), pre-registered before proxy values are revealed.

## Q4. Is the independent variable actually one-dimensional?

"Unit size" bundles lines, files, relations, obligations. **Repair:** the design must pick one primary size operationalization (recommend: number of cross-unit relations/obligations the unit must preserve) and report others as secondary, so the x-axis is well-defined.

## Q5. Biggest unaddressed threat?

The difficulty confound (Q in define). A U-curve could appear because tiny units are ambiguous and huge units are hard *regardless of the translator*. **Repair:** require a control condition or a difficulty-matched corpus, and require the pilot to test the confound explicitly.

## Verdict

**flag — proceed with four repairs** (separate proxy curves; blind SCU rubric; one primary size axis; difficulty-confound control). Carry into distill-select and design.
