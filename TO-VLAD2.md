---
to: Vlad
from: Victor (multi-agent audit, synthesized)
re: cyberAlchemyAI/Arcanum — second pass: typed sigils + typed edges
date: 2026-06-01
audit-against: arcanum @ 75b22300 (2026-06-01)
status: draft for discussion
---

# To Vlad — Arcanum, second pass

Follow-up to 2026-05-20. Same method (multi-agent audit + skeptics + revisers). The audit started looking for downstream gaps but kept tripping on the same upstream gap: **sigils are not semantically typed, and the relationships between sigils are not declared with a vocabulary**. Three findings below, ordered by depth. Finding 1 is load-bearing and blocks the other two.

Most of the audit's first-round proposals got cut — eight of ten proposed edits and two of ten proposed kinds didn't survive. What survived is below, rationed against the project's subset rule (claim ≤ proof).

Of the eight edits below, only Edits 2, 3, and 5 are unconditional. The rest are gated on open questions (Q1, Q2, Q4) or on the prior memo's Edits 1+2 shipping first — see "Prerequisites" inside the Concrete Edits section.

---

## Finding 1 — Sigils are untyped and inter-sigil edges have no vocabulary

This is the load-bearing finding. Findings 2 and 3 are downstream of it.

### Claim

Arcanum has no semantic typing of what a sigil DOES, and no enumerated vocabulary for how sigils relate to each other. Every downstream proposal in this memo (and most of the previous one) reasons over untyped objects and a single implicit edge type.

### Evidence

Sigil frontmatter today has these fields related to typing:

| Field | Coverage | Useful? |
|---|---|---|
| `tier` | 3 buckets (formulae / transmutations / arcana) | Coarse — computational character, not semantic |
| `domain` | Free-text, author-picked | Inconsistent — `knowledge-inventory`, `observability`, `reflective-maintenance`, `sigil-governance`, `dispatch` all appear without enumeration |
| `argument-hint` | Free-text modes + params | Not enforced |
| `allowed-tools` | Capability list | Tool-level, not semantic |

There is no `input-schema`, no `output-schema`, no `kind` field, no `edges` field.

For edges between sigils:

- `registry/SIGILS.md` — flat table, columns Sigil/Tier/Summary/Use When/Folder. **Zero edge columns.**
- `registry/SPELLS.md` — has `Sigils Composed` column. **One implicit edge type** (`spell --composes--> sigil`).
- Per-spell `Required Sigils` table — same single edge with role + mode columns.

Total: one edge type, declared at the spell level only.

By comparison, `domainspec/TAXONOMY.md` has 25 enumerated meta-types and `domainspec/RELATIONSHIPS.md` has 29 typed edges (`performs`, `produces`, `enforces`, `depends-on`, `triggers-cross`, `consumed-by`, etc.). Both reified as Lean inductives (`Meta` and `EdgeType` in `domainspec/internal_tools/lean-code-validator/LeanCodeValidator/Sigma.lean`, lines 13 and 28). Arcanum is doing the same kind of work over a much thinner type surface.

### Why this is foundational

Every downstream finding in this memo (and most of the previous one) is reasoning over untyped objects:

- The first-memo edit 2 (contract-join check) wants input/output schemas to exist. They don't.
- Finding 2 below (spell shape taxonomy) wants typed sigils to know what's being composed. They aren't.
- Finding 3 below (drift detection) wants a "spec" object to diff against. None is declared.
- Cross-feature naturality / dependency analysis would want typed edges. They don't exist.

You cannot build any of this on `domain: free-text` and one implicit edge.

### Recommendation

Replicate the `TAXONOMY.md` + `RELATIONSHIPS.md` pattern from domainspec, adapted to the sigil/spell surface. **Two new framework documents**, in two cuts, with retrofit. Spec is below as Edits 1–4b.

The audit's first-round proposal had ten kinds and ten edges; reviewers cut it to six kinds + two enforced edges + eight declared-only edges. The cut list is in "what I deliberately did not recommend" below.

