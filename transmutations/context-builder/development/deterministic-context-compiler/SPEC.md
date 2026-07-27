---
artifact: deterministic-context-compiler
artifact_type: sigil-extension-spec
target_sigil: context-builder
status: invoke-authored
define_gate: pass
discovery: waived
discovery_waiver_reason: same-thread manual maintenance reflection already fixed the bounded public target and evidence gap
lifecycle_owner: sigil-development
implementation_authority: none
---

# Deterministic Context Compiler

## Purpose

Add a deterministic, runtime-neutral compilation boundary around Context
Builder so exact source excerpts can be validated, deduplicated, reused, and
rendered without asking a model to repeat mechanical repository work.

The compiler improves cost and reproducibility. It does not decide canonical
meaning, approve evidence, or make omitted content available to a model.

## Problem

Context Builder currently defines a strong selector-level and
obligation-linked contract, but the canonical package contains no deterministic
software that enforces the selection manifest, hashes each selected source,
reuses exact excerpts, or records tokenizer/runtime accounting.

Public benchmark runs for the same recorded revision and nine obligations
produced different output hashes and selected-source counts. This is a
reproducibility and cost hypothesis, not proof that the current sigil is
incorrect.

## Scope

Included:

- a typed context request and candidate-evidence manifest;
- exact source and selector snapshot validation;
- a content-addressed excerpt cache;
- deterministic deduplication and cost-aware covering-set selection;
- stable Markdown, JSON/index, and compact runtime-payload rendering;
- stale-input, ambiguity, budget, and uncovered-obligation blockers;
- explicit token-measurement and runtime-usage receipts;
- deterministic fixtures plus live runtime comparison evidence;
- a later bounded update to the Context Builder contract and templates.

Excluded:

- interpreting unconstrained user prose without a model or human;
- deciding whether evidence is semantically sufficient or authoritative;
- promoting Inventory entries, definitions, ontology, sigils, or spells;
- provider-specific prompt-cache integration;
- hiding required evidence behind a path or hash the runtime cannot resolve;
- treating cached content as canonical or reusable session evidence;
- implementation or contract mutation during Invoke authoring.

## Actors And Owners

| Owner | Responsibility |
| --- | --- |
| Context author | Produces the typed obligation and candidate mapping. |
| Deterministic compiler | Validates, snapshots, deduplicates, selects, renders, and receipts admitted inputs. |
| Runtime adapter | Injects one admitted payload and returns actual usage evidence when available. |
| Inventory | Supplies non-authority candidate handles and source references. |
| Sigil Development | Owns any approved Context Builder contract mutation and reusable-behavior validation. |
| Task Session | Executes one explicitly selected implementation SWU. |

## Functional Requirements

| ID | Requirement |
| --- | --- |
| FR-01 | Accept a schema-valid request containing stable obligation IDs and pre-mapped evidence candidates. |
| FR-02 | Resolve every selected file and selector inside the repository boundary and bind it to exact source bytes. |
| FR-03 | Compute a cache key from schema version, normalizer version, source digest, selector, excerpt policy, and public/private policy. |
| FR-04 | Store cached excerpts as non-authority generated objects and revalidate source bindings before reuse. |
| FR-05 | Deduplicate byte-identical excerpts while preserving all obligation references. |
| FR-06 | Select a covering set through a documented deterministic policy with stable lexical tie-breaking. |
| FR-07 | Block when any obligation is uncovered, any required selector is missing or ambiguous, or any selected source is stale. |
| FR-08 | Render byte-stable Markdown, JSON/index, compact runtime payload, and validation receipt from the admitted manifest. |
| FR-09 | Persist both human and machine evidence when required, while the runtime adapter injects exactly one declared payload. |
| FR-10 | Permit base/delta reuse only when a runtime receipt proves the base pack is already available. |
| FR-11 | Record bytes always; record token counts only with a declared tokenizer; record actual prompt usage only from a runtime receipt. |
| FR-12 | Keep cache objects, consumer bindings, and private evidence outside the public canonical package. |

## Determinism Contract

The deterministic claim is bounded to:

```text
same compiler version
+ same normalized request manifest
+ same selected source bytes
+ same selector and excerpt policy
+ same tokenizer configuration when present
= same object hashes, selected set, rendered bytes, and receipt digest
```

It does not claim deterministic semantic interpretation, model output, provider
billing, or authority.

## Failure Contract

| Condition | Result |
| --- | --- |
| Request schema invalid | block before cache access |
| Path escapes repository root | block |
| Selector missing or ambiguous | block |
| Source or excerpt digest mismatch | block and do not reuse |
| Required obligation uncovered | block |
| Budget exceeded with no legal covering set | block |
| Tokenizer unavailable | continue with bytes and `token_measurement=not_available` |
| Runtime usage receipt unavailable | keep `actual_prompt_tokens=unknown` |
| Cache unavailable or corrupt | rebuild from current source or block if rebuild cannot validate |
| Base pack unproved | emit full admitted payload |

## Acceptance Criteria

- Identical fixture inputs reproduce exact object, pack, and receipt hashes.
- A changed selected source invalidates the affected object and pack.
- An unrelated source change does not alter the compiled pack.
- Missing, ambiguous, escaping, and stale selectors fail closed.
- Duplicate excerpts appear once with multiple obligation references.
- Markdown, JSON/index, and runtime payload agree on obligations, sources, and blockers.
- Runtime injection evidence proves that only one payload representation was sent.
- Token claims distinguish bytes, tokenizer counts, cached-provider accounting,
  and actual runtime input tokens.
- Public fixtures contain no consumer-private paths or prose.
- Live comparison measures Context Builder authoring/runtime usage before any
  token-reduction claim is promoted.

## Evidence Ceiling

This specification proves only an Invoke-authored target contract. Planned
fixtures are not executed Plan evidence. It does not prove implementation,
token savings, reusable behavior, registry release, runtime readiness, or
promotion.

## Next Owner

Invoke Design owns the architecture and planned witness contracts. Invoke Plan
owns layering and SWUs. Sigil Development remains the next lifecycle owner
after this authoring package passes its gates.
