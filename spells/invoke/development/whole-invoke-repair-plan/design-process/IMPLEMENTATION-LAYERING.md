---
title: Invoke Design Production Implementation Layering
status: draft
updatedAt: 2026-08-27
owner: invoke-design
scope: capability
---

# Invoke Design Production Implementation Layering

## Context

- Target: Invoke Design source-to-bundle production.
- Current state: W1 input closure/selection, W2 coherent candidate production,
  and W3 deterministic bundle/replay admission are implemented; W4 mirror and
  aggregate package closure are not.
- Primary operator: Design author and downstream Plan owner.
- Primary constraint: prevent locally valid Design outputs from accumulating
  into an incoherent architecture.
- Source references: `spells/invoke/design.md`, the existing three Design
  selection schemas, `SWU-WIR-007`, and the Whole-Invoke validation strategy.

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether the complete Design production contract is structurally expressible without duplicate authority. | Twenty-two schema-valid contracts, canonical process/profile/policy instances, and positive/negative fixture families. | Schema meta-validation, self-digest validation, and focused fixture PASS. | Continue only if every artifact has one owner and every edge has an exact binding. |
| L1 | After this layer, we know whether Design inputs can close scope without omission or parallel-manifest drift. | One exact `DESIGN-INPUT-CLOSURE.json` through independent closure validation, deterministic scope projection, and existing denominator extraction. | Closure receipt, input/scope equality, stale-input negatives, prior-Design determination, and no output on block. | Continue only on total input coverage. |
| L2 | After this layer, we know whether one proposed architecture can be proven coherent across all inputs and six views. | One `DESIGN-SOURCE.json` through deterministic candidate projection, independent semantic coherence validation, and atomic three-file candidate closure. | Cross-view, ownership, preserved-invariant, selection, glossary, determinism, and no-publication-on-block fixtures. | Continue only on digest-bound coherence PASS; evolution requires one independently validated L3 predecessor. |
| L3 | After this layer, we know whether the complete candidate Design family can be published atomically and admitted by a real consumer. | Source-to-`DESIGN.json` compiler, deterministic views, final receipt, and capability resolver admission. | Determinism, partial-publication negatives, producer identity, exact inventory, and consumer PASS. | Continue only if generic self-assertion is impossible. |
| L4 | After this layer, we know whether the producer remains compatible and reusable across host mirrors and the reachable Invoke suite. | Historical-read compatibility, selective mirror sync, aggregate validation, and fresh generic fixture. | Byte parity, public-boundary scan, aggregate blocker accounting, and changed-path receipt. | Close the Design slice or route exact residual blockers. |

## Non-Regression Guardrails

- Existing manifest, denominator, and selection behavior remains unchanged.
- Planned witnesses never become executed Plan evidence.
- Schema or producer PASS opens only `artifact_authored`.
- No layer mutates upstream Define outputs or prior Design artifacts.
- Later layers preserve L0 schema identities and add versions rather than
  silently widening v1 contracts.

## Recommended Next Layer

L4 is the next layer. W3 now proves deterministic human views, v2 stage closure,
independent replay admission, capability `artifact_authored`, and one genuine
evolution predecessor. Selective generated-package synchronization, aggregate
Design-slice evidence, and final compatibility closure remain deferred.
