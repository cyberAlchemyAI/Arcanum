# Spell Template Family

Use this family when invoke needs to prepare context for creating or revising a spell. This family prepares the handoff; spellcraft owns spell lifecycle mutation, validation, installation or adaptation, observation, reflection, and promotion readiness.

## Selection Rules

1. Select `spell` when the requested artifact is a spell contract, spell mode, spell trigger, or spell capability map.
2. Keep lifecycle mutation outside this template family and hand off to spellcraft.
3. Record required sigils, required spells, shared state, and observability expectations before handoff.

## Templates

| Template | Purpose |
| --- | --- |
| [spell.md](spell.md) | Spell authoring handoff contract. |
| [examples/passing.md](examples/passing.md) | Minimal passing spell example. |
| [examples/missing-input.md](examples/missing-input.md) | Missing-input negative example. |

## Gates

- Spell identity and trigger conditions are required.
- At least one mode or phase contract must be defined.
- Promotion readiness is only a handoff signal here; spellcraft decides lifecycle status.

## Validation

```bash
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/spell/README.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/spell/spell.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/spell/examples/passing.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/spell/examples/missing-input.md
```
