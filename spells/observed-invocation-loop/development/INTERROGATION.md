# Interrogation: Observed Invocation Loop Implementation Plan

## Interrogation Scope

- Target artifact: `spells/observed-invocation-loop/development/IMPLEMENTATION-PLAN.md`
- Mode: artifact readiness interrogation
- Evidence reviewed:
  - `spells/observed-invocation-loop/development/DEFINE-SPEC.md`
  - `spells/observed-invocation-loop/development/DESIGN.md`
  - `spells/observed-invocation-loop/development/IMPLEMENTATION-LAYERING.md`
  - `framework/observability/templates/invocation-envelope.json`
  - `framework/observability/scripts/start-observed-run.sh`
  - `arcana/signal-observer/SKILL.md`
  - `arcana/workflow-reflect/SKILL.md`

## Central Question

Can this plan be handed to an implementer and reliably produce telemetry and reflection routing for Arcanum-managed skills, sigils, and spells without forcing every run through the experiment harness?

## Readiness Verdict

- Verdict: pass
- Reason: the second refresh resolved the planning gaps around schema compatibility, strictness controls, per-capability ledgers, runtime adapter proof, hook-first enforcement, pilot adapter selection, and reflection runner interface. Remaining items are implementation tasks, not planning blockers.

## Findings

| ID | Severity | Finding | Evidence | Required Plan Change |
| --- | --- | --- | --- | --- |
| INT-001 | high | The current invocation envelope template is sigil-shaped, while the new spell promises skill/sigil/spell coverage. | `framework/observability/templates/invocation-envelope.json` has top-level `sigil`; `start-observed-run.sh` already models `capability.kind`. | Add schema compatibility rules: preserve `sigil` for backward compatibility, add `capability.id` and `capability.kind`, and validate both shapes during transition. |
| INT-002 | medium | The plan does not define the public strictness and reflection routing knobs. | README says standard vs strict; plan does not name flags/env vars. | Add explicit controls: `OBSERVED_INVOCATION_STRICT=1` and `OBSERVED_REFLECT=off|auto|always`. |
| INT-003 | medium | Per-capability telemetry fanout is under-specified. | Existing experiment path writes `by-sigil/experiment-harness.jsonl`; new plan covers skills and spells. | Define compatibility path and generalized path: keep `by-sigil` for old consumers and add `by-capability/<kind>/<id>.jsonl` or equivalent. |
| INT-004 | high | L3 adapter work says "document" more than "prove." That is weaker than the user goal: know for sure telemetry was emitted after running a skill. | T-004 acceptance is docs and toy fixtures only. | Add local adapter pilot task proving at least one managed skill, sigil, and spell wrapper calls the generic observer. |
| INT-005 | medium | Reflection runner behavior is still too broad for deterministic implementation. | T-003 says "deterministic enough" and groups signals, but does not lock minimum interface. | Require report path, insufficient-signal result, threshold-source evidence, and non-mutating guarantee as acceptance checks. |
| INT-006 | high | The pack implied adapters and hooks, but did not plainly forbid dependence on agent attention span. | User goal is to rely on hooks extensively so the agent does not have to remember telemetry closeout. | Add hook-first enforcement as a design principle, plan constraint, pilot acceptance rule, and work-pack gate. |

## Decisions Recorded

| Decision | Selected Default | Rejected Alternative | Rationale |
| --- | --- | --- | --- |
| Compatibility model | Dual-write compatibility during transition | Rename central ledger immediately | Existing observability consumers expect `sigil` and `by-sigil`. |
| Strict telemetry control | Standard by default, strict opt-in | Always block on telemetry failure | Primary capability result should remain visible unless a strict run explicitly requires telemetry. |
| Reflection control | `auto` by default for managed observed invocation pipeline | Always reflect after every run | Reflection should follow thresholds unless manually forced. |
| Adapter proof | Add local pilot wrappers | Documentation only | The goal requires a runnable proof, not just guidance. |
| Telemetry enforcement | Hook/runtime enforced | Agent remembers to call observer | Long sessions and context loss must not break telemetry. |

## Highest-Discrimination Question

Question: Should the new generic signal row keep the legacy top-level `sigil` field when observing skills and spells?

Recommended default: yes, keep it as a compatibility alias set to the capability id, while adding `capability.id` and `capability.kind`.

Reason: this lets existing JSONL consumers continue working while new code can reason over skill, sigil, and spell kinds.

Recorded answer: use the recommended default for this plan.

## Artifact Updates Made

- Updated `IMPLEMENTATION-PLAN.md` with schema compatibility, controls, generalized fanout, deterministic reflection acceptance, and local adapter pilot task.
- Updated `WORK-PACK.md` with added T-005 and SWU coverage for local adapter pilot.
- Updated the OIL pack with hook-first enforcement so managed telemetry does not depend on agent attention.

## Remaining Ambiguities

| Ambiguity | Impact | Route |
| --- | --- | --- |
| Adapter pilot target ambiguity. | Resolved. | Use `arcanum-orchestrate`, `arcanum-sigil-signal-observer`, and `arcanum-spell-invoke` pilot adapters. |
| Whether `by-capability` should be pluralized or nested differently. | Resolved. | Use `by-capability/<kind>/<id>.jsonl`. |

## Structured Interview Result

- Target scope: observed-invocation-loop implementation plan
- Mode: artifact-readiness interrogation
- Questions asked: 1
- Decisions recorded: 8
- Artifacts updated: `IMPLEMENTATION-PLAN.md`, `WORK-PACK.md`, `PLAN-TRANSPORT.md`, `REFRESH-REVIEW.md`
- Remaining ambiguities: none blocking implementation
- Verdict: pass
- Next step: execute L0 SWU-OIL-001 after approval

## Second Refresh Resolution

| Gap | Resolution | Artifact |
| --- | --- | --- |
| Adapter pilot file selection | Selected one local GitHub Copilot runtime adapter each for skill, sigil, and spell. | `IMPLEMENTATION-PLAN.md`, `WORK-PACK.md` |
| Reflection runner ambiguity | Added minimum CLI interface, machine output, and acceptance rules. | `IMPLEMENTATION-PLAN.md` |
| Refresh verdict | Updated from flag to pass because no planning blocker remains. | `REFRESH-REVIEW.md` |
