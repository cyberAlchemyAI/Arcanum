# TASK-CFR-004: Add Validation And Status Review Checks

## Goal

Make the readiness-index update easy to review and hard to overclaim.

## Layer

L2/L3 Validation

## Source Contracts

- [../../WORK-PACK.md](../../WORK-PACK.md)
- [../../../../../SKILL.md](../../../../../SKILL.md)
- [../../../../../templates/ledger.schema.yml](../../../../../templates/ledger.schema.yml)

## Inputs

- Schema update from `TASK-CFR-001`.
- Skill/README update from `TASK-CFR-002`.
- Example/fixture update from `TASK-CFR-003`.

## Implementation Detail

1. Add or update a reviewable validation checklist in this development packet or a local validation artifact.
2. Include parse checks for schema and examples.
3. Include grep checks for canonical terms.
4. Include a public-boundary scan.
5. Include `git diff --check`.
6. If renderer/status code exists later, add a status-output fixture; do not invent a renderer in this task.

## Edge Cases

- A checklist is enough for this work-pack because Craft does not yet own an automated renderer.
- If an executor finds a deterministic validator during execution, they may add it only inside the selected SWU scope.

## Smallest Working Units

| SWU | Work | Acceptance |
| --- | --- | --- |
| `SWU-CFR-006` | Add validation checklist and run it. | Commands pass or record exact residue. |

## Verification

```bash
python3 -m json.tool arcana/craft/development/refinement-runs/20260614T200439Z-craft-feature-readiness-indexes/evidence-index.json
python3 -m json.tool arcana/craft/development/refinement-runs/20260614T200439Z-craft-feature-readiness-indexes/dispatch-seed.json
rg -n "/home/|\\.\\./|projects/|implementation/|private workspace|local-only approval|nested product path" arcana/craft/examples arcana/craft/development/refinement-runs/20260614T200439Z-craft-feature-readiness-indexes || true
git diff --check -- arcana/craft
```

## Done When

- Reviewers can reproduce the validation checks.
- Public-boundary hits are classified as expected existing examples, new leaks, or owner-approved named example content.
- Any residual missing automation is named as a deferral, not hidden.
