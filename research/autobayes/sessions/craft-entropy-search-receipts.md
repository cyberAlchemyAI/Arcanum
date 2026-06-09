---
profile: autobayes-research
name: Craft Entropy Search — Lane Receipts
description: Per-lane source receipts from the Craft translation-entropy search fanout.
type: search-receipts
status: complete
dispatch: arcanum/research/autobayes/craft-entropy-search.dispatch.json
dispatch_id: craft-entropy-search-20260608
run_date: 2026-06-08
---

# Craft Entropy Search — Lane Receipts

Session for `entropy-source-fanout` (dispatch `craft-entropy-search-20260608`). Six
role-bound lane searchers ran in parallel under `parent_synthesis`. Each receipt
records the closest source-backed object, a citation, the schema/data/residue
mapping, per-PCRA coverage, one mark, and open residue. No lane promotes canonical
Arcanum or Craft-definition authority.

## Mark summary

| Lane | Role | Closest source object | Mark |
| --- | --- | --- | --- |
| L-info | info-theoretic-entropy-searcher | conditional entropy `H(D\|S)` | analogy |
| L-free | free-energy-elbo-searcher | variational free energy (energy + entropy terms) | promote-residue |
| L-gvi | gvi-loss-searcher | GVI loss / divergence / feasible-set triple | analogy |
| L-games | statistical-games-searcher | Bayesian lens + lax composition (mutual-information defect) | promote-residue |
| L-ppl | ppl-variance-searcher | amortization gap vs estimator variance vs model entropy | promote-residue |
| L-scu | scu-minimization-searcher | bias-variance U-curve / MDL | promote-residue |

## L-info — information-theoretic

