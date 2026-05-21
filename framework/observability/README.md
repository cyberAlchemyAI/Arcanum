# Observability

This folder defines the library-level observability convention for sigil usage.

Observability is how sigils become maintainable after their first draft. A sigil should preserve enough usage signal to show whether its trigger conditions, process, Quality Bar, Anti-Patterns, templates, and output contract are working in practice.

For the general post-run hook pattern, see [Sigil Observability Hook](SIGIL-OBSERVABILITY-HOOK.md).

For the repository-local package that makes the hook portable across consuming repositories, see [Repository Observability Package](REPOSITORY-PACKAGE.md).

For background hook audit rows and loop guards, see [Hook Operations Ledger](HOOK-OPERATIONS-LEDGER.md).

For long-running task boundaries and recoverable checkpoints, see [Observed Runs](OBSERVED-RUNS.md).

## What To Observe

Observe meaningful sigil executions: runs that produce or attempt to produce a user-facing artifact, decision, validation result, orchestration result, telemetry signal, or reflection report.

Useful signals include:

- execution mode,
- generated output count,
- Quality Bar status,
- Anti-Pattern hits,
- workflow gaps,
- output-contract drift,
- artifact redundancy,
- navigation efficiency,
- user corrections,
- observer recommendations,
- reflection trigger state.

## Where Signals Belong

For a reusable sigil, prefer sigil-local templates and clearly named signal files. A typical pattern is:

```text
<tier>/<sigil-name>/templates/usage-telemetry.md
<tier>/<sigil-name>/templates/reflection-report.md
observability/signals/sigil-invocations.jsonl
```

The central ledger is the source of truth. `by-sigil/` and `by-capability/` are rebuildable lookup indexes that point to central ledger rows rather than storing duplicate telemetry events.

Generated telemetry can be stored wherever the using project or runtime keeps operational records. The sigil library defines the schema and lifecycle pattern; it does not require one global storage backend.

Use [invocation-envelope.json](templates/invocation-envelope.json) as the portable JSON shape for one observed sigil invocation.

Use [observability-setup](../../formulae/observability-setup/) to install or verify the package in a consuming repository.

## Observer Role

Observation should be performed by a separate observer pass when possible.

The observer identifies signals, classifies gaps, and recommends reflection or iteration. The observer should not directly rewrite the sigil unless the main execution explicitly delegates that edit step.

## Reflection Triggers

Default reflection triggers:

- manual request,
- 5 meaningful executions,
- 10 generated outputs,
- 3 related workflow gaps,
- 1 severe workflow gap.

Sigils may override these defaults when their usage rate, risk level, or output size justifies a different threshold.

## Cross-Cutting Reflection Signals

Two workflow gaps should be available to every observed capability:

- `artifact-redundancy`: duplicate artifacts, duplicate ownership, or stale compatibility surfaces make it unclear which artifact is authoritative.
- `navigation-efficiency`: the artifact is hard to traverse because task IDs, SWUs, source contracts, next actions, or start-here links are missing.

These signals matter because they often appear before a quality failure. A plan may be factually correct but still expensive for the next human or agent to use. Observers should record them whenever the output forces repository search, manual reconciliation, or repeated explanation to continue the work.

## Related Sigil

Use [sigil-development](../../arcana/sigil-development/) to create, revise, observe, reflect on, or iterate a sigil through this lifecycle.
