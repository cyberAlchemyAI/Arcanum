# Research Template Family

Use this family when invoke needs evidence-first discovery before decisions, architecture, or implementation planning.

## Selection Rules

1. Select `research` when the request depends on unknown evidence, competing claims, or source discovery.
2. Prefer repository evidence when external evidence is unavailable or out of scope.
3. Keep synthesis separate from implementation planning unless the user requests a follow-on route.

## Templates

| Template | Purpose |
| --- | --- |
| [research.md](research.md) | Evidence-first discovery contract. |
| [examples/passing.md](examples/passing.md) | Minimal passing research example. |
| [examples/missing-input.md](examples/missing-input.md) | Missing-input negative example. |

## Composition

Use [../module-formulae/research-brief.md](../module-formulae/research-brief.md) as the compact Module Formulae research summary when the output needs to join a module bundle.

## Gates

- Research question and source scope are required.
- Contradictions and confidence must be explicit.
- A repository-only run is allowed when the evidence boundary says external sources are out of scope.

## Validation

```bash
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/research/README.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/research/research.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/research/examples/passing.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/research/examples/missing-input.md
```