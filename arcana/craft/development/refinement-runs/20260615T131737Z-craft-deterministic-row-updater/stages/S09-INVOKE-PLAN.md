# S09 Invoke Plan: First Safe Row-Updater SWU

## Invoke Result

- Mode: plan.
- Spell: invoke.
- Phase status: pass.
- Outputs: `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`, this stage receipt.
- Complexity: medium.
- Per-layer planning: compact layer-mapped waves.
- Implementation detail: task specs complete.
- Smallest working units: complete.
- Next route: task-session for `SWU-CRU-001`.

## Planning Decision

Create a new row-update planner task that should be inserted before or inside
the existing CSV import dry-run task. Do not implement direct mutation.

## Recommended First SWU

`SWU-CRU-001`: define and fixture the deterministic row update planner.

Write scope for later execution:

- `arcana/craft/templates/ledger.schema.yml`
- `arcana/craft/README.md`
- `arcana/craft/SKILL.md`
- `arcana/craft/fixtures/craft-row-update-planner/`

Done criteria:

- docs/schema name row update planner as dry-run patch-plan primitive;
- fixture covers stale source, no-op, scalar update, ID churn, enum violation,
  unresolved reference, and read-only nested field;
- direct YAML mutation remains explicitly blocked;
- JSON and YAML fixture parse cleanly.

Verification:

```bash
python3 - <<'PY'
import pathlib, yaml
yaml.safe_load(pathlib.Path('arcana/craft/templates/ledger.schema.yml').read_text())
PY
rg -n "row update planner|dry-run|patch plan|ledger_sha256|read-only" arcana/craft
```

## Later SWUs

| SWU | Goal |
| --- | --- |
| `SWU-CRU-002` | Implement internal deterministic planner and patch-plan report generation. |
| `SWU-CRU-003` | Wire `import-csv --dry-run` to call the planner for each CSV row. |
| `SWU-CRU-004` | Add stale fallback/status integration and runtime mirror refresh after canonical validation. |

## Blocking Rules

- `SWU-CRU-002` blocks until `SWU-CRU-001` fixture exists.
- `SWU-CRU-003` blocks until planner reports pass/block/no-op deterministically.
- Direct apply mode remains out of scope for this work-pack.
