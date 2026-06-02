---
to: Vlad
from: Victor (multi-agent audit, synthesized)
re: "Arcanum/Craft — fourth pass: the method axis (Craft as candidate primitive)"
date: 2026-06-02
audit-against: "Arcanum development/craft @ HEAD (2026-06-02), 52-file package"
status: draft for discussion
---

# To Vlad — Craft, the method pass

Follow-up to the three sigil-axis memos. Same method (multi-agent audit +
skeptics + revisers), one altitude up: this one is about a thing Arcanum is
*growing* rather than a sigil it already ships — `development/craft/`, the
candidate Craft method primitive. The audit started looking for downstream
method gaps and kept tripping on one upstream fact: **Craft names residue as its
central unit and does not type it in the one artifact that validates.**

The skeptic pass reversed two of my own first-pass claims hard — both in
Finding 3, both about how close Craft sits to the `domainspec-theorem` repo.
The honest version is more deflationary than the one I started with. Reversals
are recorded under "What the audit killed" so they don't creep back.

Prior art, named first because the discipline demands it: **Craft's entire
vocabulary — schema/data, functor-like translator, residue, reflection tower,
smallest-coherent-unit — is the operational sibling of the `domainspec-theorem`
repo**, which formalizes this in Lean (`SchemaInstance.lean`, the M6 line of
results, the reflection tower). I wrote "twin" in the first pass; the skeptic
showed it is a *sibling with inverted payload* in two places — see Finding 3.
Craft cites none of it. That non-citation survives as the load-bearing
governance finding.

The three prior memos walked the sigil axis: what a sigil *is* (residue typing —
TO-VLAD), how sigils *relate* (kinds + edges — TO-VLAD2), how a sigil *improves*
(scoring — TO-VLAD3). Craft is a *method primitive*, not a sigil. So this is the
method-axis memo, not an edit to the others. Like the prior three, this is not
independent corroboration — same audit pipeline, fourth angle.

---

## The one-sentence thesis (everything below is a subset of this)

Craft **names** residue as its central unit and does not **type** it in the one
artifact that validates; the typing it *did* ship is the governance surface the
Arcanum method already gestured at; and the differentiator I first reached for —
"residue under a probabilistic translator" — turns out to be the theorem repo's
*own flagged-open half*, not Craft's invention.

---

## Finding 1 (load-bearing, CONFIRMED — and I understated it) — Craft reproduces, inside itself, the defect TO-VLAD.md charged Arcanum with

### Claim

`CRAFT-INITIAL-DEFINITION.md` calls residue the central unit of work and says
"Craft names the discipline for detecting that residue." TO-VLAD.md Finding 1
charged Arcanum with: *"residue has no type at any layer… a doc that names
'residue' and ships a template without a residue field is asking the reader to
grant authority the artifact hasn't earned."* Craft reproduces this exactly.

### Evidence (strengthened by the skeptic pass)

- `CRAFT-LEDGER-SCHEMA.yml` — the *only* package artifact with a `pass`
  validation — has **no residue field, no residue enum, no residue row-family,
  and no residue id-prefix.** Its five row-families are
  contexts / artifacts / relations / typed_items / decisions; the only typed
  vocabularies are governance (`typed_item_kind` = {blocker, gate, enabler},
  `base_condition_types`, `operational_lane`). The 10 validation rules
  (VAL-001..010) never mention residue.
- The residue taxonomy lives only as prose in `CRAFT-INITIAL-DEFINITION.md`, and
  it is *inconsistent prose*: line 421 says "at least five," the table at
  419–431 lists seven, and a promised `RESIDUE-TAXONOMY.md` (referenced at line
  730) was never created. Residue is also defined twice, differently (lines 169
  vs 237).
