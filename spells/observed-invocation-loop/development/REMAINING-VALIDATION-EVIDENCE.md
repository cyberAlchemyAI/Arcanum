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
- Interrogation finding `INT-OIL-REM-004`: resolved by strict telemetry fixture evidence.
- Interrogation finding `INT-OIL-REM-005`: resolved by command alias telemetry evidence.

## Strict Telemetry Fixture

Temporary observer fixture with failing hook recorder:

```text
standard_exit=0
standard_obs=recorded
strict_exit=1
```

Temporary Stop-hook fixture with unavailable observer:

```text
standard=true
strict=block
```

Acceptance covered:

- standard mode preserves primary closeout when observer plumbing fails,
- strict mode blocks failed observation closeout.

## Command Alias Telemetry Fixture

Temporary observer and native hook fixtures for `/interrogation` command metadata:

```text
tools-arcanum=structured-interview-kits:interrogation:interrogation
native-pending=structured-interview-kits	sigil	interrogation	interrogation	.codex/commands/interrogation.md
native-ledger=structured-interview-kits	sigil	interrogation	interrogation	.codex/commands/interrogation.md
```

Acceptance covered:

- canonical capability remains `structured-interview-kits`,
- alias metadata records `interrogation`,
- command metadata records `interrogation`.
- native UserPromptSubmit and Stop hook paths preserve the same metadata as `tools/arcanum`.

## Central-Ledger Dedupe Recovery Fixture

Temporary observer fixture simulating a process that appended the central ledger row before committing `hooks/dedupe.jsonl`:

```text
skipped:duplicate observer emission in central ledger:1
```

Acceptance covered:

- central ledger is checked before append,
- retry without a committed dedupe marker skips,
- the central ledger remains at one row.

## Result

- Validation status: pass
- Promotion readiness: pass for repository-local Codex command-surface baseline readiness
