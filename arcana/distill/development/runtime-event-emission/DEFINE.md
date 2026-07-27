# Define: Distill Runtime-Event Emission

## Intent

Close the remaining runtime-emission gap for evidence-gated Distill runs while
adding direct Distill usage telemetry and an explicit evidence-emission status.
Preserve Distill's current behavior and keep telemetry, runtime evidence,
validation, and mutation authority separate.

## Discovery Baseline

Discovery is satisfied by the existing live artifacts:

- `../SKILL.md` defines modes, finite budgets, role policy, techniques, and output.
- `../../../../spells/invoke/development/distill-execution-evidence/VALIDATION.md`
  establishes that the Invoke-side evidence backend is closed.
- `../../../../spells/invoke/development/distill-execution-evidence/GAP-LEDGER.md`
  leaves only `GAP-DEE-002` open.
- `../../../../spells/invoke/schemas/distill-runtime-event.schema.json` and
  `../../../../spells/invoke/development/distill_runtime_events.py` define the
  accepted consumer-side event grammar, append behavior, and resolver.

No discovery waiver is required.

## Problem Statement

The accepted backend can validate and resolve checked-in runtime events, but a
live Distill execution has no Distill-owned surface that emits those events at
role/process boundaries. Direct Distill runs also lack a dedicated telemetry
append path, and the current signal vocabulary does not distinguish runtime
evidence emission from usage-telemetry recording.

Consequently:

- true-subagent and role-simulation fixtures prove resolvability, not live
  producer behavior;
- an evidence-gated run can finish without declaring whether evidence emission
  completed, partially completed, failed, or was not configured; and
- direct Distill usage can remain invisible even when repository observability
  is installed.

## Defined Terms

| Term | Definition |
| --- | --- |
| evidence-gated Distill run | A run whose downstream handoff requires the accepted `DistillRunRequest`, runtime-event, receipt, and validator contracts. |
| runtime-event emission | Producing the ordered capability, role, reconciliation, and termination evidence events during execution. |
| usage telemetry | One non-authoritative summary row for a meaningful Distill invocation. |
| evidence-emission status | `complete`, `partial`, `failed`, `not-required`, or `not-configured`; this reports producer state and carries no verdict authority. |
| direct telemetry | Usage telemetry for a Distill run without caller lineage; Distill owns the append. |
| invoked telemetry | Usage telemetry for a child Distill run; the caller owns the append and lineage. |

## Delivery Boundary

Included:

- a Distill-owned runtime-event emitter for evidence-gated runs;
- ordered emission for true-subagent and role-simulation paths;
- compatibility validation against the accepted Invoke-side schema/resolver;
- a Distill-owned direct-telemetry helper;
- evidence-emission status in Distill telemetry and closeout guidance;
- validation/readiness updates that close `GAP-DEE-002` only after evidence;
- canonical-first regeneration of Codex and Claude runtime mirrors.

Excluded:

- changing Compact, Standard, Tournament, Deep, or Validate behavior;
- changing proposal-track or recursive-round budgets;
- changing the true-subagent-preferred role policy;
- changing the technique pack or activation rules;
- changing verdict, recomposition, navigation, or next-route semantics;
- moving or redefining Invoke's accepted schemas, resolver, validator, or
  mutation-handoff authority;
- implementing deferred Invoke modes;
- rewriting historical observability or DEE evidence.

## Ownership

| Surface | Owner | Authority Boundary |
| --- | --- | --- |
| role/process emission timing and producer helper | Distill through Sigil Development | Emits evidence only; cannot validate or authorize handoff. |
| event schema, resolver, receipt, and handoff gate | Invoke lifecycle | Consumes and validates evidence; does not own Distill role behavior. |
| direct Distill telemetry append | Distill through Sigil Development | Records one direct-run signal only. |
| invoked Distill telemetry append | caller capability | Preserves caller/child lineage and deduplicates by child run ID. |
| central observability ledger | Signal Observer | Append-only evidence; no lifecycle authority. |
| generated runtime packages | bootstrap owner | Derived from accepted canonical sources only. |

## Functional Requirements

1. An evidence-gated run must bind every event to one accepted run ID and one
   execution path.
2. The emitter must preserve the accepted boundary order: capability probe,
   Proposer start/result, Balancer start/result, reconciliation, termination.
3. True-subagent role events must carry stable, distinct native invocation
   references.
4. Role-simulation events must carry no invented native invocation references.
5. Event append must fail closed on schema error, duplicate ID, sequence drift,
   changed run/path, or changed ledger digest.
6. Direct meaningful runs must append exactly one Distill usage signal when
   observability is configured.
7. Invoked runs must remain caller-appended; Distill must not double-append.
8. Telemetry must record evidence-emission status separately from
   execution-evidence status and telemetry status.
9. Emission or telemetry failure must not rewrite the Distill verdict, but
   incomplete evidence must prevent evidence-gated mutation handoff.
10. Canonical and generated runtime surfaces must remain byte-equivalent for
    selected Distill files.

## Non-Functional Requirements

- Deterministic scripts and fixtures; no model call in validation.
- Append-only, optimistic-digest event writes.
- Public, repository-neutral language.
- No new required dependency for non-evidence-gated Distill use.
- Actionable diagnostics for path, role, sequence, and ledger failures.
- Backward-compatible additive telemetry fields.

## Preserved Semantics

The work must not change:

- mode names or selection rules;
- mode budgets, finite rounds, or cycle guards;
- Proposer/Balancer roles or true-subagent preference;
- technique pack, triggers, or skipped-technique rules;
- pass/flag/block verdict meaning;
- the Distill output's optimization, recomposition, navigation, or routing
  semantics.

## Define Gate

**PASS.** The goal, discovery source, ownership split, preserved semantics,
requirements, exclusions, and next lifecycle owner are explicit.
