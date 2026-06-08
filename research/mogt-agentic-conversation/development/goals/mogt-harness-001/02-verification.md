# Verification

Required verification evidence:

1. Validator passes a valid synthetic fixture.
2. Validator rejects an invalid synthetic fixture.
3. The invalid fixture rejection covers at least one required blocker class:
   missing run metadata, missing objective vector, missing policy regime, or
   malformed metric fields.
4. The final report records exact commands and outputs.

Use the context pack for required fields:

- `research/mogt-agentic-conversation/development/context-mogt-harness-001.md`
- `research/mogt-agentic-conversation/development/context-mogt-harness-001.index.json`

If the repository already has a preferred JSON Schema validator dependency, use
it. Otherwise choose a lightweight local validator implementation and document
the choice.
