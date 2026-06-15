# Public Boundary Scan Summary

## Scan

```bash
rg -n "/home/|\\.\\./|projects/|implementation/|Body War|GoldenQuill|Parque|DomainSpec|Strava|private workspace|local-only approval|nested product path" \
  arcanum/arcana/craft/examples \
  arcanum/arcana/craft/development/refinement-runs/20260614T200439Z-craft-feature-readiness-indexes
```

## Result

- Status: `flag`
- Syntax impact: none
- Publication impact: review gate

## Classification

| Hit Class | Examples | Classification | Required Follow-Up |
| --- | --- | --- | --- |
| Existing named public examples | `Body War`, `GoldenQuill`, `Parque`, `DomainSpec`, `Strava`, `projects/body-war`, `implementation/domainspec` under `arcana/craft/examples/` | Existing public examples, not new readiness fixture evidence. | Do not reuse as readiness-index fixture without owner review. |
| Planned denylist text | denylist command strings in `WORK-PACK.md`, `TASK-CFR-003.md`, and `TASK-CFR-004.md` | Expected self-reference to the validation gate. | Keep as validation text. |
| Protected-context prose | phrases such as `private workspace` in the run packet | Expected boundary language. | Keep as guardrail text. |

## Gate Decision

- `SWU-CFR-001`: may proceed as schema-only if write scope stays in `arcana/craft/templates/ledger.schema.yml` and does not touch examples.
- `SWU-CFR-005`: must default to a new synthetic readiness fixture. Existing named examples may be parsed for compatibility only unless an owner explicitly approves editing or reusing them.
- Publication: keep blocked until hits are classified in the task result and any new example content passes the stricter scan.
