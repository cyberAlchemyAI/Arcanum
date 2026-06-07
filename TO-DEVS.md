---
to: Devs
from: Victor (multi-agent audit, synthesized)
re: "Arcanum structure — the tiers are a flat partition by design, not a tower"
date: 2026-06-07
audit-against: "Arcanum @ HEAD (2026-06-07); benchmark = domainspec-theorem reflection-tower functor"
status: structural note (self-description, not a change order)
---

# To Devs — what Arcanum's tier structure *is*

A short structural note so the repo can describe itself accurately, and so the
next pass does not re-propose an axis already audited and closed. This is not a
TO-VLAD memo (those are external review memos to the maintainer); it is an
internal self-description.

## One sentence

Arcanum's three tiers — `formulae` / `transmutations` / `arcana` — are a **flat
epistemic partition, by design**, not an embedded stack: there is **no promotion
functor between tiers**, so "tower" language about tiers is metaphor, not
structure.

## What this means concretely

The comparison object is `domainspec-theorem`'s reflection-tower promotion functor
`P : L_n ⥤ L_{n+1}` (`lean-formalization/ReflectionTowerAnchored.lean:195`), whose
defining signature is **full + faithful + not essentially surjective**: each level
embeds everything below it intact, yet always adds an object not reducible to
below. That signature is exactly what distinguishes a *reflection tower* from a
*pile of stacked ontologies*.

Arcanum's tiers do **not** carry that signature, and a 2026-06-07 multi-agent audit
(explorer + skeptic + auditor) confirmed it on disk — three independent
confirmations:

1. **Disjoint contents.** The three tier directories hold disjoint sigils
   (`dispatch-spec` is a formula, `codex-goal-profile` a transmutation,
   `robot-talks` an arcanum); no formula is a sub-object of any transmutation.
   There is no embedding `formulae ↪ transmutations ↪ arcana`.
2. **The one inter-tier relation points the other way.** `arcana/README.md:128` —
   "Arcana can delegate Formulae checks": a higher tier *calls* a lower one. That
   is service/delegation, the **reverse** of an embedding.
3. **Flat on purpose.** The framework already types tiers as a flat epistemic
   classification deliberately (`TO-VLAD/TO-VLAD.md:48`, "tier as epistemic
   classification, not as a measured stack"; `:66`, "why three things sit in one
   tier on purpose").

## Why it is recorded (and not turned into machinery)

With no embedding direction there is no promotion functor to type — so the
"inter-ontology functor" axis contributes **zero** as a new artifact. Stripped of
categorical vocabulary it reduces to the `tier ↔ promotion` crosswalk already
owned by the TO-VLAD2 drift addendum (2026-06-02). It merely re-raises memo 1's
still-open question (`TO-VLAD/TO-VLAD.md:84`, "Is `arcana/` one tier or three?").

This note is the closure record so the axis is not re-opened by accident.

## The one condition that would change this

The functor axis becomes real **only if** Arcanum re-types its tiers as an
**ordered stack** (`formulae ⊂ transmutations ⊂ arcana`, with each tier embedding
the one below). If that is ever a deliberate design move, the promotion functor
gains a referent and the signature (full / faithful / ¬ess-surj) becomes something
Arcanum could state and check — at which point it earns a TO-VLAD memo, stated
*to-be-checked*, not achieved. Until then, tiers are flat and that is the correct
design.

Audit trail: `domainspec-theorem/research-ai/inter-ontology-functor-layer/`.

— V.
