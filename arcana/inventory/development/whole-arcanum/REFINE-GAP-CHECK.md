---
module: inventory-whole-arcanum
version: 0.1.0
status: resolved-by-decision
updatedAt: 2026-05-29
docType: refine-gap-check
refinePreset: compact
research: no-research
---

# Refine Gap Check: Whole Arcanum Inventory

## Verdict

No blocker currently prevents the next Task Session from starting W1.

The W1 validation-shape gap was resolved by selecting **B. Slice-aware validator
contract** in `decisions/W1-VALIDATION-SHAPE-DECISION.md`.

W0 passed: `source-manifest.json` and `SOURCE-POLICY.md` establish the source
boundary, generated/local runtime exclusions, and durable evidence promotion
rule. The next execution can proceed as long as W1 stays inside the declared
write scopes.

## Non-Blocking Gaps

| Gap | Severity | Why It Matters | Recommended Handling |
| --- | --- | --- | --- |
| Validator fixture shape is pilot-named | resolved | `validate-evidence-card-fixtures.sh` expects files such as `pilot-cards.json`, `pilot-index.json`, and `pilot-retrieval.json`. W1 write scopes are `cards/inventory/`, `cards/governance/`, and `cards/lifecycle/`, so a worker could create valid cards in a shape the current validator does not inspect. | Selected option B: add or wrap slice-aware validation for conventional slice files such as `cards.json`, `index.json`, `retrieval.json`, and optional `evidence-sets.json`. |
| W1 card count is not explicit | low | The task says cards should cover schema, validator, retrieval, and boundaries, but does not name the minimum proof set. | Use a minimum of four Inventory self-slice cards: schema contract, validator runtime, retrieval/index behavior, downstream authority boundary. |
| EvidenceSet query is only explicit for cross-pilot | low | `TASK-WAI-003` names a realistic cross-pilot question; `TASK-WAI-002` only says "query example." | For `SWU-WAI-004`, use the query: "What source context does an agent need before adding the next Inventory card slice?" |
| Candidate durable evidence promotion remains conservative | low | The policy is correct, but W1 workers may need to cite task-session result/context files. | Include only `TASK-WAI-001-RESULT.md` and `TASK-WAI-001-CONTEXT.md` when they directly justify the source boundary. |

## Blocker Check

| Gate | Status | Notes |
| --- | --- | --- |
| Source boundary before cards | pass | W0 synchronized and validated. |
| Generated/local runtime exclusion | pass | Policy excludes runtime, generated run output, observability ledgers, benchmark artifacts/logs, `output/`, and `tmp/`. |
| EvidenceSet promotion | deferred | Not blocking; W1 uses candidate sets only. |
| Human UI | deferred | Not blocking; agent shell plus `jq` remains the runtime surface. |
| Schema constitution | pass | W1 should not create new schemas; if it does, they must be `.schema.yml`. |

## Refined Next Step

Run `task-session` on `SWU-WAI-003` first.

Execution note for `SWU-WAI-003`:

- write under `arcana/inventory/development/whole-arcanum/cards/inventory/`,
- create a slice-aware validator contract or wrapper for conventional slice
  filenames,
- include at least the four proof cards listed above,
- record any selector that would require broad full-file ingestion as a selector
  gap rather than expanding scope.
