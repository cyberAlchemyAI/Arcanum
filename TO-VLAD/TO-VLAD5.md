---
to: Vlad
from: Victor (multi-agent audit, synthesized)
re: "Arcanum/framework — fifth pass: the meta-governance axis (does the framework encode the discipline its own audits use?)"
date: 2026-06-03
audit-against: "Arcanum/framework @ HEAD (2026-06-03) + arcana/ skill contracts; benchmark = domainspec-theorem/CLAUDE.md"
status: draft for discussion
---

# To Vlad — the framework's own constitution, audited

Fifth pass. The prior four walked the sigil object (what a sigil *is*, *how they
relate*, *how it improves*) and then stepped off it (Craft, a candidate method
primitive). This one steps off again, one altitude up from memo 4: the object is
**the framework's own governance constitution** — `CYBERALCHEMY-METHOD.md`,
`QUALITY-BAR.md`, the constitutions, the validation protocol. The question is
recursive, and I want to be honest that it is: **do Arcanum's governance docs
encode the discipline that these very memos use to audit Arcanum?**

I came in expecting a clean "no" and a tidy three-part gap. The skeptic pass took
that apart. What survives is **one** load-bearing finding, not three; the other
two collapse to a rename and a deferral. The deflation is the result — recording
it honestly is the point, because shipping three co-equal "absences" would be the
exact claim ≫ evidence defect this memo is about.

Prior art, named first because the discipline demands it: the benchmark for
"governs claim against evidence" is **`domainspec-theorem`** — its `CLAUDE.md`
subset rule (claim ≤ proof), four pre-write triggers, the
math-open / formalization-open / overlay-open typing, and the keystone
collapse-test. This memo measures Arcanum's framework against that benchmark and
reports where Arcanum already has the equivalent (most places) and the one place
it does not.

Like the prior four, this is not independent corroboration — same audit pipeline
(explorers + two skeptics + auditor, subset rule), fifth angle. Audit trail:
`domainspec-theorem/research-ai/arcanum-claim-evidence-governance-axis/`.

---

## The one-sentence thesis (everything below is a subset of this)

Arcanum's constitution governs the **promotion** direction of a claim well —
nothing reaches the registry without passing evidence — but does not govern the
**novelty** direction at all: nothing makes a sigil default to *"this capability
is assumed to already exist in the registry until a check shows otherwise,"* the
exact move `domainspec-theorem` makes when it defaults *"Mathlib doesn't have
it"* to formalization-open rather than new-math; and that gap has a present-tense
harm — a sigil shipped as novel that duplicates a capability already in the
registry — that Pass/Flag/Block and the promotion gate cannot catch.

---

## Finding 1 (load-bearing, SURVIVED both skeptics) — the framework gates promotion, never novelty

### Claim

Every promotion gate in the framework is *existence*-gated: an artifact is
registry-ready when its contract validates, fixtures pass, and no blocker is open
(`EXPERIMENT-HARNESS-STANDARD.md:167-179`; "avoid silent promotion,"
`CYBERALCHEMY-METHOD.md:341`). None of them asks the orthogonal question
`domainspec-theorem` forces before any publication-bound write: *is this actually
new, or does it already exist elsewhere?* The framework has a 2-bin gap classifier
(blocker / non-blocker, `CYBERALCHEMY-METHOD.md:232,343`) — severity, never
epistemic status.

### Why the obvious port is wrong

Do **not** import `domainspec-theorem`'s three bins
(math-open / formalization-open / overlay-open) verbatim. For a registry of ~a
dozen sigils that is ceremony with no decision attached — the skeptic killed it
outright. The Arcanum-native shape is narrower and operational: a **novelty
default**. When a sigil's prose claims a capability is "new," the burden is a
registry-check showing no existing sigil or library already does it. Default to
*exists-elsewhere*, not *novel* — the same polarity as "Mathlib doesn't have it →
formalization-open, not new-math."

### Collapse-test (binds the headline, per house rule)

