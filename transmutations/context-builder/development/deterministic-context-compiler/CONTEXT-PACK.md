# Context Pack: Deterministic Context Compiler

## Context Pack Summary

- Task: define, design, and plan deterministic Context Builder compilation and context reuse
- Mode: standard
- Files selected: 7
- Snippets selected: 15
- Obligation coverage: 100 percent
- Noise ratio: 0 selected items without an obligation
- Output markdown: this file
- Output index: `CONTEXT-INDEX.json`
- Handoff pack: none
- Session evidence path: none; this is an Invoke authoring input
- Strict coverage: pass
- Blockers: 0

## Obligations

| ID | Obligation | Status |
| --- | --- | --- |
| O-01 | Preserve selector-level, obligation-linked evidence. | covered |
| O-02 | Persist reusable context without making the cache authoritative. | covered |
| O-03 | Make identical admitted inputs produce byte-identical compiled outputs. | covered |
| O-04 | Detect selected-source drift with per-source content hashes. | covered |
| O-05 | Reduce model-side discovery and assembly work without claiming that stored bytes are free to read. | covered |
| O-06 | Preserve strict coverage, explicit blockers, authority precedence, and session-evidence boundaries. | covered |
| O-07 | Measure token effects honestly and keep provider/runtime accounting separate. | covered |
| O-08 | Keep the public package generic and exclude consumer-private evidence. | covered |

## Included Context

- `transmutations/context-builder/SKILL.md`
  - Selectors: flags, handoff-pack contract, process, quality bar, anti-patterns
  - Obligations: O-01, O-02, O-04, O-06
  - Why: canonical behavior and authority boundary for the target sigil
- `transmutations/context-builder/README.md`
  - Selectors: problem, output, handoff schema, Transmutation rationale
  - Obligations: O-01, O-05, O-06
  - Why: human-facing target contract
- `transmutations/context-builder/templates/runtime-handoff-pack.md`
  - Selectors: obligation coverage, selected sources, provenance, output paths
  - Obligations: O-01, O-04, O-06
  - Why: current human-readable output shape
- `transmutations/context-builder/templates/runtime-handoff-index.json`
  - Selectors: identity, obligations, selected sources, gaps, output paths
  - Obligations: O-01, O-03, O-04, O-06
  - Why: current machine-readable output shape
- `benchmark/development/refinement-runs/20260527T085305Z-benchmark/context-builder/context-index.json`
  - Selectors: identity, obligations, selected sources, excluded candidates
  - Obligations: O-03, O-04, O-05
  - Why: first public repeat of the same benchmark target
- `benchmark/development/refinement-runs/20260527T091133Z-benchmark/context-builder/context-index.json`
  - Selectors: identity, obligations, selected sources, excluded candidates
  - Obligations: O-03, O-04, O-05
  - Why: second public repeat of the same benchmark target
- `benchmark/development/refinement-runs/20260527T093001Z-benchmark/context-builder/context-index.json`
  - Selectors: identity, obligations, selected sources, excluded candidates
  - Obligations: O-03, O-04, O-05
  - Why: third repeat selected one additional source despite the same recorded repository revision and obligation count

## Evidence

- The canonical folder contains contracts and templates but no deterministic compiler.
- The three public benchmark indexes record the same repository revision and nine obligations.
- Two benchmark packs select 11 sources; the third selects 12.
- The three index files and three Markdown packs have distinct content hashes.
- Current provenance permits a content hash or Git SHA, but the machine template does not require one hash per selected excerpt.

## Inference

- A deterministic compiler can remove repeated model work for hashing, selector extraction, deduplication, ordering, rendering, and structural validation.
- A content-addressed cache can reuse exact excerpt bytes when every selected-source binding is current.
- Neither disk persistence nor a cache handle lets a model reason over omitted content. Runtime prompt reduction requires a smaller injected payload, lazy retrieval, or a proved base-pack binding.
- Semantic obligation formation and evidence-sufficiency judgment should remain outside the deterministic kernel.

## Excluded Candidates

- Consumer-local telemetry: excluded from the public package because it is execution evidence, not reusable public source.
- Consumer-local Inventory entries: lookup informed the authoring pass, but private read-model paths and prose are not copied into public Arcanum.
- Provider-specific prompt-cache APIs: excluded because the public design is runtime-neutral.

## Authority Precedence

1. Current `context-builder` canonical contract.
2. Current public templates.
3. Public benchmark evidence.
4. Invoke-authored inference and planned witnesses.

## Next Actions

1. Close Define with an explicit non-authority cache contract.
2. Design the compiler, cache, renderer, adapter boundary, and receipts.
3. Plan the smallest deterministic proof before any sigil contract mutation.
