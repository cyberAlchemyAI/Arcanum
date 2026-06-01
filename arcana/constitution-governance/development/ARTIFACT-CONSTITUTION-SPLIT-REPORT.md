# Artifact Constitution Split Report

Status: candidate
Task: CG-004
Date: 2026-05-27

## Question

Should the chart rendering rules remain in `framework/ARTIFACT-CONSTITUTION.md`, or should they move to a separate visual-artifact constitution?

## Current Artifact Constitution Shape

`framework/ARTIFACT-CONSTITUTION.md` currently governs:

- artifact classes,
- versioning and ignored-path policy,
- generated/runtime artifact boundaries,
- validation contract,
- chart/visual rendering rules.

The rendering rules are small and currently tied to the same validator as the artifact classification checks.

## Split Criteria

Split a constitution when at least one of these is true:

| Criterion | Current Result |
| --- | --- |
| The constitution has multiple unrelated owners. | Not yet. Artifact Constitution still owns source/generated/runtime artifact policy and rendering validation. |
| Selected task packs repeatedly need only one section and the full file becomes noisy. | Emerging, but the current composition pack solves this without moving files. |
| Validator ownership diverges. | Not yet. `tools/validate-artifact-constitution.sh` enforces both artifact visibility and chart line-break checks. |
| The rule family needs its own examples, fixtures, or promotion path. | Partially. Chart line-break self-test exists, but not enough to justify a new constitution yet. |
| Rules conflict with the parent constitution's scope. | No. Durable/source visual artifacts are still artifact governance. |
| The file becomes hard to scan or apply. | No. Rendering section is short. |

## Recommendation

Keep rendering rules in `framework/ARTIFACT-CONSTITUTION.md` for now.

Do not split yet. Instead, rely on Constitution Governance composition packs to select the relevant rendering rules for chart tasks.

## Rationale

The rendering rule is currently:

- short,
- artifact-form focused,
- enforced by the same validator,
- useful as part of the general artifact validation contract,
- not large enough to dilute the constitution.

A split would add a new file and precedence rule before there is evidence that the current constitution is too large or that visual artifact governance needs independent ownership.

## Future Split Trigger

Create `framework/VISUAL-ARTIFACT-CONSTITUTION.md` if at least two of these become true:

- there are five or more visual rendering rules,
- chart/presentation/HTML artifact tasks repeatedly select only rendering rules,
- rendering validation grows beyond `tools/validate-artifact-constitution.sh`,
- visual artifact rules need screenshot/export evidence,
- rendering rules conflict with another artifact constitution,
- reviewers report that Artifact Constitution is too broad to load effectively.

## Proposed Future Extraction

If split later, move:

- `Rendering Rules`,
- chart line-break examples,
- renderer/export validation rules,
- screenshot/export fixture expectations.

Keep in Artifact Constitution:

- source/generated/runtime classes,
- durable evidence policy,
- generic validation contract,
- a short pointer to Visual Artifact Constitution.

## Decision Status

No decision gate required now.

Reason: the recommended action is no split and no canonical rename. A future split should go through Decision Gate once the trigger conditions are met.
