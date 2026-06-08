# Sigil Template Family

Use this family when invoke needs to prepare context for creating or revising a sigil. This family prepares the handoff; sigil-development owns sigil lifecycle mutation, validation, observability, reflection, iteration, and promotion readiness.

## Selection Rules

1. Select `sigil` when the requested artifact is a reusable sigil, sigil mode, runtime adapter expectation, or interaction contract.
2. Keep lifecycle mutation outside this template family and hand off to sigil-development.
3. Record inputs, outputs, runtime expectations, validation examples, and observability before handoff.

## Templates

| Template | Purpose |
| --- | --- |
| [sigil.md](sigil.md) | Sigil authoring handoff contract. |
| [examples/passing.md](examples/passing.md) | Minimal passing sigil example. |
| [examples/missing-input.md](examples/missing-input.md) | Missing-input negative example. |

## Gates

- Sigil identity and purpose are required.
- Inputs and outputs must be explicit.
- Promotion readiness is only a handoff signal here; sigil-development decides lifecycle status.

## Validation

```bash
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/sigil/README.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/sigil/sigil.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/sigil/examples/passing.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/sigil/examples/missing-input.md
```
