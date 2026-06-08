# Architecture Template Family

Use this family when invoke needs architecture planning, design transport, dependency rules, or interface decisions before implementation work.

## Selection Rules

1. Select `architecture` when the request asks how a system, module, spell, sigil, workflow, or capability should be structured.
2. Require source contracts unless the request explicitly allows discovery-mode architecture.
3. Keep architecture outputs separate from task execution; route delivery work to the implementation-plan family.

## Templates

| Template | Purpose |
| --- | --- |
| [architecture.md](architecture.md) | Architecture planning contract. |
| [examples/passing.md](examples/passing.md) | Minimal passing architecture example. |
| [examples/missing-input.md](examples/missing-input.md) | Missing-input negative example. |

## Composition

Use [../module-formulae/architecture-bundle.md](../module-formulae/architecture-bundle.md) as the minimum Module Formulae view-set when architecture output must be bundled with module artifacts.

## Gates

- Block when required source contracts are missing and discovery mode is not approved.
- Flag unresolved dependency or interface risk.
- Record every major option in the decision log.

## Validation

```bash
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/architecture/README.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/architecture/architecture.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/architecture/examples/passing.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/architecture/examples/missing-input.md
```