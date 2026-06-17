# Arcanum Manual — Craft View

> Human view of [`.craft/ledger.yml`](.craft/ledger.yml). The ledger is the source of truth;
> this file is a linked rendering only.

- **Project:** Arcanum Manual — Research Strategy and Authoring
- **Root context:** `CTX-ARCANUM-MANUAL-ROOT`
- **Stage / gate:** validate / **pass**
- **Source of truth:** [`.craft/ledger.yml`](.craft/ledger.yml)

## Quick links

- **Next move:** Operator review of [ARCANUM-MANUAL.md](development/user-guide/ARCANUM-MANUAL.md);
  optionally render an HTML/PDF companion, then commit inside the arcanum submodule before bumping
  the parent gitlink.
- **Blocking decisions:** none
- **Active blockers:** none
- **Active gaps:** none (GAP-AUDIENCE-TAXONOMY-001 resolved)
- **Deliverables:** [**ARCANUM-MANUAL.md**](development/user-guide/ARCANUM-MANUAL.md) (pass) ·
  [validation evidence](development/user-guide/ARCANUM-MANUAL.validation.md) ·
  [surface x-ray HTML](development/user-guide/arcanum-surface-xray.html) ·
  [distill notes/corpus](.craft/artifacts/arcanum-manual-distill-notes.md) ·
  [research dispatch](.craft/artifacts/20260616-arcanum-manual-research-strategy.dispatch.json)

## Purpose

Build a leverage-oriented Arcanum manual that explains **what Arcanum is**, **what its processes
are**, and **how each kind of user can use it**, by researching the full Arcanum knowledge surface
and authoring through `whisper`. `development/user-guide/` is the explanatory pattern base and the
final home for the manual.

## The strategy (validated dispatch route)

The research strategy is encoded as a single validated dispatch route,
[ART-MANUAL-RESEARCH-DISPATCH](.craft/artifacts/20260616-arcanum-manual-research-strategy.dispatch.json)
(`dispatch-spec` verdict: **pass**). It plans, but does not execute:

| Step | Capability | Pattern | Produces |
| --- | --- | --- | --- |
| s01 X-ray the Arcanum surface | `x-ray` | xray | layered map + `arcanum-surface-xray.html` |
| s02 Inventory the knowledge corpus | `inventory` | sequential | source-backed knowledge ledger |
| s03 Distill per audience | `distill` | distill | concept units grouped by reader leverage |
| s04 Whisper the manual | `whisper` | synthesis | `ARCANUM-MANUAL.md` |
| s05 Validate against source | `necronomicon` | validation | per-claim source-resolution evidence |

**Executed 2026-06-16** with operator-approved subagent fan-out: five read-only explorer lanes
(framework/method, sigils, spells, observability/lifecycle, user-guide pattern + audiences) joined
by parent synthesis → distill → whisper authoring → source validation (**pass**). Trace:
`dispatch-authored → subagent-strategy-approved → arcanum-surface-xrayed → knowledge-corpus-inventoried
→ concept-units-distilled → manual-whispered → arcanum-manual-validated`.

## Contexts

### <a id="context-ctx-arcanum-manual-root"></a>CTX-ARCANUM-MANUAL-ROOT — Arcanum Manual

- Stage / gate: design / flag
- Next move: present the validated dispatch + subagent strategy for approval, then execute the
  route to produce [ARCANUM-MANUAL.md](development/user-guide/ARCANUM-MANUAL.md).
- Owns: [ledger](.craft/ledger.yml), [this view](CRAFT.md),
  [research dispatch](.craft/artifacts/20260616-arcanum-manual-research-strategy.dispatch.json),
  [user-guide base](development/user-guide/), [final manual (planned)](development/user-guide/ARCANUM-MANUAL.md)

## Definitions (candidate, local)

- **<a id="definition-def-arcanum-manual-001"></a>Arcanum manual** (`DEF-ARCANUM-MANUAL-001`,
  candidate): a leverage-oriented explanatory artifact that lets a reader understand what Arcanum
  is, its processes, and how each kind of user can use it, with every claim backed by an Arcanum
  source path. It is documentation, not a canonical surface.

## Gaps

- **<a id="gap-gap-audience-taxonomy-001"></a>GAP-AUDIENCE-TAXONOMY-001** (**resolved**): "How each
  user can leverage it" needed an explicit reader/persona taxonomy. Resolved in the distill step — a
  7-persona taxonomy grounded in README Start-Here, `FRIEND-INSTALL-TUTORIAL.md`, the user-guide
  thesis, and registry use-when conditions; inferred personas are labelled as such. See
  [distill notes](.craft/artifacts/arcanum-manual-distill-notes.md) and
  [manual Part 3](development/user-guide/ARCANUM-MANUAL.md).

## Boundary check

Craft governed local state and residue; `dispatch-spec` validated route shape only. The route was
executed as documentation work: it created a manual, an x-ray surface, distill notes, and validation
evidence under `development/user-guide/` and `.craft/`. **No sigil, spell, definition, registry, or
other canonical Arcanum surface was created, mutated, or promoted.** Subagents were read-only and
gathered/distilled only; the parent owned synthesis and authoring.
