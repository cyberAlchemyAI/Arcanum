# Refine Seed Proposal: Translate Before Guide

## Target

`development/user-guide/`

## Raw Operator Intent

Maybe the framework needs a separate `Translate` sigil before `Guide`. Vocabulary and domain translation should not be buried inside Guide. Then Guide can be more general: `/guide this architecture` could dispatch subagents, research, inspect structure, orchestrate explanation, and call Translate when it needs vocabulary/domain bridging.

## Refinement Objective

Decide whether `Translate` should become the first sigil candidate between `User` and `Guide`, and update the recommended capability ordering without implementing or promoting anything.

## Source Context

| Source | Role |
| --- | --- |
| `development/user-guide/refinement-runs/20260529T131319Z-user-guide-ledger/RESULT.md` | Prior User/Guide refinement selected User ledger + Guide receipt and named bridge/ladder candidates. |
| `development/user-guide/refinement-runs/20260529T131319Z-user-guide-ledger/RUN-MANIFEST.md` | Prior runtime caveat and evidence status. |
| `formulae/dispatch-spec/dispatch.schema.yml` | Dispatch validation schema. |
| User follow-up, 2026-05-29 | Introduces the Translate split and generalized Guide orchestration. |

## Preset

`standard`

## Research Mode

`no-research`

This is an internal boundary decision over existing local design evidence. No new external learning-science research is needed.

## Hypothesis

`Translate` should be created before `Guide` as a sigil candidate if it owns:

- source-domain to target-domain vocabulary mapping,
- analogy/metaphor selection and limits,
- user vocabulary preferences,
- glossary-aware term selection,
- concept primitive mapping,
- translation receipts for what worked or failed.

`Guide` should then own:

- route framing,
- question decomposition,
- architecture/system walkthrough,
- subagent/research dispatch,
- sequencing explanation sections,
- deciding when to call Translate,
- deciding when to call User ledger updates.

## Done Criteria

- Decide whether Translate should be a separate candidate.
- Define Translate/Guide/User boundaries.
- Name the revised candidate sigil/spell order.
- Preserve the prior User ledger result without overwriting it.
- Validate the dispatch route against the local dispatch schema.
