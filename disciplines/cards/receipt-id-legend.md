# Receipt Id Legend Discipline

Status: candidate
Steward: Constitution Governance

## Purpose

Any Arcanum sigil or spell receipt (its returned `## ... Result` block) that **cites a tracked id must gloss that id inline** with a one-line meaning, so the receipt is self-contained and decodable without opening the source artifact.

Tracked ids are the stable identifiers capabilities mint and reference, for example:

- Craft ledger ids — `CTX-`, `BLK-`, `GAP-`, `DEC-`, `ENA-`, `GATE-` (owned by [craft](../../arcana/craft/README.md)),
- work-pack / plan ids — `TASK-`, `SWU-` (owned by [invoke](../../arcana/invoke/README.md) and [task-session](../../arcana/task-session/README.md)),
- refine residue and run ids — `R-*`, run-id (owned by [refine](../../arcana/refine/README.md)),
- dispatch ids and route step ids — `dispatch_id`, step ids (owned by [dispatch-spec](../../formulae/dispatch-spec/README.md)).

The rule has two halves: when an id is **first named/created** in an artifact, that artifact defines it; when an id is **cited in a receipt**, the receipt restates its one-line meaning (id → gloss) rather than assuming the reader holds the ledger.

## Boundary

This discipline names the *receipt legibility* practice. It does not own:

- the id schemes themselves or where ids are minted — Craft owns `BLK-/GAP-/DEC-`, invoke/task-session own `SWU-/TASK-`, refine owns `R-*`, dispatch-spec owns `dispatch_id`,
- the underlying blocker/gap/decision content or its resolution,
- the ledger or index that stores the ids (Craft's `indexes.by_id` remains the source of truth).

Enforcement of the receipt-form rule routes through [constitution-governance](../../arcana/constitution-governance/) and each sigil's output contract; mutation of the catalog and this card routes through [discipline-governance](../../arcana/discipline-governance/).

## Evidence

- [craft SKILL output contract](../../arcana/craft/SKILL.md) - the `Pending by node` receipt lists blockers, decisions, and gaps by id; without an inline gloss the receipt is unreadable outside the ledger.
- [task-session SKILL output contract](../../arcana/task-session/SKILL.md) - the result block cites resolved decision counts and SWU/decision ids and a Decision Gate Result that references option/decision ids.
- [refine SKILL output contract](../../arcana/refine/SKILL.md) - the result and residue ledger cite run ids and `R-*` residue ids that are opaque without a gloss.
- [dispatch-spec README](../../formulae/dispatch-spec/README.md) - dispatch routes carry `dispatch_id` and step ids surfaced in downstream receipts.
- [Discipline Catalog](../DISCIPLINES.md) - the `craft`, `planning`, and `decision-gating` rows show id-bearing receipts are a recurring, cross-capability concern.

## Validation

- Mode: mixed
- Check: `python3 disciplines/scripts/validate-discipline-catalog.py` (catalog row shape) + `python3 tools/validate-receipt-legend.py <receipt.md>` — a deterministic check that every cited tracked id carries an inline gloss or in-file definition (`gloss-on-cite` rule; `--self-test` covers pass/fail fixtures).
- Latest result: pass (validator self-test green 2026-06-21)

## Quality Bar

A useful receipt-id-legend discipline entry must:

- name a recurring practice (glossing cited tracked ids in receipts) rather than a one-off formatting note,
- cite concrete repository evidence (sigil output contracts that emit id-bearing receipts),
- identify Constitution Governance as steward,
- separate the receipt-legibility rule from the id schemes and ledger content it references,
- name the next hardening move (the receipt-id-legend constitution and a future receipt-legend validator).

## Promotion Guardrail

Discipline evidence can recommend a route, but it cannot directly promote registry, ontology, glossary, sigil, or spell knowledge. Advancing this discipline beyond `candidate` requires the constitution's rules to gain a validation surface (a receipt-legend check) and a named mutation boundary.
