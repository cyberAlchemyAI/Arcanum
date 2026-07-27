---
module: deterministic-context-compiler
version: current
status: plan-authored
updatedAt: 2026-07-27
docType: implementation-layering
active_layer: L0
lifecycle_owner: sigil-development
---

# Implementation Layering: Deterministic Context Compiler

## Purpose

Sequence implementation so each layer answers one decision before broader
selector support, measurement, reuse, or canonical integration is admitted.

## Source Contract

- Define contract: [SPEC.md](SPEC.md)
- Design contract: [ARCHITECTURE.md](ARCHITECTURE.md)
- Planned witnesses: [WITNESS-CONTRACTS.md](WITNESS-CONTRACTS.md)
- Canonical target: `transmutations/context-builder/`

## Target And Scope

- Target: Context Builder deterministic compiler extension
- Scope: reusable sigil behavior, deterministic tooling, and evidence
- Current state: specified and designed; not implemented

## Layer Boundary Rule

Every layer ends with:

```text
After this layer, we know whether the named decision is supported by the
declared evidence; we do not infer later-layer readiness.
```

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether one typed selector can be compiled and replayed exactly against current source bytes. | Request and receipt schemas, one exact Markdown selector, one content-addressed object, one payload, one receipt. | SWU-DCC-001 and SWU-DCC-002; schema validation; in-root snapshot; stale-source negative; byte-identical replay. | Multi-candidate selection, format parity, tokenizer support, delta reuse, live evidence, canonical contract changes. | DCC-FIX-001, DCC-FIX-003, DCC-FIX-006 and exact output digests. | Continue to L1 only if replay and negative fixtures pass. |
| L1 | After this layer, we know whether deterministic multi-candidate selection and output parity are credible. | A repeatable covering-set compile with deduplication and one runtime payload. | SWU-DCC-003 and SWU-DCC-004; stable tie-breaking; duplicate collapse; Markdown/JSON/payload parity; injection contract. | Actual runtime token claims, base/delta reuse, live comparison, canonical integration. | DCC-FIX-002, DCC-FIX-004, DCC-FIX-005, DCC-FIX-007, DCC-FIX-008, DCC-FIX-011, DCC-FIX-012. | Harden only if coverage, ordering, blockers, and parity pass. |
| L2 | After this layer, we know whether measurement labels, cache invalidation, and base/delta governance hold. | Evidence-separated token accounting plus exact cache and base-pack proof. | SWU-DCC-005 and SWU-DCC-006; named tokenizer counts; unknown runtime usage; stale/corrupt cache behavior; proved base requirement. | Provider-specific cache integration, cache cleanup policy, canonical sigil mutation. | DCC-FIX-009, DCC-FIX-010, cache corruption mutants, receipt schema validation. | Proceed to live evidence only if no estimate is mislabeled and stale reuse fails closed. |
| L3 | After this layer, we know whether reusable behavior and a bounded canonical Context Builder update are supportable. | Paired baseline/candidate experiment followed by lifecycle-owned integration. | SWU-DCC-007 and SWU-DCC-008; coverage parity; actual usage where available; public hygiene; canonical contract update. | Provider-specific optimization, automatic promotion, consumer-specific adapters, production-readiness claims. | Experiment receipts, reusable-behavior evidence, public package checks, lifecycle-owner receipt. | Sigil Development decides integrate, narrow, or defer; execution evidence alone does not authorize release. |

## Non-Regression Guardrails

- Later layers preserve L0 source freshness, in-root path, and byte-stability
  guarantees.
- Cost reduction cannot lower obligation coverage or omit authority-critical
  evidence.
- Bytes, tokenizer counts, provider-cache accounting, and actual runtime usage
  remain separate fields and claims.
- Cache objects stay disposable, consumer-local, and non-authoritative.
- Full payload remains the fallback whenever a runtime base receipt is absent.
- Canonical contract mutation occurs only in L3 through Sigil Development.
- Generated evidence cannot become lifecycle, registry, publication, or
  promotion authority.

## Recommended Next Layer

- Next layer: L0
- First candidate SWU: `SWU-DCC-001`
- Selected SWU: `none`
- Key decision unlocked: whether the request/snapshot/receipt contracts fail
  closed before a compiler implementation is trusted
- Major deferred scope: selection optimization, token claims, delta reuse, and
  canonical integration

## Gate Result

- Status: pass
- Evidence ceiling: layering and sequencing only
- Execution admission: blocked until Sigil Development accepts the handoff and
  one SWU is explicitly selected
