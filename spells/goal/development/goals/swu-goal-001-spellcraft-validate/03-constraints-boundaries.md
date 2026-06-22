# Constraints And Boundaries

## Write Scope

Allowed:

- `arcanum/spells/goal/development/spellcraft-runs/`
- an equivalent public-safe validation report path under
  `arcanum/spells/goal/development/`

Not allowed:

- runtime implementation files,
- active Craft ledger rows,
- filled decision profiles,
- generated host runtime surfaces such as `SKILL.md`,
- publication, commit, push, pull request, or parent gitlink movement.

## Source Context Boundary

Use the strict handoff pack first. Read extra sources only when one of the named
gaps requires it:

- `G-GOAL-SCHEMA-HOME`
- `G-GOAL-CRAFT-SYNC`

Every extra source must be reported with:

- source path,
- gap that justified it,
- whether it changed the result.

## Public/Private Boundary

The public spell package may include schema and neutral defaults only. Do not
copy filled runtime profile contents into public artifacts or validation
reports.

## Capability Policy

Allowed:

- Spellcraft lifecycle validation.
- Read-only inspection of the handoff pack and listed source contracts.
- Local validation/report writing inside the write scope.

Not allowed:

- subagents,
- runtime SWU execution,
- broad Invoke/Refine/Craft mutation,
- Decision Gate approval claims,
- Experiment Harness promotion evidence claims.
