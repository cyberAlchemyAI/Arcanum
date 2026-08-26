# Experiment Prompt: create-low

Use `$evidence-grounded-diagrams` from
`transmutations/evidence-grounded-diagrams` to create the smallest faithful
diagram answering: “What can the reviewer do after receiving a draft?”

Permitted evidence:

- `POL-12 §3`: “After receiving a draft, the reviewer may approve that version
  or request changes.”
- `POL-12 §4`: “After requested changes, the author may submit a new version.”

The result is a non-official draft. Persist any emitted diagram under a temporary
workspace output root. Return the complete user-facing result, not a save summary.
