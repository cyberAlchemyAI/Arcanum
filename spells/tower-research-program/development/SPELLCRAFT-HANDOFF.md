# Invoke Handoff → Spellcraft: `tower-research-program`

> Produced by `invoke` **handoff** mode (contract: [`spells/invoke/handoff.md`](../../invoke/handoff.md)).
> This is a development-stage handoff artifact, **not** a promoted spell. Spellcraft
> ([`arcana/spellcraft/`](../../../arcana/spellcraft/)) remains the lifecycle authority for spell
> composition, validation, and registry promotion. Nothing here mutates a canonical surface.

## Identity & source session

- Spell: `invoke`
- Mode: `handoff`
- Handoff type: **`new-lifecycle-thread`** (a reusable workflow pattern emerged and needs its own spell lifecycle)
- Target lifecycle owner: **`spellcraft`**
- Next route: **`spellcraft`**, starting at **design** (a fully-worked, gate-passed reference instance already exists — this is generalization, not greenfield define)
- Prospective canonical spell ID: `tower-research-program`
- Candidate aliases: `Tower Research Program`, `Isolated Tower Research`, `Research Tower Fan-out`
- Source session: a Claude Code session in a sibling **private** research repo (2026-06), governed by that repo's `domainspec-subagents-strategy` skill chain. (Instance-specific provenance is redacted — this published handoff carries only the reusable spell pattern.)

## New session prompt (what spellcraft should act on)

> Author a reusable Arcanum spell, `tower-research-program`, that lets any repository set up a
> bounded, multi-corpus research program: a `meta` umbrella that fans out into N mutually-isolated
> "tower" research dispatches (each a self-scoped mini research pipeline with its own in-corpus
> skeptic), all tagged into one shared target taxonomy, then reconciled by a single cross-corpus
> synthesis dispatch — with a hard search bound that prevents recursive citation-chasing.

## Route rationale

The source session built this pattern by hand, iterating through three designs (single fan-out →
flat two-phase split → meta multi-tower program) and ratifying it with the human. The composition is
stable, repeatable across domains, has shared artifacts and gates, and would otherwise be rebuilt
from scratch each time — exactly the README's "Use Spells When" criteria. It is **not** a single
sigil's job (it composes dispatch proposal + check-tension gate + per-tower research + synthesis +
inventory), so it belongs in the spell layer.

## The pattern to generalize (selected session context)

### Problem shape
Turn one **primary source** + several **source corpora** into a source-backed research map, without
(a) cross-contaminating corpora, (b) tripping recursive paper-research, or (c) over-promoting
research claims into policy/tokenomics.

### Structure (the reference instance, gate-passed)
```
META PROGRAM (meta:true, no agents — plans the program)
│
├─ Tower dispatch × N            ← each its own ISOLATED context
│    explorers (n self-scoped, tensioned on METHODOLOGY — corpus is fixed)
│      → tower-synthesizer ⇄ in-corpus skeptic (zig-zag ≤1)
│      → lane-tagged tower-findings; final_approver = parent
│    invariants: single shared base only, no sibling output, depth-1 search bound, ≤K sources/sub-lane
│
└─ PROGRAM SYNTHESIS dispatch     ← READY only when all towers close
     synthesizer (aggregates BY shared-taxonomy lane)
       → reviewers (robot-talks, tensioned on ATTACK-VECTOR / cross-corpus)
       → writer → auditor (dedicated final_approver)
```

### The two load-bearing ideas a generic spell must preserve
1. **Two-axis tension.** *Within* a tower the corpus is fixed, so sub-lanes tension on the
   **methodology** axis; *across* towers each tower is a distinct corpus, so cross-corpus tension is
   deferred to the program synthesis (**source-corpus** axis). This is what makes both levels pass
   the check-tension spread test.
2. **Degree decided inside each tower.** Sub-lane count is scoped from each corpus's own breadth
   (its residue/target map), not a global constant. A thinner corpus self-selects fewer lanes.

### Invariants (parameterize, don't hardcode)
- **Isolation:** one shared base source; no tower receives another tower's output; each tower is its
  own context.
- **Search bound (recursion guard):** depth-1, no citation/bibliography chasing; ≤K admitted sources
  per sub-lane (K≈6 in the instance); single web pass; cited-but-unfetched → residue.
