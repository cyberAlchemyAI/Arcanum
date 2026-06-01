# Template Manifest: Inventory Evidence-Card

## Invoke Result

- Mode: inventory/template selection companion
- Spell: invoke
- Phase status: pass
- Template family: Inventory evidence-card
- Target production root: `arcana/inventory/templates/`

## Template Outputs

| Development Template | Target Production Path | Status | Purpose |
| --- | --- | --- | --- |
| `templates/evidence-card-schema.md` | `arcana/inventory/templates/evidence-card-schema.md` | candidate | Schema contract for the canonical record. |
| `templates/evidence-card.md` | `arcana/inventory/templates/evidence-card.md` | candidate | Authoring template for full/minimal cards. |
| `templates/evidence-card-lint.md` | `arcana/inventory/templates/evidence-card-lint.md` | candidate | Static lint and validation contract. |
| `templates/evidence-card-index.md` | patch source for `arcana/inventory/templates/index.md` | candidate | Index families and retrieval output contract. |

## Selection Evidence

- User requested a complete refresh of the Inventory development package.
- Invoke output contracts require more than planning artifacts.
- Inventory development needs templates before runtime or production package mutation.

## Promotion Rule

These are development templates. They become production Inventory templates only through the work-pack SWUs that copy or adapt them into `arcana/inventory/templates/` and run the corresponding review checks.