---

## Finding 2 — Spell composition is heterogeneous; the prior memo's edit 2 only covers part of it

### Claim

The 2026-05-20 memo's edit 2 (`spellcraft validate` checks phase N output covers phase N+1 source-schema) assumes every spell is a linear chain. Five of eleven spells are. The other six are not, and edit 2 will silently false-positive on three of them, run vacuously on one, and apply the wrong check-class to two.

### Evidence — eleven spells classified

| Spell | Shape | Why |
|---|---|---|
| discovery-to-inventory | pipeline | scope-interview → feature-glossary → inventory |
| implementation-readiness | pipeline | implementation-layering → decision-gate → task-session |
| ontology-harness | pipeline | inventory → ontology-vault → context-builder |
| repository-harness | pipeline | inventory → architecture-pattern-inventory → context-builder |
| sigil-maintenance-loop | pipeline | signal-observer → workflow-reflect → sigil-development |
| arcanum-bootstrap | lifecycle | setup with checkpoints + rollback |
| guide-architecture | lifecycle | frontmatter declares `Lifecycle owner: spellcraft` |
| invoke | dispatcher | modes define/design/plan/handoff/refresh/full/validate are alternatives |
| observed-invocation-loop | wrapper | wraps any invocation, reads envelope |
| whisper | interview | turn-taking with human |
| necronomicon | orchestrator | session memory + routes + classification — no chain shape |

Pipeline: 5. Non-pipeline: 6 (lifecycle 2, dispatcher 1, wrapper 1, interview 1, orchestrator 1).

Without a `shape:` tag, `spellcraft validate`'s contract-join check will:

- False-positive on `observed-invocation-loop` (wrapper input by design does not match wrapped output).
- False-positive on `whisper` (interview branches on human input, not contract).
- False-positive on `necronomicon` (no chain to check).
- Run vacuously on `invoke` (no adjacent phases — every check trivially passes, indistinguishable from a real pass; shape-aware validation should report `n/a: dispatcher`).
- Apply the wrong check-class on `arcanum-bootstrap` and `guide-architecture` (lifecycles need gate-validity checks, not contract-join).

### Recommendation

Add a `shape:` tag to spell frontmatter before shipping the prior memo's edit 2. Make the validator's check conditional on shape. See Edit 5 below.

The first-round audit framed this as "make composition a category with associativity / identity laws per spell." Reviewers correctly pointed out that most spells (dispatcher, wrapper, interview, orchestrator) don't form categories — there's no identity sigil for a wrapper. Categorical framing was decoration; the engineering kernel is shape-aware validation.

---

## Finding 3 — No reverse path from deployed sigil to design intent

### Claim

Once a sigil is in `registry/`, there is no tool that reads it and emits the spec it was authored from. Drift between deployed sigil and original spec is undetectable.

### Evidence

`registry/SIGILS.md` carries `name`, `tier`, `status`. It does not carry the authoring spec. `skill-transcriptor`'s input (a spec) is not preserved as part of the output package.

### Recommendation

**Do NOT build a reverse-extractor yet.** Answer the drift question (Q1 below) first. If drift is real, ship `arcana/spec-extractor/`. If not, defer.

The first-round audit framed this as an adjoint pair `compile ⊣ extract` with triangle identities. Reviewers correctly killed this: there is no `compile : Spec → Sigil` function in arcanum (sigil authoring is human-mediated), so there's no forward half of an adjunction to build. The honest engineering form is a drift-detection tool — same shape as docstring extractors.

---

## A subtler finding worth keeping

### Envelope schemas are the missing typed object

When I tried to write down what "composition" means in arcanum, the answer kept being "the envelope of phase N is whatever phase N+1 reads." Envelopes are nowhere declared. Phase outputs are free-form; phase inputs are validated only against structural completeness rules.

