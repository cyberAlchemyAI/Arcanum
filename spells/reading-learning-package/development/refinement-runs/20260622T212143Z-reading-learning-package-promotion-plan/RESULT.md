# Refine Result: Reading Learning Package Promotion

## Status

`pass`

## Desired Outcome

Finish the `reading-learning-package` goal by promoting the reusable candidate
into a discoverable library spell with registry entry, generated runtime surface
validation, public-safe evidence, and submodule-first publication.

## Current Finding

The implementation goal is functionally finished, but promotion execution is not
finished. The remaining gap is release governance:

- `arcanum/registry/SPELLS.md` does not yet list `Reading Learning Package`;
- generated native runtime mirrors for the promoted spell have not been
  validated or synchronized as a promotion receipt;
- no promotion receipt ties Spellcraft validation, experiment fixture evidence,
  registry discoverability, and publication gates into one final record;
- no submodule-first commit/push sequence has been run for this promotion.

## Selected Strategy

Use a confirmation-gated Refine route with these overlays:

- `baseline_sequence`: preserve the ten-stage refinement loop and keep artifacts
  ordered.
- `promotion_gate_for_spell_candidate`: treat registry, runtime surfaces,
  validation receipts, and publication gates as promotion requirements.
- `state_namespace_boundary`: keep public `arcanum`, private parent gitlink,
  generated runtime mirrors, and generated learning outputs separate.

## Final Promotion Plan

1. Confirm the promotion scope.
2. Add `Reading Learning Package` to `arcanum/registry/SPELLS.md` with:
   - aliases: none unless the maintainer explicitly wants a short alias;
   - purpose: compose reader-facing learning packages from completed
     `research-tower` output through a Whisper-compatible substrate;
   - composed sigils/spells: `research-tower`, `whisper`,
     `experiment-harness`, `task-session` as optional downstream route;
   - use-when: a completed tower should become a readable learning package with
     source trace and HTML/PDF fallback.
3. Validate spell resolution through a temporary target, for example:
   - `bash arcanum/tools/bootstrap_arcanum.sh --target <tmp> --sigils none --spells reading-learning-package --profile repo-codex,claude --force`
   - inspect the temporary generated skill package for correct
     `canonical_source`, runtime, name, and README content.
4. Synchronize generated mirrors only for standard repository profiles proven by
   the temporary-target validation.
5. Re-run validation:
   - `python3 -m py_compile arcanum/spells/reading-learning-package/runtime/reading_learning_package.py arcanum/spells/reading-learning-package/validation/run-fixtures.py`
   - `python3 arcanum/spells/reading-learning-package/validation/run-fixtures.py`
   - `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py arcanum/spells/reading-learning-package/development/reading-learning-package.dispatch.json`
   - `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py arcanum/spells/reading-learning-package/development/refinement-runs/20260622T212143Z-reading-learning-package-promotion-plan/REFINE-DISPATCH.json`
   - markdown-link checks for the spell package, registry, and promotion
     receipt
   - JSON parse checks for runtime schemas and dispatch files
   - public-boundary scan for absolute private paths and private repo names
   - `git -C arcanum diff --check -- spells/reading-learning-package registry`
6. Add a final promotion receipt under
   `arcanum/spells/reading-learning-package/development/`.
7. Commit and push inside `arcanum` first.
8. From the parent repository, run `make bump-check`.
9. Commit and push the parent gitlink only after the `arcanum` commit is pushed.

## Deferred Work

- Deterministic PDF renderer integration remains optional future
  `task-session` work, because the current HTML fallback behavior is validated.
- Aliases such as `learning-pack` or `tower-to-learning-package` require a
  maintainer decision and are not part of the default promotion plan.
- External research is not needed for the promotion path.

## Recommended Next Route

Execute the promotion patch through `spellcraft`:

1. add the registry row;
2. validate bootstrap resolution;
3. synchronize generated mirrors only if the validated profile output requires
   them;
4. rerun validation;
5. add a promotion receipt;
6. commit and push `arcanum`;
7. run parent `make bump-check`;
8. commit and push the parent gitlink.

This Refine run does not claim the spell has been promoted. It produces the
promotion-ready plan and route evidence.