- The single residue-named type anywhere — `craft.residue_classification_gate`
  (`CRAFT-LEDGER-TYPE-SYSTEM.md:153`) — is a **governance gate**, base-type
  `validation_gate`. It types the checkpoint that *gates* residue
  classification, not residue itself, and it is **never instantiated** (zero
  rows in `LEDGER.md`). This paradoxically strengthens the finding: the only
  typed surface residue touches is governance.

### Collapse-test

If the taxonomy never becomes a ledger `row_family` with a `closure_state`,
Craft is a governance ledger wearing residue vocabulary. That single fact
reduces Finding 1's "central unit" claim to bookkeeping. A hostile reader will
reach for `residue_classification_gate` (line 153) or the taxonomy table as the
counterexample — pre-empt both: the gate types the checkpoint, not the residue,
and the table contradicts its own "at least five."

---

## Finding 2 (FAIR — the real fact is sharper than "one MVP") — Documentation-to-validated-capability ratio is the risk

### Claim

This is TO-VLAD.md Finding 3 ("the tower is documentary, not measured") at the
method altitude. Craft describes a method far past where it has been run.

### Evidence

- 52 top-level markdown files. The method surface described: 6 lifecycle phases,
  7 architectural parts, 7 residue types, 5 layer-ladders, a formal model
  `C = (I,S,F,E,D,R,G,V)`.
- **Distinct complete, engine-validated Craft loops: zero.** 15 dated
  task-sessions are each single-phase slices (one task ID, one write scope) of
  three work-packs (MVP / GAP / ARCH). The recursive-ledger MVP is the one case
  where the phases were *covered* — but hand-assembled across 4 sessions and
  checked by a Markdown-table review (`LEDGER-VALIDATION.md`), with no Reflect
  artifact.
- The one full-engine pipeline "pass" was a **false pass, since retracted**:
  `CRAFT-RECEIPT-001` patched `tools/arcanum` because the Context Builder stage
  had been counting a runtime handoff *stub* as owner-stage execution. The six
  subsequent re-runs all **block** at Context Builder; the latest live run
  (`20260601T015552Z`) blocks. README verdict:
  `refine-validation-stage-receipt-blocked-promotion-deferred`.
- `CRAFT-PROMOTION-READINESS.md` is honest: `defer`, "evidence too fresh."

### Recommendation

Endorse the `defer`, harden it: **no new method surface until an existing
surface runs green twice without a retraction.** The honest count of surviving
engine-validated loops is zero; the one hand-validated MVP records blockers in
YAML. Everything above it is design about a method whose engine has never closed
a clean loop.

---

## Finding 3 (DEMOTED by the skeptic — this is where I was wrong) — Craft is the operational instance of `domainspec-theorem`, and even its candidate differentiator is the repo's own open half

### What I claimed first pass

That Craft is the "operational twin" of the theorem repo, that M6 gives a
*symmetric* schema-side/instance-side residue separation Craft could inherit,
and that the one thing Craft adds is "residue under a probabilistic translator
(PCRA)," because the repo's Δ is deterministic and types residue only on that
deterministic functor.

### What the skeptic showed

Both halves broke.

- **The "twin" is inflated; the sibling has inverted payload.** M6 is not a
  symmetric cut. The repo's result is *asymmetry*: instance-side residue (η^ins)
  is typed, but the schema-side companion (η^sch) is "structurally inexpressible
  / permanently independent" (`InterAxisIndependence.lean:327,369`) and the
  schema-side adjunction is marked **Open**
  (`two-layer-framework.md:167`). Two further inversions: the repo's Δ is a
  functor as a property of the *compilation contract*, "not because any
  generation process is deterministic" (`two-layer-framework.md:90`) — Craft's
  translator is the *realization act*, the side the repo explicitly brackets as
  "the unsolved half" (`:285`); and the repo's reflection tower is a *negative*
  result (residue never absorbs — `ReflectionTowerAnchored.lean:408`,
  M6-strong refuted at every level), whereas Craft's tower is a *constructive*
  method (residue seeds the next layer). Same words, opposite payload.

