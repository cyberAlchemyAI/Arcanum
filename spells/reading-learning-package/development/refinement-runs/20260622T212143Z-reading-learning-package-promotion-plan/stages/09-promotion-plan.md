# Stage 09: Non-Executed Promotion Plan

Status: pass
Owner: `invoke`
Mode: plan

## Objective

Promote `reading-learning-package` to a discoverable library spell without
changing source authority or adding new runtime features.

## Work Units

| ID | Work Unit | Write Scope | Acceptance Evidence |
| --- | --- | --- | --- |
| RLP-PROMO-001 | Add registry row. | `arcanum/registry/SPELLS.md` | Registry link resolves and row names purpose, composed capabilities, use-when text. |
| RLP-PROMO-002 | Prove bootstrap resolution. | temporary target outside repo or ignored output | Generated spell package has correct metadata and contract content. |
| RLP-PROMO-003 | Sync generated mirrors if required. | Standard generated runtime surfaces only | Diff matches bootstrap output; no unrelated mirror churn. |
| RLP-PROMO-004 | Rerun validation bundle. | spell validation results and receipt | Commands pass or expected renderer flag is recorded. |
| RLP-PROMO-005 | Add promotion receipt. | `arcanum/spells/reading-learning-package/development/` | Receipt links Spellcraft, fixture, registry, bootstrap, boundary, and publication evidence. |
| RLP-PROMO-006 | Publish public submodule. | `arcanum` git repo | Commit pushed to `origin/main` or current tracked branch. |
| RLP-PROMO-007 | Publish parent gitlink. | parent repo gitlink only | `make bump-check` passes and parent commit points at pushed submodule commit. |

## Verification Commands

```bash
python3 -m py_compile \
  arcanum/spells/reading-learning-package/runtime/reading_learning_package.py \
  arcanum/spells/reading-learning-package/validation/run-fixtures.py

python3 arcanum/spells/reading-learning-package/validation/run-fixtures.py

python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py \
  arcanum/spells/reading-learning-package/development/reading-learning-package.dispatch.json

python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py \
  arcanum/spells/reading-learning-package/development/refinement-runs/20260622T212143Z-reading-learning-package-promotion-plan/REFINE-DISPATCH.json

python3 -m json.tool \
  arcanum/spells/reading-learning-package/runtime/presets.json

python3 -m json.tool \
  arcanum/spells/reading-learning-package/runtime/preset-profile.schema.json

find arcanum/spells/reading-learning-package -name '*.md' -print0 |
  xargs -0 -n1 bash tools/check_markdown_links.sh

bash tools/check_markdown_links.sh arcanum/registry/SPELLS.md

git -C arcanum diff --check -- spells/reading-learning-package registry
```

## Stop Conditions

- Stop if bootstrap cannot resolve `reading-learning-package`.
- Stop if validation output implies generated learning artifacts are canonical
  source evidence.
- Stop if generated mirror diffs include unrelated capabilities.
- Stop if `arcanum` cannot be pushed before parent gitlink publication.

## Recommended Next Route

`spellcraft` promotion execution, then submodule-first publish.

