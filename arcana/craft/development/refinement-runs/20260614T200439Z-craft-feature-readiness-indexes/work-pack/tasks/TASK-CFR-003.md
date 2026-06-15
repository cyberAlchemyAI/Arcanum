# TASK-CFR-003: Add Public-Safe Example Or Fixture Coverage

## Goal

Add public-safe example coverage for execution-readiness indexes.

## Layer

L2 Examples And Fixture Coverage

## Source Contracts

- [../../GLOSSARY-CONSISTENCY.md](../../GLOSSARY-CONSISTENCY.md)
- [../../../../../examples/body-war-ledger.yml](../../../../../examples/body-war-ledger.yml)
- [../../../../../examples/goldenquill-ledger.yml](../../../../../examples/goldenquill-ledger.yml)

## Inputs

- L0 schema update.
- L1 skill/README wording.
- Existing public examples.

## Implementation Detail

1. Prefer a small synthetic fixture if modifying existing named examples would blur their current story.
2. If updating an existing example, only use already-public information in the current example.
3. Demonstrate:
   - a current execution target;
   - one ready SWU ID;
   - an approval record reference;
   - an allowed execution mode;
   - one blocked mutation or publication scope.
4. Keep all paths relative and public-safe.
5. Do not copy private workspace names, findings, nested product paths, or local-only approval records.

## Edge Cases

- A work-pack path may exist as a planned artifact rather than an executed artifact.
- A readiness fixture may show `flag` while still being valid, because readiness can expose blocked scopes.
- A missing approval should be represented as pending, not silently omitted when execution is otherwise blocked.

## Smallest Working Units

| SWU | Work | Acceptance |
| --- | --- | --- |
| `SWU-CFR-005` | Add public-safe fixture or example update. | Example parses and demonstrates readiness without private evidence. |

## Verification

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
for path in Path("arcana/craft/examples").glob("*.yml"):
    yaml.safe_load(path.read_text())
    print(f"YAML OK: {path}")
PY
rg -n "/home/|\\.\\./|private workspace|local-only approval|nested product path" arcana/craft/examples arcana/craft/development/refinement-runs/20260614T200439Z-craft-feature-readiness-indexes || true
```

## Done When

- Public-safe fixture coverage exists.
- The privacy scan does not reveal private workspace evidence in public Craft examples.