- **Shared target taxonomy:** towers **tag** findings into one shared lane set; synthesis aggregates
  into a lane × tower matrix (never duplicate the taxonomy per tower).
- **Promotion boundary:** research-only; the spell must refuse promotion of claims into definitions,
  specs, token policy, governance weights, or implementation.
- **Gates & lineage:** every child dispatch re-enters the init-time tension gate **and** a human
  confirm; `meta:true` umbrella carries lineage to children via `parent_dispatch_id`.

## Draft spell skeleton (input for spellcraft `design`, per `templates/spell.md`)

| Aspect | Proposal (spellcraft confirms) |
|---|---|
| **Trigger** | One primary source + ≥2 source corpora to combine into a bounded, contamination-free research map. |
| **Required sigils** | dispatch-proposal/strategy · check-tension gate · research-dispatch (per tower & synthesis) · `inventory` (trace) |
| **Optional sigils** | `decision-gate` (scoping/route choices) · `context-builder` (corpus framing) · `observability` |
| **Shared state** | program scoping table (towers × sub-lane count) · per-tower lane-tagged findings · shared attack-lane taxonomy · search-bound config |
| **Phases** | 1 plan-program (meta) → 2 per-tower research (parallel, isolated) → 3 program synthesis (barrier: all towers closed) → 4 inventory/closeout |
| **Gates** | per-child tension-gate PASS/PASS + human confirm; synthesis blocked until all towers register findings |
| **Failure policy** | a tower error degrades to a partial-program result the synthesis + final_approver are told about |

## Obligation coverage matrix

| Obligation for the new spell thread | Covered by this handoff? | Where |
|---|---|---|
| Concrete, validated reference instance | ✅ | source-session paths below |
| The generalized structure & invariants | ✅ | "pattern to generalize" + skeleton above |
| Tension-design rules (two axes) | ✅ | load-bearing idea #1 |
| Self-scoping rule | ✅ | load-bearing idea #2 |
| Recursion/search bound | ✅ | invariants |
| Exact arcanum sigil IDs to bind | ⚠️ gap | spellcraft resolves against the sigil registry |
| Spell registry entry / canonical README | ⚠️ deferred | spellcraft owns promotion |

## Excluded context (tempting but not needed for the spell)
- The specific instance domain (a private token-economy research project — its tickers, its
  attack-lane set, and its agent roster): these are *instance bindings*, not spell structure. The
  spell takes corpora + a taxonomy + an agent pool as parameters.
- The full check-tension rubric (owned by the `domainspec-check-tension` skill in the source repo);
  the spell references the gate sigil, it does not re-encode the rubric.

## Reference instance layout (the gate-passed structure this spell generalizes)
- Umbrella: `dispatch/PROPOSED-META-PROGRAM.md`
- Towers: `dispatch/towers/PROPOSED-TOWER-{1..N}-*.md` (gate-passed)
- Synthesis: `dispatch/PROPOSED-PROGRAM-SYNTHESIS.md` (gate-passed)
- Shared taxonomy: `lanes/<taxonomy>.md`
- Search-bound discipline: `subtowers/*/levels/L0-corpus.md` ("Search Bound" sections)
- Genesis/lineage: `dispatch/PROPOSED-DISPATCH.md`

## Gaps & blockers
- **Gap:** sigil-ID binding (which arcanum sigils realize "dispatch-proposal", "check-tension",
  "research-dispatch") — spellcraft resolves against `registry/SPELLS.md` + the sigil registry.
- **No blockers.** This handoff mutates nothing; it only stages a development pack for spellcraft.

## Next-session start prompt (for spellcraft)
> Using `spells/tower-research-program/development/SPELLCRAFT-HANDOFF.md`, run spellcraft **design**
> for `tower-research-program`: bind the phases to concrete sigils, define shared-state artifacts and
> gates, generalize the two-axis tension + self-scoping + search-bound invariants into spell
> parameters, then produce the canonical `spells/tower-research-program/README.md` and registry entry
> for validation.

## Provenance & output
- Output path: `spells/tower-research-program/development/SPELLCRAFT-HANDOFF.md` (this file)
- Context Builder coverage: **flag** (structure fully covered; sigil-ID binding is a named, safe gap for the next thread)
- Produced: 2026-06-27