**If no two sigils in the registry ever overlap in capability, this finding
contributes nothing.** It earns its place only as the registry grows — which is
precisely Arcanum's trajectory (`tools/bootstrap_arcanum.sh --sigils all` ships
the whole set into consuming repos). A hostile reader will point at the
blocker/non-blocker classifier as the counter — pre-empt it: that types whether a
gap *stops work*, never whether a claimed capability *already exists*.

### The harm, concretely

A sigil authored and promoted as a new capability that duplicates one already in
`registry/SIGILS.md`. The promotion gate passes it (its own fixtures are green);
Pass/Flag/Block has no flag for "this overlaps an existing capability"; the
duplicate lands. This is the one sub-finding with a standalone present-tense harm.

---

## Finding 2 (SECONDARY — wounded to magnitude, half is a rename) — claim-strength binding is label-deep

### Claim

This is the subset rule (claim ≤ proof) measured against Arcanum. The honest
result is split:

- **The promotion half is already present — concede it.** Arcanum enforces
  claim ≤ *validation-report* at the gate: Pass/Flag/Block, the harness check that
  rejects a `pass` carrying an open blocker, "avoid silent promotion." Mapping the
  subset rule onto that and calling it "absent" would be the easy kill, and the
  benchmark explorer (built to resist this memo's hypothesis) scored it PRESENT.
- **The surviving slice is magnitude.** `QUALITY-BAR.md:25,70` requires evidence
  and inference to be *separated by label* — it is silent on whether a sentence
  *labeled* "inference" overclaims its magnitude. A conformant output can tag a
  claim "inference" and still say more than its evidence sustains. The
  strength-binding (claim ⊆ evidence, not merely claim *labeled*) is the unowned
  delta.

### Recommendation

One line in `QUALITY-BAR.md`: a claim's strength must be a subset of what its cited
evidence sustains, not merely labeled as inference. Ship it *with* the rename-half
conceded in the body, or a reviewer rightly calls it a re-skin of the promotion
gate.

---

## Finding 3 (DEFERRED — real, but idle at current scale) — demotion-reversal is forward-only

### Claim

Arcanum's anti-silent-change family is entirely *promotion-directional*: "avoid
silent promotion," Trace Before Promotion, and recording rejected alternatives in
the current decision's trace (`CYBERALCHEMY-METHOD.md:88,120,341`). None locks the
*reverse*: re-asserting a previously-demoted claim need not surface the prior
demotion. The recorded trace is passive provenance, not an active re-assertion
gate. `domainspec-theorem` has the symmetric lock (demote/promote protocol: never
silently reverse an audit verdict).

### Why it is deferred, not shipped

It is idle at 4 memos / 1 maintainer. It bites only at Reflection-Outer-Loop scale
(`CYBERALCHEMY-METHOD.md:270`), where a later `workflow-reflect` run silently
re-promotes what an earlier run demoted — a multi-agent failure mode Arcanum is
building toward but has not reached. Ship as a flagged watch-item tied to
reflection automation, not a present gap.

---

## What the audit killed (honesty about my first-pass claims)

The skeptic pass reversed or demoted four things. Recording them so they don't
creep back:

- **"Three co-equal absences (a)(b)(c)."** — **demoted.** Absence ≠ significance.
  Only Finding 1 carries a standalone present-tense harm. Shipping them as
  co-equal would itself be claim ≫ evidence.
- **"claim≤evidence is absent from Arcanum."** — **demoted to magnitude-only.**
  Present at the promotion gate (claim ≤ validation-report); absent only at
  sentence-level magnitude. The strong version is a rename.
- **"Port the typed-open three bins verbatim."** — **killed.** Ceremony for a
  dozen sigils; the Arcanum-native reshape is a novelty/duplication default, not
  an epistemic taxonomy.
- **"A clean new altitude."** — **conditional.** Distinct only because the object
  is the framework's own constitution; re-pointed at a sigil it would be memo-4's
  move generalized. The partial-overlap pressure is real and conceded below.

What survived intact: Finding 1 (novelty/duplication gate — the only one with a
present harm), and the *shape* of Findings 2–3 once narrowed.

## What the audit confirmed (so it isn't repackaging)

- TO-VLAD.md's open question — *"is the Quality Bar's iso framing deliberate or
  accidental"* — is **orthogonal**. That is a residue-alphabet expressiveness
  question; this memo neither resolves nor expands it. Memo 5 is not memo 1's open
  question restated.
- **No prior memo recommends Arcanum *adopt* the discipline as first-class
  governance.** In all four, the subset rule / collapse-test / "what the audit
  killed" / cite-don't-rediscover appear only as the auditor's own method, or
  applied to cut a specific overclaim — never proposed *as* Arcanum's published
  rule. The lane is open. (Honest dissent, surfaced: memo 3's grader-independence
  rule — "the scored artifact must not be self-authored" — is the nearest prior
  recommendation, and memo 4 already subset-ruled a framework-grown artifact
  (Craft). Memo 5 generalizes their spirit; it is clean on the *object* — the
  constitution — and contested on the *spirit*.)

---

## Concrete edits, ordered by leverage

1. **Add a novelty default to the sigil promotion gate** — in
   `SIGIL-DEVELOPMENT-WORKFLOW.md` / the registry-promotion step: a sigil claiming
   a "new" capability must carry a registry-check result showing no existing
   sigil/library covers it; default assumption is *exists-elsewhere*. Add a
   Pass/Flag/Block **flag** value for "overlaps existing capability." *Effect:*
   closes Finding 1 — the only present-harm gap. **Gated on Q1** (is the overlap
   real yet, or anticipatory).

2. **One QUALITY-BAR line on magnitude** — a claim's strength is a subset of what
   its cited evidence sustains, not merely labeled inference. *Effect:* closes the
   surviving slice of Finding 2. Concede the promotion-gate half in the same edit.
   **Unconditional but small.**

3. **Cite `domainspec-theorem` as the benchmark** in whichever framework doc states
   the governance philosophy — the way TO-VLAD2 made Arcanum cite
   `domainspec/TAXONOMY.md`. *Effect:* cite-don't-rediscover; the novelty-default
   and subset-rule vocabulary is borrowed, not invented here. **Unconditional.**

4. **Defer demotion-reversal explicitly** — a one-line flagged-open note that
   forward-only is a known gap that bites at `workflow-reflect` scale, to be
   encoded when reflection automates. *Effect:* Finding 3, honestly parked rather
   than over-shipped.

Edits 2, 3, 4 are unconditional (and cheap). Edit 1 is the load-bearing one and is
gated on Q1.

---

## What I'm leaving open for you

### Q1 — Is the registry-duplication harm real *yet*, or anticipatory?

The collapse-test resolves this empirically: **name two current sigils with
overlapping capability.** If you can, Finding 1 ships as a present gap. If you
cannot, it ships as anticipatory-but-cheap — still worth edit 1, but framed as
"before the registry grows," not "you have duplicates today."

### Q2 — Is the QUALITY-BAR magnitude line worth it?

Does label-separation suffice in practice, or have you seen a sigil's prose
overclaim inside a correctly-labeled "inference"? If you haven't, edit 2 is
theory; if you have, it's a one-line fix.

### Q3 — Demotion-reversal: encode the forward-lock now, or wait?

Cheap to add now (a rule that re-asserting a demoted claim surfaces the prior
demotion); idle until `workflow-reflect` runs at scale. Your call on whether to
pay for it before it bites.

---

## One observation beyond the audit

The recursive finding is the interesting one even after the deflation: the
strongest version of this memo establishes that **the discipline these five memos
run on is more rigorous than the framework they audit publishes about itself** —
not as an indictment, but as a citation debt and a single concrete wire (the
novelty default). The framework already governs the direction that protects the
registry from *bad* capabilities. The one direction it leaves open is protecting
the registry from *redundant* ones — and that is the gap that grows exactly as
fast as Arcanum succeeds.

---

## Three sharpest questions, in order

1. **Q1 — name two overlapping sigils, or concede Finding 1 is anticipatory.**
2. **Q2 — has a correctly-labeled "inference" ever overclaimed? (decides edit 2.)**
3. **Q3 — pay for the demotion-reversal lock now, or defer to reflection scale?**

— V.
