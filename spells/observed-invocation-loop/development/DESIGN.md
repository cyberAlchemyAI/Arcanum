# Invoke Design Bundle: Observed Invocation Loop

## Source Contracts

| Ref | Source | Role |
| --- | --- | --- |
| SD-001 | `spells/observed-invocation-loop/development/DEFINE-SPEC.md` | approved define source |
| SD-002 | `arcana/signal-observer/SKILL.md` | telemetry append and threshold semantics |
| SD-003 | `arcana/workflow-reflect/SKILL.md` | reflection report semantics |
| SD-004 | `framework/observability/templates/invocation-envelope.json` | envelope shape |
| SD-005 | `framework/observability/scripts/record-hook-operation.sh` | hook operation append support |

## Six Views

### 1. Context View

The spell sits between Arcanum runtime adapters and the observability package. It observes managed invocations after the primary capability result exists.

The spell is hook-first: runtime adapters, wrappers, or deterministic closeout hooks own telemetry emission. Agent attention must not be required for the signal append, because long sessions, context loss, or missed closeout instructions would otherwise break the observability guarantee.

External actors:

- user invoking a capability,
- runtime adapter or orchestrator,
- target skill, sigil, or spell,
- observability package,
- maintainers consuming reflection reports.

### 2. High-Level Structure View

| Component | Responsibility |
| --- | --- |
| Managed invocation adapter | Resolves and runs the target capability. |
| Envelope assembler | Converts primary result evidence into a safe invocation envelope. |
| Generic observer runner | Appends telemetry, records hook rows, updates counters, and evaluates thresholds. |
| Reflection router | Calls or queues `workflow-reflect` when recommendation is `reflect-now`. |
| Closeout reporter | Returns the primary result plus telemetry and reflection status. |
| Agent-authored closeout | Supplies optional evidence or remediation context, but is not the telemetry append mechanism. |

### 3. Low-Level Components View

| Component | Inputs | Outputs |
| --- | --- | --- |
| `start-observed-run.sh` integration | capability id, kind, mode | run id and run directory |
| envelope writer | primary result, outputs, validation, gaps | invocation envelope JSON |
| `observe-invocation.sh` | envelope path | ledger row, hook rows, threshold result |
| `reflect-invocation-signals.sh` | ledger, reflection state, target filter | reflection report or skipped result |
| adapter wrappers | runtime contract and target capability | observed invocation result |

### 4. Workflow Process View

1. Resolve target capability and kind.
2. Start observed run metadata.
3. Execute target capability.
4. Capture result status, outputs, files changed, validation, and gaps.
5. Write a privacy-safe invocation envelope.
6. Run generic observation.
7. If recommendation is `reflect-now`, run or queue reflection.
8. Return primary result with telemetry state.

### 5. Decision Flow View

| Decision | Rule |
| --- | --- |
| Is telemetry required? | Standard mode flags skip; strict mode blocks skip or append failure. |
| Can an envelope be written? | Require status, capability id, kind, mode, request summary, outputs or skip reason, validation, observer evidence. |
| Should reflection run? | Run when recommendation is `reflect-now` and reflection routing is enabled, or when manually requested. |
| Should capability source mutate? | Never inside this spell; route to `sigil-development` or `spellcraft`. |
| Can the agent be trusted to remember telemetry? | No; hooks/adapters must enforce observation closeout. |

### 6. Dependency Interface View

| Interface | Producer | Consumer | Contract |
| --- | --- | --- | --- |
| invocation envelope | runtime adapter | generic observer | JSON object based on framework template |
| telemetry signal | generic observer | ledger, workflow-reflect | one JSONL object per observed invocation |
| hook operation | observer/reflection hooks | hook-health review | observe false, separate from capability telemetry |
| reflection report | workflow-reflect | maintainers and lifecycle spells | markdown report with proposal summary |

## Glossary Consistency

All define terms are preserved. `signal-observer` currently names sigils in some places, but this design generalizes the telemetry target to skill, sigil, or spell while preserving the existing central ledger name for compatibility.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Runtime adapters bypass the observed path. | Missing telemetry. | L3 adapter coverage and documentation gate. |
| Telemetry depends on agent attention. | Missed signals during long or interrupted sessions. | Hook-first closeout and adapter pilot proof. |
| Observer writes to wrong repo root. | Fragmented telemetry. | Resolve observability root from artifact or explicit env. |
| Reflection runs too aggressively. | Noisy reports. | Threshold-backed default, manual override only. |
| Sensitive raw content is stored. | Privacy violation. | Envelope summary-only policy and redaction gate. |

## Design Result

- Phase status: pass
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Implementation layering: required for plan
- Work-pack: required for plan
- Next route: plan