- Closest source object: conditional entropy `H(D|S)` (entropy of produced artifact given schema).
- Citation: Shannon 1948, "A Mathematical Theory of Communication", §II.7 (equivocation); Cover & Thomas, *Elements of Information Theory*, 2nd ed., ch. 2.
- Mapping: The intuition maps — a fixed schema `S` induces a distribution over many plausible outputs `D`, and entropy measures that spread (Craft's "probabilistic spread"). It does **not** compute: Craft never defines `p(D|S)`, the outcome space, or a measure. Decisive break: `H(D|S)` is monotone-decreasing as the schema specifies more, but Craft entropy is **U-shaped in unit size** — the "too small loses meaning / high recomposition ambiguity" arm has no conditional-entropy analogue. The `entropy(F_PCRA, S, context, relation_load, unit_size)` signature also carries structural arguments that are not random variables.
- PCRA coverage: expresses probabilistic spread (this *is* equivocation) and contextual dependence (absorbable as `H(D|S, context)`). Cannot express relational load (a dependency-graph property, not a sample space) or attentional decay (no attention/salience primitive in Shannon entropy).
- MARK: **analogy**
- Open residue: Is there any outcome space + measure over artifacts `D` such that `p(D|S)` exists? Even granting it, the U-shape cannot come from `H(D|S)` alone — Craft entropy may be a **rate-distortion / information-bottleneck** quantity (description length traded against fidelity), which would explain the interior minimum but moves outside a plain-entropy borrow.

## L-free — variational free energy / ELBO

- Closest source object: variational free energy (negative ELBO), decomposed by the free-energy chain rule into a separate **energy** term and **entropy/regularizer** term.
- Citation: AutoBayes (arXiv:2503.18608); local `GLOSSARY.md` rows "Variational free energy", "Energy", "Entropy / regularizer"; `DEFINITIONS.md` D8 "Local Loss Composition"; Blei, Kucukelbir & McAuliffe 2017, "Variational Inference: A Review for Statisticians"; Jordan, Ghahramani, Jaakkola & Saul 1999.
- Mapping: schema ↔ generative model/prior `p`; produced data ↔ approximate posterior `q`; validation comparing data back to schema ↔ the evidence-gap that free energy `F = E_q[log q − log p]` measures; residue ↔ the realized value of that gap. The schema→data→validate→residue loop is structurally the model→q→bound→F loop. What does **not** map: free energy is signed and decomposes into **two** terms; Craft's single scalar `E` carries neither sign nor that decomposition, and Craft's residue is measured post-hoc against one schema, not as KL between two declared distributions.
- PCRA coverage: expresses Probabilistic (genuine distributions) and Relational strongly (entropy term composes via posterior-indexed expectation); Contextual weakly (context-as-conditioning). Cannot express Attentive — free energy has no attention-bandwidth primitive.
- MARK: **promote-residue**
- Open residue: Craft's scalar `E` conflates the two terms AutoBayes keeps separate — a fit/divergence **energy** term (what residue actually measures) and a **spread/entropy** term (multiplicity of plausible PCRA continuations). Should Craft split `E` into `E_energy` (expected schema↔data divergence, pre-translation, ≈ expected free energy) and `H_spread` (PCRA continuation entropy), reserving "entropy" for the latter?

## L-gvi — generalized variational inference

- Closest source object: the GVI optimization triple `P(ℓ, D, Q)` — a LOSS `ℓ` (how data attaches to parameters), a DIVERGENCE/regularizer `D` (toward a prior), and a feasible set `Q` — as a modular replacement for rigid KL-to-posterior.
- Citation: Knoblauch, Jewson, Damoulas, "Generalized Variational Inference" (arXiv:1904.02063); local `tracks/related-framework-crosswalk.md` rows 56, 68, 101–120; `levels/L0-corpus.md:56`.
- Mapping: the four Craft properties **split across the triple** instead of collapsing to one term — probabilistic spread + contextual dependence ↔ LOSS `ℓ`; relational load ↔ DIVERGENCE `D` (regularizer = pressure to preserve a structured prior of relations/obligations); attentional decay ↔ feasible set `Q` + optimization budget (bounded realizable family = attention/salience budget). What does **not** map: GVI has no object for recomposition/promotion upward (the tower step), and its `D` is divergence-to-prior, not entropy — so the name "entropy" is **not** vindicated by the regularizer (refutes the default hypothesis).
- PCRA coverage: expresses Probabilistic, Contextual, Relational. Cannot cleanly express Attentive as a *decay over unit growth* (`Q`/budget is static capacity, not a salience-decay curve), nor the recompose/promote dynamics.
- MARK: **analogy**
- Open residue: the valuable bridge is structural — Craft "entropy" is better modeled as a **modular triple** (evidence-attachment loss + relation-to-prior divergence + feasible/attention budget) than as one scalar `E`. Does adopting this require demoting the word "entropy", which matches none of the three GVI elements?

## L-games — statistical games / Bayesian lens

- Closest source object: the Bayesian lens forward/reverse structure composed into a parameterized statistical game, with the free-energy chain rule as the exact composition law; sharpest single object = the **lens reverse pass indexed by the pushed-forward prior `c_* π`**.
- Citation: Toby St Clere Smithe, "Approximate Inference via Fibrations of Statistical Games", arXiv:2306.17009 (`tracks/semantics-functor-reader.md:9`); AutoBayes §4–5 via `tracks/local-loss-composition-distill.md`, `tracks/semantics-functor-reader.md`; lens in `tracks/bayesian-lens-definition-card.md`; genus = Ghani/Hedges/Winschel/Zahn compositional game theory.
- Mapping: Craft forward pass (schema→data) ↔ lens forward model `c`; validate-and-residue ↔ lens reverse pass `c'_π(y)` and the gap to the exact inverse `c†_π`; **recomposition** ↔ lens/game composition `d ∘ c`. The chain rule shows recomposition is **not flat concatenation**: the parent composes typed local receipts but the upstream term must be evaluated under the downstream reconstruction and the correct belief-state index `c_* π` — a near-exact analogue of "the parent composes receipts; it does not rediscover the whole." Decisive finding: composed local gradients are generally **not** equal to the gradient of the global composite loss — the assignment is **lax**, the mismatch measured (under Shannon entropy) by **mutual information** between components. That laxness *is* relational load made formal: the cost of holding many coupled concepts is the non-additive mutual-information gap between local and global correctness. What does **not** map: lens objects carry exact distributions and a measured optimum (free energy); the PCRA translator has no measured posterior, no metric, no gradient.
- PCRA coverage: expresses Relational load directly and structurally (wiring + belief-state index + lax defect) and the optimization/parameter-exposure semantics (`(Θ, c)` = optimizer may only touch declared, authorized handles ≈ Craft bounded `relation_load(SCU)` / governed write scope). Cannot express probabilistic spread, contextual dependence, or attentional decay as scalar uncertainty.
- MARK: **promote-residue** (with a borrow component) — promote the games/lens view as the structural home for relational load, precisely because it shows relational load is **composition/laxness cost, not a scalar entropy term**.
- Open residue: the games framework *measures* its relational defect (mutual-information / lax gradient mismatch) because every local object is an exact distribution; Craft's residue is unmeasured. Can Craft's relational load be given an operational defect measure analogous to the lax mutual-information gap — a measurable cross-unit coupling residue — **without** inventing a posterior the PCRA translator does not have?

## L-ppl — PPL guide mismatch / inference variance

- Closest source object: the **amortization gap** (systematic guide error) as distinct from sampling/estimator variance and from irreducible model entropy.
- Citation: Cremer, Li, Duvenaud 2018, "Inference Suboptimality in Variational Autoencoders" (approximation vs amortization gap); Bingham et al. 2019, "Pyro"; Staton 2017, "Commutative Semantics for Probabilistic Programming"; local `GLOSSARY.md:33-34`.
- Mapping: three quantities must not merge — (1) **irreducible conditional spread** `H(p(data|schema))`, a property of the translator's distribution itself (Staton model semantics); (2) **estimator variance**, reducible Monte-Carlo noise, a pure runtime property; (3) **amortization gap**, systematic non-vanishing bias because one shared guide cannot hit the per-instance posterior. Craft's "probabilistic spread" clause ("many plausible continuations for the same schema") denotes (1), but Craft's *remedies* (more examples, declared constraints, stabilized vocabulary, SCU sizing) act on (2)/(3). So Craft **describes (1) but operates on (3)** and never separates them.
- PCRA coverage: probabilistic spread maps cleanly to irreducible conditional spread (definitional). Attentional decay maps to **none** of guide mismatch / estimator variance — it changes the *target* `p(data|schema)` as `|schema|` grows, not the approximation of a fixed target; PPL vocabulary assumes a fixed posterior.
- MARK: **promote-residue**
- Open residue: does "probabilistic spread" name a **definitional** property `H(p(data|schema))` (borrow) or the **runtime** suboptimality of approximating it (reject as definitional)? The split to promote: definitional entropy `= H(p(data|schema))` vs operational entropy `= inference suboptimality (approximation + amortization + sampling variance)`, with attentional decay belonging to neither and needing a third axis (target-drift under input load) PPL has no native term for.

## L-scu — SCU minimization / fidelity curve

- Closest source object: the **bias-variance trade-off** (U-shaped generalization error vs model/unit complexity); MDL a close second; free-energy minimization the weakest (no intrinsic U-shape in capacity).
- Citation: Geman, Bienenstock & Doursat 1992, "Neural Networks and the Bias/Variance Dilemma", Neural Computation 4(1); Rissanen 1978 (MDL); local `CRAFT-INITIAL-DEFINITION.md:187-244, 570-579`.
- Mapping: too-small unit = high bias / underdetermined ("high recomposition ambiguity"); too-large unit = high variance / attention loss ("relation drift, rising residue" — Craft's own word "overfit" on the large arm is direct bias-variance vocabulary). The SCU minimum and "smallest unit that still carries meaning" mirror MDL's two-part code (model cost vs residual cost). What does **not** map: bias-variance and MDL have a *defined, measurable* error axis with an estimable minimum; Craft's "translation entropy" axis has no defined estimator — the *shape* is a real analogue but the *axis is currently unmeasured* (Craft Open Question #4 concedes this).
- PCRA coverage: Probabilistic + Contextual drive the too-small (high-bias) arm; Relational + Attentional drive the too-large (high-variance) arm. SCU minimum = where bounded relation_load (variance control) still meets sufficient meaning (bias control).
- MARK: **promote-residue**
- Open residue: the missing measurement is the *vertical axis*. To answer OQ#4, operationalize `E` as one of: (a) output-distribution dispersion under resampling (self-consistency / semantic-entropy variance over N generations per unit — the most literal "entropy"); (b) a two-part description length (schema/context bits + residue/repair bits → MDL minimizer); or (c) post-hoc residue/validation-failure rate vs unit size. Until an axis is instrumented and an interior minimum is demonstrated, "SCU is the local minimum of entropy" is a bias-variance-shaped **hypothesis**, not a measured law, and "SCU selection is the pre-translation control on `E`" is unfalsifiable as written.
