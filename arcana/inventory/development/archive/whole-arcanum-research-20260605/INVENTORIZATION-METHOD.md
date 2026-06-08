---
module: inventory-whole-arcanum
version: 0.1.0
status: active
updatedAt: 2026-06-05
docType: method
---

# Method: How To Inventorize Arcanum

## Purpose

This method explains how agents should continue inventorizing Arcanum without
turning the work into broad source dumping.

The goal is not exhaustive capture. The goal is a reusable knowledge layer that
helps future agents find the right source selectors faster, preserve authority
boundaries, and record gaps honestly.

## Operating Rule

Inventorize by task-shaped source slices, not by whole-folder summarization.

Each slice should answer a real retrieval question:

```text
What source context does an agent need before doing <bounded Arcanum task>?
```

If the answer requires reading a whole folder or whole source family, the slice
is too broad. Record a selector gap and narrow the question.

## Source Authority Ladder

Use this order when deciding what to cite:

| Authority | Use For | Examples |
| --- | --- | --- |
| Canonical source contract | Behavior, modes, ownership, anti-patterns | `arcana/*/SKILL.md`, `spells/*/README.md` |
| Governance framework | Cross-cutting rules | `framework/ARTIFACT-CONSTITUTION.md`, schema rules, observability docs |
| Registry | Discovery and navigation only | `registry/SIGILS.md`, `registry/SPELLS.md` |
| Development package | Current plan, readiness, task evidence | `development/*/WORK-PACK.md`, `READINESS.md`, task-session results |
| Generated or local runtime state | Excluded by default | `.arcanum/observability/**`, `.codex/commands/**`, run folders |

Generated or local runtime state may become source evidence only when a nearby
source artifact explicitly promotes it as durable evidence.

## Inventorization Loop

Run this loop for each new slice.

1. **Pick the retrieval question**
   - Start from a real task or recurring agent confusion.
   - Write the question in the slice context or tracker.
   - Reject questions that require broad full-file ingestion.

2. **Select source anchors**
   - Start with `source-manifest.json` and `SOURCE-POLICY.md`.
   - Choose 2-7 source selectors.
   - Prefer headings, line spans, or compact sections.
   - Include development task-session evidence only when it is cited by a work-pack, readiness report, package README, or validation report.

3. **Draft cards**
   - Each card should capture one reusable object: concept, method, decision, source-summary, workflow, dependency rule, validation rule, or contradiction.
   - Every material claim needs `source_refs`, or must be marked as inference, synthesis, or open question.
   - Use `trace` for full cards.
   - Preserve `residue` when authority, schema, or selector ambiguity remains.

4. **Update slice index**
   - Add every card to `index.json`.
   - Add tag lookup entries only for tags that future queries should use.
   - Avoid tag sprawl; prefer existing tag families.

5. **Create retrieval fixture**
   - Write one realistic query in `retrieval.json`.
   - Include selected cards with reasons.
   - Include excluded cards when a nearby card could mislead the task.
   - The retrieval fixture should teach how to use the slice.

6. **Write coverage report**
   - Name what was captured.
   - Name intentional omissions.
   - Name duplicate or ownership risks.
   - Record selector gaps instead of expanding the slice.

7. **Consider EvidenceSet only after repeated retrieval shape appears**
   - EvidenceSets group card IDs; they do not copy card content.
   - Keep status `candidate`.
   - Include selected and excluded card refs with reasons.
   - Do not promote after one successful run.

8. **Validate**
   - Run slice validation.
   - Run whole-inventory validation before claiming readiness.
   - Treat validation failures as task failures unless the failure is explicitly unrelated and documented.

9. **Record tracker state**
   - Update `INVENTORIZATION-TRACKER.md`.
   - Record cards added, omissions, selector gaps, validation result, and next slice.

## Slice Shape

Each slice folder should look like:

```text
cards/<slice-id>/
  cards.json
  index.json
  retrieval.json
  COVERAGE.md
```

Use `evidence-sets/evidence-sets.json` only when a stable group of cards helps
with repeated handoff or retrieval.

## Card Acceptance Checklist

Before accepting a card, check:

- `id` is unique and stable.
- `source_refs` point to existing paths and line spans.
- `summary` is short and source-backed.
- `authority_level` does not imply downstream promotion.
- `promotion_status` and `promotion_owner` are compatible.
- `claim_shape.non_authority_notice` exists when a card could be mistaken for ontology, definition, lifecycle, or runtime authority.
- `trace` explains important extraction choices.
- `residue` records ambiguity instead of hiding it.

## Coverage Acceptance Checklist

A coverage report must answer:

- What did this slice capture?
- What did it intentionally omit?
- What would be dangerous to merge or flatten?
- Which source areas need future slices?
- Which omissions are harmless until a concrete task needs them?

## Reuse Evidence Template

When a task uses Inventory first, record:

```markdown
## Inventory Reuse Evidence

- Task:
- Query used:
- Cards selected:
- EvidenceSets selected:
- Source files opened because of Inventory:
- Broad searches avoided:
- Fallback searches required:
- Missing cards:
- Stale cards:
- Candidate EvidenceSet decision: keep | split | reject | promote-later
- Validation after task:
```

## Stop Conditions

Stop and route to a decision gate when:

- a slice needs broad full-file ingestion,
- a generated artifact is needed but lacks durable-evidence promotion,
- two artifacts claim authority over the same behavior or definition,
- a proposed EvidenceSet would become de facto canonical after one use,
- the task wants ontology or definition promotion instead of Inventory evidence.

## Current Recommended Next Slice

Use the live Arcanum test to choose the next slice. Recommended lane remains:

```text
C. EvidenceSet reuse lane
```

If that lane reveals missing context, add a focused slice from the missing
selectors rather than expanding the whole inventory.
