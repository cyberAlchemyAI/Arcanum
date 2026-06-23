# Reading Learning Package Promotion Receipt

Date: 2026-06-22
Owner: `spellcraft`
Canonical id: `reading-learning-package`
Scope: reusable library spell
Status: promoted-local

## Promotion Evidence

| Evidence | Result | Notes |
| --- | --- | --- |
| Spell contract | pass | `README.md` defines aliases, purpose, triggers, required and optional sigils, prerequisites, shared state, phases, handoffs, gates, failure policy, customization, observability, experiment harness, and output contract. |
| Registry entry | pass | `registry/SPELLS.md` lists `Reading Learning Package` with no aliases. |
| Fixture suite | pass | `validation/results/fixture-report.md` covers `deep_voice_reading`, `quick_video`, `medium_explanation`, and missing-source block behavior. |
| Dispatch route | pass | `development/reading-learning-package.dispatch.json` validates through `dispatch-spec`. |
| Refine promotion plan | pass | `development/refinement-runs/20260622T212143Z-reading-learning-package-promotion-plan/RESULT.md` selected the registry, generated surface, receipt, and publication path. |
| Generated surface resolution | pass | Temporary bootstrap generation produced repo Codex and Claude packages with `canonical_source: spells/reading-learning-package/README.md`. |
| Public boundary | pass | Source authority remains in `research-tower`; composition authority remains in `whisper`; generated learning artifacts are not promoted as tower evidence. |

## Bootstrap Proof

Validated command:

```bash
bash arcanum/tools/bootstrap_arcanum.sh \
  --target <tmp-target> \
  --sigils "" \
  --spells reading-learning-package \
  --profile repo-codex,claude \
  --force
```

Generated surfaces:

- `.agents/skills/reading-learning-package/SKILL.md`
- `.claude/skills/reading-learning-package/SKILL.md`

The help text advertises `--sigils none`, but this script currently treats
`none` as a sigil id. The validated spell-only invocation uses an empty sigil
selection: `--sigils ""`.

## Runtime Mirror Sync

Repo-local generated mirrors were synchronized from the validated temporary
bootstrap output:

- `.agents/skills/reading-learning-package/`
- `.claude/skills/reading-learning-package/`

The parent bootstrap was not run with `--force` because that broader path would
also rewrite existing generated `orchestrate` front doors. The synced packages
therefore remain direct products of the validated bootstrap output while keeping
the mutation boundary limited to this promoted spell.

## Publication Gate

This receipt does not claim publication. To publish:

1. Commit and push the public `arcanum` submodule changes first.
2. Run parent `make bump-check`.
3. Commit and push the parent gitlink only after the public submodule commit is
   pushed.

## Validation Commands

```bash
python3 -m py_compile \
  arcanum/spells/reading-learning-package/runtime/reading_learning_package.py \
  arcanum/spells/reading-learning-package/validation/run-fixtures.py
python3 arcanum/spells/reading-learning-package/validation/run-fixtures.py
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py \
  arcanum/spells/reading-learning-package/development/reading-learning-package.dispatch.json
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py \
  arcanum/spells/reading-learning-package/development/refinement-runs/20260622T212143Z-reading-learning-package-promotion-plan/REFINE-DISPATCH.json
python3 -m json.tool arcanum/spells/reading-learning-package/runtime/presets.json
python3 -m json.tool arcanum/spells/reading-learning-package/runtime/preset-profile.schema.json
bash tools/check_markdown_links.sh arcanum/registry/SPELLS.md
git -C arcanum diff --check -- spells/reading-learning-package registry
```