- **The PCRA differentiator collapses.** The premise that the repo's typing
  rides on a deterministic Δ is contradicted verbatim: the repo already factors
  determinism out (`:90`) and names *stochastic realization* as its own open
  half (`:285`). And `QubitSpectralPresheaf.lean` already types `Carrier(η^ins)`
  under a contextual (Kochen–Specker) translator with a Wave-4 rational
  Born-probability layer — contextual + probabilistic residue, already typed
  in-tree. My first-pass instinct that the *named* Markov file
  (`GeneratorFFinFiniteMarkov`) doesn't save the claim was right — its
  `FFDefect = M − 1` collapses the stochastic flow to a deterministic-identity
  test — but I missed the qubit file, which is the actual counterexample.

### What survives

Not "PCRA is Craft's residue." At most, Craft's defensible differentiator
shrinks to the **unbounded-context realization-termination** question
(`two-layer-framework.md:285`) — and that is *still the repo's flagged-open
half*, owed a citation, not Craft's invention. The honest conclusion is the
deflationary one: **Craft is the operational instance of an already-formalized
(and in places already-refuted) framework, and owes it a first-section
citation regardless of how Q1 resolves.**

(One caveat the skeptic flagged on itself: `QubitSpectralPresheaf.lean` carries
`[GAP]` markers, so "typed" there means "a `Carrier(η^ins)` construction with a
non-emptiness theorem and a Born layer exists," not "sorry-free / PR-grade." The
memo's literal words — "not typed anywhere" — are already falsified by the
construction's existence plus `:90/:285`; but if you want Strike B airtight,
run the build gate on that file.)

---

## A subtler finding worth keeping (CONFIRMED)

### The "Universal Physics of Craft" section is the `PRIZES.md` ambition without the anchors

`CRAFT-INITIAL-DEFINITION.md` stages a four-level claim ladder ending in "reality
itself may be intelligible as a recursive craft process." Under the subset rule
this is claim ≫ proof — the theorem repo's prize ambition with no Lean
underneath. The doc half-admits it ("the universal claim should be staged") and
then spends a long section on it anyway. Keep the operational claim (level 1);
cut levels 3–4 to one paragraph marked horizon-not-proven. Cheapest credibility
fix in the package.

---

## What I'm leaving open for you

Three calls only you should make.

### Q1 — Is Craft a method primitive, or the operational instance of `domainspec-theorem`?

After the skeptic pass this is close to decided: the vocabulary, the lifecycle,
and even the candidate differentiator all trace back to the theorem repo. The
live question is narrower — **is there *any* Craft contribution that the repo
does not already hold (typed or flagged-open)?** If no, Craft cites the repo and
demotes the universal-physics horizon. If you believe yes, name it precisely
enough to survive the same skeptic pass that just killed PCRA.

### Q2 — Given the schema-side is open in the repo, what does Craft's residue typing inherit?

