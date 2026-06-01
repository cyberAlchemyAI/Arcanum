# Runtime Handoff Pack

Session evidence artifact. This pack is evidence for the `20260527T093001Z-benchmark` refinement run and is not a canonical benchmark planning document.

## Identity

- Task/SWU: `benchmark-refine-distill-invoke-validation-context`
- Source task/work-pack: `benchmark`
- Session/run id: `arcanum-context-builder-20260527T093339Z`
- Session evidence path: `benchmark/development/refinement-runs/20260527T093001Z-benchmark/context-builder`
- Runtime handoff: `runtime`
- Repository revision: `93a6553d56118eb3a67614aa44ab2773d818f418`
- Evidence date: `2026-05-27`

## Target Task

Build a strict context baseline for refining the idea of using `refine`, `distill`, and `invoke` to validate the Arcanum tool against completed benchmark smoke tests. The downstream runtime may author refinement artifacts, but must not mutate benchmark source files or recompute benchmark scores.

## Obligation Coverage

| Obligation | Status | Selected Evidence | Resolution |
| --- | --- | --- | --- |
| O1 target and output | covered | `benchmark/development/refinement-runs/20260527T093001Z-benchmark/REFINE-SEED-PROPOSAL.md#Target`, `#Source Request`, `#Validation Surface`; `GOAL-HANDOFF.md#Objective` | The output is a context-builder handoff pack for the benchmark refinement run. |
| O2 completed benchmark baseline | covered | `benchmark/WORK-PACK.md#Control Fields`, `#Objective Summary`, `#Task Status Board`, `#Gate Checks`; `benchmark/artifacts/verification-traceability-audit/report.md#Status`, `#Validation`, `#Verdict` | The W0-W3 pilot and closure audit are complete and provide the local evidence baseline. |
| O3 smoke-test evidence surface | covered | `benchmark/WORK-PACK.md#SWU Execution Handoff`; `benchmark/artifacts/campaign-report-smoke/campaign-report.md#Summary`, `#Runs`, `#Evidence Gaps`; `benchmark/artifacts/verification-traceability-audit/report.md#Score Artifacts` | Use persisted smoke/report artifacts as evidence; do not rerun or rescore them. |
| O4 refine loop contract | covered | `arcana/refine/SKILL.md#canonical-loop`, `#stage-dispatch-contract`, `#ownership-boundary`, `#research-policy`; `arcana/refine/REFINEMENT-LOOP.md#Required Local Baseline`, `#Canonical Default Loop`, `#Research Bounds` | Runtime must preserve the ten-stage Refine loop, command-backed stage ownership, local-first research decision, and context-builder-first baseline. |
| O5 invoke authoring boundary | covered | `.codex/commands/invoke.md#Purpose`, `#Mode Contracts`, `#Lifecycle Authority Chain`, `#Target Artifact Provenance` | Invoke may define, design, plan, and hand off; it must not claim benchmark lifecycle completion. |
| O6 distill optimization boundary | covered | `arcana/distill/SKILL.md#objective`, `#modes`, `#process`, `#cycle-guards`, `#complexity-balance`, `#quality-bar` | Distill should choose the smallest coherent validation concept and avoid overbuilt abstractions without a named tension. |
| O7 constraints and non-goals | covered | `benchmark/development/refinement-runs/20260527T093001Z-benchmark/REFINE-SEED-PROPOSAL.md#Source Request`; `benchmark/WORK-PACK.md#Handoff To Execution Pack`; `benchmark/package.json#scripts` | Do not mutate benchmark source; do not recompute scores; recommended next execution inside the closed work-pack is none. |
| O8 runtime validation surface | covered | `benchmark/development/refinement-runs/20260527T093001Z-benchmark/REFINE-SEED-PROPOSAL.md#Validation Surface`; `arcana/refine/SKILL.md#stage-dispatch-contract`; `benchmark/package.json#scripts`; `benchmark/development/refinement-runs/refine-distill-invoke-benchmark-validation-result-4.md#Stage Evidence` | Runtime validation is artifact and command-surface validation, not score recomputation. Previous run context-builder passed, with the first downstream block at Invoke Define. |
| O9 fallback research rule | covered | `arcana/refine/SKILL.md#research-policy`; `arcana/refine/REFINEMENT-LOOP.md#Research Bounds` | External research is not needed for current coverage; only run if a later named gap appears and the user confirms. |

Strict coverage: `pass`

## Selected Sources

- `benchmark/development/refinement-runs/20260527T093001Z-benchmark/REFINE-SEED-PROPOSAL.md`
  - Selectors: `Target`, `Source Request`, `Runtime Configuration`, `Validation Surface`
  - Obligations: O1, O7, O8, O9
  - Evidence excerpt: The run targets `benchmark`, uses preset `standard`, selects `research-if-gap-appears`, asks to refine use of `refine/distill/invoke`, and explicitly says not to mutate benchmark source or recompute benchmark scores.