This is the same gap the prior memo's edit 1 (`<source-schema>` with `required:` and `degrades-on:`) targets. Finding 1 in this memo is the typing layer underneath. The two layers (sigil-level envelope schemas + sigil-kind typing) need to ship together to be useful.

### Recommendation

No new edit. Finding 1's Edit 3 (frontmatter `edges:` block) and the prior memo's edit 1 (sigil `<source-schema>`) are the two halves of this fix.

---

## What I'm leaving open for you

Four calls only you should make.

### Q1 — Is sigil-vs-spec drift actually happening?

Determines whether Finding 3 becomes an edit.

**Signal:** Have you ever pulled a sigil from `registry/SIGILS.md` and been surprised by behavior the README didn't promise? Has any downstream consumer flagged a sigil that "doesn't do what its name says anymore"?

**Action if yes:** Ship `arcana/spec-extractor/` as a future edit.
**Action if no:** Defer Finding 3. Revisit in 6 months.

### Q2 — Is the six-kind taxonomy the right axis for sigils?

Determines whether Edit 1 ships as proposed. Specifically:

- `Discoverer` lumps scope-interview / distill / x-ray / architecture-pattern-inventory. Reviewer flagged this kind as broad. Should it split (Conversational / Recursive-critique / Artifact-producer)?
- `constitution-governance` is dual-classified (Authority + LifecycleOwner). Acceptable, or sign of wrong axis?
- Seven sigils are deferred with `kind-candidate:` (skill-decomposer, skill-transcriptor, sigil-runtime-installer, structured-interview-kits, residuality-spec, invoke-example-runner, decision-gate). Promote any of them to full kinds now, or wait for inhabitant count to grow?

### Q3 — Is the spell-shape taxonomy {pipeline, wrapper, dispatcher, lifecycle, interview, orchestrator} correct?

Determines Edit 5's legal values for `shape:` and Edit 6's conditional branches.

### Q4 — Are you willing to take a CI gate on frontmatter ↔ table drift?

Determines whether Edit 4b ships. If yes, the generator script + CI gate become part of arcanum's infrastructure. If no, drop Edit 4b; keep only Edit 4a (one-time retrofit). The `Required Sigils` tables drift over time — Edit 2's validator still works on freshly-edited spells but documentation reference goes stale.

---

## Concrete edits, ordered by leverage

Eight edits total. Edits 1–4b land Finding 1 (typing + edges). Edits 5–6 land Finding 2 (spell-shape). Edit 7 is gated on Q1.

Several edits are gated on open questions: Edit 1 on Q2, Edit 4b on Q4, Edit 7 on Q1. Don't ship a gated edit before its question resolves.

### Prerequisites (status check)

Before this memo's edits land, three preconditions must be honest:

1. **The prior memo's Edits 1 + 2 (`<source-schema>` field + contract-join check) are recommendations, not shipped artifacts.** `grep -rn "<source-schema>" arcana/` returns zero. Edit 6 of THIS memo extends "the prior memo's edit 2", so Edit 6 cannot ship until the prior memo's Edits 1+2 ship. State this dependency, or fold the prior memo's Edit 1 in as a precondition.
2. **Spell `README.md` files have no YAML frontmatter today.** `composes:` does not exist as a field. Edit 4a must include a retrofit pass over the 11 spell READMEs to add frontmatter blocks with `composes:` + `shape:`, in addition to the 23 sigil SKILL.md retrofits.
3. **Unknown frontmatter keys must be ignored by current parsers.** Audit `tools/install_arcanum.sh` and any frontmatter parser in `framework/runtime/` to confirm before Edit 3 and Edit 5 land. Otherwise downstream repos that pulled arcanum at `main` break silently on new fields.

### Edit 1 (gated on Q2) — `framework/SIGIL-KINDS.md` (new file)

Enumerates the semantic kinds for sigils, declares the lineage from `domainspec/TAXONOMY.md`, and lists deferred kind-candidates.

Ship this only after Q2 resolves — if Discoverer splits or the dual-class rule changes, the table below is wrong.

