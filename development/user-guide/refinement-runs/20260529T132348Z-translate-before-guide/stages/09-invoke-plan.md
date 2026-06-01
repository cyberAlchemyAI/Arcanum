# Stage 09: Invoke Plan

Status: `pass`

## Non-Executed Plan

### Task 1: Translate Define

Create:

- `development/user-guide/TRANSLATE-DEFINE.md`
- `development/user-guide/TRANSLATE-GLOSSARY.md`

Define the sigil candidate as vocabulary/domain translation, not teaching orchestration.

### Task 2: Translate Schema

Create:

- `development/user-guide/TRANSLATE-SCHEMA.yml`
- `development/user-guide/TRANSLATE-RECEIPT-SCHEMA.yml`

Required fields:

- source domain,
- target domain,
- target concept,
- source vocabulary,
- target vocabulary,
- term map,
- bridge map,
- mapping limits,
- target-domain definition,
- user preference handles,
- receipt.

### Task 3: Translate Fixture Corpus

Use the examples from the prior run:

- sales terms -> software architecture decision,
- software engineering terms -> scientific formula,
- musician terms -> civil construction plan.

Add one negative fixture where the analogy fails and Translate must preserve the target definition.

### Task 4: Guide Reframe

After Translate fixtures pass, refine Guide as an orchestrator:

```text
/guide <target>
  -> frame
  -> inspect/research/subagents
  -> translate when needed
  -> sequence explanation
  -> validate understanding
  -> propose User ledger update
```

## Recommended Route

Run `sigil-development` for `translate` before `spellcraft` for `guide`.
