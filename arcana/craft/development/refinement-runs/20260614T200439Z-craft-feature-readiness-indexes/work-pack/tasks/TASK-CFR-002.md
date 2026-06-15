# TASK-CFR-002: Update Skill And README Contract

## Goal

Update Craft's human and executable contract text so agents know how to expose execution readiness without letting Craft become the executor.

## Layer

L1 Skill And View Contract

## Source Contracts

- [../../INVOKE-DESIGN.md](../../INVOKE-DESIGN.md)
- [../../../../../SKILL.md](../../../../../SKILL.md)
- [../../../../../README.md](../../../../../README.md)

## Inputs

- L0 schema/index contract from `TASK-CFR-001`.
- Current `<linking-and-indexing-contract>`.
- Current `<all-status-contract>`.
- Current `<interaction-boundary>`.

## Implementation Detail

1. Extend the linking/indexing contract with optional execution-readiness handles.
2. Extend all-status output to include a compact "Execution readiness" line when readiness handles exist.
3. Preserve `Pending by node` as the main status view.
4. State that readiness fields point to Invoke work-packs, approvals, execution modes, and blocked scopes.
5. State that Craft records these handles but does not execute, validate, or close the work-pack.
6. Update README with a short package-level summary and link/index rule.

## Edge Cases

- If a ledger has no readiness index, status output should not invent one.
- If readiness says "ready SWU" but an approval is missing, status should report that approval as pending.
- If product worktree differs from Craft scope, status should name that boundary without treating workspace status as product status.

## Smallest Working Units

| SWU | Work | Acceptance |
| --- | --- | --- |
| `SWU-CFR-003` | Update `SKILL.md`. | Skill text names readiness handles and preserves non-execution boundary. |
| `SWU-CFR-004` | Update `README.md`. | README summarizes readiness indexing as optional lookup data. |

## Verification

```bash
rg -n "execution_readiness|Execution readiness|approval_record|blocked_mutation_scope|product_worktree" arcana/craft/SKILL.md
rg -n "execution readiness|approval|work-pack|SWU" arcana/craft/README.md
```

## Done When

- Contract text points future agents at readiness indexes.
- Contract text does not authorize Craft to execute work.
