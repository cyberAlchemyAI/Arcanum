# Validation Evidence: Observed Invocation Loop Remaining Items

## Scope

- Pack: Observed Invocation Loop remaining-items hardening pack.
- Evidence target: promotion from interrogation `flag` to `pass`.
- Real repository ledger mutation: none from behavioral probes; fixture probes used temporary observability stores.

## Static Validation

Command:

```bash
bash -n framework/observability/scripts/*.sh tools/arcanum .codex/hooks/*.sh
jq empty .codex/hooks.json .arcanum/observability/config.json .arcanum/observability/reflection-state.json
jq -s empty .arcanum/observability/signals/sigil-invocations.jsonl .arcanum/observability/hooks/hook-operations.jsonl .arcanum/observability/hooks/dedupe.jsonl
framework/observability/scripts/check-observability-migration.sh
```

Result:

```text
MIGRATION_CHECK=pass
ANONYMOUS=0
LEGACY_FALLBACK=4
groups: sigil:experiment-harness=4, sigil:interrogation=1, spell:invoke=6
```

## Observer And Reflection Fixture

Temporary observability store results:

```text
OBSERVATION=recorded
REFLECTION_TRIGGER=none
RECOMMENDATION=none

OBSERVATION=skipped
REASON=duplicate observer emission
REFLECTION_TRIGGER=none
RECOMMENDATION=none

OBSERVATION=recorded
REFLECTION_TRIGGER=output-threshold
RECOMMENDATION=reflect-now

REFLECTION=written
REASON=threshold-hit
SIGNALS_ANALYZED=2
THRESHOLDS_TRIGGERED=output-threshold
STATE=updated

OBSERVATION=recorded
REFLECTION_TRIGGER=none
RECOMMENDATION=none

OBSERVATION=recorded
REFLECTION_TRIGGER=severe-gap
RECOMMENDATION=reflect-now
```

Acceptance covered:

- first append records telemetry,
- duplicate skips without recomputing stale thresholds,
- ordinary threshold writes reflection,
- ordinary post-reflection event cools to `none`,
- severe gap remains immediate.

## Stop Hook Partial And Blocked Fixture

Temporary Git repository and observability store results:

```text
partial=partial:partial
blocked=blocked:partial
ledger_rows=2
reflection_partial=REFLECTION=skipped;REASON=reflection-disabled;REPORT=n/a
```

Acceptance covered:

- pending `partial` with no final assistant message remains `partial` and `quality_bar_status=partial`,
- pending `blocked` remains `blocked` and `quality_bar_status=partial`,
- both close through the observer into the temp ledger,
- `OBSERVED_REFLECT=off` records an explicit skipped reflection result.

## Promotion Decision

- Interrogation finding `INT-OIL-REM-001`: resolved by this evidence artifact.
- Interrogation finding `INT-OIL-REM-002`: resolved by partial and blocked Stop-hook fixture evidence.
- Interrogation finding `INT-OIL-REM-003`: resolved by README status boundary note.
- Interrogation finding `INT-OIL-REM-004`: accepted boundary for standard mode; strict-mode dedupe failure can be future hardening if strict mode becomes a release gate.
- Interrogation finding `INT-OIL-REM-005`: accepted metadata cleanup follow-up; not a readiness blocker.

## Result

- Validation status: pass
- Promotion readiness: pass for repository-local Codex runtime baseline readiness
