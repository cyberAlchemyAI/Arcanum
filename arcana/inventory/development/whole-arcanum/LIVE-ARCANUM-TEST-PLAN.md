---
module: inventory-whole-arcanum
version: 0.1.0
status: decision-gated
updatedAt: 2026-06-03
docType: invoke-plan
invokeMode: plan
---

# Invoke Plan: Live Arcanum Inventory Test

## Objective

Test whether the whole-Arcanum Inventory can reduce source-discovery cost inside
Arcanum itself, where knowledge is dispersed across sigils, spells, formulae,
framework docs, registry files, tools, development artifacts, and validation
scripts.

This plan does not execute the test. It prepares one continuous work stream for
the next task-session run after the blocker decision is resolved.

## Current Baseline

| Area | Evidence |
| --- | --- |
| Inventory readiness | `READINESS.md` says the package is ready for agent-facing POC, not canonically promoted. |
| Validation | `validate-whole-arcanum-inventory.sh` returns `RESULT: pass`. |
| Query surface | `OPERATIONAL-COMMANDS.md` documents shell plus `jq` queries. |
| Card coverage | 24 cards across inventory, governance, lifecycle, arcana, composition, and runtime slices. |
| EvidenceSets | 2 candidate EvidenceSets, both non-authority and aimed at context-builder handoff. |
| Runtime boundary | Native/generated skill packages are live proof; legacy `.codex/commands` are excluded. |

## Gaps And Blockers First

| ID | Classification | Gap Or Blocker | Why It Matters | Handling |
| --- | --- | --- | --- | --- |
| B-LAT-001 | blocker | First real task lane is not selected. | Different tasks test different claims: install/runtime proof, retrieval quality, EvidenceSet reuse, or missing-card discovery. | Resolve through `DECISION-LIVE-ARCANUM-TEST.md` before task-session mutation. |
| G-LAT-001 | gap | No measurement template yet records source-search cost. | Without a reuse ledger, the test can feel successful without proving retrieval value. | Add a small reuse record in the task-session result. |
| G-LAT-002 | gap | EvidenceSets are candidate-level. | They can speed retrieval, but should not be promoted without repeated reuse evidence. | Record use/split/reject signal only; do not promote during first stream. |
| G-LAT-003 | gap | Cards are clustered, not exhaustive. | Missing cards are expected and should become backlog, not test failure. | Treat missing context as evidence for future slices. |
| G-LAT-004 | gap | Current Arcanum repo has repo-local symlink skills and global generated skills, while external install smoke used generated repo packages. | Live Arcanum behavior and target-repo install behavior are related but not identical. | Keep this stream scoped to current-repo Inventory-first execution; target-repo install can be a later stream. |
| G-LAT-005 | gap | Artifact Constitution emits pre-existing benchmark generated-artifact warnings. | Warnings are noisy but not blockers because validator returns pass. | Report warnings without expanding this work into benchmark cleanup. |

## Refined Test Method

Use an Inventory-first, bounded-search protocol:

1. Run the whole-inventory validator.
2. Query cards and candidate EvidenceSets for the selected task lane.
3. Record selected cards, excluded cards, and initial source anchors.
4. Open only the source files/selectors named by the cards first.
5. If context is missing, perform bounded `rg` fallback and record the gap.
6. Execute one task-session SWU.
7. Rerun validation.
8. Write a reuse result:
   - cards used,
   - EvidenceSets used,
   - broad searches avoided,
   - fallback searches required,
   - stale/missing cards,
   - EvidenceSet promotion/split/reject recommendation.

## Candidate Task Lanes

| Option | Test Claim | Candidate Task | Strength | Risk |
| --- | --- | --- | --- | --- |
| A. Native runtime/install lane | Inventory can guide runtime-surface work without legacy commands. | Verify current Arcanum native skill/runtime surfaces and produce a target-repo install handoff. | Strongly aligned with latest blocker resolution. | May mostly retest what the smoke already proved. |
| B. Missing-card expansion lane | Inventory exposes useful omissions when used before source search. | Add a focused card slice for a concrete omitted package-level area. | Best for improving Inventory coverage. | Can drift into broad ingestion if not bounded. |
| C. EvidenceSet reuse lane | Candidate EvidenceSets help decide whether a SWU is executable. | Use `evidence-set.whole-arcanum.can-implement-next-swu` before executing one small SWU. | Best test of EvidenceSet value. | Needs a real SWU choice and careful non-promotion language. |
| D. Cross-sigil boundary lane | Inventory preserves authority boundaries across dispersed knowledge. | Test a task that crosses `invoke`, `task-session`, `refine`, and `context-builder`. | Best for Arcanum’s real complexity. | Highest context risk; may need more fallback search. |

## Recommended Route

Choose **C. EvidenceSet reuse lane** for the first live Arcanum test.

Reason: it directly tests the remaining promotion gate. If a candidate
EvidenceSet helps decide and execute a bounded SWU, we get the exact reuse
evidence needed without prematurely promoting EvidenceSets.

## Implementation Layers

| Layer | Goal | Exit Evidence |
| --- | --- | --- |
| L0 | Establish baseline validation and selected task lane. | Validator pass plus decision record. |
| L1 | Run Inventory-first query and capture retrieval packet. | Card/EvidenceSet selection record with exclusions. |
| L2 | Execute one bounded task-session SWU. | Task-session result with files, validation, and reuse evidence. |
| L3 | Synthesize promotion signal. | Recommendation to keep, split, promote later, or reject candidate EvidenceSet. |

## Validation Strategy

Required checks:

```bash
bash arcana/inventory/development/whole-arcanum/scripts/validate-whole-arcanum-inventory.sh
jq empty arcana/inventory/development/whole-arcanum/evidence-sets/evidence-sets.json
jq -r '.cards[] | [.id, .title] | @tsv' arcana/inventory/development/whole-arcanum/cards/*/cards.json
```

Task-specific checks are chosen after the decision gate selects the first lane.

## Next Route

Run `task-session` against `LIVE-ARCANUM-TEST-WORK-PACK.md` after
`DECISION-LIVE-ARCANUM-TEST.md` resolves `B-LAT-001`.
