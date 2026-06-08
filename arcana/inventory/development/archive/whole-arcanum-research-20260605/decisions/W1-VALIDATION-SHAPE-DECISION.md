---
module: inventory-whole-arcanum
version: 0.1.0
status: resolved
updatedAt: 2026-05-29
docType: decision-record
decisionGate: W1-validation-shape
---

# Decision Gate: W1 Validation Shape

## Target Scope

Whole-Arcanum Inventory W1 proof slices, especially:

- `SWU-WAI-003`: Inventory self-slice cards.
- `SWU-WAI-005`: governance cards.
- later family slices that need fast agent validation.

## Consequential Work Blocked

Starting W1 card generation is blocked until the validation shape is explicit.
The current validator checks pilot-style filenames, while W1 write scopes are
slice directories.

## Decision Question

How should W1 evidence-card slices be shaped so task-session can validate them?

## Options

| Option | Description | Benefit | Cost / Risk | Choose When | Downstream Impact |
| --- | --- | --- | --- | --- | --- |
| A. Pilot-compatible slice fixtures | Each slice folder uses the existing expected filenames, such as `pilot-cards.json`, `pilot-index.json`, `pilot-retrieval.json`, and optional `evidence-sets.json`. | Fastest path. Reuses the existing validator with minimal code changes. | The word `pilot` becomes semantically awkward outside the original pilot. Later slices may look like copied fixtures instead of first-class inventory packages. | We want the next SWU to run immediately and accept naming awkwardness for now. | `SWU-WAI-003` can proceed with almost no validator work; later cleanup may rename the contract. |
| B. Slice-aware validator contract | Extend or wrap validation so a slice can provide explicit file paths or conventional names like `cards.json`, `index.json`, `retrieval.json`, and `evidence-sets.json`. | Better long-term shape for whole-Arcanum inventory. Keeps slices first-class and agent-readable. | Requires a small validator task before or inside `SWU-WAI-003`; more moving parts. | We want the whole-Arcanum inventory to establish the reusable slice pattern now. | `SWU-WAI-003` begins by adding a slice validation wrapper/contract, then creates cards. |
| C. Single central collection | Store all W1 cards in one central `cards.json` and use slice tags/index terms rather than separate slice folders. | Simplest query target for agents. Avoids multi-folder validator complexity. | Higher merge/conflict risk, weaker write-scope isolation, harder parallelization. | We prioritize one file for query speed over task-session isolation. | Future parallel slices become harder; work-pack write scopes need revision. |

## Recommendation

Choose **B. Slice-aware validator contract**.

Rationale:

- It preserves the user’s core requirement that Inventory is fast for agents.
- It keeps slice folders meaningful rather than pretending every slice is a
  pilot.
- It supports future parallel W1/L2 work because each slice can validate locally.
- The extra cost is small and belongs naturally at the front of `SWU-WAI-003`.

## Current Status

Resolved by user selection on 2026-05-29.

## Selected Option

**B. Slice-aware validator contract**

User signal: `invoke refresh B`.

Rationale:

- Each whole-Arcanum slice should be first-class and agent-readable.
- Slice-local validation preserves write-scope isolation and future
  parallelization.
- The additional validator wrapper/contract is small and belongs at the front of
  `SWU-WAI-003`.

## Remaining Blockers

| Blocker | Status |
| --- | --- |
| W1 validation shape | resolved |

## Deferred Decisions

| Decision | Status | Revisit Trigger |
| --- | --- | --- |
| EvidenceSet canonical promotion | deferred | After repeated task-session reuse across multiple slices. |
| Human UI | deferred | After agent shell plus `jq` surface becomes hard to inspect manually. |

## Assumptions

- W0 source boundary remains valid.
- W1 should remain candidate-only and should not promote EvidenceSets.
- Schema constitution remains in force for any new machine-readable schemas.
