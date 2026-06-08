# Craft Interface Development Gap Review

Status: pass-with-watchpoints
Date: 2026-06-07
Review modes: interrogation, decision-gate

## Purpose

Pressure-test `CRAFT-INTERFACE-001` and `CRAFT-INTERACTION-001` before
execution and identify blockers or gaps that could surface mid-development.

## Structured Interview Result

Target scope: Craft interface and interaction development.

Mode: readiness-risk-review.

Questions asked: 0.

Decisions recorded: 4 in
`docs/decisions/craft-interface-development-risk-gates.md`.

Artifacts updated:

- `docs/decisions/craft-interface-development-risk-gates.md`
- `development/craft/CRAFT-INTERFACE-DEVELOPMENT-GAP-REVIEW.md`

Remaining ambiguities:

- Runtime/helper shape is intentionally deferred.
- Executable receipt validation is intentionally deferred.
- Promotion target remains intentionally undecided.

Verdict: pass.

Next step: run the interface task, then the interaction task.

## Current Blocker Review

No new blocker prevents the local interface and interaction artifact build.

The active background blocker is the aggregate Refine receipt:

- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/refine-run.json`
- status: `block`
- meaning: internal Refine evidence remains incomplete.
- impact on `CRAFT-INTERFACE-001`: non-blocking.
- impact on `CRAFT-INTERACTION-001`: non-blocking.
- becomes blocking if: the work claims Refine completion, Craft promotion, or
  reusable lifecycle readiness.

## Mid-Development Watchpoints

| ID | Watchpoint | Why It Could Surface | Gate |
| --- | --- | --- | --- |
| W-001 | Runtime or helper shape pressure | While writing methods, it may be tempting to decide CLI/library/skill-helper shape. | Keep local file-backed contract only; record helper shape as deferred. |
| W-002 | Receipt validation scope creep | Interaction receipts invite executable validators. | Require parseable YAML fixtures now; defer executable validator until repeated examples exist. |
| W-003 | Route-shape evidence confused with execution evidence | `dispatch-spec` can pass even when no task ran. | State that dispatch pass validates only route shape. |
| W-004 | Owner verdict overwritten by Craft | `apply_receipt` could be misread as rewriting native capability results. | Craft records and applies receipts but does not rewrite native verdicts. |
| W-005 | Context closed without recomposition | `task-session` pass may look like enough to close a Craft context. | Require recomposition evidence before closure. |
| W-006 | Definitions drift into glossary promotion | Interface includes candidate definitions. | Keep definitions local unless a glossary owner route promotes them. |
| W-007 | Existing aggregate Refine block misread as interface blocker | Current package state says Refine receipt is blocked. | Treat it as background state unless this task claims Refine readiness. |
| W-008 | Work-pack becomes the ledger root again | The interface may overfit to task-session work-packs. | Keep work-packs as artifacts owned by contexts, not the ledger root. |
| W-009 | Generated `CRAFT.md` expectations | The target project has both `.craft/ledger.yml` and `CRAFT.md`. | Ledger YAML is source of truth; Markdown view can stay manual in this slice. |
| W-010 | Cross-context relations underspecified | Interaction receipts can affect blockers/gaps outside the current child context. | Fixture should include at least one relation from receipt to affected condition. |

## Gaps

| Gap | Severity | Treatment | Blocks Current Build |
| --- | --- | --- | --- |
| Runtime/helper shape not selected. | deferred | Decide in a later owner route after local fixtures prove the shape. | no |
| Executable receipt validation not implemented. | flag | Keep manual validation plus YAML parsing in this slice. | no |
| Multiple independent Craft live tests not available. | flag | Run after interface and interaction artifacts exist. | no |
| Generated ledger index still lacks consumers. | deferred | Keep out of scope. | no |
| Priority scoring lacks repeated states. | deferred | Keep out of scope. | no |
| Role delegation automation lacks enough examples. | deferred | Keep role hints manual. | no |
| External registry or ontology conflict review not done. | flag-for-promotion | Required only for promotion. | no |

## Hard Gates For The Next Task Session

- Block if the task edits command surfaces, runtime adapters, registries, sigils,
  spells, or canonical glossary state.
- Block if the interface schema makes `CRAFT.md` the source of truth instead of
  `.craft/ledger.yml`.
- Block if a receipt can close a context without recomposition evidence.
- Block if a dispatch pass is represented as execution pass.
- Block if a raw blocker can be resolved directly.
- Block if definitions are promoted without an owner route.

## Decision Gate Result

Target scope: Craft interface and interaction development.

Result: PASS.

Decisions resolved: 4.

Blockers remaining: 0.

Decision artifact: `docs/decisions/craft-interface-development-risk-gates.md`.

Deferred decisions:

- runtime/helper shape;
- executable receipt validation;
- generated Markdown view;
- direct runtime execution through Craft.

Assumptions recorded:

- local file-backed interface first;
- interaction receipts are route memory, not owner lifecycle mutation;
- promotion remains deferred.

Validation:

- source artifacts reviewed;
- dispatch artifacts already validate;
- watchpoints converted into hard gates.

Next step: proceed to `CRAFT-INTERFACE-001`.
