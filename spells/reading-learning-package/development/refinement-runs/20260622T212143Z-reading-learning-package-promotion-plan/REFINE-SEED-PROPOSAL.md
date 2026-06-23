# Refine Seed Proposal: Reading Learning Package Promotion

## Target

- Target folder: `arcanum/spells/reading-learning-package/`
- Primary spell contract: `arcanum/spells/reading-learning-package/README.md`
- Promotion registry: `arcanum/registry/SPELLS.md`
- Current validation evidence:
  - `arcanum/spells/reading-learning-package/development/VALIDATION.md`
  - `arcanum/spells/reading-learning-package/development/VALIDATION-EXPERIMENT.md`
  - `arcanum/spells/reading-learning-package/validation/results/fixture-report.md`
  - `arcanum/spells/reading-learning-package/validation/results/implementation-report.md`

## Operator Intent

Refine a plan for finishing the goal and promoting `reading-learning-package`
from reusable spell candidate to discoverable promoted library spell.

## Current State

The implementation and Spellcraft candidate review are materially complete:

- the spell contract exists and names lifecycle, sigils, phases, gates,
  handoffs, observability, experiment harness evidence, and output contract;
- runtime fixtures pass for `deep_voice_reading`, `quick_video`,
  `medium_explanation`, and the missing-source block case;
- deterministic PDF renderer absence is treated as an explicit non-blocking
  renderer flag when HTML fallback exists;
- generated learning artifacts preserve the no-promotion boundary for source
  claims and tower vocabulary.

The remaining promotion work is not runtime implementation. It is release
governance: registry exposure, generated runtime surface synchronization,
validation receipts, public-boundary checks, and submodule-safe publication.

## Desired Outcome

A non-executed, confirmation-gated promotion plan that can be run after operator
approval and that keeps these boundaries:

- `research-tower` remains source authority;
- `whisper` remains composition authority;
- generated learning packages do not become canonical evidence;
- public `arcanum` changes are committed and pushed before the private parent
  gitlink;
- parent generated mirrors are synchronized only after the public submodule
  state is validated.

## Preset And Research Mode

- Preset: `standard`
- Research: `no-research`

Local repository evidence is enough for this promotion plan. External research
would add noise and cannot override repository promotion rules.

## Proposed Promotion Finish Line

1. Add `Reading Learning Package` to `arcanum/registry/SPELLS.md`.
2. Validate that `tools/bootstrap_arcanum.sh` can resolve and install
   `--spells reading-learning-package` into a temporary target.
3. Synchronize the generated native runtime mirrors selected by the repository's
   standard profiles, after a dry-run or temporary-target validation proves the
   expected file set.
4. Re-run the spell validation bundle:
   - `python3 -m py_compile ...`
   - `python3 arcanum/spells/reading-learning-package/validation/run-fixtures.py`
   - `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py ...`
   - markdown link checks for the spell package and registry row
   - JSON parse checks for runtime schemas and dispatch files
   - public/private boundary scan
   - `git -C arcanum diff --check -- spells/reading-learning-package registry`
5. Record a promotion receipt under the spell's development evidence.
6. Commit and push inside `arcanum` first.
7. Run parent `make bump-check`, then commit and push the parent gitlink only
   after the submodule commit is pushed.

## Planned Stage Configuration

The validated dispatch preserves Refine's ten-stage loop, but all runtime-backed
stages are `not_run` until the operator confirms. No subagents are needed for
the first promotion plan.

