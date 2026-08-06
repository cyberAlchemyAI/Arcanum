# Work Pack: Work-Pack Execution Grant

## Control fields

- Work Pack ID: `WP-WPEG-20260804`
- Target: `implementation-readiness` plan-to-execution composition
- Complexity: high
- Output mode: split
- Authority effect: none; authored implementation plan
- Current state: candidate-local prototype complete; lifecycle reconciliation deferred
- Selected SWU: none
- Recommended first SWU: none; captured frontier complete
- Next lifecycle owner: `invoke:refresh` for post-prototype reconciliation

## Objective

Replace repeated per-tool/per-owner authorization prompts with one bounded
Work-Pack execution intent and continue declared routes until the frontier is
complete or a real blocker appears.

## Source artifacts

- `SPEC.md`
- `architecture-bundle.md`
- `IMPLEMENTATION-LAYERING.md`
- `IMPLEMENTATION-PLAN.md`
- `PLAN-DISTILL-VALIDATION.md`
- `execution-pack.md`
- `work-pack/shared/SWU-MANIFEST.json`

## Execution policy for this Work Pack

This authored package did not itself authorize implementation. The user's
direct execution instruction selected the bounded Candidate-Local Prototype
Fast Lane, which completed all eight SWUs. Internal tools and declared owner
routes were automatic; stop classes remained those in `SPEC.md`.

## SWU sequence

| SWU | Parent task | Primary behavior | Dependencies | Successor |
| --- | --- | --- | --- | --- |
| `SWU-WPEG-001` | `TASK-WPEG-CONTRACT` | validate execution policy, entry projection, and intent binding | none | 002 |
| `SWU-WPEG-002` | `TASK-WPEG-CONTRACT` | emit one consistent Plan execution-entry state | 001 | 003 |
| `SWU-WPEG-003` | `TASK-WPEG-ROUTER` | admit Work-Pack-bound owner hops without per-route authorization | 002 | 004 |
| `SWU-WPEG-004` | `TASK-WPEG-ROUTER` | implement the Implementation Readiness outer loop | 003 | 005 |
| `SWU-WPEG-005` | `TASK-WPEG-TASK-SESSION` | classify prerequisites before deep Task Session context | 004 | 006 |
| `SWU-WPEG-006` | `TASK-WPEG-TASK-SESSION` | resume through a fresh Task Session after an owner hop | 005 | 007 |
| `SWU-WPEG-007` | `TASK-WPEG-INTEGRATION` | prove the direct-intent route and stop boundaries end to end | 006 | 008 |
| `SWU-WPEG-008` | `TASK-WPEG-INTEGRATION` | sync generated packages, docs, and observability | 007 | none |

## Task documents

- `work-pack/tasks/TASK-WPEG-CONTRACT.md`
- `work-pack/tasks/TASK-WPEG-ROUTER.md`
- `work-pack/tasks/TASK-WPEG-TASK-SESSION.md`
- `work-pack/tasks/TASK-WPEG-INTEGRATION.md`

## Global acceptance

- One direct Work Pack execution request is sufficient for all declared,
  in-scope, repository-local internal tool/capability hops.
- No `--authorize-route` is required for a route matched to the current Work
  Pack binding.
- Route matching includes exact capability, mode, target, write scope, effect
  class, required inputs, expected receipt, frontier, and route digest.
- Entry classification precedes deep Context Builder work.
- Expected selected-unit material absence uses plan-once admission, not a
  pre-execution Refresh.
- Real semantic drift routes to Invoke Refresh and rejoins the outer loop.
- Task Session mutation gates remain exact and single-use.
- Series execution uses fresh one-unit Task Sessions and finite frontier state.
- Stop-class decisions halt before effects.
- Undeclared routes, expanded targets/writes, stale bindings, and repeated
  fingerprints block before dispatch.
- A typed repairable owner condition may retry the unchanged declared route
  once within the normal step budget; a second retry blocks before dispatch.
- Public fixtures and generated packages pass parity checks.

## Closeout contract

Each implementation SWU must return:

- exact source and generated paths changed;
- pre-mutation baselines for every existing target;
- validation commands and results;
- owner lifecycle receipt;
- no-scope-expansion statement;
- residue and exact successor;
- a closeout projection that does not execute the successor.

## Current blockers

No design blocker remains. Implementation is intentionally unselected. The
current Arcanum worktree contains unrelated pending changes, so every later SWU
must inventory overlap before mutation and preserve existing work.
