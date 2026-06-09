# Craft Formal Foundations

Status: initial research product
Date: 2026-06-08
Scope: map Craft's operational vocabulary to the formal results that already prove (or refute) its load-bearing claims
Source frame: `development/craft/CRAFT-INITIAL-DEFINITION.md`, the `domainspec-theorem` Lean formalization, and Smithe & Perin, *AutoBayes* (arXiv:2503.18608)

## Purpose

Craft was defined operationally and grounded in analogy to Spivak's functorial data migration, Lawvere's functorial semantics, and Bedau's weak emergence (see `CRAFT-INITIAL-DEFINITION.md#research-grounding`). Those were named as *analogy, not authority*.

Since then, two bodies of work have made the analogy precise:

- **`domainspec-theorem`** — a machine-checked (Lean 4) category-theoretic formalization of schema/data translation and the information it loses. This is the **discrete, categorical** cousin of Craft.
- **AutoBayes** (Smithe & Perin, 2025) — a category-theoretic framework for compositional variational inference, where the gap between an approximate and an exact model is a composable loss. This is the **continuous, probabilistic** cousin of Craft.

This document records, term by term, where each Craft concept has a formal counterpart, what that counterpart **proves** versus what remains **analogy**, and which proven results should constrain Craft's design.

This is a foundations map, not a promotion. Nothing here moves a Craft term into a canonical surface. It records external formal support and the honesty boundary around it.

## How To Read This

Craft's translator is PCRA — probabilistic, contextual, relational, attentive — and so Craft deliberately does **not** target zero residue (`CRAFT-INITIAL-DEFINITION.md#loop-2-stabilize-the-formal-spine`). The formal cousins assume cleaner translators than an LLM. So the correct reading is:

```text
The formal results describe the structure Craft operates inside.
They do not claim an LLM achieves the clean cases.
They tell Craft which gaps are unavoidable, which are independent,
and which can never be closed by recursion alone.
```

Two altitudes, kept separate throughout:

- **Proven**: there is a sorry-free Lean theorem (domainspec) or a stated-and-proved proposition (AutoBayes) for this.
- **Analogy**: the correspondence is structural and useful, but the formal object assumes conditions LLM-centered work does not meet.

## Two Formal Cousins, One Shape

Both cousins formalize the same move Craft calls schema → translator → data → residue.

| Craft frame | domainspec-theorem (discrete) | AutoBayes (probabilistic) |
| --- | --- | --- |
| Schema | small category `L1` (concepts and their relations) | open model `c : X →• Y` (a measure kernel with latent space) |
| Data | `Set`-valued functor / instance on the schema | a distribution / sampled artifact from the model |
| Functor-like translator | compilation functor `Δ : L1 → L2`, with the migration triple `Σ_Δ ⊣ Δ* ⊣ Π_Δ` | the model together with its Bayesian inversion `c†`, composed by the Bayesian chain rule |
| Residue | failure of the adjunction unit `η` to be an isomorphism (typed: schema-level and instance-level) | the divergence between approximate inversion `c′` and exact posterior `c†` (KL, then variational free energy) |
| Reflection / recompose | the reflection tower as a diagram `N → Cat` with a colimit | composition of local losses by the chain rule for free energy |

The shared claim both cousins make precise — and that Craft asserts operationally — is: **a complex artifact's correctness can be assembled from the correctness of its parts, as long as the residue is carried correctly between layers.** AutoBayes proves this as a chain rule (their Theorem 23); domainspec proves the tower assembles into a colimit.

## Term-By-Term Map

