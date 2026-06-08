---
module: skill-surface-dispatch-canonicalization
version: current
status: block
updatedAt: 2026-06-05
docType: task-session-context
task: SWU-DISP-SURF-005
runId: arcanum-hook-019e9916-b93d-78e3-88b4-9e0448e9a5be
contextMode: lean
---

# Task Session Context: SWU-DISP-SURF-005

## Objective

Refresh live installed Codex packages only after explicit approval, using a backup-first process that preserves non-Arcanum and unknown packages.

## Selected Evidence

| Evidence | Selector | Obligation |
| --- | --- | --- |
| `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-WORK-PACK.md` | `TASK-DISP-SURF-005`, `SWU-DISP-SURF-005`, `B-DISP-SURF-001`, `G-DISP-SURF-004`, Recommended Next Route | Defines write scope, approval blocker, backup requirement, and post-refresh validation. |
| `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-SWU-002-RESULT.md` | Verdict, Remaining Hit Classification, Validation | Proves active skill contract migration completed before live refresh. |
| `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-SWU-004-RESULT.md` | Verdict, Validation Matrix, Notes | Proves staged generated packages validate without missing dispatch-spec dependency files. |
| `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-LIVE-REFRESH-DECISION.md` | Decision Needed, Options, Recommendation, Stop Condition | Records unresolved approval decision for machine-global skill mutation. |

## Obligation Coverage

| Obligation | Status | Evidence |
| --- | --- | --- |
| Dependencies complete before live refresh | covered | SWU-002 and SWU-004 result artifacts are `PASS`. |
| Write scope identified | covered | `/mnt/c/Users/vlad_/.codex/skills`, optional repo `.agents/skills`, and backup report path are listed in the work-pack. |
| Approval required before mutation | block | Work-pack and decision artifact both require explicit user approval. |
| Backup-first process required | covered | Work-pack step 1 requires timestamped backup of generated Arcanum packages being replaced. |
| Unknown/non-Arcanum packages preserved | covered | Work-pack and decision artifact require preserving non-Arcanum and unknown packages. |
| Validation surface identified | covered | Installed inventory and installed `refine`/`dispatch-spec` smoke are listed. |

## Gate Verdict

`BLOCK`: `G-DISP-SURF-004` requires explicit approval and backup manifest before live refresh. The current user message invoked `task-session` but did not explicitly approve Option A or Option B from the decision artifact.

## Strict Coverage

Strict coverage for a local mutation run is blocked by missing approval. Strict coverage for a blocker report is pass.
