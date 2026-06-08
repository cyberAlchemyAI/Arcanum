# Missing-Input Example: Sigil Template

Template: [../sigil.md](../sigil.md)

## Missing Inputs

- Outputs are absent.
- Runtime expectations are unclear.

## Expected Result

- Gate status: block for missing outputs.
- Runtime expectations may be flagged if optional, but output contract must be resolved before handoff.
- Sigil-development lifecycle work must not begin from this incomplete handoff.