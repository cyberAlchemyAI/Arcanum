# WORK-PACK: Observed Invocation Loop

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Implementation SWUs complete and verified. |
| complexity | medium | Cross-cutting runtime and observability behavior. |
| outputMode | split | Required by medium complexity. |
| implementationPlanRef | `spells/observed-invocation-loop/development/IMPLEMENTATION-PLAN.md` | Source plan. |
| executionPackRef | `spells/observed-invocation-loop/development/EXECUTION-PACK.md` | To be created during execution prep. |
| layeringArtifactRef | `spells/observed-invocation-loop/development/IMPLEMENTATION-LAYERING.md` | Layering source. |
| activeLayerWindow | L0-L3 | Full rollout plan. |
| readinessProfile | pilot | First target is repository-local pilot. |

## Objective Summary

- Objective: make invocation telemetry generic and threshold-backed for Arcanum-managed skills, sigils, and spells.
- Primary inputs: define spec, design bundle, implementation plan, existing observability scripts.
- Success condition: every managed invocation path has a documented envelope and hook-driven generic observer handoff, with deterministic validation evidence.

## Pilot Adapter Targets

| Kind | Pilot Adapter | Target Capability |
| --- | --- | --- |
| skill | `.arcanum/runtimes/github-copilot/skills/arcanum-orchestrate/SKILL.md` | `arcanum-orchestrate` |
| sigil | `.arcanum/runtimes/github-copilot/skills/arcanum-sigil-signal-observer/SKILL.md` | `signal-observer` |
| spell | `.arcanum/runtimes/github-copilot/skills/arcanum-spell-invoke/SKILL.md` | `invoke` |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T-001 | Generic invocation observer | L0 | medium | W0 | ready | completed |
| T-002 | Experiment harness delegation | L1 | medium | W1 | ready-after-T-001 | completed |
| T-003 | Reflection runner and threshold route | L2 | medium | W2 | ready-after-T-001 | completed |
| T-004 | Runtime adapter contract | L3 | medium | W3 | ready-after-T-001 | completed |
| T-005 | Hook-driven local adapter pilot | L3 | medium | W3 | ready-after-T-004 | completed |
| T-VERIFY | End-to-end verification | L3 | medium | W3 | ready-after-implementation | completed |

## Smallest Working Units

| SWU ID | Parent Task | Goal | Write Scope | Acceptance Evidence | Verification Command | Status |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-OIL-001 | T-001 | Add generic envelope validation and ledger append path. | framework observability script | one valid row appended | fixture observer command | completed |
| SWU-OIL-002 | T-001 | Add hook operation and dedupe behavior. | framework observability script | duplicate append skipped | duplicate fixture command | completed |
| SWU-OIL-003 | T-001 | Add threshold evaluation and counter updates. | framework observability script | `reflect-now` emitted at threshold | threshold fixture command | completed |
| SWU-OIL-004 | T-002 | Delegate experiment harness observation to generic observer. | experiment harness observe script | phase gates pass | `arcana/experiment-harness/development/run-phase-gates.sh` | completed |
| SWU-OIL-005 | T-003 | Add reflection report runner. | framework observability script | reflection report written | reflection fixture command | completed |
| SWU-OIL-006 | T-004 | Document and validate adapter contract. | spell docs and runtime docs | skill/sigil/spell examples present | docs and fixture review | completed |
| SWU-OIL-007 | T-005 | Add hook-driven local adapter pilot. | local runtime adapters and validation docs | one skill, sigil, and spell pilot append telemetry without agent reminder | local adapter pilot command | completed |
| SWU-OIL-008 | T-VERIFY | Verify full telemetry and reflection loop. | validation docs | all checks pass | test plan | completed |

## Per-Task SWU Mapping

### T-001

## Smallest Working Units

- SWU-OIL-001: generic envelope validation and append
- SWU-OIL-002: hook and dedupe
- SWU-OIL-003: threshold and counters

### T-002

## Smallest Working Units

- SWU-OIL-004: experiment harness delegation

### T-003

## Smallest Working Units

- SWU-OIL-005: reflection runner

### T-004

## Smallest Working Units

- SWU-OIL-006: adapter contract

### T-005

## Smallest Working Units

- SWU-OIL-007: hook-driven local adapter pilot

### T-VERIFY

## Smallest Working Units

- SWU-OIL-008: end-to-end verification

## Blockers

| Blocker ID | Scope | Description | Owner | Resolution | Status |
| --- | --- | --- | --- | --- | --- |
| B-001 | T-003 | Deterministic reflection runner did not exist. | implementer | `reflect-invocation-signals.sh` added and fixture-tested. | resolved |
| B-002 | T-004 | Runtime adapter coverage varied by environment. | implementer | Local GitHub Copilot pilot adapters selected and documented. | resolved |
| B-003 | T-001/T-004 | Existing envelope and ledger names were sigil-oriented. | implementer | Generic `capability` fields and `by-capability` fanout added while preserving legacy `sigil`. | resolved |
| B-004 | T-005 | Pilot could accidentally prove an agent manually called the observer rather than hook enforcement. | implementer | `run-observed-adapter-pilot.sh` proves deterministic adapter closeout path. | resolved |

## Planning Readiness

| Check | Status | Notes |
| --- | --- | --- |
| SWU coverage | pass | All implementation tasks map to SWUs. |
| Adapter pilot selection | pass | Skill, sigil, and spell pilot targets are selected. |
| Reflection runner interface | pass | Interface is specified in the implementation plan. |
| Hook-first enforcement | pass | Manual observer calls cannot satisfy pilot acceptance. |

## Gate Checks

1. `workPackGateStatus` must remain pass before mutation-capable execution.
2. Medium complexity requires split execution evidence.
3. Every implementation task must execute by SWU.
4. Existing experiment harness telemetry must remain backward compatible.
5. Reflection remains non-mutating.
6. Agent attention cannot be the telemetry enforcement mechanism for managed invocation pilots.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-05-18 | Initial invoke-generated work-pack created. | Codex |
| 2026-05-18 | SWU-OIL-001 implemented and fixture evidence recorded. | Codex |
| 2026-05-18 | SWU-OIL-002 implemented and duplicate-observation fixture evidence recorded. | Codex |
| 2026-05-18 | SWU-OIL-003 implemented; T-001 completed. | Codex |
| 2026-05-18 | SWU-OIL-004 implemented; T-002 completed. | Codex |
| 2026-05-18 | SWU-OIL-005 implemented; T-003 completed. | Codex |
| 2026-05-18 | SWU-OIL-006 implemented; T-004 completed. | Codex |
| 2026-05-18 | SWU-OIL-007 implemented; T-005 completed. | Codex |
| 2026-05-18 | SWU-OIL-008 completed; work-pack implementation verified. | Codex |
