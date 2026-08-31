# Signal Observer

Signal Observer is an Arcana sigil for post-run observation of sigil executions. It reads a completed invocation envelope, derives behavior-level signals, appends telemetry, and recommends whether the sigil needs reflection or targeted maintenance.

It is non-blocking by default. Its job is not to redo the user's task; its job is to make the execution learnable.

## Problem It Solves

Without observation, sigils only improve when someone remembers a problem and manually revisits the workflow. Signal Observer captures lightweight evidence from real use: quality status, anti-pattern hits, workflow gaps, output drift, validation gaps, and reflection triggers.

That evidence lets future maintainers improve sigils from repeated signals rather than isolated impressions.

## Use When

- a sigil run has just completed, blocked, or failed,
- an invocation envelope exists or can be assembled,
- the project uses the repository-local observability package,
- the team wants a durable signal record for future reflection,
- usage patterns should influence sigil maintenance.

## Do Not Use When

- the primary task is still in progress,
- the run produced no meaningful output or decision,
- telemetry would include secrets or sensitive raw content,
- observability write failure would distract from urgent user work,
- a full reflection cycle is already underway.

## Observation Flow

1. Load or assemble the invocation envelope.
2. Validate that required envelope sections exist.
3. Inspect visible execution results, changed artifacts, and validation outcomes.
4. Derive behavior-level signals.
5. Append one JSON object to the configured JSONL ledger.
6. Update reflection counters when configured.
7. Return signal counts and recommended follow-up.

## Output

The sigil emits:

- observed sigil name,
- observation result,
- signal counts by type,
- ledger path,
- reflection trigger state,
- recommended follow-up actions.

## Hook Self-Tracking

Signal Observer may record its own background work only in the hook operations ledger:

```text
.arcanum/observability/hooks/hook-operations.jsonl
```

It must not emit normal capability telemetry for its own hook operation. Hook rows carry `observe: false` so observer activity does not recursively trigger more observation.

## Related Docs

- [Sigil Observability Hook](../../framework/observability/SIGIL-OBSERVABILITY-HOOK.md)
- [Repository Observability Package](../../framework/observability/REPOSITORY-PACKAGE.md)
- [Hook Operations Ledger](../../framework/observability/HOOK-OPERATIONS-LEDGER.md)
- [Observed Runs](../../framework/observability/OBSERVED-RUNS.md)
- [Observability Setup](../../formulae/observability-setup/)

## Why This Is Arcana

Signal Observer coordinates evidence interpretation, quality assessment, telemetry mutation, and reflection routing. It is not just a file append; it turns execution traces into governed maintenance signals.
