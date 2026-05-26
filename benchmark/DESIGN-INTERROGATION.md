---
docType: interrogation-review
target: benchmark architecture and TASK-004 refinement
status: flag
updatedAt: 2026-05-25
---

# Design Interrogation: Benchmark Evidence Bridge

## Target Scope

Review the refined benchmark design after official SWE-bench Lite evidence and the Distill pass that selected the **Benchmark Evidence Bridge** as the L2 optimization point for SmellBench and PerfCodeBench.

## Mode

Evidence-backed design readiness review.

## Questions Asked

No user-facing blocker question was needed. The review used the current design, layering, work-pack, W2 wave, TASK-004 contract, and current public benchmark references.

## Findings

### Finding 1: Upstream Contract Probes Are Now The Correct Gate

Verdict: pass.

The refined design no longer assumes SmellBench or PerfCodeBench are installable, runnable, or shaped like SWE-bench. `TASK-004` now requires contract probes before scoring smokes, which is the right correction after the SWE-bench result-layout lesson.

Evidence:

- `ARCHITECTURE.md` defines `BenchmarkContractProbe`, `CandidateManifest`, `UpstreamResultImport`, and score-authority rules.
- `TASK-004.md` splits SmellBench and PerfCodeBench into `007A/007B` and `008A/008B`.
- `WORK-PACK.md` marks only contract probes as ready; scoring smokes remain blocked until benchmark-specific blockers resolve.

### Finding 2: Design Correctly Separates Benchmark Failure From Infra Failure

Verdict: pass.

The design preserves the official SWE-bench distinction: an upstream unresolved score is a valid `fail`, while missing runner, missing candidate artifact, noisy worker, or unavailable release artifact is `infra-fail`, `quarantined`, or a block record.

Evidence:

- `ARCHITECTURE.md` adds runner-unavailable, candidate-missing, and performance-noise compensation paths.
- `TASK-004.md` requires score artifacts derived only from raw upstream result files.

### Finding 3: SmellBench Scoring Is Still A Contract Risk

Verdict: flag.

The design identifies SmellBench dimensions: repair effectiveness, false-positive identification, and net codebase impact. It does not yet know whether the release artifact exposes a canonical runner/result file that can produce those dimensions directly. This is acceptable only because `SWU-HARNESS-007A` is explicitly a contract probe.

Required guard:

- `SWU-HARNESS-007A` must not be marked complete unless it records the exact command/result surface or a precise unavailable-artifact block.

### Finding 4: PerfCodeBench Requires A Worker Decision Before Score Claims

Verdict: flag.

The design says PerfCodeBench needs correctness, runtime, baseline/reference metadata, repetition count, threshold, and noise status. It also says performance runs need deterministic worker constraints. The missing decision is not design-level architecture; it is runtime provisioning. The plan correctly keeps `SWU-HARNESS-008B` blocked until `SWU-HARNESS-008A` plus worker/profile decision.

Required guard:

- A local laptop/shared daemon score must not be promoted as PerfCodeBench benchmark evidence unless the contract probe proves that profile satisfies benchmark constraints.

### Finding 5: Candidate Leakage Guard Is Now Explicit

Verdict: pass.

The design now prohibits gold/reference solutions in candidate manifests and explicitly requires redaction from agent paths. This addresses the leakage risk discovered while preparing the SWE-bench smoke metadata.

Evidence:

- `ARCHITECTURE.md` adds R-007 and boundary rules forbidding gold/reference exposure.
- `TASK-004.md` forbids gold patches, reference optimized code, and local fixture substitutes as benchmark evidence.

## Decisions Recorded

| Decision | Status | Rationale |
| --- | --- | --- |
| Use Benchmark Evidence Bridge as L2 architecture unit. | accepted | Small enough to execute, large enough to preserve upstream evidence authority. |
| Split each remaining benchmark into contract probe then real smoke. | accepted | Prevents unverified upstream assumptions from becoming adapters. |
| Keep SmellBench/PerfCodeBench score smokes blocked until contract probes resolve. | accepted | Avoids local substitutes and avoids false benchmark support claims. |
| Treat official/raw upstream output as score authority. | accepted | Matches SWE-bench implementation evidence. |