| Craft term | Formal counterpart | Cousin / file | Status |
| --- | --- | --- | --- |
| Schema / Data | category and instance; open model and distribution | domainspec `DomainSpec.lean`; AutoBayes Def. 1, 9 | proven (objects exist and compose) |
| Functor-Like Translator | compilation functor `Δ` with migration triple `Σ_Δ ⊣ Δ* ⊣ Π_Δ` | domainspec `DomainSpec.lean` | proven |
| PCRA Translation | stochastic kernel `X ⤳ Y` (probabilistic, context-dependent map) | AutoBayes §2 notation | analogy (kernel is probabilistic; LLM-specific PCRA properties are not formalized) |
| Residue | failure of unit `η` to be iso; `noise = coker(η)` | domainspec `UniversalResidueFunctor.lean`, `NoiseFunctor.lean` | proven |
| Residue — two independent levels | schema-level `η^sch` and instance-level `η^ins` are independent | domainspec `M6Counter.lean` | proven (see Design Constraint 1) |
| Residue — as divergence | KL divergence between approximate and exact inversion | AutoBayes §4, `KLDivergence.lean` (domainspec) | proven |
| Entropy (translation) | fiber cardinality of a too-coarse schema; `S = k log W` as functorial residue | domainspec `EntropyAsFFResidue.lean` | proven (discrete, uniform prior) |
| Entropy stabilizes | finite monotone residue chain reaches a constant plateau | domainspec `SecondLawDiscrete.lean` | proven (finite, discrete) — see Design Constraint 3 |
| Reflection Tower | anchored tower as `N → Cat` diagram with colimit `L_ω` | domainspec `ReflectionTowerAnchored.lean`, `TowerColimit.lean` | proven (the tower assembles) |
| Tower has no final closure | self-description obstruction persists at every finite rung; ω-absorption refuted | domainspec `F11TransfinitePersistence.lean`, `StrangeLoop.lean` | proven — see Design Constraint 2 |
| Recompose / chain rule | inversions compose by the Bayesian chain rule; free energies compose | AutoBayes Thm 13 (inference), Thm 23 (free energy) | proven |
| Local validation that composes | local loss functions compose without re-deriving the whole | AutoBayes Thm 23 ("statistical games") | proven |

## Load-Bearing Correspondences

### Residue is real, typed, and composable

Craft treats residue as a first-class object, not an error. Both cousins agree and go further:

- domainspec defines residue as the precise failure of an adjunction unit `η` to be an isomorphism, and `noise` as its cokernel — a *typed categorical object*, exactly Craft's stance that "residue is signal, not waste."
- AutoBayes defines the residue between an approximate inversion and the true posterior as a KL divergence, then shows (their §4) that this divergence **obeys a chain rule**: the residue of a composite is built from the residues of its parts.

Craft consequence: residue can be recorded per layer and recomposed up the ledger without re-deriving a global measure. This is the formal license for the recursive ledger.

### Translation entropy has a literal meaning

Craft's "translation entropy" was introduced by analogy. domainspec gives it a definition: in `EntropyAsFFResidue.lean`, Boltzmann entropy `S = k log W` is exactly the fiber cardinality of a coarsening functor — *the count of distinct things the schema cannot tell apart*.

Craft consequence: "entropy rose because the unit carried too many competing relations" stops being metaphor. It is, in the clean case, the number of distinct intents that map to the same under-specified schema slot. This sharpens the SCU rationale: a good unit is one whose schema slot is not collapsing distinct meanings.

### The tower assembles, and it never finishes

domainspec proves both halves of what Craft needs:

- the reflection tower is a genuine diagram with a colimit `L_ω` (`TowerColimit.lean`) — *something coherent exists at the limit*, so recursion is not just hand-waving;
- the self-description obstruction persists at **every finite rung** and the limit does not absorb its own residue (`F11TransfinitePersistence.lean`, `StrangeLoop.lean`) — *no finite number of layers fully closes*.

Craft consequence: this is the formal backing for stopping by decision, not by completion. See Design Constraints 2 and 3.

## Design Constraints These Results Impose

These are not validation. They are places where the proven results should shape Craft.

### Constraint 1 — Validate schema and data separately

`M6Counter.lean` refutes the tempting claim that a clean schema forces clean data. With a four-object counterexample it shows: a translator can be injective and faithful on the *schema* and still lose information at the *instance* level (the migration functor inserts fresh "Skolem null" witnesses where the schema underdetermines the data).

Craft must therefore treat schema-fidelity and instance-fidelity as **two independent gates**. Passing a design/schema review tells you nothing, by itself, about whether the produced artifact preserved intent. Craft's validation surface should record both, separately, and never let one stand in for the other.

This maps cleanly onto Craft's existing residue taxonomy: *domain/structural residue* lives at the schema gate; *translation/attention/recomposition residue* lives at the instance gate.

### Constraint 2 — Stop by decision, keep the ledger permanent

Because the tower provably never reaches completeness (Constraint above), the only legitimate stop is the one Craft already names: *"the cost of the next layer exceeds the value of residue reduction"* (`CRAFT-INITIAL-DEFINITION.md#stop-criteria`). Closure is never a reason to stop because closure is unreachable.

Two wording disciplines follow:

```text
1. No Craft artifact should imply the tower can "fully close",
   "converge", or "reach completeness". It stops at acceptable residue.
2. The residue ledger is permanent. Every stop is a stop with
   known-open residue, so the ledger can never be retired.
```

