---
module: skill-surface-dispatch-canonicalization
version: current
status: context-pack
updatedAt: 2026-06-03
docType: task-session-context
task: SWU-DISP-SURF-003
runId: arcanum-hook-019e8ee4-da45-7803-b9a0-97f4bd047ab8
---

# Context Pack: SWU-DISP-SURF-003

## Task

Fix generated dispatch-spec package dependency resolution so staged generated packages are canonical or self-sufficient.

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Treat `dispatch-spec` as canonical Formulae source, not a hidden `.agents/formulae` dependency. | covered |
| O2 | Generated `dispatch-spec/SKILL.md` must be usable without `.codex/commands`. | covered |
| O3 | Generated package must carry or resolve `dispatch.schema.yml`, `TECHNIQUE-CATALOG.md`, and validator instructions. | covered |
| O4 | Keep copied assets minimal and avoid copying unrelated Arcanum internals. | covered with follow-up note |
| O5 | Validate staged personal and repo packages before live refresh. | covered |

## Selected Evidence

| Source | Selectors | Obligations | Why Included |
| --- | --- | --- | --- |
| `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-WORK-PACK.md` | `TASK-DISP-SURF-003`, `SWU-DISP-SURF-003`, validation commands | O1-O5 | Defines task scope, write scope, done criteria, and validation surface. |
| `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-L0-RESULT.md` | Root cause and recommended fix | O1, O5 | Establishes live install drift and points to staged proof before live refresh. |
| `tools/bootstrap_arcanum.sh` | `copy_generated_skill_support`, `write_generated_skill_file`, `write_runtime_skill_packages` | O2-O4 | Generator owns package contents for personal and repo Codex skills. |
| `formulae/dispatch-spec/scripts/validate-dispatch.py` | package path constants | O3 | Validator must work both from repo canonical package and generated package copy. |
| `/tmp/arcanum-dispatch-surface-personal/.codex/skills/dispatch-spec/` | generated package file list and validator smoke | O2-O5 | Proves personal staged package has schema/catalog and validates a dispatch fixture. |
| `/tmp/arcanum-dispatch-surface-repo/.agents/skills/dispatch-spec/` | generated package file list and validator smoke | O2-O5 | Proves repo staged package has schema/catalog and validates a dispatch fixture. |

## Excluded Candidates

| Source | Reason |
| --- | --- |
| `/mnt/c/Users/vlad_/.codex/skills` | Live personal skill home is out of scope until staged proof and explicit approval. |
| `.codex/commands/*` | Legacy command adapters are not needed for native skill package dependency resolution. |
| Active skill-contract wording migration | Belongs to `SWU-DISP-SURF-002`, not this generator/package task. |

## Context Builder Summary

- Mode: lean
- Files selected: 6
- Snippets selected: 6
- Obligation coverage: 100%
- Noise ratio: low
- Handoff pack: none
- Strict coverage: pass
- Blockers: 0

## Constraints

- Do not refresh live `$CODEX_HOME` packages.
- Keep generator changes scoped to generated package support files and validator portability.
- Preserve repo-root validator behavior.
- Do not make `.codex/commands/` a prerequisite for validation.

## Next Action

Patch generator support-file copying and validator local-package path resolution, then record staged install validation.