- `benchmark/development/refinement-runs/20260527T093001Z-benchmark/GOAL-HANDOFF.md`
  - Selectors: `Objective`, `Runtime Mode`, `Stage Dispatch Contract`, `Source Request`
  - Obligations: O1, O4, O8
  - Evidence excerpt: The objective is to run the canonical Refine loop for `benchmark` without recursive Codex execution; root `tools/arcanum` owns stage dispatch.

- `benchmark/development/refinement-runs/20260527T093001Z-benchmark/RUNTIME-HANDOFF.md`
  - Selectors: full short file
  - Obligations: O4, O8
  - Evidence excerpt: The run uses native Refine orchestration through `tools/arcanum`, a `codex-bypass` child stage adapter, and a 600-second stage timeout to prevent nested Codex recursion.

- `benchmark/WORK-PACK.md`
  - Selectors: `Control Fields`, `Objective Summary`, `Delivery Slices`, `Task Status Board`, `SWU Execution Handoff`, `Blockers`, `Gate Checks`, `Handoff To Execution Pack`
  - Obligations: O2, O3, O7, O8
  - Evidence excerpt: The work-pack gate is complete, active layer window is closed, TASK-VERIFY completed reproducibility and traceability audit, L3 and TASK-VERIFY are complete, and the next route is closeout or a new planning session.

- `benchmark/artifacts/verification-traceability-audit/report.md`
  - Selectors: `Status`, `Summary`, `Score Artifacts`, `Validation`, `Verdict`
  - Obligations: O2, O3, O8
  - Evidence excerpt: TASK-VERIFY status is `pass`; total runs are 6 with 5 pass, 1 fail, 0 infra fail, and 0 evidence gaps; validation includes tests, campaign report, dashboard API, JSON parsing, and traceability assertions; verdict says W0-W3 is complete.

- `benchmark/artifacts/campaign-report-smoke/campaign-report.md`
  - Selectors: `Summary`, `Runs`, `Evidence Gaps`
  - Obligations: O3
  - Evidence excerpt: Campaign report records 6 runs, 5 pass, 1 fail, 0 infra fail, 19 telemetry events, and no evidence gaps across fixture-local, SWE-bench Lite, SmellBench, and PerfCodeBench runs.

- `benchmark/package.json`
  - Selectors: `scripts`
  - Obligations: O3, O8
  - Evidence excerpt: Validation commands include `test`, kernel smoke, Docker smoke, batch smoke, official SWE-bench commands, SmellBench smoke, campaign report, and dashboard API smoke. Downstream runtime should reference these as historical validation surface unless explicitly authorized to rerun.

- `arcana/refine/SKILL.md`
  - Selectors: `canonical-loop`, `stage-dispatch-contract`, `stage-configuration`, `ownership-boundary`, `research-policy`, `process`, `quality-bar`
  - Obligations: O4, O8, O9
  - Evidence excerpt: Refine requires the canonical ten-stage loop; command-backed stages resolve and execute through root `tools/arcanum`; research is local-first unless a named gap triggers confirmation; stage commands own their own artifacts.

- `arcana/refine/REFINEMENT-LOOP.md`
  - Selectors: `Ownership Boundary`, `Required Local Baseline`, `Canonical Default Loop`, `Research Bounds`, `Handoff Output`
  - Obligations: O4, O8, O9
  - Evidence excerpt: The loop starts with a bounded context pack, uses command-backed stages with native artifact ownership, and bounds external research.

- `.codex/commands/invoke.md`
  - Selectors: `Purpose`, `Mode Contracts`, `Core Required Sigils`, `Lifecycle Authority Chain`, `Shared State`, `Target Artifact Provenance`
  - Obligations: O5
  - Evidence excerpt: Invoke is an authoring front door for define/design/plan/handoff/refresh; it prepares artifacts and hands off to the owning capability rather than taking lifecycle ownership.

- `arcana/distill/SKILL.md`
  - Selectors: `objective`, `modes`, `process`, `cycle-guards`, `complexity-balance`, `quality-bar`, `output-contract`
  - Obligations: O6
  - Evidence excerpt: Distill reduces broad models into the smallest coherent unit, proves recomposition, applies finite rounds and cycle guards, and defers complexity without named tension or evolution pressure.

- `benchmark/development/refinement-runs/refine-distill-invoke-benchmark-validation-result-4.md`
  - Selectors: `Verdict`, `Summary`, `Stage Evidence`, `Next Route`
  - Obligations: O8
  - Evidence excerpt: A prior native Refine run blocked at Invoke Define after context-builder passed. The next route was to inspect the first blocked stage artifact/log before rerunning Refine.

## Architecture Guidance

