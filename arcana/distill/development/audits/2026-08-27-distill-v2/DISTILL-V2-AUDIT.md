# Distill v2 Machine-First Audit

- Audit ID: `DISTILL-V2-AUDIT-2026-08-27`
- Date: 2026-08-27
- Mode: Distill `validate`
- Verdict: `block`
- Authority effect: `none`
- Claim ceiling: audit and schema proposal only

## Outcome

Distill is ready to begin a v2 machine-contract design, but it is not ready for
canonical schema authoring yet. The current machine-readable Distill surfaces
belong to Invoke's invocation and evidence adapter. Distill's own semantic
objects remain prose contracts, and several wire choices are not frozen.

The smallest coherent v2 start is not one large result schema and not a copy of
Invoke's schemas. It is one Distill-owned five-contract vertical:

1. contract profile,
2. run source,
3. append-only semantic trace event,
4. substantive result envelope, and
5. exact stage receipt.

That vertical preserves the current authority boundary: Distill owns semantic
meaning and deterministic human projection; Invoke owns invocation, evidence
admission, provenance, and any mutation-handoff decision.

## Why the Audit Blocks

The block is semantic, not procedural. Writing schemas now would silently pick:

- technique IDs (`underscore` versus historical `hyphen` forms),
- exact Tournament, Deep, and Validate budget ceilings,
- execution-path vocabulary and whether `mixed` is a core value,
- exact-reference wire shape (`size` versus `size_bytes`),
- verdict-to-route rules and nullable selected-unit behavior, and
- whether direct and evidence-gated runs share one semantic family.

Those choices affect every producer, fixture, adapter, and generated projection.
They must be selected once before exact schema bytes are frozen.

## Findings

| ID | Severity | Finding | Consequence |
| --- | --- | --- | --- |
| 001 | critical | No Distill-owned schema exists for RunFrame, profiles, semantic trace, or ResultEnvelope. | No exact semantic source/result closure. |
| 002 | high | The existing request schema is an Invoke adapter and omits core Distill inputs. | Schema-valid does not mean Distill-executable. |
| 003 | high | The live request has one stale exact input reference. | Current exact-byte admission is `3/4`, not PASS. |
| 004 | high | Canonical technique IDs use underscores while the request uses hyphens. | Unknown techniques remain schema-valid. |
| 005 | high | The Invoke receipt is not the complete Distill result. | Semantic closure and navigability are unproven. |
| 006 | high | The Invoke semantic validator uses adapter categories and arbitrary technique strings. | Its PASS does not prove the Distill contract. |
| 007 | high | No semantic finalizer produces source, trace, result, Markdown, and receipt atomically. | The v2 production chain is absent. |
| 008 | medium | README, SKILL, and manual examples carry different output detail. | Human views can drift. |
| 009 | medium | Execution-path, exact-ref, and version vocabularies vary by surface. | Compatibility would be inferred by schema authors. |
| 010 | medium | Work Pack and Readiness prose describe different lifecycle moments. | Prose cannot be a single v2 readiness source. |

The machine-readable finding details live in
[`DISTILL-V2-AUDIT.json`](DISTILL-V2-AUDIT.json).

## Existing Machine Evidence That Remains Valid

- The ten inspected Draft 2020-12 schemas are structurally valid.
- The current request is valid against the existing Invoke request schema.
- The runtime-event emitter fail-closes on event shape, identity, ordering,
  execution path, timestamp monotonicity, and stale ledger digest.
- Invoke's runtime evidence remains non-authoritative with respect to the
  Distill verdict.

This evidence should be retained as adapter and compatibility evidence. It does
not substitute for a Distill-owned semantic contract.

## Exact-Reference Check

| Reviewed input | Result |
| --- | --- |
| `DESIGN.md` | PASS |
| `IMPLEMENTATION-LAYERING.md` | PASS |
| `IMPLEMENTATION-PLAN.md` | PASS |
| `WORK-PACK.md` | BLOCK: expected `7ae02e.../8768`, actual `b37763.../8784` |

The stale request was not repaired because it is existing owner work and its
repair does not resolve the v2 semantic schema decisions.

## Proposed Schema Set

| Candidate path | Distill-owned meaning |
| --- | --- |
| `arcanum/arcana/distill/schemas/distill-profile-v2.schema.json` | finite ModeProfile, TechniqueSpec, hooks, objections, overrides, and output version |
| `arcanum/arcana/distill/schemas/distill-source-v2.schema.json` | RunFrame, discovery, exact inputs, lineage, profile binding, and optional evidence context |
| `arcanum/arcana/distill/schemas/distill-trace-event-v2.schema.json` | append-only semantic setup, role, objection, reconciliation, technique, round, and termination events |
| `arcanum/arcana/distill/schemas/distill-result-v2.schema.json` | complete substantive ResultEnvelope with `authority_effect: none` |
| `arcanum/arcana/distill/schemas/distill-stage-receipt-v2.schema.json` | finalizer/schema identity, exact artifact inventory, validation state, and receipt digest |

The exact open choices and recommended defaults are in
[`DISTILL-V2-SCHEMA-DECISIONS.json`](DISTILL-V2-SCHEMA-DECISIONS.json).

## Decision Gate

The deterministic option prefilter admitted four routes and returned `gate`:

