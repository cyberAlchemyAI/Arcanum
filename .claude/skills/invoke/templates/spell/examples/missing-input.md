# Missing-Input Example: Spell Template

Template: [../spell.md](../spell.md)

## Missing Inputs

- Spell identity is absent.
- No mode contract is defined.

## Expected Result

- Gate status: block.
- The template must request identity and at least one mode contract before handoff.
- Spellcraft lifecycle work must not begin from this incomplete handoff.