Use the benchmark smoke artifacts as a completed evidence baseline, not as inputs for a new benchmark execution. The refinement concept should validate Arcanum behavior against those completed artifacts by checking whether `context-builder -> invoke define -> interrogation -> research decision -> distill -> invoke design -> interrogation -> distill repair -> invoke plan -> final interrogation/synthesis` can produce coherent, auditable authoring output without altering the benchmark harness.

The smallest coherent validation unit appears to be: "Can the Refine loop turn completed benchmark smoke evidence into a bounded, non-executed validation design for the Arcanum tool?" Distill should test and possibly revise that unit, but should not expand into a new benchmark implementation or score suite.

## Related Feature Context

- The benchmark harness is closed at the pilot W0-W3 level with TASK-VERIFY complete.
- The campaign report has 6 runs, 5 pass, 1 official benchmark fail, 0 infra fail, and 0 evidence gaps.
- A prior native Refine run for the same concept passed Context Builder and blocked at Invoke Define; the next runtime should preserve this as a known downstream risk, not as a context-builder blocker.
- The current run folder already contains seed, goal handoff, runtime handoff, and task-zero observer artifacts for this exact request.

## Constraints And Non-Goals

- Do not mutate benchmark source files under `benchmark/src`, benchmark fixtures, task definitions, score artifacts, official smoke raw outputs, or work-pack status.
- Do not recompute benchmark scores or rerun smoke commands unless the user explicitly changes that constraint.
- Do not promote Invoke, Distill, or Refine as benchmark lifecycle owners; they are validation-authoring tools for this run.
- Do not use broad repository search unless a named obligation gap appears.
- Do not treat external research as authoritative over local benchmark and Arcanum contracts.

## Write Scope

- Allowed: `benchmark/development/refinement-runs/20260527T093001Z-benchmark/`
- Allowed for this Context Builder stage: `benchmark/development/refinement-runs/20260527T093001Z-benchmark/context-builder/`
- Allowed observability: repository-local append-only telemetry if deterministic hooks are available.
- Disallowed: `benchmark/src/`, `benchmark/test/`, `benchmark/fixtures/`, `benchmark/artifacts/*score*`, official raw benchmark outputs, canonical command contracts, and canonical skill contracts.

## Done Criteria

- Context pack exists in Markdown form.
- Structured JSON/index exists.
- Every obligation is covered or explicitly resolved.
- Handoff is marked runnable with strict coverage pass.
- Runtime fallback exploration is limited to named gaps only.
- Observability closeout records success or an explicit telemetry gap.

## Validation Surface

- Artifact existence: `context-pack.md`, `context-index.json`, and `observer-envelope.json`.
- JSON syntax: `jq empty benchmark/development/refinement-runs/20260527T093001Z-benchmark/context-builder/context-index.json`.
- Source preservation: no benchmark source, fixture, test, score, or official raw-output artifact is changed by this context-builder run.
- Runtime validation after handoff: command-backed Refine stages should use root process dispatch and write stage artifacts under the current run folder.

## Gaps And Blockers

- None for context-builder strict handoff coverage.
- Deferred to downstream Refine stages: whether the proposed validation idea passes invoke, interrogation, distill, design, repair, plan, and final synthesis gates.
- Known downstream risk: previous run evidence shows Invoke Define blocked after context-builder passed.

## Contradictions

- None found among selected local sources.

## Authority Precedence

1. User request for this invocation.
2. `.codex/commands/context-builder.md` canonical embedded contract.
3. Current-run artifacts under `benchmark/development/refinement-runs/20260527T093001Z-benchmark/`.
4. `benchmark/WORK-PACK.md` and benchmark closure audit artifacts.
5. `arcana/refine`, `.codex/commands/invoke.md`, and `arcana/distill` local contracts.
6. Prior run artifacts and historical benchmark reports.

## Fallback Exploration Rule

Broad repository exploration is allowed only for obligations listed in `Gaps And Blockers` or for a new gap explicitly named by a downstream stage. Extra sources must be reported in the runtime result with selectors and obligation mapping.

## Provenance

- Source refs: selected paths and selectors listed above.
- Content hash or git SHA: `93a6553d56118eb3a67614aa44ab2773d818f418`
- Builder mode: `standard`
- Command contract: `.codex/commands/context-builder.md`
- Request: `target=benchmark --strict --emit both --handoff runtime --persist benchmark/development/refinement-runs/20260527T093001Z-benchmark/context-builder preset=standard request=target=benchmark; preset=standard; research=research-if-gap-appears; refine the idea of using refine/distill/invoke to validate our tool against the completed benchmark smoke tests; do not mutate benchmark source or recompute benchmark scores`

## Output Paths

- Markdown: `benchmark/development/refinement-runs/20260527T093001Z-benchmark/context-builder/context-pack.md`
- JSON/index: `benchmark/development/refinement-runs/20260527T093001Z-benchmark/context-builder/context-index.json`
- Observer envelope: `benchmark/development/refinement-runs/20260527T093001Z-benchmark/context-builder/observer-envelope.json`
