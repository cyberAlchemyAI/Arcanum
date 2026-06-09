---
profile: autobayes-research
name: Craft Translation-Entropy Search Strategy
description: Source-disciplined search strategy that grounds, contrasts, and bounds the Craft "translation entropy" definition against the AutoBayes research tower and its related literature.
type: search-strategy
status: draft
parent_tower: arcanum/research/autobayes/TOWER.md
target_definition: arcanum/development/craft/CRAFT-INITIAL-DEFINITION.md
dispatch: arcanum/research/autobayes/craft-entropy-search.dispatch.json
last_updated: 2026-06-08
---

# Craft Translation-Entropy Search Strategy

## Why This Strategy Exists

[CRAFT-INITIAL-DEFINITION.md](../../development/craft/CRAFT-INITIAL-DEFINITION.md)
introduces **translation entropy** as a load-bearing term:

> Entropy in Craft is the uncertainty introduced when a schema is translated into
> data by a PCRA functor-like process.

It is decomposed into four coupled properties — **probabilistic spread**,
**contextual dependence**, **relational load**, **attentional decay** — and it is
explicitly distinguished from residue:

> Entropy is the uncertainty pressure before and during translation; residue is
> what remains after the artifact exists and validation compares it back to the
> schema.

This term currently has **no source-backed grounding**. It reads like Shannon
entropy, like variational free energy, and like a generalized-variational-inference
loss all at once, but the definition commits to none of them. That ambiguity is the
exact residue the AutoBayes tower is positioned to address: AutoBayes and its cited
literature are precisely about uncertainty, divergence, loss composition, and
optimization semantics over a syntax/inversion/loss/parameter ladder.

The strategy does **not** try to formalize Craft entropy. It searches for the
nearest source-backed formal objects, marks each as borrow / analogy / reject /
promote-residue, and returns a sharpened definition card with an explicit honesty
boundary. No result here promotes canonical Arcanum glossary, ontology, sigil, or
spell knowledge.

## Search Question

> Is Craft's "translation entropy" groundable in, or cleanly distinguishable from,
> the established uncertainty objects surfaced by the AutoBayes tower — Shannon /
> differential entropy, conditional entropy, KL divergence, variational free energy
> (ELBO), the GVI loss/divergence/regularizer triple, statistical-game optimization
> uncertainty, and PPL guide-program variance — such that the Craft definition can be
> sharpened without overclaiming a formal isomorphism?

## Search Lanes

Each lane is one bounded search unit. Each lane must return: the closest
source-backed formal object, a citation or concrete artifact path, a single mark
(`borrow` / `analogy` / `reject` / `promote-residue`), and named open residue.

| Lane | Craft target | Source object to search | Default skeptical hypothesis |
| --- | --- | --- | --- |
| L-info | "uncertainty introduced", probabilistic spread | Shannon entropy `H`, conditional entropy `H(D\|S)`, mutual information | Craft entropy is conditional entropy of data given schema, nothing more |
| L-free | "uncertainty pressure before/during translation" | Variational free energy, ELBO, `KL(q‖p)` | Craft entropy is really a *divergence/loss*, mislabeled as entropy |
| L-gvi | four coupled properties as a single pressure | GVI loss / divergence / regularizer triple (Knoblauch et al.) | Craft "entropy" maps to the GVI regularizer, not to entropy |
| L-games | relational load, optimization semantics | Parameterized statistical games, Bayesian lens reverse-state (Smithe) | Relation load is game composition cost, not an entropy term |
| L-ppl | probabilistic spread, attentional decay | PPL guide-program mismatch, amortized-inference variance (Pyro, Staton) | "Spread" is sampling/guide variance, a runtime not a definitional property |
| L-scu | non-linear fidelity curve, SCU as local minimum | Free-energy minimization, bias/variance, under- vs over-parameterization | SCU selection is free-energy minimization restated operationally |

## Operating Rule

Every lane closes with exactly one mark:

- `borrow`: a source object can be cited directly to define part of Craft entropy.
- `analogy`: the source object illuminates but does not define; analogy-only.
- `reject`: the source object does **not** map; record why.
- `promote-residue`: the lane reveals a missing layer; sharpen into a next object.

A lane that cannot reach a cited source is recorded as **missing-source residue**,
not silently closed.

## Convergence Target

The contrast step runs a two-role dialectic — a source-loyal formal reading against
a Craft-operator translation — and must converge on one of three honest verdicts:

1. **Operational proxy**: Craft entropy is best read as an operational proxy for a
   named divergence/loss; record the proxy and its limits.
2. **Distinct construct**: Craft entropy is a genuinely distinct operational
   construct (pre-translation uncertainty over schema/data realizations); record what
   makes it irreducible to the formal objects.
3. **Metaphor**: Craft entropy is currently metaphor; record the smallest source-backed
   reformulation that would make it defensible.

The verdict, its marks, and its honesty boundary land in
`tracks/craft-entropy-definition-card.md` and feed the open-residue ledger.

## Boundaries

- This is a research search inside `research/autobayes`. It may write only under that
  namespace.
- Findings about Craft are **candidate readings**. Updating
  `arcanum/development/craft/CRAFT-INITIAL-DEFINITION.md` is a separate, owner-approved task.
- The full-mode fanout uses delegated subagents and requires explicit operator approval.

## Artifacts

- [craft-entropy-search.dispatch.json](craft-entropy-search.dispatch.json) — the validated search route.
- `sessions/craft-entropy-search-receipts.md` — per-lane source receipts (produced on run).
- `tracks/craft-entropy-definition-card.md` — converged entropy definition card (produced on run).
- `residue/craft-entropy-open-residue.md` — open residue after the search pass (produced on run).
