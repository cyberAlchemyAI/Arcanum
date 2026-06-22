# Validation Experiment

This experiment validates the candidate package without private examples or
runtime registration.

## Hypothesis

A shell-first fixture runner can validate the `VERIFICATION-WEAVE` parent
receipt contract, positive synthetic fixtures, and twelve negative controls
without needing TypeScript or owner-runtime execution.

## Fixture Families

- `spec-derivation-basic`
- `frontend-ux-seed-flag`
- `execution-repeatability-basic`
- `architecture-gap-basic`
- `research-evidence-basic`
- `mixed-target-split`

## Negative Controls

The negative-control fixtures cover:

- mixed target without complete child routing;
- unsupported target;
- public-safety failure;
- generated run artifact as authority;
- missing oracle;
- UX human comprehension residue;
- dense expert UI false positive;
- flaky evidence;
- adapter failure;
- research dry-run promotion attempt;
- architecture folder-only inference;
- parent promotion attempt.

## Method

Run:

```sh
bash arcanum/arcana/verification-weaver/development/run-validation-fixtures.sh
```

The runner checks:

- required files exist;
- receipt type and schema version;
- target kind enumeration;
- owner lane references;
- status and promotion enumeration;
- expected pass, flag, or block outcome;
- public-safety fields;
- negative-control-specific assertions.

## Evidence Status

The experiment proves candidate contract behavior only. It does not register
the package, promote the package, or replace owner-lane validation.

## Residue

- Add richer structured parsing if the receipt schema grows beyond the current
  simple YAML profile.
- Run `sigil-development` review before any registry exposure.
- Run `experiment-harness` calibration with more realistic command adapters
  before treating execution evidence as stable.