## Remaining Ambiguities

- Whether SmellBench's release artifact contains a runnable scoring harness or only data/scripts requiring reconstruction.
- Whether PerfCodeBench's public artifact is accessible, complete, and runnable from this environment.
- Which worker profile is acceptable for PerfCodeBench score evidence.

## Verdict

Flag, not block.

The refined design is ready for contract-probe execution. It is not ready for SmellBench or PerfCodeBench scoring smoke execution until `SWU-HARNESS-007A` and `SWU-HARNESS-008A` resolve their benchmark-specific blockers.

## Next Step

Run `task-session` on either:

- `SWU-HARNESS-007A` for SmellBench contract probing, or
- `SWU-HARNESS-008A` for PerfCodeBench contract probing.

---

# Readiness Interrogation: Benchmark Integration Inventory

## Target Scope

Review whether the benchmark work-pack is ready after adding explicit references and per-benchmark implementation inventory for SWE-bench, SmellBench, and PerfCodeBench.

## Mode

Readiness review with evidence-backed questioning.

## Questions Asked

No user-facing question was required. The current artifacts already answer the readiness distinction: contract probes are ready; score smokes are not ready until those probes resolve upstream/runtime blockers.

## Findings

### Finding 1: The Work-Pack Is Ready For TASK-004 Contract Probes

Verdict: pass.

Evidence:

- `WORK-PACK.md` marks `TASK-004` as `ready-contract-probes`.
- `SWU-HARNESS-007A` and `SWU-HARNESS-008A` are marked `ready`.
- `TASK-004.md` now includes source references, implementation steps, outputs, block conditions, and acceptance evidence for both contract probes.

### Finding 2: The Work-Pack Is Not Ready For SmellBench Or PerfCodeBench Score Smokes

Verdict: flag.

This is the intended state, not a defect. `SWU-HARNESS-007B` and `SWU-HARNESS-008B` remain blocked because the upstream scoring surfaces and runtime constraints have not been verified yet.

Required guard:

- Do not run `npm run smoke:smellbench:official` or `npm run smoke:perfcodebench:official` until the matching `A` probe records the runner, raw output files, score semantics, and candidate requirements.

### Finding 3: Benchmark-Specific Steps Are Concrete Enough To Execute

Verdict: pass.

The inventory now names:

- SWE-bench official JSONL and harness flow as the reference pattern.
- SmellBench release, PyExamine relation, scoring dimensions, and block conditions.
- PerfCodeBench release, correctness-first scoring, timing series, worker profile, and noise constraints.

### Finding 4: The Remaining Uncertainty Is Operational, Not Design-Level

Verdict: flag.

The design no longer needs another architecture pass before execution. The unknowns are exactly the ones the probes are meant to discover:

- whether SmellBench release artifacts are runnable and score-bearing,
- whether PerfCodeBench artifacts are accessible and complete,
- whether a deterministic worker profile can be accepted for PerfCodeBench evidence.

## Decisions Recorded

| Decision | Status | Rationale |
| --- | --- | --- |
| Treat the pack as ready for `SWU-HARNESS-007A` and `SWU-HARNESS-008A`. | accepted | The contract-probe work has explicit references, outputs, and block criteria. |
| Keep `SWU-HARNESS-007B` and `SWU-HARNESS-008B` blocked. | accepted | Running smokes before contract probes would recreate the local-substitute risk. |
| Route through `task-session` next. | accepted | The next work is bounded execution, not more design. |

## Remaining Ambiguities

- SmellBench runnable artifact and score output shape.
- PerfCodeBench runnable artifact and score output shape.
- PerfCodeBench acceptable worker/profile constraints.

## Verdict

Flag, not block.

Everything is ready for the next bounded execution step: contract-probe execution. Everything is not ready for benchmark scoring smokes yet, and the work-pack correctly says so.

## Next Step

Run `task-session` on `SWU-HARNESS-007A` first unless there is a reason to prioritize performance infrastructure. `SWU-HARNESS-008A` can run in parallel or immediately after because both probes are read/probe-oriented and have disjoint artifact paths.
