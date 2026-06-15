# Traceability: Craft Feature Readiness Indexes

## Source To Plan Map

| Source | Uses |
| --- | --- |
| `arcana/craft/SKILL.md` | Skill contract update target for readiness status and interaction boundary. |
| `arcana/craft/README.md` | Package-level user explanation target. |
| `arcana/craft/templates/ledger.schema.yml` | Schema/index contract update target. |
| `arcana/craft/examples/` | Public-safe fixture or example coverage. |
| `INVOKE-DESIGN.md` | Architecture and boundary source for task design. |
| `IMPLEMENTATION-LAYERING.md` | L0-L3 promotion gate source. |
| `WORK-PACK.md` | Current execution state and SWU manifest. |

## Boundary Assertions

- Craft records readiness; it does not execute.
- Readiness indexes are optional; missing readiness fields do not invalidate old ledgers.
- Private evidence is abstracted before entering public Craft artifacts.
- Generated runtime surfaces are regenerated from canonical source.
