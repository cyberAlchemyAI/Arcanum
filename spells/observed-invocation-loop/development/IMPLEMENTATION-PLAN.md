# Implementation Plan: Observed Invocation Loop

## Implementation Objective

Deliver a reusable observed invocation pipeline for Arcanum-managed skills, sigils, and spells. The implementation must move reusable telemetry mechanics out of the experiment harness, preserve the current experiment evidence path, and add threshold-backed reflection routing.

The pipeline must be hook-first: deterministic adapters, wrappers, or closeout hooks enforce telemetry append and threshold evaluation. Agent-authored closeout text may enrich evidence, but the implementation must not rely on the agent remembering to emit signals.

## Source Design References

| Ref ID | Source | Required | Notes |
| --- | --- | --- | --- |
| SD-001 | `spells/observed-invocation-loop/development/DESIGN.md` | yes | approved design bundle |
| SD-002 | `arcana/signal-observer/SKILL.md` | yes | telemetry semantics |
| SD-003 | `arcana/workflow-reflect/SKILL.md` | yes | reflection semantics |
| SD-004 | `arcana/experiment-harness/scripts/observe-harness.sh` | yes | current concrete implementation to extract from |
| SD-005 | `framework/observability/scripts/record-hook-operation.sh` | yes | hook operation support |

## Delivery Boundary

- Included: generic observation script, reflection runner, experiment harness delegation, spell contract, runtime adapter guidance, validation fixtures.
- Excluded: editing every installed runtime adapter in all external repositories, direct native invocation hooks outside Arcanum, automatic mutation from reflection reports.
- Deferral rules: unsupported runtime adapters must be listed as L3 follow-up, not silently claimed as covered.

## Delivery Slices

| Slice ID | Outcome | Dependencies | Validation |
| --- | --- | --- | --- |
| S-001 | Generic invocation observation can append telemetry from an envelope. | observability scripts and template | fixture envelope appends one JSONL row |
| S-002 | Experiment harness delegates to generic observation. | S-001 | existing experiment harness phase gates pass |
| S-003 | Reflection routing runs from threshold recommendation. | S-001 | threshold fixture writes reflection report or explicit skip |
| S-004 | Runtime adapter contract is documented for skills, sigils, and spells. | S-001, S-003 | toy capability fixtures prove kind coverage |
| S-005 | Local managed adapters prove telemetry after skill, sigil, and spell runs. | S-001, S-004 | repository-local adapter pilot emits telemetry for each kind |

## Dependency Plan

| Dependency | Needed By | Readiness | Risk |
| --- | --- | --- | --- |
| `.arcanum/observability/` package | all slices | ready | missing package must skip or route setup |
| `jq` | scripts | ready | script should fail gracefully when missing |
| `workflow-reflect` contract | S-003 | ready | no deterministic script exists yet |
| runtime adapters | S-004, S-005 | partial | coverage may vary by runtime |

## Pilot Adapter Targets

Repository-local L3 pilot targets are selected now so implementation does not need to choose them:

| Kind | Pilot Adapter | Target Capability | Acceptance Rule |
| --- | --- | --- | --- |
| skill | `.arcanum/runtimes/github-copilot/skills/arcanum-orchestrate/SKILL.md` | `arcanum-orchestrate` | Managed skill wrapper emits telemetry with `capability.kind = skill`. |
| sigil | `.arcanum/runtimes/github-copilot/skills/arcanum-sigil-signal-observer/SKILL.md` | `signal-observer` | Managed sigil adapter emits telemetry with `capability.kind = sigil`. |
| spell | `.arcanum/runtimes/github-copilot/skills/arcanum-spell-invoke/SKILL.md` | `invoke` | Managed spell adapter emits telemetry with `capability.kind = spell`. |

If a pilot target cannot execute without model access, use deterministic dry-run or mock closeout evidence, but the telemetry append must still be initiated by the adapter or hook path rather than a manual observer call.

## Layer Window

- Layering companion: `spells/observed-invocation-loop/development/IMPLEMENTATION-LAYERING.md`
- Selected start layer: L0
- Selected stop layer: L3
- Layer deferrals: external runtime rollout beyond repository-local adapters