The six kinds:

| Kind | Distinguisher | Inhabitants |
|---|---|---|
| Observer | Read-only over execution events | signal-observer, workflow-reflect |
| Authority | Owns canonical state; promote/demote | definitions-governance, constitution-governance, ontology-vault, inventory |
| Discoverer | Produces structured findings | scope-interview, distill, x-ray, architecture-pattern-inventory |
| LifecycleOwner | Coordinates multi-sigil + human-gate + promotion | sigil-development, spellcraft, refine, constitution-governance\* |
| Executor | Runs bounded action end-to-end | task-session |
| Researcher | Multi-agent / experimental investigation | robot-talks, experiment-harness |

\* dual classification permitted only here.

Six kinds, six inhabited cells. Earlier draft included a seventh `Maintainer` kind for "modifies existing artifacts without owning their lifecycle"; reviewer pass cut it as a zero-inhabitant placeholder. If a future sigil needs that slot, re-add via `kind-candidate:` first.

Seven sigils deferred as `kind-candidate:` until inhabitant count justifies a separate kind: skill-decomposer, skill-transcriptor (Transcriber); sigil-runtime-installer (Installer); structured-interview-kits (Interviewer); residuality-spec (Specifier); invoke-example-runner (Orchestrator); decision-gate (Gate).