`CRAFT-INITIAL-DEFINITION.md` line 262 already states the first discipline correctly. This constraint asks the rest of the Craft corpus to stay consistent with it.

### Constraint 3 — A finite plateau makes stopping safe

`SecondLawDiscrete.lean` proves that a monotone residue chain reaches a constant tail after finitely many steps: residue growth halts. This is the reassuring counterpart to Constraint 2. The tower has no final rung, but along any single coarsening line the *residue stops growing*, so a finite stop does not silently accumulate unbounded loss.

Craft consequence: the stop criterion "residue stable across runs" is formally meaningful. When successive layers stop reducing residue, the plateau is reached and climbing further is provably wasted.

## What Craft Deliberately Does Not Import

`domainspec-theorem` includes a **fractal-functor taxonomy** (a graded ladder of fully-faithfulness conditions describing zero-residue translations). Craft does **not** adopt this taxonomy as a method criterion. The reason is consistency with Craft's own stance: the PCRA translator does not achieve the clean (iso / fully-faithful) cases by default, so a promotion ladder built on degrees of zero-residue would not match how Craft actually closes layers. Craft closes on *acceptable, named, governed residue*, not on a fidelity grade.

The single concept Craft borrows from that region is the bare definition of residue — *the failure of the unit `η` to be an isomorphism* — without the graded ladder built on top of it.

## Honesty Boundary

```text
Proven by the cousins:
  - residue is a typed, composable object
  - residue composes by a chain rule
  - schema-fidelity and instance-fidelity are independent
  - the reflection tower assembles but never finitely closes
  - a monotone residue chain reaches a finite plateau
  - translation entropy = count of distinctions a schema cannot make

Still analogy for Craft:
  - that an LLM-based PCRA translator behaves like a clean kernel/functor
  - that Craft's seven residue types reduce exactly to the two formal levels
  - any "universal physics of craft" claim
```

The cousins describe the space Craft operates in. They do not certify that any particular Craft run achieved a clean translation. Each local run must still answer the honesty-boundary questions in `CRAFT-INITIAL-DEFINITION.md#the-honesty-boundary`.

## Open Questions

1. Do Craft's seven residue types (`CRAFT-INITIAL-DEFINITION.md#residue-classification`) map onto exactly the two proven levels (schema `η^sch`, instance `η^ins`), or is there a third axis? domainspec's "three independent axes" (vertical, horizontal, diagonal) suggests there may be.
2. Can the Craft validation surface be split into an explicit schema gate and instance gate without doubling ledger overhead?
3. Is there a discrete, computable proxy for "translation entropy" in a real Craft run (e.g. count of distinct intents collapsing to one schema slot), following `EntropyAsFFResidue.lean`?
4. Does the AutoBayes free-energy chain rule (Thm 23) give Craft a way to *compose* per-layer residue scores into a single governed number, the way the ledger composes status?

## Sources

Craft (local):

- `development/craft/CRAFT-INITIAL-DEFINITION.md`
- `development/craft/CRAFT-GLOSSARY.md`

domainspec-theorem (sibling repo, `../domainspec-theorem`):

- `lean-formalization/DomainSpec.lean` — two-layer residue; migration triple `Σ_Δ ⊣ Δ* ⊣ Π_Δ`
- `lean-formalization/M6Counter.lean` — schema-clean does not force instance-clean (Constraint 1)
- `lean-formalization/UniversalResidueFunctor.lean`, `NoiseFunctor.lean` — residue and noise as functors
- `lean-formalization/EntropyAsFFResidue.lean` — entropy as fiber cardinality (Constraint, entropy)
- `lean-formalization/SecondLawDiscrete.lean` — finite monotone residue plateau (Constraint 3)
- `lean-formalization/ReflectionTowerAnchored.lean`, `TowerColimit.lean` — tower assembles
- `lean-formalization/F11TransfinitePersistence.lean`, `StrangeLoop.lean` — no finite closure (Constraint 2)
- `lean-formalization/KLDivergence.lean` — KL bridge toward AutoBayes
- `GLOSSARY.md`, `docs/reflection-tower-framework.md` — prose exposition

AutoBayes (external, analogy not authority):

- Toby St Clere Smithe and Marco Perin, "AutoBayes: A Compositional Framework for Generalized Variational Inference", arXiv:2503.18608, 2025. Key results: Bayesian chain rule (Thm 13), statistical games and the chain rule for free energy (Thm 23), variational free energy as composable loss (§4).
