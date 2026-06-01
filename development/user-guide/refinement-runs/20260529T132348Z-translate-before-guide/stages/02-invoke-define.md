# Stage 02: Invoke Define

Status: `pass`

## Definition

`Translate` is a candidate sigil that transforms a concept, artifact, decision, or architecture from one vocabulary/domain frame into another while preserving target-domain truth and recording mapping limits.

`Guide` is a more general orchestration and explanation capability. It receives a user request such as `/guide this architecture`, decides what kind of understanding route is needed, dispatches subagents or research if needed, and calls Translate when vocabulary/domain bridging is part of the route.

## Translate Owns

- source-domain vocabulary,
- target-domain vocabulary,
- user vocabulary preferences,
- analogy/metaphor selection,
- mapping limits,
- bridge receipts,
- glossary-aware term choices,
- primitive alignment across domains.

## Guide Owns

- framing a guide request,
- decomposing the target,
- deciding the guide route,
- dispatching research/subagents/x-ray/inventory/context-builder,
- sequencing explanation sections,
- deciding when Translate is needed,
- asking for confirmation or active evidence,
- returning guide receipts to User ledger.

## User Owns

- preferences,
- prior domains,
- concept states,
- glossary entries,
- guide and translate receipts,
- consent/visibility rules.
