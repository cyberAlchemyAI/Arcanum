---
module: skill-surface-dispatch-canonicalization
version: current
status: context-pack
updatedAt: 2026-06-03
docType: task-session-context
task: SWU-DISP-SURF-004
runId: arcanum-hook-019e8f23-bfe0-7401-8587-20ce15a6b5db
---

# Context Pack: SWU-DISP-SURF-004

## Task

Validate staged personal and repo installs after generated dispatch-spec package dependency fixes.

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Generate a fresh personal Codex staged install. | covered |
| O2 | Generate a fresh repo Codex staged install. | covered |
| O3 | Verify generated `dispatch-spec` package assets or canonical resolver guidance. | covered |
| O4 | Run dispatch fixture validation from canonical repo package. | covered |
| O5 | Run generated package validator against `pass-refine-dispatch.json` from staged contexts. | covered |
| O6 | Preserve the no-live-refresh boundary. | covered |

## Selected Evidence

| Source | Selectors | Obligations | Why Included |
| --- | --- | --- | --- |
| `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-WORK-PACK.md` | `TASK-DISP-SURF-004`, `SWU-DISP-SURF-004`, validation commands | O1-O6 | Defines selected task, write scope, done criteria, and live-refresh blocker. |
| `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-SWU-003-RESULT.md` | Follow-up and validation evidence | O3-O5 | Establishes generator/validator fixes that this SWU validates formally. |
| `/tmp/arcanum-dispatch-surface-personal/.codex/skills/` | generated package list and dispatch-spec assets | O1, O3, O5 | Fresh personal staged install evidence. |
| `/tmp/arcanum-dispatch-surface-repo/.agents/skills/` | generated package list, dispatch-spec assets, resolver output | O2, O3, O5 | Fresh repo staged install evidence. |
| `formulae/dispatch-spec/development/run-validation-fixtures.sh` | full fixture suite output | O4 | Canonical dispatch-spec regression evidence. |

## Excluded Candidates

| Source | Reason |
| --- | --- |
| `/mnt/c/Users/vlad_/.codex/skills` | Live personal skill home remains blocked until explicit approval. |
| `tools/bootstrap_arcanum.sh` | Already changed by `SWU-DISP-SURF-003`; this SWU only validates staged output. |
| `formulae/dispatch-spec/scripts/validate-dispatch.py` | Already changed by `SWU-DISP-SURF-003`; this SWU only validates canonical and generated behavior. |

## Context Builder Summary

- Mode: lean
- Files selected: 5
- Snippets selected: 5
- Obligation coverage: 100%
- Noise ratio: low
- Handoff pack: none
- Strict coverage: pass
- Blockers: 0

## Constraints

- Do not mutate live `$CODEX_HOME`.
- Do not mutate generator or validator source in this SWU unless staged validation fails.
- Keep evidence under `formulae/dispatch-spec/development/`.

## Next Action

Write the staged install validation result and synchronize `SWU-DISP-SURF-004` in the work-pack.
