# WORK-PACK: Observed Invocation Loop Remaining Items

## Control Fields

| Field | Value |
| --- | --- |
| workPackGateStatus | pass |
| complexity | medium |
| outputMode | split |
| implementationPlanRef | `spells/observed-invocation-loop/development/REMAINING-IMPLEMENTATION-PLAN.md` |
| defineRef | `spells/observed-invocation-loop/development/REMAINING-DEFINE-SPEC.md` |
| designRef | `spells/observed-invocation-loop/development/REMAINING-DESIGN.md` |
| validationEvidenceRef | `spells/observed-invocation-loop/development/REMAINING-VALIDATION-EVIDENCE.md` |
| readinessProfile | runtime-hardening |

## Objective Summary

Finish OIL maturity hardening without rewriting the completed original OIL work-pack. The work-pack targets reflection routing, threshold cooling, dedupe safety, accurate hook closeout status, and legacy ledger migration checks.

## Task Status Board

| Task ID | Goal | Layer | Status |
| --- | --- | --- | --- |
| T-REM-001 | Dedupe check/commit modes | L2 | implemented |
| T-REM-002 | Threshold scoping and reflection state | L1 | implemented |
| T-REM-003 | Managed reflection routing | L0 | implemented |
| T-REM-004 | Stop hook status inference | L3 | implemented |
| T-REM-005 | Migration validation | L3 | implemented |
| T-REM-VERIFY | Verification | L3 | completed |

## Smallest Working Units

| SWU ID | Parent Task | Status |
| --- | --- | --- |
| SWU-OIL-REM-001 | T-REM-001 | implemented |
| SWU-OIL-REM-002 | T-REM-002 | implemented |
| SWU-OIL-REM-003 | T-REM-002 | implemented |
| SWU-OIL-REM-004 | T-REM-003 | implemented |
| SWU-OIL-REM-005 | T-REM-003 | implemented |
| SWU-OIL-REM-006 | T-REM-004 | implemented |
| SWU-OIL-REM-007 | T-REM-005 | implemented |
| SWU-OIL-REM-008 | T-REM-VERIFY | completed |

## Acceptance Gates

1. `observe-invocation.sh` commits dedupe only after the telemetry path succeeds.
2. Managed closeout returns both observation and reflection status.
3. Ordinary thresholds are scoped since the last reflection report.
4. Severe gaps remain immediate.
5. Stop hook no longer blindly marks every closeout as completed/pass.
6. Migration check reports no anonymous capability groups.
7. Reflection remains non-mutating.

## Promotion Evidence

- Validation evidence: `spells/observed-invocation-loop/development/REMAINING-VALIDATION-EVIDENCE.md`
- Interrogation result: `spells/observed-invocation-loop/development/REMAINING-INTERROGATION.md`
- Promotion status: pass for repository-local Codex runtime baseline readiness.

## Validation Commands

```bash
bash -n framework/observability/scripts/*.sh tools/arcanum .codex/hooks/*.sh
jq empty .codex/hooks.json .arcanum/observability/config.json .arcanum/observability/reflection-state.json
jq -s empty .arcanum/observability/signals/sigil-invocations.jsonl .arcanum/observability/hooks/hook-operations.jsonl .arcanum/observability/hooks/dedupe.jsonl
framework/observability/scripts/check-observability-migration.sh
```

## Blockers

| Blocker | Status | Resolution |
| --- | --- | --- |
| Reflection recommendation not routed | resolved | Managed closeout calls reflector according to `OBSERVED_REFLECT`. |
| Permanent hot thresholds | resolved | Threshold checks use signals since `last_reflection_at`. |
| Early dedupe commit | resolved | Hook recorder supports check and commit modes. |
| Over-optimistic Stop telemetry | resolved | Stop hook derives status from evidence. |
| Anonymous legacy summaries | resolved | Migration check validates fallback grouping. |
