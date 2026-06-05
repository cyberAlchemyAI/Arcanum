---
module: skill-surface-dispatch-canonicalization
version: current
status: context-pack
updatedAt: 2026-06-03
docType: task-session-context
task: SWU-DISP-SURF-001
runId: arcanum-hook-019e8eaf-7a7f-70b0-8836-01817a70b084
---

# Context Pack: SWU-DISP-SURF-001

## Task

Classify the installed dispatch-spec dependency gap before source or live-install mutation.

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Inspect installed `refine`, `invoke`, and `dispatch-spec` packages. | covered |
| O2 | Search installed and repo surfaces for `.agents/formulae/dispatch-spec`, `dispatch.schema.yml`, and `TECHNIQUE-CATALOG.md`. | covered |
| O3 | Confirm whether canonical dispatch-spec source files exist. | covered |
| O4 | Determine whether the package expects copied dependencies or should resolve repo canonical paths. | covered |
| O5 | Record one recommended fix without mutating generator or live installs. | covered |

## Selected Evidence

| Source | Selectors | Obligations | Why Included |
| --- | --- | --- | --- |
| `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-WORK-PACK.md` | `TASK-DISP-SURF-001`, `SWU-DISP-SURF-001`, validation commands | O1-O5 | Defines the selected task, write scope, done criteria, and validation surface. |
| `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-IMPLEMENTATION-LAYERING.md` | L0 row, guardrails | O4-O5 | Establishes that this layer should classify dependency drift before generator or live refresh mutation. |
| `/mnt/c/Users/vlad_/.codex/skills/refine/SKILL.md` | frontmatter and alias body | O1, O4 | Shows the installed `refine` package is a thin alias to `arcanum-refine`. |
| `/mnt/c/Users/vlad_/.codex/skills/invoke/SKILL.md` | frontmatter and alias body | O1, O4 | Shows the installed `invoke` package is a thin alias to `arcanum-invoke`. |
| `/mnt/c/Users/vlad_/.codex/skills/dispatch-spec/SKILL.md` | frontmatter and alias body | O1, O4 | Shows the installed `dispatch-spec` package is a thin alias to `arcanum-dispatch-spec`. |
| `formulae/dispatch-spec/dispatch.schema.yml` | file existence | O3 | Confirms canonical schema exists in the repo. |
| `formulae/dispatch-spec/TECHNIQUE-CATALOG.md` | file existence | O3 | Confirms canonical technique catalog exists in the repo. |
| `formulae/dispatch-spec/scripts/validate-dispatch.py` | executable file existence and fixture validation | O3 | Confirms canonical validator exists and can validate the refine fixture. |
| `tools/bootstrap_arcanum.sh` | `write_generated_skill_file`, `write_generated_alias_skill`, `write_runtime_skill_packages` | O4-O5 | Shows current generator writes full visible skill packages by default, while prefixed packages are optional aliases. |

## Excluded Candidates

| Source | Reason |
| --- | --- |
| `*/development/refinement-runs/*` | Historical evidence; not needed to classify the installed package drift. |
| `.codex/commands/*` backups | Legacy command adapters; not involved in the current missing `.agents/formulae/dispatch-spec` failure. |
| live `$CODEX_HOME` package mutation | Out of scope for L0 and blocked until staged proof plus approval. |

## Context Builder Summary

- Mode: lean
- Files selected: 9
- Snippets selected: 9
- Obligation coverage: 100%
- Noise ratio: low
- Handoff pack: none
- Strict coverage: pass
- Blockers: 0

## Constraints

- Do not mutate `/mnt/c/Users/vlad_/.codex/skills` in this SWU.
- Do not edit `tools/bootstrap_arcanum.sh` in this SWU.
- Do not treat `.agents/` as canonical source.
- Preserve historical evidence and exclude it from active blocker classification.

## Next Action

Write the L0 result report and synchronize `SWU-DISP-SURF-001` evidence in the work-pack.