## Per-Layer Planning Slices

| Layer | Tasks | Dependencies | Validation Evidence | Blockers | Promotion Criteria |
| --- | --- | --- | --- | --- | --- |
| L0 | T-001 | observability package, jq | fixture envelope appends exactly one row and one hook append row | none | generic script works without experiment harness report parsing |
| L1 | T-002 | T-001 | experiment harness gates pass and observed rows are unchanged in shape | none | existing users see no regression |
| L2 | T-003 | T-001 | threshold fixture returns `reflect-now` and reflection result path | report format details | reflection is non-mutating and deterministic enough |
| L3 | T-004, T-005, T-VERIFY | T-001, T-002, T-003 | toy skill/sigil/spell coverage, docs review, and hook-driven local adapter pilot | runtime adapter gaps | adapters have a clear integration contract and one hook-enforced proof per kind |

## Task Decomposition

| Task ID | Slice ID | Task | Done When |
| --- | --- | --- | --- |
| T-001 | S-001 | Extract generic observation from experiment harness into framework observability script. | `observe-invocation.sh` accepts an envelope and appends telemetry with dedupe. |
| T-002 | S-002 | Refactor experiment harness observation to assemble an envelope and delegate to generic observer. | Existing phase gates and invoke live observation still pass. |
| T-003 | S-003 | Add deterministic reflection runner and threshold handoff. | `reflect-invocation-signals.sh` writes a report when recommendation is `reflect-now`. |
| T-004 | S-004 | Add observed invocation adapter contract for skill, sigil, and spell wrappers. | docs and toy fixtures show kind-specific telemetry. |
| T-005 | S-005 | Add repository-local adapter pilot for one skill, one sigil, and one spell invocation path. | local managed invocations append telemetry through a hook/adapter closeout, not an agent reminder. |
| T-VERIFY | S-005 | Verify end-to-end telemetry, reflection routing, and non-regression. | test commands pass and report evidence is recorded. |

## Implementation Detail Specs

| Task ID | Detail Status | Inputs | Outputs | Implementation Notes | Edge Cases | Validation Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T-001 | complete | envelope JSON, observability dir, observer version | ledger row, per-capability row, hook rows, reflection state update | Parse envelope with `jq`; validate required fields; compute run id and dedupe key; record started hook; evaluate thresholds before counter mutation; append one JSON row; update counters; print machine fields. | missing jq, missing observability dir, duplicate dedupe key, invalid envelope, missing reflection state | fixture append command, JSONL validation, dedupe rerun |
| T-002 | complete | experiment report or loop report | invocation envelope passed to T-001 | Keep report parsing local to experiment harness; translate parsed fields into the generic envelope; call generic observer; preserve old output fields. | report missing, observability absent, generic observer skipped | experiment harness phase gates |
| T-003 | complete | ledger, reflection state, target capability, recommendation | reflection markdown report and result summary | Read valid JSONL rows; filter by capability or all; group status, quality, gaps, recommendations; require threshold or manual flag; write report under `.arcanum/observability/reflections/`; print report path, analyzed count, threshold source, and insufficient-signal status; do not edit capability artifacts. | insufficient signals, malformed rows, report directory missing, privacy-sensitive summaries | threshold fixture, insufficient-signal fixture, and dry-run fixture |
| T-004 | complete | runtime adapter contracts, target capability metadata | wrapper guidance and fixtures | Define required adapter phases: start run, execute target, assemble envelope, observe, optionally reflect, close out. Include `capability.id`, `capability.kind`, legacy `sigil` compatibility alias, and `target_artifact`. Define public controls: `OBSERVED_INVOCATION_STRICT=1` blocks telemetry failure; `OBSERVED_REFLECT=off|auto|always` controls reflection execution. | adapter cannot capture output path, primary run fails, strict telemetry mode, legacy consumer expects `sigil` | toy skill/sigil/spell fixture checks |
| T-005 | complete | local runtime adapter files, T-004 contract, target capability metadata | pilot wrapper or adapter integration evidence | Discover the local adapter entrypoints, choose one skill adapter, one sigil adapter, and one spell adapter, and route each through the observed invocation sequence. Preserve primary result output and append telemetry through hook/adapter closeout into the generic observer. Do not count an agent manually calling the observer as pilot success. | adapter file missing, target capability cannot run without model access, telemetry succeeds but primary result is hidden, pilot only proves manual observer call | local mock or dry-run managed invocation for skill, sigil, and spell |
| T-VERIFY | n/a | completed tasks and evidence | validation report | Run deterministic checks and existing gates; compare telemetry shape; confirm hook rows have `observe:false`. | stale generated evidence, external runtime unavailable | commands listed below |

