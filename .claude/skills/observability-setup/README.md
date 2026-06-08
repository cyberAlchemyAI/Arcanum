# Observability Setup

Observability Setup is a Formulae sigil for installing the standard sigil observability package into any repository.

It creates the repo-local folder structure, configuration files, telemetry ledgers, and reflection state needed for sigils to record post-run JSON events without assuming a specific application stack or agent runtime.

## Problem It Solves

Sigils can be used in any repository, but Arcanum should not own every consuming repository's telemetry. Each repository needs a predictable local place to store usage signals and reflection state.

This sigil solves that by scaffolding a portable observability package that any sigil can write to.

## Use When

- a repository will use one or more sigils repeatedly,
- a sigil needs to emit post-run invocation telemetry,
- a team wants reflection thresholds and usage counters to live with the consuming repo,
- the repository does not yet have a sigil observability package,
- an existing package needs to be checked or repaired against the standard structure.

## Do Not Use When

- the task is only to design a sigil without running it in a repository,
- the repository should not persist telemetry,
- the user only wants a one-off manual reflection report,
- the consuming runtime already provides an equivalent telemetry backend and only needs schema mapping.

## Default Package Layout

```text
.arcanum/observability/
  README.md
  config.json
  reflection-state.json
  signals/
    sigil-invocations.jsonl
  by-sigil/
    .gitkeep
  by-capability/
    .gitkeep
  reflections/
    .gitkeep
```

## Storage Recommendation

Use one central source-of-truth ledger with rebuildable lookup indexes by default:

- central ledger: `.arcanum/observability/signals/sigil-invocations.jsonl`,
- per-sigil indexes: `.arcanum/observability/by-sigil/<sigil-name>.jsonl`,
- per-capability indexes: `.arcanum/observability/by-capability/<kind>/<capability-id>.jsonl`,
- reflection reports: `.arcanum/observability/reflections/`.

The central ledger preserves chronological history across all capabilities. Index files contain compact references back to central ledger rows, not full duplicate telemetry events. They can be rebuilt with `framework/observability/scripts/rebuild-observability-indexes.sh`.

## Why This Is Formulae

This sigil performs deterministic setup. It does not decide what a sigil means, synthesize ambiguous evidence, or coordinate reflection. It creates or verifies a known folder and file contract.
