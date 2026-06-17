# Product Launch Craft Ledger

Human-readable view of `.craft/ledger.yml`. The ledger is
the source of truth; this page is a linked navigation surface.

## Quick Links

- Current next move: [run the pilot-evidence task](#next-move).
- Active blocker: [BLK-PILOT-EVIDENCE-001](#blocker-blk-pilot-evidence-001).
- Active gap: [GAP-SEED-DATA-001](#gap-gap-seed-data-001).
- Closed decision: [DEC-API-BOUNDARY-001](#decision-dec-api-boundary-001).
- Key artifacts: `docs/decisions/api-boundary.md`, `docs/pilot-evidence-plan.md`, `receipts/api-contract-review.json`.

## Contexts

### <a id="context-ctx-product-launch-root"></a>CTX-PRODUCT-LAUNCH-ROOT - Product Launch Readiness

- Stage: `plan`
- Gate: `flag`
- Purpose: track the smallest launch-ready slice, its blockers, decisions, evidence, and next move.

#### <a id="next-move"></a>Next Move

Run the first pilot-evidence task and attach the receipt to
[BLK-PILOT-EVIDENCE-001](#blocker-blk-pilot-evidence-001).

### <a id="context-ctx-product-launch-api-review"></a>CTX-PRODUCT-LAUNCH-API-REVIEW - API Contract Review

- Stage: `closed`
- Gate: `pass`
- Closure evidence: `docs/decisions/api-boundary.md` and `receipts/api-contract-review.json`.
- Selected boundary: narrow contract adapter.

## Blockers

### <a id="blocker-blk-pilot-evidence-001"></a>BLK-PILOT-EVIDENCE-001

- Lane: `validator`
- Status: `active`, `refined`
- Role: `evidence_reviewer`
- Allowed roles: `evidence_reviewer`, `validator`, `product_owner`
- Human required: `false`
- Role confidence: `candidate`
- Summary: launch readiness cannot pass until at least one pilot evidence receipt exists.
- Closure: a pilot run produces a receipt that satisfies the launch evidence checklist without expanding scope.
- Route: `task-session`
- Role note: validator owns the evidence check; product reviews whether the evidence satisfies launch meaning.

## Decisions

### <a id="decision-dec-api-boundary-001"></a>DEC-API-BOUNDARY-001

- Question: Which API boundary should the launch slice use?
- Status: `closed`, non-blocking
- Selected: `narrow-contract-adapter`
- Rationale: gives the launch slice a stable integration point without copying ownership or widening implementation scope.
- Impact: launch planning can continue; shared packaging remains future hardening.
- Evidence: `docs/decisions/api-boundary.md`

## Gaps

### <a id="gap-gap-seed-data-001"></a>GAP-SEED-DATA-001

- Severity: `flag`
- Treatment: `plan`
- Summary: seed data exists only as a fixture and has not been checked against a live pilot run.

## Route Evidence

- API contract review handoff: `handoffs/api-contract-review.md`
- API contract review receipt: `receipts/api-contract-review.json`
- Pilot evidence plan: `docs/pilot-evidence-plan.md`

Important boundary: route and receipt evidence explain what happened. They do
not replace the source ledger.

## Recomposition

[CTX-PRODUCT-LAUNCH-API-REVIEW](#context-ctx-product-launch-api-review)
recomposed into [CTX-PRODUCT-LAUNCH-ROOT](#context-ctx-product-launch-root)
with the selected API boundary. Remaining residue:
[BLK-PILOT-EVIDENCE-001](#blocker-blk-pilot-evidence-001) and
[GAP-SEED-DATA-001](#gap-gap-seed-data-001).
