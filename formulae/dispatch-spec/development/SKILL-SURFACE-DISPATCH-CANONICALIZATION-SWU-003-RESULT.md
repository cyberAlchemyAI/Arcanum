---
module: skill-surface-dispatch-canonicalization
version: current
status: pass
updatedAt: 2026-06-03
docType: task-session-result
task: SWU-DISP-SURF-003
runId: arcanum-hook-019e8ee4-da45-7803-b9a0-97f4bd047ab8
---

# Task Session Result: SWU-DISP-SURF-003

## Verdict

`PASS`: generated dispatch-spec packages are now self-sufficient for the required deterministic validation assets in staged personal and repo installs.

## Changes

| File | Change |
| --- | --- |
| `tools/bootstrap_arcanum.sh` | `copy_generated_skill_support` now copies adjacent package support files when present: `README.md`, `TECHNIQUE-CATALOG.md`, `dispatch.schema.yml`, `dispatch.schema.yaml`, and `dispatch.schema.json`. |
| `formulae/dispatch-spec/scripts/validate-dispatch.py` | Validator now prefers the local package directory when `dispatch.schema.yml` exists beside the generated package, and falls back to the repository `formulae/dispatch-spec` path for canonical in-repo use. |

## Validation

| Check | Result |
| --- | --- |
| `bash -n tools/bootstrap_arcanum.sh` | pass |
| Repo canonical validator on `pass-refine-dispatch.json` | pass |
| Staged personal install generated visible `dispatch-spec`, `refine`, `invoke`, and `orchestrate` packages only | pass |
| Staged repo install generated visible `dispatch-spec`, `refine`, `invoke`, and `orchestrate` packages only | pass |
| Staged personal `dispatch-spec` package contains `dispatch.schema.yml` and `TECHNIQUE-CATALOG.md` | pass |
| Staged repo `dispatch-spec` package contains `dispatch.schema.yml` and `TECHNIQUE-CATALOG.md` | pass |
| Staged personal generated validator validates `pass-refine-dispatch.json` | pass |
| Staged repo generated validator validates `pass-refine-dispatch.json` | pass |

## Commands Run

```bash
bash -n tools/bootstrap_arcanum.sh
python3 formulae/dispatch-spec/scripts/validate-dispatch.py formulae/dispatch-spec/development/fixtures/pass-refine-dispatch.json --json
rm -rf /tmp/arcanum-dispatch-surface-personal
bash tools/bootstrap_arcanum.sh --profile personal-codex --codex-home /tmp/arcanum-dispatch-surface-personal/.codex --sigils dispatch-spec,refine --spells invoke --force
/tmp/arcanum-dispatch-surface-personal/.codex/skills/dispatch-spec/scripts/validate-dispatch.py formulae/dispatch-spec/development/fixtures/pass-refine-dispatch.json --json
rm -rf /tmp/arcanum-dispatch-surface-repo
bash tools/bootstrap_arcanum.sh --target /tmp/arcanum-dispatch-surface-repo --profile repo-codex,repo-local --sigils dispatch-spec,refine --spells invoke --force
/tmp/arcanum-dispatch-surface-repo/.agents/skills/dispatch-spec/scripts/validate-dispatch.py formulae/dispatch-spec/development/fixtures/pass-refine-dispatch.json --json
find /tmp/arcanum-dispatch-surface-personal/.codex/skills -maxdepth 2 -name SKILL.md -print
find /tmp/arcanum-dispatch-surface-repo/.agents/skills -maxdepth 2 -name SKILL.md -print
```

## Notes

- The staged packages do not require `.codex/commands`.
- The active generated `SKILL.md` files are full visible packages, not thin aliases to absent `arcanum-*` packages.
- Existing generator behavior still copies the source `development/` directory for generated skills. That means historical evidence can appear inside staged packages. It did not block this SWU because the active package files and validator are correct, but a later hygiene task may want a tighter generated-package support policy.
- Live personal skill refresh remains blocked pending explicit approval.

## Synchronization

- Context pack: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-SWU-003-CONTEXT.md`
- Work-pack synchronized: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-WORK-PACK.md`
- Live installs not mutated.

## Follow-Up

1. `SWU-DISP-SURF-004` can now record full staged install validation as complete or near-complete using the evidence from this task.
2. `SWU-DISP-SURF-005` remains blocked until explicit approval to mutate `/mnt/c/Users/vlad_/.codex/skills`.
3. Consider a future support-copy hygiene task to exclude generated task-session evidence from installed packages while preserving required schemas, catalogs, scripts, templates, examples, and assets.
