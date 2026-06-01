# Run Manifest: Record Kind Schema Gap

Status: pass
Run id: `20260529T104000Z-record-kind-decision`
Preset: compact
Research: no-research

## Target

`arcana/ontology-vault/development/schema-validation-plan/VALIDATION-REPORT.md`

## Command Resolution

| Command | Resolved file | Status |
| --- | --- | --- |
| `context-builder` | `.codex/commands/context-builder.md` | pass |
| `invoke` | `.codex/commands/invoke.md` | pass |
| `interrogation` | `.codex/commands/interrogation.md` | pass |
| `distill` | `.codex/commands/distill.md` | pass |
| `dispatch-spec` | n/a | flag: command surface unavailable |

## Dispatch Validation

`REFINE-DISPATCH.json` validated against:

```text
formulae/dispatch-spec/dispatch.schema.json
```

Validation command:

```bash
python3 - <<'PY'
import json
from pathlib import Path
import jsonschema
schema = json.loads(Path('formulae/dispatch-spec/dispatch.schema.json').read_text())
doc = json.loads(Path('arcana/ontology-vault/development/schema-validation-plan/refinement-runs/20260529T104000Z-record-kind-decision/REFINE-DISPATCH.json').read_text())
jsonschema.Draft202012Validator(schema).validate(doc)
print('dispatch-schema: pass')
PY
```

Result: pass

## Stage Evidence

| Stage | Owner | Adapter | Status | Evidence |
| --- | --- | --- | --- | --- |
| Context Builder evidence baseline | `context-builder` | dry-run | pass | `stages/context-builder.output.md` |
| Invoke Define | `invoke` | dry-run | pass | `stages/invoke-define.output.md` |
| Interrogation refine-review | `interrogation` | dry-run | pass | `stages/interrogation-review.output.md` |
| Research decision | refine | n/a | pass | no-research, local evidence sufficient |
| Distill | `distill` | dry-run | pass | `stages/distill.output.md` |
| Invoke Redefine / Design | `invoke` | dry-run | pass | `stages/invoke-design.output.md` |
| Interrogation refine-design-review | `interrogation` | dry-run | pass | `stages/interrogation-design-review.output.md` |
| Distill Repair | `distill` | dry-run | pass | `stages/distill-repair.output.md` |
| Invoke Plan | `invoke` | dry-run | pass | `stages/invoke-plan.output.md` |
| Final Interrogation and Synthesis | `interrogation` plus refine synthesis | dry-run plus local synthesis | pass | `stages/interrogation-final.output.md`, `RESULT.md` |

## Boundaries Preserved

- No schema candidate mutation.
- No fixture mutation.
- No Inventory mutation.
- No structured-action-schema mutation.
- No canonical template mutation.

## Verdict

Add `record_kind` as a candidate schema field before JSON Schema generation.