## Compatibility And Controls

- Generic telemetry rows must add `capability.id` and `capability.kind`.
- During transition, generic telemetry rows must keep top-level `sigil` as a compatibility alias set to `capability.id`.
- Existing `by-sigil/<id>.jsonl` fanout may remain for sigil-compatible consumers.
- New generic fanout should write `by-capability/<kind>/<id>.jsonl` when observability storage exists.
- `OBSERVED_INVOCATION_STRICT=1` makes telemetry append failure a blocking result.
- `OBSERVED_REFLECT=off|auto|always` controls reflection routing; default is `auto` for managed observed invocation pipeline and `off` for low-level observer-only calls.
- Hook-first enforcement is required for managed invocation pilots. Manual observer calls are allowed only for recovery and development diagnostics.

## Reflection Runner Interface

`reflect-invocation-signals.sh` must expose this minimum interface:

```bash
reflect-invocation-signals.sh [--all|--capability <id>] [--kind skill|sigil|spell] [--since <iso-date>] [--min-signals <n>] [--dry-run]
```

Minimum machine output:

```text
REFLECTION=written|skipped|failed
REASON=<threshold-hit|manual|insufficient-signals|invalid-ledger|...>
SIGNALS_ANALYZED=<n>
THRESHOLDS_TRIGGERED=<csv-or-none>
REPORT=<path-or-n/a>
STATE=updated|unchanged|unavailable
```

Acceptance rules:

- `--dry-run` must not write a report or mutate state.
- Insufficient signals must return `REFLECTION=skipped` and `REASON=insufficient-signals`.
- Threshold-backed runs must include the threshold source in the report.
- Reports must be written under `.arcanum/observability/reflections/`.
- The runner must not edit the observed capability.

## Smallest Working Units

Shared manifest:

| SWU ID | Parent Task | Goal | Write Scope | Acceptance Evidence | Verification Command |
| --- | --- | --- | --- | --- | --- |
| SWU-OIL-001 | T-001 | Add generic envelope validation and ledger append path. | `framework/observability/scripts/observe-invocation.sh` | valid fixture appends one row | `jq -e . <fixture-envelope>` plus script fixture |
| SWU-OIL-002 | T-001 | Add hook operation and dedupe behavior to generic observer. | `framework/observability/scripts/observe-invocation.sh` | duplicate run skips append and records hook skip | generic observer duplicate fixture |
| SWU-OIL-003 | T-001 | Add threshold evaluation and reflection state update. | `framework/observability/scripts/observe-invocation.sh` | threshold fixture emits `reflect-now` | threshold fixture command |
| SWU-OIL-004 | T-002 | Convert experiment report parsing into envelope assembly. | `arcana/experiment-harness/scripts/observe-harness.sh` | existing output fields preserved | `arcana/experiment-harness/development/run-phase-gates.sh` |
| SWU-OIL-005 | T-003 | Implement reflection report runner from signal ledger. | `framework/observability/scripts/reflect-invocation-signals.sh` | report written for threshold-backed fixture | reflection fixture command |
| SWU-OIL-006 | T-004 | Document observed adapter contract and wrapper flow. | `spells/observed-invocation-loop/README.md`, runtime docs | skill/sigil/spell contract examples present | docs review |
| SWU-OIL-007 | T-005 | Add hook-driven local adapter pilot coverage. | local runtime adapters and validation docs | skill, sigil, and spell managed pilot paths append telemetry without agent reminder | local adapter pilot command |
| SWU-OIL-008 | T-VERIFY | Add end-to-end validation evidence. | development validation docs | all checks listed in validation strategy pass | test plan commands |

