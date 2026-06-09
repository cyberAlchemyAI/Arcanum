---
stage: 6
name: Invoke Redefine / Design (proxy tournament)
capability: invoke
mode: design
pattern: tournament
join: ranked
status: pass
dispatch_id: refine-scu-entropy-experiment-20260608
subagent_receipts:
  - role: proxy-A-semantic-entropy-designer
    agent_id: a6a30a1d4da026afb
  - role: proxy-B-mdl-description-length-designer
    agent_id: a0b98eeab5d253d40
  - role: proxy-C-residue-rate-designer
    agent_id: a974d9e386b43c115
---

# Invoke Design — SCU Entropy Measurement (proxy tournament, ranked)

## Headline finding (reshapes the experiment)

**No single proxy produces the U-curve.** The semantic-entropy proxy (A), which most
literally measures `H_spread`, predicts a **monotone *decreasing* and saturating**
curve — it supplies only the **left (under-determination) arm**. The right (overload)
arm is owned by `R_rel`/`A_att`, which surface downstream as residue. Therefore:

> The SCU U-curve is **not** a property of one entropy axis. It is the sum of a
> descending spread/under-determination arm and an ascending overload/residue arm. The
> interior minimum exists only where these two separately-measured arms cross.

This is itself a sharpening of the Craft claim: "SCU = local minimum of entropy" is
only coherent if "entropy" means the *composite bundle*, not `H_spread` alone — exactly
the four-way split the [definition card](../../tracks/craft-entropy-definition-card.md) proposed.

## Proxy receipts (summary)

| Proxy | Measures | Predicted curve | Decisive falsifier | Measurability | Cost |
|---|---|---|---|---|---|
| A — semantic-entropy dispersion (Miller–Madow-corrected semantic-cluster entropy, N=20) | `H_spread` (left arm) | monotone ↓ then flat | left arm absent → Spearman ρ(size, Ê_A) not negative | 4/5 | high (~210 calls/unit) |
| B — two-part MDL `bits(schema\|ctx)+bits(residue\|repair)` (frozen reference LM NLL) | full bundle (both arms by construction) | U by construction; **r\*** is the empirical claim | **r\* not invariant across reference models/serializations** → U is an encoding artifact | 4/5 | moderate (×2 models ×2 serializations) |
| C — residue / validation-failure rate, per-obligation normalized | `E_energy` realized trace (downstream) | U (under-determination ↓, attention-loss ↑) | U vanishes under L(u) normalization, or argmin ≠ blind-rubric argmin | 5/5 | cheapest (mostly deterministic) |

## Pareto ranking (measurability × cost × falsifiability × construct depth)

1. **B (spine).** Only proxy that natively carries *both* arms and a single falsifiable
   minimizer `r*`. Its non-circular core — `r*` **codebook-invariance** plus H2
   co-location — is the strongest falsification in the tournament. Caveat: a U-shape
   alone is vacuous (guaranteed by construction); all empirical weight is on `r*`
   location, so pre-registration is load-bearing.
2. **A (left-arm validator).** Not dominated — it is the *only* direct measurement of
   `H_spread`, and its monotone-descending prediction independently proves B's
   descending arm is real spread, not an encoding artifact. Expensive but unique.
3. **C (right-arm anchor + cheap screen).** Not dominated — cheapest, run *first* to
   screen whether any U is plausible before paying for A/B, and quantifies how much of
   the curve is realized residue vs forward pressure. Weak on construct depth (trace, not
   pressure); strong on cost and directness.

**Decision: composite design, all three retained with distinct roles** — B as spine, A
validates the left arm, C anchors the right arm and screens cheaply. The blind SCU
rubric is the independent H2 axis. This is a ranked join, not an elimination: each proxy
de-circularizes the others.

## The composed experiment (recomposition proof)

- **Corpus:** one fixed, difficulty-matched corpus; unit size swept by **re-bundling the
  same obligations** into different granularities (so difficulty is constant; only
  relations-per-unit `r(u)` varies). This single control answers refine-review Q5.
- **x-axis:** `r(u)` = cross-unit relations/obligations per unit (the one primary size
  operationalization; others secondary).
- **y-axes (separate, never blended):** Ê_A (left arm), Ê_B/r(u) (composite, with `r*`),
  Ê_C normalized (right-arm trace). Each with bootstrap CIs.
- **Independent H2 axis:** blind SCU-quality rubric (one-responsibility, recomposition
  success), pre-registered, scored without seeing any proxy value.
- **H1 supported iff:** Ê_A descends, Ê_C ascends past an interior point, and Ê_B/r(u)
  shows an interior minimum whose `r*` is invariant across ≥2 reference models and ≥2
  serializations.
- **H2 supported iff:** the proxy minima and the blind-rubric quality peak co-locate at
  the same `r*` within a pre-registered tolerance band.
- **Falsified if:** Ê_A is flat/rising (no real spread), or Ê_B `r*` moves with the
  codebook (artifact), or all proxies are monotone, or minima do not track blind SCU
  quality.

Carried to the pilot for low-cost falsification before any full sweep is planned.