| Option | Benefit | Cost or risk | Downstream effect |
| --- | --- | --- | --- |
| `STRICT-V2` (recommended) | Smallest auditable contract: underscore technique IDs only, `true_subagent`/`role_simulation`, one `size_bytes` exact-ref form, one semantic family, current documented mode defaults fixed in the first profile, and strict verdict/route conditions. | New v2 production rejects historical aliases; adapters need explicit projection. | Author five strict schemas, fixtures, and one core profile; preserve old adapters as compatibility-read-only. |
| `COMPATIBILITY-V2` | New v2 production accepts historical hyphenated IDs, display execution labels, exact-ref variants, and bounded profile overrides. | More branches, more negative fixtures, and a larger semantic validator; accidental adapter vocabulary may become permanent. | Author compatibility unions and mappings before the producer/finalizer. |
| `DEFER-SCHEMAS` | No premature wire decision. | v2 implementation remains blocked. | Review the component decisions separately; no schema mutation. |
| `STOP-V2` | Ends the effort without more mutation. | No machine-first Distill v2. | Keep this audit only. |

The request and receipt are
[`DISTILL-V2-SCHEMA-OPTIONS.json`](DISTILL-V2-SCHEMA-OPTIONS.json) and
[`DISTILL-V2-SCHEMA-OPTIONS-RECEIPT.json`](DISTILL-V2-SCHEMA-OPTIONS-RECEIPT.json).
The receipt classifies options only; it is not user consent and authorizes no
schema creation.

## Producer and Consumer Closure Target

```text
direct normalizer or Invoke adapter
  -> DISTILL-SOURCE.json
  -> Distill core with exact DISTILL-PROFILE.json
  -> model-produced semantic trace and result candidates
  -> deterministic Distill finalizer
  -> DISTILL-TRACE.jsonl
  -> DISTILL-RESULT.json
  -> deterministic DISTILL-RESULT.md
  -> DISTILL-STAGE-RECEIPT.json
  -> direct consumer or Invoke-owned adapter projection
```

The future finalizer may validate, bind, render, and publish atomically. It must
not invent Proposer/Balancer semantics or convert runtime evidence into a
substantive verdict.

## Repair Order

1. Select the open decisions in the decision record.
2. Add the five schemas and one canonical public profile instance.
3. Add positive and mutation-negative schema fixtures.
4. Add cross-artifact semantic validation and a deterministic atomic finalizer.
5. Wire direct Distill production.
6. Add separately versioned Invoke v2 projections and prove direct/invoked consumers.
7. Derive Markdown mechanically, then selectively regenerate native mirrors.
8. Update v2 readiness only after compatibility and terminal validation pass.

## Distill Result

- Target context: public Arcanum Distill capability, semantic v2 contract.
- Objective and output artifact: audit Distill and identify the first machine-first v2 artifact family; machine audit plus owner-decision surface.
- Mode and budget: Validate; one Balancer-led bounded review.
- Proposal tracks: one proposal, independently balanced.
- Recursive rounds: one completed.
- Verdict: `block` for canonical schema authoring.
- Role conversation trace: Proposer suggested the Invoke source/profile/result pattern; Balancer separated semantic ownership from Invoke adapter authority and required an explicit semantic trace plus stage receipt; reconciliation selected a five-contract vertical.
- Current smallest coherent unit: profile + source + semantic trace + result + stage receipt.
- Optimization point: all five are needed to bind meaning, reasoning history, exact bytes, and a deterministic human view without moving Invoke authority.
- Concept layer map: Distill v2 capability -> semantic machine contract -> five-contract vertical -> deterministic finalizer -> direct/Invoke consumers.
- Technique pack trace: abstraction-level guard PASS; recomposition proof PASS; evolution profile PASS; frame-expiry PASS; cognitive-load check FLAG; requisite-variety PASS; boundary-object check PASS; concept-vs-knowledge PASS; premortem BLOCK without decision freeze; navigable-result PASS.
- Closure and recomposition proof: the five contracts close semantic input, policy, trace, output, and exact production; they recompose into direct execution and separately owned Invoke projections.
- Evolution profile: new modes, techniques, and adapters can version through the profile and adapter namespaces without rewriting old receipts.
- Deferred complexity: finalizer implementation, canonical profile instance, Invoke v2 adapters, generated mirrors, and readiness promotion.
- Tension ledger: version is user-directed as v2; ownership, identifiers, budgets, wire vocabulary, verdict routing, and evidence-family choices remain open.
- Premortem: the likely failure is freezing a superficially tidy schema that encodes accidental adapter vocabulary; guardrail is one owner-selected decision set before schema bytes.
- Frame-expiry note: rerun this audit if Distill's ownership boundary, mode family, technique registry, or accepted evidence backend changes.
- Navigation guide: start with the decision JSON, then author the schema set in listed order; do not begin with adapters or generated mirrors.
- Evidence emission: not-required; this audit is repository evidence, not a Distill execution-evidence handoff.
- Telemetry: not configured; no telemetry authority claimed.
- Next route: decision-gate, then schema implementation.

## Authority Limits

This audit does not request or grant acceptance, execution, publication,
deployment, registry promotion, generated mirror synchronization, or external
effect. No canonical Distill v2 schema has been authored yet.