The symmetric two-budget cut I leaned on does not exist: η^ins is typed,
η^sch is open/inexpressible. So Craft can at most inherit the **instance-side**
typing and mark schema-side residue *open* (the repo's own status) — not
fabricate a symmetric enum. Or Craft picks a different first axis entirely
(e.g. PCRA-induced vs structural) and owns the burden of showing it isn't the
repo's open half renamed.

### Q3 — Promotion gate: BLOCK-free full loop, or ledger-MVP-alone?

Either Craft must run one full Define→…→Reflect loop BLOCK-free (no retraction)
before promotion, or the recursive-ledger MVP alone is the promotable unit
(narrow scope) and the method frame stays in development indefinitely.

---

## Concrete edits, ordered by leverage

1. **`CRAFT-LEDGER-SCHEMA.yml`** — add `row_families: residue` with a
   `residue_type` enum, a `closure_state` (absorbed / split / routed / promoted —
   verbs already in the definition's decision step), and `source_layer` /
   `target_layer`. Inherit the **instance-side** typing the repo has; mark
   schema-side residue `open` rather than inventing a symmetric field (gated on
   Q2). *Effect:* Craft's central claimed unit becomes first-class in the one
   artifact that validates. Closes Finding 1.

2. **First section of `CRAFT-INITIAL-DEFINITION.md`** — cite `domainspec-theorem`
   as parent prior art, the way TO-VLAD2 made Arcanum cite
   `domainspec/TAXONOMY.md`. State the inversions honestly: the repo's tower is a
   negative result, its schema-side is open, its Δ already factors out
   determinism. *Effect:* cite-don't-rediscover; stops Craft re-deriving (and
   silently re-polarizing) the framework it instantiates. **Unconditional** —
   holds however Q1 resolves.

3. **Reconcile the residue taxonomy with itself** — fix "at least five" vs the
   7-row table, drop or create the phantom `RESIDUE-TAXONOMY.md`, and pick one
   definition of residue. *Effect:* removes the cheap rebuttals to Finding 1.

4. **Cut "Universal Physics of Craft" to one staged paragraph** — keep
   operational claim 1, mark 3–4 horizon-not-proven. *Effect:* removes the
   biggest claim ≫ proof surface in the package. **Unconditional.**

5. **Run one full loop BLOCK-free** (no retraction) before any promotion
   language — the README's own next-move. *Effect:* converts Finding 2 from
   "documentary" toward "measured." **Unconditional.**

Edits 2, 4, 5 are unconditional. Edit 1 is gated on Q2; edit 3 is a
self-consistency fix that should land regardless.

---

## What the audit killed (honesty about my first-pass claims)

The skeptic pass reversed or demoted three things. Recording them so they don't
creep back:

- **"Craft is the operational *twin* of the theorem repo."** — **demoted to
  sibling-with-inverted-payload.** M6 is asymmetric (η^sch open/inexpressible),
  the repo's tower is a *negative* result, and its Δ already factors out
  determinism. The structural overlap is real; the polarity is not shared.
- **"M6 gives a symmetric schema/instance two-budget cut Craft can inherit."** —
  **false.** Instance-side is typed; schema-side is Open
  (`two-layer-framework.md:167`, `InterAxisIndependence.lean:327,369`). Q2 was
  rewritten around this.
- **"Craft's one genuine residue is PCRA — residue under a probabilistic
  translator, untyped anywhere."** — **collapsed.** The repo factors determinism
  out (`:90`), names stochastic realization as its own open half (`:285`), and
  `QubitSpectralPresheaf.lean` already types contextual+Born-probability residue
  in-tree. What survives is at most the repo's *own* open realization-termination
  question — owed a citation, not Craft's invention.

What survived the pass intact: Finding 1 (residue untyped — in fact understated),
Finding 2 (zero clean engine loops; the one pass retracted), and the
universal-physics over-claim.

---

## One observation beyond the audit

I came in expecting to find Craft's contribution and instead the skeptic kept
returning it to the repo two directories over. That is itself the result: the
strongest thing this pass establishes is not a gap to fill but a *citation debt*
to pay. Craft is a faithful operational re-narration of a framework that is, in
places, further along (and more negative) than Craft's prose assumes. The bridge
worth building is not "make Craft novel"; it is "wire Craft's ledger to the
typed residue the repo already has, mark the schema-side open as the repo does,
and stop the universal-physics prose from claiming what the Lean already
refuted."

---

## Three sharpest questions, in order

1. **Q1 — is there *any* Craft contribution the repo does not already hold or
   flag-open?** (If no, Craft cites and demotes the horizon.)
2. **Q2 — given the repo's schema-side is open, Craft inherits instance-side
   typing and marks schema-side open — or owns a different axis.** (Fixes Edit 1.)
3. **Q3 — promotion gate: BLOCK-free full loop, or ledger-MVP-alone?** (Fixes
   scope.)

— V.
