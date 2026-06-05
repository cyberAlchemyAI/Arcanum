---
module: skill-surface-dispatch-canonicalization
version: current
status: pass
updatedAt: 2026-06-03
docType: task-session-result
task: SWU-DISP-SURF-004
runId: arcanum-hook-019e8f23-bfe0-7401-8587-20ce15a6b5db
---

# Task Session Result: SWU-DISP-SURF-004

## Verdict

`PASS`: fresh staged personal and repo installs validate without missing `.agents/formulae/dispatch-spec` files, and generated `dispatch-spec` validators work from their installed package locations.

## Validation Matrix

| Check | Result |
| --- | --- |
| Fresh personal Codex staged install generated | pass |
| Fresh repo Codex staged install generated | pass |
| Personal staged packages are visible names: `dispatch-spec`, `invoke`, `orchestrate`, `refine` | pass |
| Repo staged packages are visible names: `dispatch-spec`, `invoke`, `orchestrate`, `refine` | pass |
| Personal `dispatch-spec` package includes `dispatch.schema.yml`, `TECHNIQUE-CATALOG.md`, and `scripts/validate-dispatch.py` | pass |
| Repo `dispatch-spec` package includes `dispatch.schema.yml`, `TECHNIQUE-CATALOG.md`, and `scripts/validate-dispatch.py` | pass |
| Personal generated validator validates `pass-refine-dispatch.json` | pass |
| Repo generated validator validates `pass-refine-dispatch.json` | pass |
| Canonical dispatch fixture suite passes | pass, ended with `DISPATCH_SPEC_VALIDATION=pass` |
| Staged repo resolver finds `dispatch-spec` and `refine` through `.agents/skills` | pass |
| Staged repo default adapter is `native-skill` | pass |
| Active staged `SKILL.md` bodies are not thin aliases to `arcanum-*` packages | pass |

## Commands Run

```bash
rm -rf /tmp/arcanum-dispatch-surface-personal /tmp/arcanum-dispatch-surface-repo
bash tools/bootstrap_arcanum.sh --profile personal-codex --codex-home /tmp/arcanum-dispatch-surface-personal/.codex --sigils dispatch-spec,refine --spells invoke --force
bash tools/bootstrap_arcanum.sh --target /tmp/arcanum-dispatch-surface-repo --profile repo-codex,repo-local --sigils dispatch-spec,refine --spells invoke --force
bash -n tools/bootstrap_arcanum.sh
python3 formulae/dispatch-spec/scripts/validate-dispatch.py formulae/dispatch-spec/development/fixtures/pass-refine-dispatch.json --json
find /tmp/arcanum-dispatch-surface-personal/.codex/skills -maxdepth 2 -name SKILL.md -print
find /tmp/arcanum-dispatch-surface-repo/.agents/skills -maxdepth 2 -name SKILL.md -print
test -f /tmp/arcanum-dispatch-surface-personal/.codex/skills/dispatch-spec/dispatch.schema.yml
test -f /tmp/arcanum-dispatch-surface-personal/.codex/skills/dispatch-spec/TECHNIQUE-CATALOG.md
test -f /tmp/arcanum-dispatch-surface-personal/.codex/skills/dispatch-spec/scripts/validate-dispatch.py
test -f /tmp/arcanum-dispatch-surface-repo/.agents/skills/dispatch-spec/dispatch.schema.yml
test -f /tmp/arcanum-dispatch-surface-repo/.agents/skills/dispatch-spec/TECHNIQUE-CATALOG.md
test -f /tmp/arcanum-dispatch-surface-repo/.agents/skills/dispatch-spec/scripts/validate-dispatch.py
/tmp/arcanum-dispatch-surface-personal/.codex/skills/dispatch-spec/scripts/validate-dispatch.py formulae/dispatch-spec/development/fixtures/pass-refine-dispatch.json --json
/tmp/arcanum-dispatch-surface-repo/.agents/skills/dispatch-spec/scripts/validate-dispatch.py formulae/dispatch-spec/development/fixtures/pass-refine-dispatch.json --json
formulae/dispatch-spec/development/run-validation-fixtures.sh
rg -n 'Alias package for arcanum-|Use the canonical generated package named `arcanum-' /tmp/arcanum-dispatch-surface-personal/.codex/skills/*/SKILL.md /tmp/arcanum-dispatch-surface-repo/.agents/skills/*/SKILL.md
/tmp/arcanum-dispatch-surface-repo/tools/arcanum --resolve dispatch-spec
/tmp/arcanum-dispatch-surface-repo/tools/arcanum --resolve refine
/tmp/arcanum-dispatch-surface-repo/tools/arcanum --get-default-adapter
```

## Notes

- No live personal Codex packages were changed.
- No `.codex/commands` surface is required by the staged packages.
- The generated `dispatch-spec` package carries the required deterministic validation assets.
- Staged package support still includes copied `development/` evidence because that is existing generator behavior; this is a possible future hygiene task, not a blocker for staged validation.

## Synchronization

- Context pack: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-SWU-004-CONTEXT.md`
- Work-pack synchronized: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-WORK-PACK.md`
- Live installs not mutated.

## Follow-Up

1. Execute `SWU-DISP-SURF-002` to remove command-surface invocation requirements from active skill contracts.
2. After `SWU-DISP-SURF-002` passes, request explicit approval before `SWU-DISP-SURF-005` mutates `/mnt/c/Users/vlad_/.codex/skills`.
