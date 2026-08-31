# TASK-DV2-FINALIZER — Semantic Validation And Atomic Publication

## Objective

Turn model-produced semantic candidates into one validated, deterministic,
digest-bound bundle without inventing reasoning or verdict semantics.

## SWU-DV2-024

Behavior: implement cross-artifact semantic validation.

Write scope: Distill-owned semantic validator, fixtures, and focused tests.

Acceptance: enforce the ten invariants in `../SCHEMA-PLAN.md`; reject trace
ordering, budget, hook, omission, contradiction, evidence-authority, and
result-erasure mutations. Adapter vocabulary is not accepted as canonical semantics.

## SWU-DV2-025

Behavior: deterministically render Markdown and atomically publish the exact family.

Write scope: Distill-owned renderer/finalizer, atomicity/determinism fixtures, and tests.

Acceptance: two isolated runs are byte-identical; receipt binds exact schemas,
profile, source, trace, result, Markdown, and finalizer identity; injected failure
at every boundary publishes no partial candidate and preserves prior bytes.

## Authority Ceiling And Successor

The validator/finalizer may reject, bind, render, inventory, and publish a
semantic bundle. It may not create role claims, resolve tensions, select a unit,
choose a verdict, or convert runtime evidence into semantics. Successor: SWU-DV2-026.