Task-local mapping:

```markdown
## Smallest Working Units

- T-001: SWU-OIL-001, SWU-OIL-002, SWU-OIL-003
- T-002: SWU-OIL-004
- T-003: SWU-OIL-005
- T-004: SWU-OIL-006
- T-005: SWU-OIL-007
- T-VERIFY: SWU-OIL-008
```

## Blocker Ledger

| Blocker ID | Blocker | Impact | Resolution |
| --- | --- | --- | --- |
| B-001 | No deterministic workflow-reflect script exists yet. | L2 cannot fully close reflection routing. | Build `reflect-invocation-signals.sh` as part of T-003. |
| B-002 | Runtime adapter coverage may not include every installed environment. | L3 may be partial. | Document adapter contract and validate local adapters first. |
| B-003 | Existing envelope and ledger names are sigil-oriented. | Skill and spell telemetry could be awkward or break consumers. | Preserve legacy `sigil` field and add generic `capability` fields plus `by-capability` fanout. |
| B-004 | Pilot could accidentally prove an agent manually called the observer rather than hook enforcement. | The user goal would not be satisfied. | Require adapter or hook closeout evidence for pilot acceptance. |

## Planning Readiness Decisions

| Former Gap | Decision | Status |
| --- | --- | --- |
| Local adapter file selection | Use the three pilot adapters listed in `Pilot Adapter Targets`. | resolved |
| Deterministic reflection runner details | Use the interface and machine output in `Reflection Runner Interface`. | resolved |
| Concrete validation script naming | Add fixture commands during SWU execution; validation behavior is already specified. | resolved for planning |

## Validation Strategy

| Check ID | Check | Scope | Tool Or Evidence |
| --- | --- | --- | --- |
| V-001 | generic observer fixture append | L0 | fixture command with temp observability dir |
| V-002 | generic observer dedupe | L0 | rerun same envelope, expect skipped append |
| V-003 | experiment harness non-regression | L1 | `arcana/experiment-harness/development/run-phase-gates.sh` |
| V-004 | reflection threshold report | L2 | threshold fixture creates reflection report |
| V-005 | kind coverage | L3 | toy skill, sigil, spell envelopes all append |
| V-006 | hook-driven local adapter pilot | L3 | one local skill, sigil, and spell managed path append telemetry without manual observer calls |
| V-007 | hook separation | all | hook rows carry `observe:false` and no capability signal recursion |

## Work-Pack Handoff

- Work-pack companion: `spells/observed-invocation-loop/development/WORK-PACK.md`
- Required manifest entries: generic observer, experiment delegation, reflection runner, adapter contract, validation
- Deferred entries: external runtime rollout beyond local repository

## Execution-Pack Handoff

- Output mode: split
- Wave grouping:
  - W0: generic observer proof
  - W1: experiment harness delegation
  - W2: reflection routing
  - W3: adapter packaging and validation
- Parallelization boundary: T-003 can start after T-001; T-004 can draft in parallel after design is approved.

## Closure Criteria

| Criterion | Evidence |
| --- | --- |
| Managed invocation telemetry is generic. | non-experiment fixture appends central signal |
| Experiment harness delegates safely. | phase gates pass |
| Reflection threshold produces route. | `reflect-now` fixture writes or queues report |
| Skill/sigil/spell kind is represented. | toy fixture coverage plus hook-driven local adapter pilot |
| Telemetry does not depend on agent attention. | pilot evidence shows adapter or hook closeout appended telemetry without manual observer call |

## Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: spells/invoke/plan.md
- Outputs: implementation plan, implementation layering, work-pack, transport report
- Complexity: medium
- Per-layer planning: L0, L1, L2, L3
- Implementation detail: task specs complete
- Smallest working units: complete
- Next route: spellcraft
