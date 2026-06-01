# Refine Result: Translate Before Guide

## Verdict

Status: `pass-with-runtime-caveat`

Yes: create `Translate` as a separate sigil candidate before building general `Guide`.

## Why

The previous User/Guide refinement correctly identified the need for user ledger receipts and cross-domain explanation. This follow-up splits the responsibilities more cleanly:

```text
User = memory and learning ledger
Translate = vocabulary/domain/concept bridge
Guide = orchestration for understanding
```

If translation stays inside Guide, Guide becomes too broad too early. If Translate becomes a reusable sigil first, Guide can stay general and call it only when needed.

## Translate Boundary

Translate should answer:

> How do I say this concept in terms this user or source domain understands, while preserving what the target concept really means?

Translate owns:

- term maps,
- domain maps,
- analogy/metaphor maps,
- mapping limits,
- target-domain definition,
- user vocabulary preference handles,
- translation receipts.

Translate does not own:

- subagent dispatch,
- research orchestration,
- full teaching route,
- durable user ledger writes,
- canonical glossary promotion.

## Guide Boundary

Guide should answer:

> What route should help the user understand this target, and which capabilities should I call?

For `/guide this architecture`, Guide can route:

```text
frame request
  -> inspect architecture
  -> dispatch research/subagents if needed
  -> x-ray structure
  -> call Translate for vocabulary/domain bridge
  -> assemble walkthrough
  -> validate understanding
  -> propose User ledger update
```

## Revised Candidate Order

1. Minimal User ledger fixture handles.
2. `Translate` sigil candidate.
3. Translate fixture corpus.
4. Guide orchestration design.
5. Guide spell candidates.

## Next Routes

1. Run `sigil-development` for `translate`.
2. Create `TRANSLATE-SCHEMA.yml` and `TRANSLATE-RECEIPT-SCHEMA.yml`.
3. Validate fixtures:
   - sales terms -> software architecture decision,
   - software engineering terms -> scientific formula,
   - musician terms -> civil construction plan,
   - failed analogy with target-definition preservation.
4. After Translate passes fixtures, refine Guide as an orchestration spell that can dispatch Translate, research, x-ray, Inventory, and subagents.

## Runtime Caveat

The local dispatch route can be schema-validated, but canonical command-backed stage execution remains caveated because `dispatch-spec` and `runtime-handoff` commands are not registered in the local command surface.
