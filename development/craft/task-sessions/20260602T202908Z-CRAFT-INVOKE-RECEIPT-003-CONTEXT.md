# Context Pack: CRAFT-INVOKE-RECEIPT-003

## Identity

| Field | Value |
| --- | --- |
| task | CRAFT-INVOKE-RECEIPT-003 |
| mode | lean |
| work-pack | `development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md` |
| run folder | `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof` |
| strict coverage | pass |

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Validate `receipts/02-invoke-define.json`. | Covered by receipt JSON and artifact path checks. |
| O2 | Re-evaluate current run evidence through local skill/artifact review only. | Covered by refresh report, shared context, task contract, and local evidence files. |
| O3 | Update `evidence-index.json`, `RUN-MANIFEST.md`, and `RESULT.md` so Invoke Define is receipt-backed. | Covered by task write scope and run evidence. |
| O4 | Identify first remaining non-pass stage. | Covered by stage evidence order in `evidence-index.json`. |
| O5 | Sync README, SESSION-LEDGER, and work-pack status. | Covered by task write scope. |
| O6 | Preserve Craft promotion deferral and avoid command-surface routing. | Covered by refresh report, README/ledger guardrails, and task implementation detail. |

## Selected Evidence

| Source | Selectors | Obligation |
| --- | --- | --- |
| `work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-003.md` | Objective, write scope, implementation detail, done criteria, validation | O1-O6 |
| `CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md` | Task status board, SWU handoff, gate checks | O2, O5, O6 |
| `CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-REFRESH-REPORT.md` | Applied changes and boundaries | O2, O6 |
| `receipts/02-invoke-define.json` | `status=pass`, `evidence_kind=receipt`, artifact paths, blockers | O1, O3 |
| `invoke-define/RESULT.md` | Define-stage owner artifact and native output boundary | O1, O3 |
| `evidence-index.json` | Stage order and existing first blocker | O3, O4 |
| `RUN-MANIFEST.md` and `RESULT.md` | Existing stage evidence tables | O3 |
| `README.md` and `SESSION-LEDGER.md` | Current verdict, next move, promotion boundary | O5, O6 |

## Constraints

- Use local skill/artifact review only.
- Do not call `tools/arcanum`, `.codex/commands`, or generated resume commands for this active workflow.
- Do not promote Craft.
- Do not mutate canonical registry, runtime, sigil, spell, or command surfaces.
- Do not execute downstream owner stages in this task.

## Gate Verdict

Gate status: pass.

The receipt exists, validates as JSON, cites an existing owner-stage artifact, and the task has bounded write scope and validation. No blocker-level human decision is required.
