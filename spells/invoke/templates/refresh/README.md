# Refresh Template Family

Use this family when `invoke refresh` turns latest session evidence into scoped artifact refresh proposals or approved updates.

## Selection Rules

1. Select `refresh` when the user asks to update existing invoke-authored artifacts from new session evidence.
2. Require source evidence, target artifact inventory, refresh scope, evidence date, and mutation mode.
3. Default mutation mode to `proposal-only`.
4. Require explicit approval before any `apply-approved` mutation.
5. Preserve the distinction between setup proof, blocker evidence, completion proof, artifact drift, and no-op state.

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
- Artifact drift flags when no safe correction is obvious.
- No-op is valid when evidence is already represented.
- Apply mode requires explicit approval, declared scope, and validation commands.

## Validation

Run invoke validation after edits:

```bash
./spells/invoke/development/run-validation-fixtures.sh
```
