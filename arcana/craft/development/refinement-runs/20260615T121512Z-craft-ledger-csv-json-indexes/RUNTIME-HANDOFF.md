# Runtime Handoff: Craft Ledger CSV And JSON Indexes

## Current State

The route has been executed into a design/plan packet with status `flag`.
Canonical Craft files have not been changed.

## Execute Next Only After Approval

The next executor should not rerun Refine by default. It should select an SWU
from `WORK-PACK.md`, starting with `SWU-CLP-001`, then execute through the
appropriate Craft lifecycle route.

Already produced:

- `DEFINE.md`
- `INVOKE-DESIGN.md`
- `INVOKE-PLAN.md`
- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`

## Initial Design Bias

Keep this shape unless the Refine loop discovers a blocker:

```text
.craft/
  ledger.yml
  index.json
  projections/
    contexts.csv
    artifacts.csv
    typed_items.csv
    decisions.csv
    relations.csv
    gaps.csv
    descriptions.csv
    definitions.csv
    route_handoffs.csv
    receipts.csv
    recomposition.csv
    pending.csv
    links.csv
```

`ledger.yml` is the only source of truth. `index.json` and
`projections/*.csv` are generated. CSV writeback must go through a dry-run
reconcile command that validates row IDs, references, nested links, source
freshness, and live row-family coverage before editing the YAML ledger.

## Suggested SWU Sequence

| SWU | Goal | Write Scope |
| --- | --- | --- |
| `SWU-CLI-001` | Add projection contract to schema and docs. | `arcana/craft/templates/ledger.schema.yml`, `arcana/craft/README.md`, `arcana/craft/SKILL.md` |
| `SWU-CLI-002` | Add public-safe toy fixture and expected outputs. | `arcana/craft/fixtures/` or `arcana/craft/examples/` |
| `SWU-CLI-003` | Add generator/validator script for JSON and CSV projection. | `arcana/craft/scripts/` |
| `SWU-CLI-004` | Add import/reconcile dry-run command. | `arcana/craft/scripts/` |
| `SWU-CLI-005` | Refresh generated runtime mirrors and publication gates. | generated runtime packages, parent gitlink only after submodule push |

## Validation

1. Parse `REFINE-DISPATCH.json`.
2. Validate dispatch with `arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py`.
3. Parse execution receipt JSON.
4. Parse YAML schema and fixtures during SWU execution.
5. Run projection toy-game round trip before import support.
6. Run public-boundary scan before public submodule commit.
7. Run `git -C arcanum diff --check`.
8. Run parent `make bump-check` before publishing the parent gitlink.

## Blockers

- CSV import can corrupt nested structures if links and lists are flattened
  without a reversible mapping.
- Generated projections can become stale unless source hash and generator
  metadata are enforced.
- Embedded ledger indexes with positional selectors can drift when row order
  changes unless a generated index owns lookup freshness.
- Current examples contain row families beyond the first schema contract; the
  projection generator must either define those families or explicitly flag
  unsupported rows.
- Public Craft fixtures cannot include private workspace paths or unpublished
  product context.
