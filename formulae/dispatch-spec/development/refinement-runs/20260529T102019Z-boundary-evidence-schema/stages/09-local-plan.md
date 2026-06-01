# Local Plan: Implement Boundary Evidence Schema

Status: flag
Owner: refine fallback synthesis
Reason: `invoke plan` command surface resolved, but semantic execution used dry-run evidence only.

## Non-Executed Plan

### Task 1: Rename Technique Family

Files:

- `formulae/dispatch-spec/TECHNIQUE-CATALOG.md`
- `formulae/dispatch-spec/README.md`
- `formulae/dispatch-spec/ARCANUM-DISPATCH-SYNTHESIS.md`

Edits:

- Replace `Runtime Bridge And Evidence Techniques` with
  `Boundary And Evidence Techniques`.
- Remove Tandem-specific motivation language.
- Replace runtime-specific phrasing with cross-capability boundary language.
- Rename technique ids according to the repaired family.

Validation:

- `rg -n "Tandem|runtime adapter|Runtime Bridge" formulae/dispatch-spec`
  should show no canonical docs hits except historical development artifacts.

### Task 2: Add Schema Shape

File:

- `formulae/dispatch-spec/dispatch.schema.json`

Edits:

- Add optional `boundary_evidence`.
- Add `$defs` for `boundary`, `authority_map`, `receipt_expectation`,
  `state_namespace`, and `promotion_split`.
- Keep `additionalProperties: true` for early iteration where appropriate.

Validation:

- `python3 -m json.tool formulae/dispatch-spec/dispatch.schema.json`

### Task 3: Add Validator Rules

File:

- `formulae/dispatch-spec/scripts/validate-dispatch.py`

Rules:

- Known boundary/evidence techniques should flag if `boundary_evidence` is
  absent.
- `boundaries[].applies_to_steps` must reference known step ids.
- `state_namespace_boundary` should require at least one state namespace.
- `memory_promotion_split` should require at least one promotion split.
- Promotion split violations should block when execution evidence claims direct
  canonical promotion.

### Task 4: Add Fixtures

Files:

- `formulae/dispatch-spec/development/fixtures/pass-boundary-evidence.json`
- `formulae/dispatch-spec/development/fixtures/flag-boundary-technique-no-schema.json`
- `formulae/dispatch-spec/development/fixtures/block-boundary-unknown-step.json`
- `formulae/dispatch-spec/development/fixtures/block-promotion-split-violation.json`

Validation:

- `formulae/dispatch-spec/development/run-validation-fixtures.sh`

### Task 5: Update Documentation Examples

Files:

- `formulae/dispatch-spec/README.md`
- `formulae/dispatch-spec/ARCANUM-DISPATCH-SYNTHESIS.md`

Edits:

- Show a minimal `boundary_evidence` block.
- Explain that dispatch validates boundary claims, not execution.
- Keep Task Session as the execution owner for implementation work.

## Stop Conditions

- Stop if schema changes make existing fixtures fail unexpectedly.
- Stop if validator rules over-block dispatches without execution boundaries.
- Stop if wording reintroduces Tandem/runtime-specific ownership.

## Recommended Next Route

Run `task-session` on this plan after review.
