---
docType: refine-seed-proposal
target: benchmark
status: seed-ready-runtime-blocked
preset: standard
researchMode: research-if-gap-appears
updatedAt: 2026-05-27
---

# Refine Seed Proposal: Validate Refine/Distill/Invoke Against Benchmark Evidence

## Target

Refine the idea of using `refine`, `distill`, and `invoke` as the validation workflow for the completed benchmark harness under `benchmark/`.

The benchmark work-pack has already completed its smoke-test path across:

- fixture-local run kernel,
- Docker/local mirror run,
- official SWE-bench Lite smoke,
- SmellBench official smoke,
- PerfCodeBench official smoke,
- campaign report and dashboard API closure.

This refinement must not reopen benchmark implementation. It should define how the completed benchmark evidence becomes a validation corpus for Arcanum authoring tools.

## Source Context

Primary local evidence:

- `benchmark/WORK-PACK.md`
- `benchmark/DISTILL-OPTIMIZATION.md`
- `benchmark/DESIGN-INTERROGATION.md`
- `benchmark/work-pack/tasks/TASK-VERIFY.md`
- `benchmark/artifacts/verification-traceability-audit/report.md`
- `benchmark/artifacts/invoke-refine-benchmark-plan-envelope.json`
- `benchmark/package.json`

## Write Scope

Allowed:

- Add this refinement run under `benchmark/development/refinement-runs/20260527T000000-refine-distill-invoke-benchmark/`.
- Record blocked command execution evidence and dry-run command-surface evidence.
- Produce non-executed validation design and next-route recommendations.

Not allowed:

- Mutate benchmark source code.
- Recompute benchmark score claims.
- Promote dry-run Arcanum outputs as semantic command execution.
- Rewrite completed benchmark work-pack status.

## Core Idea

Use the benchmark smoke-test corpus as a regression target for Arcanum authoring tools:

1. `refine` should turn a vague validation intent into a ten-stage auditable run with a manifest, evidence index, blocked fields, and final synthesis.
2. `distill` should select the smallest coherent validation unit from the benchmark evidence without collapsing the whole harness into one broad claim.
3. `invoke` should produce define/design/plan artifacts for a validation campaign that preserve benchmark evidence authority, traceability, and non-reexecution boundaries.

## Proposed Validation Unit

**Benchmark Evidence Validation Corpus**

Responsibility: use completed benchmark smoke evidence as fixed input cases for validating Arcanum tool behavior.

Inputs:

- completed benchmark work-pack and task records,
- score artifacts for SWE-bench Lite, SmellBench, and PerfCodeBench,
- campaign/dashboard reports with zero evidence gaps,
- prior invoke/distill/interrogation envelopes from benchmark planning.

Outputs:

- refine run manifest and evidence index,
- distill selected-unit artifact,
- invoke define/design/plan artifacts,
- interrogation verdicts,
- validation report comparing generated artifacts against benchmark invariants.

## Benchmark Invariants

The validation workflow must preserve these invariants:

- Official benchmark score artifacts remain the score authority.
- `fail` from an official completed benchmark run is not an infra failure.
- Local fixture evidence cannot be promoted as upstream benchmark support.
- SmellBench and PerfCodeBench score claims require upstream-derived raw result evidence.
- Closure validation may summarize or replay reporting, but must not recompute benchmark outcomes.
- Campaign and dashboard evidence gaps must remain zero for promoted score claims.

## Done Criteria

A full future run passes when:

- all command-backed stages execute through `tools/arcanum --exec` without runtime adapter failure,
- the refine manifest contains all ten canonical stages,
- `distill` identifies the Benchmark Evidence Validation Corpus or a narrower justified unit,
- `invoke define/design/plan` produces validation artifacts without mutating benchmark implementation status,
- final interrogation either passes the validation campaign or records precise gaps,
- the result recommends `task-session` only for an approved validation implementation task.

## Validation Surface

Deterministic checks:

- `tools/arcanum --resolve refine`
- `tools/arcanum --resolve context-builder`
- `tools/arcanum --resolve invoke`
- `tools/arcanum --resolve interrogation`
- `tools/arcanum --resolve distill`
- JSON parse checks for `evidence-index.json`
- path existence checks for all referenced artifacts

Runtime checks:

- full `tools/arcanum --exec` stage execution after adapter repair,
- optional `npm test`, `npm run report:campaign`, and `npm run smoke:dashboard-api` only if the validation task needs fresh closure proof.

## Research Decision

Mode: `research-if-gap-appears`.

Decision: no external research for this seed. The benchmark evidence and local command contracts are sufficient to define the validation campaign. External comparison should only be considered if a later interrogation names a specific benchmark-validation standard gap.

## Planned Stage Configuration

Use the canonical refine loop:

1. Context Builder evidence baseline.
2. Invoke Define.
3. Interrogation using `refine-review`.
4. Research decision.
5. Distill.
6. Invoke Redefine / Design.
7. Interrogation using `refine-design-review`.
8. Distill Repair.
9. Invoke Plan.
10. Final Interrogation and Refine-owned synthesis.

Current status: command resolution succeeds, but semantic stage execution is blocked by the runtime adapter.
