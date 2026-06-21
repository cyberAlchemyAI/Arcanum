# Receipt Id Legend Constitution

Status: candidate
Date: 2026-06-21
Owner: Constitution Governance

## Purpose

A sigil or spell receipt that cites a tracked id must gloss that id inline, so the receipt is self-contained: a reader can understand what each cited id means without opening the ledger, work-pack, or run folder that minted it.

This constitution hardens the [receipt-id-legend discipline](../disciplines/cards/receipt-id-legend.md) into reviewable rules.

## Scope

Applies to:

- the returned `## ... Result` blocks of Arcanum sigils and spells,
- any receipt, status report, residue ledger, or handoff that references a tracked id (`CTX-`, `BLK-`, `GAP-`, `DEC-`, `ENA-`, `GATE-`, `TASK-`, `SWU-`, `R-*`, run ids, `dispatch_id`, and peer schemes),
- all-status / pending-by-node receipts that list ids in bulk.

Does not apply to:

- the id schemes themselves or where ids are minted (owned by craft, invoke/task-session, refine, dispatch-spec),
- the full source artifact (ledger, work-pack, dispatch) where the id is already defined in place,
- internal machine indexes (`indexes.by_id`) whose job is lookup, not human-facing explanation.

## Rules

| Rule ID | Rule | Validation Mode | Validator | Status |
| --- | --- | --- | --- | --- |
| `receipt-id.gloss-on-cite` | Every tracked id cited in a receipt carries an inline one-line gloss (`ID - meaning`), not a bare token. | review | none yet | candidate |
| `receipt-id.define-on-mint` | When an artifact first names/creates a tracked id, it defines that id in place (summary + meaning), so downstream receipts have a source to restate. | review | none yet | candidate |
| `receipt-id.no-orphan-cite` | A receipt must not cite an id that is defined nowhere reachable; an undefined id is a block-level defect, not a stylistic one. | review | none yet | candidate |
| `receipt-id.bulk-legend` | A receipt that lists ids in bulk (all-status, pending-by-node, residue ledger) glosses each listed id, or links to the one place each is defined. | review | none yet | candidate |
| `receipt-id.scheme-not-owned` | Glossing an id in a receipt never redefines or mutates the id's owning scheme; the gloss restates, it does not author. | review | none yet | candidate |

## Examples

Preferred:

- `BLK-TDE-AUTH-CONVENTION-001 - auth round-trip fails on oracle-convention drift; needs general bridging + new δ rules`,
- a pending-by-node block where each `GAP-`/`DEC-` line carries its one-line meaning,
- a residue ledger that writes `R-C2-3 (honesty gate mandatory) - no feature PASS without the negative control`.

Not preferred:

- `Active blockers: BLK-TDE-AUTH-CONVENTION-001, BLK-TDE-GATE-HONESTY-001` with no glosses,
- citing `SWU-ENG-005` in a result with no statement of what it is,
- a receipt that references a `dispatch_id` defined in no reachable artifact,
- "explaining" an id by silently changing what the ledger says it means.

## Validation

No deterministic validator exists yet. Until one does, receipts are reviewed against these rules.

Next hardening move: add a receipt-legend check under `tools/` that scans a returned receipt for tracked-id token patterns and flags any cited id lacking an inline gloss or a resolvable definition, then raise the affected rules from `review` to `deterministic`.

## Promotion Boundary

This constitution is `candidate`. Promote it to canonical only after the receipt-legend validator exists and the [receipt-id-legend discipline](../disciplines/cards/receipt-id-legend.md) names its validation surface and mutation boundary.
