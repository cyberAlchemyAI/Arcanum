# TASK-CFR-001: Add Schema And Index Contract

## Goal

Add an optional execution-readiness index contract to `arcana/craft/templates/ledger.schema.yml`.

## Layer

L0 Schema Contract

## Source Contracts

- [../../INVOKE-DESIGN.md](../../INVOKE-DESIGN.md)
- [../../IMPLEMENTATION-LAYERING.md](../../IMPLEMENTATION-LAYERING.md)
- [../../../../../templates/ledger.schema.yml](../../../../../templates/ledger.schema.yml)

## Inputs

- Existing `index_contract.required_ledger_indexes`.
- Existing validation rule `VAL-014`.
- Proposed optional fields from the refine result.

## Implementation Detail

1. Add an optional `readiness_index_contract` or equivalent subsection beside the existing index contract.
2. Define the readiness lookup family as optional, not required:
   - `current_execution_target`
   - `work_pack_gate_status`
   - `ready_swu_ids`
   - `approval_record`
   - `execution_mode`
   - `product_worktree`
   - `blocked_mutation_scope`
   - `blocked_publication_scope`
   - `owner_route`
3. State that readiness indexes must point to row IDs, artifact IDs, SWU IDs, or paths and must not redefine work-pack content.
4. Add validation notes that missing readiness indexes are not errors.
5. Keep existing ledgers valid without adding new required fields.

## Edge Cases

- Existing ledgers without work-packs must remain valid.
- Readiness fields must not imply execution proof.
- `execution_mode` should remain an open string until broader examples justify an enum.
- `product_worktree` should be optional because many Craft scopes match their product repo directly.

## Smallest Working Units

| SWU | Work | Acceptance |
| --- | --- | --- |
| `SWU-CFR-001` | Add optional readiness index contract. | Schema names every readiness handle and marks the family optional. |
| `SWU-CFR-002` | Confirm existing examples remain compatible. | Product Launch and Platform Governance examples parse without requiring readiness fields. |

## Verification

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
for path in [
    Path("arcana/craft/templates/ledger.schema.yml"),
    Path("arcana/craft/examples/product-launch-ledger.yml"),
    Path("arcana/craft/examples/platform-governance-ledger.yml"),
]:
    yaml.safe_load(path.read_text())
    print(f"YAML OK: {path}")
PY
rg -n "execution_readiness|current_execution_target|approval_record|blocked_mutation_scope" arcana/craft/templates/ledger.schema.yml
```

## Done When

- Schema parses.
- Existing examples parse.
- New readiness contract is optional and link/index oriented.
