# Refresh Template Family

Use this family when `invoke refresh` turns latest session evidence into scoped artifact refresh proposals or approved updates.

## Selection Rules

1. Select `refresh` when the user asks to update existing invoke-authored artifacts from new session evidence.
2. Require source evidence, target artifact inventory, refresh scope, evidence date, and activation source.
3. Resolve an omitted mutation mode to `apply-approved` for a direct user invocation and to `proposal-only` for delegated or continuation activation.
4. Treat the direct user request as approval evidence only for the exact declared scope; require separate approval evidence for any broader `apply-approved` mutation.
5. Preserve the distinction between setup proof, blocker evidence, completion proof, artifact drift, and no-op state.
6. Derive phase status from the current Refresh artifact and report apply, target-lifecycle, and audit readiness separately.

## Templates

| Template | Purpose |
| --- | --- |
| [refresh.md](refresh.md) | Refresh report and patch proposal contract. |
| [examples/passing.md](examples/passing.md) | Minimal passing refresh example. |
| [examples/missing-input.md](examples/missing-input.md) | Missing-input negative example. |

## Gates

- Source evidence is required.
- Target artifact inventory is required.
- Every proposed or applied change must map to a `RefreshSignal`.
- Every blocker declares `refresh-authoring`, `apply-authorization`, `target-lifecycle`, or `audit` scope.
- A complete proposal-only artifact passes even when its handoff is gated by apply authorization or downstream work.
- Artifact drift flags when no safe correction is obvious.
- No-op is valid when evidence is already represented.
- Apply mode requires scoped approval evidence, declared scope, a valid material package, and validation commands.

## Validation

Run invoke validation after edits:

```bash
./spells/invoke/development/run-validation-fixtures.sh
```
