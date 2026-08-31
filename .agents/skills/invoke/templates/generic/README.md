# Generic Template Family

Use this family when an invoke request needs a neutral governed artifact and no more specific template family is eligible.

## Selection Rules

1. Select `generic` only when no specialized family fits or the user explicitly asks for a neutral fallback.
2. Record why `research`, `architecture`, `implementation-plan`, `spell`, `sigil`, and `ux-plan` were not selected when they were plausible.
3. Keep all unresolved fit questions in the gap ledger instead of silently narrowing scope.

## Templates

| Template | Purpose |
| --- | --- |
| [generic.md](generic.md) | Neutral governed artifact contract. |
| [examples/passing.md](examples/passing.md) | Minimal passing generic example. |
| [examples/missing-input.md](examples/missing-input.md) | Missing-input negative example. |

## Gates

- Required goal, scope, evidence, and output depth must be present before pass.
- If a specialized family becomes eligible, generic must defer or ask for explicit user choice.
- Candidate output remains non-canonical until promotion evidence and approval exist.

## Validation

Run link validation for this directory after edits:

```bash
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/generic/README.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/generic/generic.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/generic/examples/passing.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/generic/examples/missing-input.md
```