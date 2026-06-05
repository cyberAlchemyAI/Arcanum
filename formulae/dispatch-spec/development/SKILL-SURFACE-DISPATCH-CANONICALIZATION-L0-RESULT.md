---
module: skill-surface-dispatch-canonicalization
version: current
status: pass
updatedAt: 2026-06-03
docType: task-session-result
task: SWU-DISP-SURF-001
runId: arcanum-hook-019e8eaf-7a7f-70b0-8836-01817a70b084
---

# Task Session Result: SWU-DISP-SURF-001

## Verdict

`PASS`: the installed dispatch-spec gap is classified. Canonical dispatch-spec source is present and valid; the failing live installed skill surface is stale/thin alias state that points to removed `arcanum-*` packages.

## Findings

| Finding | Evidence | Classification |
| --- | --- | --- |
| Canonical dispatch-spec source exists. | `formulae/dispatch-spec/dispatch.schema.yml`, `formulae/dispatch-spec/TECHNIQUE-CATALOG.md`, and `formulae/dispatch-spec/scripts/validate-dispatch.py` are present. | canonical-source-present |
| Canonical validator works for the refine fixture. | `python3 formulae/dispatch-spec/scripts/validate-dispatch.py formulae/dispatch-spec/development/fixtures/pass-refine-dispatch.json --json` returned `validation=pass`. | canonical-validator-pass |
| Installed `dispatch-spec` is a thin alias. | `/mnt/c/Users/vlad_/.codex/skills/dispatch-spec/SKILL.md` says to use `arcanum-dispatch-spec`. | live-install-drift |
| Installed `refine` is a thin alias. | `/mnt/c/Users/vlad_/.codex/skills/refine/SKILL.md` says to use `arcanum-refine`. | live-install-drift |
| Installed `invoke` is a thin alias. | `/mnt/c/Users/vlad_/.codex/skills/invoke/SKILL.md` says to use `arcanum-invoke`. | live-install-drift |
| The referenced prefixed packages are absent. | `find /mnt/c/Users/vlad_/.codex/skills -maxdepth 1 -type d -name 'arcanum-dispatch-spec' -o ...` returned no matching package directories. | broken-alias-target |
| The issue likely affects many personal aliases. | Personal skill home has 45 `SKILL.md` files; `rg` found many descriptions of the form `Alias package for arcanum-*`. | broader-live-refresh-needed |
| Current generator source appears newer than live install. | `tools/bootstrap_arcanum.sh` writes full generated skill files to visible names by default and writes prefixed aliases only when `--prefixed-skill-packages` is set. | generator-likely-fixed |

## Root Cause

The failure is not that `dispatch-spec` lacks canonical files. The failure is a stale live install state: alias packages in `/mnt/c/Users/vlad_/.codex/skills` are thin pointers to prefixed `arcanum-*` packages that are no longer present after duplicate cleanup.

The `.agents/formulae/dispatch-spec/*` message is a downstream symptom of runtime/package fallback behavior after the installed alias cannot provide a self-contained canonical contract.

## Recommended Fix

Proceed to `SWU-DISP-SURF-004` style staged install validation before live mutation:

1. Generate a fresh staged personal install from current `tools/bootstrap_arcanum.sh`.
2. Confirm visible packages such as `refine`, `invoke`, and `dispatch-spec` contain full canonical content, not thin alias text.
3. Confirm staged `dispatch-spec` can locate or carry `dispatch.schema.yml`, `TECHNIQUE-CATALOG.md`, and validator instructions.
4. Only after staged proof, run the approved live refresh task for `/mnt/c/Users/vlad_/.codex/skills`.

Because the current generator already appears to write full visible packages by default, `SWU-DISP-SURF-003` may be reduced to a no-op confirmation unless staged install exposes a Formulae support-copy gap.

## Commands Run

```bash
find /mnt/c/Users/vlad_/.codex/skills -maxdepth 2 \( -path '*/refine/SKILL.md' -o -path '*/invoke/SKILL.md' -o -path '*/dispatch-spec/SKILL.md' -o -path '*/arcanum-dispatch-spec/SKILL.md' -o -path '*/arcanum-refine/SKILL.md' \) -print
sed -n '1,220p' /mnt/c/Users/vlad_/.codex/skills/dispatch-spec/SKILL.md
sed -n '1,220p' /mnt/c/Users/vlad_/.codex/skills/refine/SKILL.md
sed -n '1,220p' /mnt/c/Users/vlad_/.codex/skills/invoke/SKILL.md
rg -n "\.agents/formulae|dispatch\.schema\.yml|TECHNIQUE-CATALOG" /mnt/c/Users/vlad_/.codex/skills .agents tools formulae arcana spells
test -f formulae/dispatch-spec/dispatch.schema.yml
test -f formulae/dispatch-spec/TECHNIQUE-CATALOG.md
test -x formulae/dispatch-spec/scripts/validate-dispatch.py
python3 formulae/dispatch-spec/scripts/validate-dispatch.py formulae/dispatch-spec/development/fixtures/pass-refine-dispatch.json --json
rg -n "write_generated_alias_skill|write_generated_skill_file|alias_of|Alias package|prefixed|surface_kind" tools/bootstrap_arcanum.sh
```

## Validation

| Check | Result |
| --- | --- |
| Canonical schema exists | pass |
| Canonical technique catalog exists | pass |
| Canonical validator exists | pass |
| Refine fixture validates | pass |
| Installed alias target packages exist | block, but classified as live-install drift |
| L0 mutation boundary preserved | pass |

## Synchronization

- Context pack: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-L0-CONTEXT.md`
- Work-pack synchronized: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-WORK-PACK.md`
- Generator and live installs not mutated.

## Follow-Up

1. Run staged install validation from `TASK-DISP-SURF-004`.
2. If staged install proves current generator output is correct, request approval for `TASK-DISP-SURF-005` live refresh.
3. If staged install still produces thin aliases or misses Formulae support files, execute `TASK-DISP-SURF-003` before live refresh.
