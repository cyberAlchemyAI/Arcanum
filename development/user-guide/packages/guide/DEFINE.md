# Guide Define

## Invoke Result

- Mode: full authoring package, define slice
- Spell: invoke
- Canonical ID: invoke
- Scope: `development/user-guide/packages/guide/`
- Phase status: `pass`
- Mode contract: `spells/invoke/define.md`
- Template/profile selection: spell/orchestrator candidate scaffold
- Next route: `spellcraft`

## Objective

Define `guide` as a candidate spell/orchestrator that helps a user understand a target by framing the request, inspecting context, optionally dispatching research or subagents, calling Translate when needed, sequencing explanation, validating understanding, and proposing User ledger updates.

## Example Trigger

```text
/guide this architecture
```

## Scope

In scope:

- guide request frame,
- route selection,
- context inspection,
- research/subagent dispatch decision,
- x-ray or inventory call decision,
- Translate call decision,
- explanation sequencing,
- active-evidence prompt,
- guide receipt.

Out of scope:

- owning user memory,
- owning translation internals,
- writing canonical definitions,
- executing unbounded research,
- implementing runtime command before User/Translate contracts pass.

## Acceptance Criteria

| Criterion | Evidence |
| --- | --- |
| Guide can route a target through inspect/research/translate/explain/validate. | Guide route design. |
| Guide calls Translate instead of owning translation logic. | Dependency interface. |
| Guide can emit receipt proposals to User. | Receipt fields in design. |
| Guide dispatch is budgeted and bounded. | Work-pack task for dispatch gates. |