Doc must open with a "Lineage" section crediting `domainspec/TAXONOMY.md` + `domainspec/RELATIONSHIPS.md` as parent pattern (cite-don't-rediscover discipline). Doc must state explicitly that `kind:` is engineering vocabulary, not a categorical claim — overlap with CT terminology (e.g., `Observer`) is coincidence of word.

*Effect:* gives arcanum a semantic axis distinct from `tier:` / `domain:`. Required input for every downstream edit.

### Edit 2 — `framework/SIGIL-EDGES.md` (new file)

Enumerates ten typed edges in two cuts.

**Validator-enforced after Edit 4a + 5 land (2 edges):**

| Edge | Source | Target | Validator check |
|---|---|---|---|
| `composes` | Spell | Sigil \| Spell | parse spell `composes:` frontmatter (introduced by Edit 4a retrofit); cross-check against the `Required Sigils` markdown table |
| `observes` | Observer | Sigil | static check: parse Observer sigil's `edges:` block; verify each declared target exists in `registry/SIGILS.md`. Telemetry-grounded cross-check (envelope shows the observer actually ran on the declared target) requires extending `SIGIL-OBSERVABILITY-HOOK.md` to carry an `observer.sigil_id` + `observer.observed_sigil` pair — out of scope for this memo. |

**Declared-only — authoring-discipline edges (8).** These are documented in frontmatter for graph-traversal and human navigation. They are **not** machine-enforced; some (e.g., `delegates-to` vs `composes` distinguished by "no return arrow") cannot be enforced by today's per-invocation envelope at all, because the ledger does not capture call-graph topology. Treat these as discipline for authors, not as validator promises. Each has a one-line distinguisher to keep authors from picking by vibe:

| Edge | Distinguisher (what makes it not its neighbor) |
|---|---|
| `delegates-to` | Source hands control to target; no return arrow expected. Distinct from `composes`, which is a phase-of relationship with implicit return. |
| `requires-evidence-from` | Source consumes target's emitted telemetry / signal as gating input. Distinct from `observes` (which is the inverse direction) and `composes` (no envelope dependency). |
| `produces-handoff-for` | Source emits a typed package shaped to a specific target's input contract. Distinct from `delegates-to` (no typed envelope) and `composes` (no boundary crossing). |
| `wraps` | Source executes target's invocation and reads its envelope without consuming its output. The wrapper-shape spell relation (Finding 2). |
| `auto-adds` | Installing source implicitly installs target as runtime dependency. Install-time only; no runtime relation. |
| `routes-to` | Coordinator dispatches work to target by classification rule. Distinct from `composes` (per-invocation routing, not fixed phase). |
| `produces-candidate-for` | Source emits a candidate that target Authority decides to promote / reject. Distinct from `delegates-to` because the receiving Authority owns the decision, not the sender. |
| `feeds` | State-mediated transfer via shared-state envelope. Distinct from `composes` (no direct call) and `produces-handoff-for` (no typed package). |

Dropped (proposed but unattested): `extends`, `replaces`, `validates`, `promotes-via` (subsumed into `produces-candidate-for`).

*Effect:* gives arcanum a morphism vocabulary. Validator enforces the two edges that have telemetry today; remaining eight are honest declarations awaiting telemetry-derive work.

### Edit 3 — `framework/templates/sigil-template.md`

Add to frontmatter:

```yaml
kind: <one of six SIGIL-KINDS>   # or [list] for dual-classified
# OR (deferred sigils only):
kind-candidate: <one of six candidates>

edges:
  - to: <target>
    type: <one of ten SIGIL-EDGES>
```

*Effect:* every new sigil declares kind + edges from creation.

### Edit 4a — Retrofit 23 sigils in `arcana/` with `kind:` + `edges:`, and 11 spells with `composes:` + `shape:`

Two mechanical frontmatter passes:

- **Sigils (23 files):** add `kind:` (or `kind-candidate:` for the deferred set) and `edges:` to each `SKILL.md`.
- **Spells (11 files):** add a frontmatter block (none exists today) with `composes:` (mirrors the `Required Sigils` table content) and `shape:` (one of the six from Edit 5).

Edit 4a depends on Edit 1 + Edit 3 + Edit 5 having merged first. Validator in Edit 2 must accept both `kind:` and `kind-candidate:` (treat the latter as declared-but-unenforced).

*Effect:* sigils declare their kind + edges; spells declare their composition + shape. Necessary input to Edit 2's validator and Edit 6's shape-aware check.

### Edit 4b (gated on Q4) — Generator script + CI gate for `Required Sigils` tables

Spell `Required Sigils` tables become GENERATED from spell `composes:` frontmatter. Generator script + CI gate that blocks PRs where the table and the frontmatter diverge.

This is a separate work item from 4a because it commits arcanum to running CI infrastructure on documentation drift. If you don't take this, Edit 2's validator is still enforceable on freshly-edited spells, but the documentation tables drift within a quarter and become unreliable as reference.

*Effect:* single source of truth for composition (frontmatter); tables are derived artifacts.

### Edit 5 — `framework/templates/spell-template.md`

Add to frontmatter:

```yaml
shape: { pipeline | wrapper | dispatcher | lifecycle | interview | orchestrator }
```

*Effect:* Finding 2 — declares spell shape so Edit 6 knows which validation to apply.

### Edit 6 — `arcana/spellcraft/SKILL.md` (validate mode)

**Depends on prior-memo Edits 1+2 having shipped** (otherwise there's no `<source-schema>` to do contract-join against). Once those land, make the contract-join check conditional on `shape:`:

- `pipeline` → check phase N output covers phase N+1 source-schema (the prior memo's check).
- `wrapper` → check wrapped capability's envelope is reachable to wrapping sigil.
- `dispatcher` → check each branch is internally valid; skip join.
- `lifecycle` → check phase-to-phase gates are well-defined.
- `interview` → check question tree is well-formed; skip join.
- `orchestrator` → routing rules well-defined; skip join.

*Effect:* validator stops false-positive-ing on 6/11 spells.

### Edit 7 — `arcana/spec-extractor/` (new sigil, CONDITIONAL on Q1)

Reverse-extractor that reads a deployed sigil and emits the inferred spec, diffs against original spec, surfaces drift.

*Effect:* drift detection. Ship only if Q1 = yes.

---

## What I deliberately did not recommend

For honesty about what was considered and cut. The audit generated ten kinds and ten edges; only six kinds and two enforced edges survive.

**Kinds dropped (3 of 10):**

- **Composer** — name borrows the most reserved CT term and misdescribes the candidates (skill-decomposer / skill-transcriptor are external→sigil importers, not categorical composers). Renamed `Transcriber` and demoted to deferred.
- **Persister** — folded into Authority. Reviewer's diagnostic: ontology-vault was double-classified as both Authority and Persister, which means the two distinguishers ("owns canonical state" / "owns durable storage") collapse onto the same artifact. Wrong axis.
- **Interviewer** — singleton (only structured-interview-kits). Deferred as `kind-candidate:` until a second inhabitant exists.

**Edges dropped (3 of 10):**

- **extends**, **replaces** — zero instances in the repo. Speculative.
- **validates** — weakly attested only via experiment-harness; subsumed under `observes` and `requires-evidence-from`.

**Other proposals cut:**

- **Spec ↔ sigil adjunction with triangle identities.** No `compile` function exists in arcanum to be the forward half. Collapsed into Finding 3 as plain drift detection.
- **Categorical NAMING (associativity / identity / functorial language) per spell.** The vocabulary was cut. The type-matching engineering kernel survives as Edit 6's `pipeline` branch (codomain of phase N must cover domain of phase N+1) — I'm being honest that this is the rejected proposal's content, with the categorical pitch stripped. What was actually cut is the claim that arcanum spells form categories — most don't (no identity sigil for wrappers / dispatchers / interviews / orchestrators), so the categorical framing was decoration. The check survives in the cases where it applies.
- **Cross-feature naturality audit, faithful-functor lint, Yoneda equivalence check, Hom(-,C) section on concept cards, Lan_Δ push-forward migration tool, Ran_Δ pull-back migration tool.** All target domainspec (the deployed companion repo), not arcanum. Wrong addressee. Separate memo to that repo's maintainer. The Hom(-,C) incoming-edges index per concept card is the strongest standalone-engineering case among them.
- **Coalgebra re-promotion in the theorem repo.** Proposal was based on a misreading: `domainspec-theorem/NOVEL-MAPPINGS.md` line 527 marks coalgebraic iteration as standard prior art (Hasuo–Jacobs–Niqui, Bhattacharya, Leinster), not out-of-scope. Once corrected, no action.

The pattern: where a CT name was load-bearing in a proposal's pitch, the engineering kernel underneath was either (a) already queued in the prior memo, (b) targeted at a different repo, or (c) borrowing categorical authority the operational behavior didn't sustain. The lens told me where to look. It rarely told me what to ship.

---

## One observation that's beyond the audit

The first memo identified what was missing at the sigil layer (residue, source-schema, output-contract drift detail, residue accumulation in reflection state). This memo identifies what was missing one layer down: the type system that sigils and spells are nodes of, and the edge vocabulary they relate through. Without that type substrate, the first memo's edits are reasoning over untyped objects.

Both memos surface the same gap. Since both came from the same audit pipeline (my multi-agent loop against the same repo), this is not independent corroboration — treat it as one observation seen from two angles, not two.

The domainspec sibling already has the typed-graph pattern (`TAXONOMY.md` + `RELATIONSHIPS.md`, reified as Lean enums). Arcanum needs the same surface. This memo's Edits 1–4b are that surface. The theorem-repo discussion about how typed residue transports across deployments is adjacent; not relevant until Arcanum has its own typed surface to compare against.

---

## Three sharpest questions

Q4 (CI gate) is an infrastructure call, listed above with the others. The three below are the taxonomy-and-existence calls that shape what actually gets built.

1. **Q2 — Is the six-kind sigil taxonomy the right axis?** → fixes Edit 1.
2. **Q3 — Is the {pipeline, wrapper, dispatcher, lifecycle, interview, orchestrator} spell-shape taxonomy correct?** → fixes Edit 5 and Edit 6.
3. **Q1 — Is sigil-vs-spec drift actually happening?** → ship Edit 7 or defer.

— V.
