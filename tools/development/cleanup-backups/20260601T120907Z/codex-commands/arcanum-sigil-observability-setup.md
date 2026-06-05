# Arcanum Sigil: observability setup

<!-- arcanum:capability-id observability-setup -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier formulae -->
<!-- arcanum:command arcanum-sigil-observability-setup -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-sigil-observability-setup-<UTC timestamp>`.
- `capability.id`: `observability-setup`
- `capability.kind`: `sigil`
- `capability.tier`: `formulae`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum sigil `observability-setup` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `observability-setup`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/formulae/observability-setup/README.md

````markdown
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

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/formulae/observability-setup/SKILL.md

````markdown
---
name: observability-setup
description: "Use when: installing or verifying the standard sigil observability package in a repository so sigils can append post-run JSON telemetry and reflection state."
argument-hint: "[--path <repo-root>] [--storage central|per-sigil|hybrid] [--repair]"
tier: formulae
domain: observability
version: 0.1.0
origin: created to make sigil telemetry portable across consuming repositories
allowed-tools: Read, Write, Glob, Grep
---

# Sigil: Observability Setup

<objective>
Install or verify a deterministic repository-local observability package for sigil usage telemetry.
</objective>

<logic-type>
Formulae: deterministic repository scaffolding and contract verification.
</logic-type>

<applicability>
Use this sigil when a repository needs a standard local package for sigil invocation telemetry, reflection counters, and reflection reports.
</applicability>

<inputs>
Expected inputs, if available:

- repository root path,
- preferred storage model: `central`, `per-sigil`, or `hybrid`,
- whether existing files should be repaired,
- existing observability folder path, if non-standard.
  </inputs>

<default-output>
Create or verify this package at the repository root:

```text
.arcanum/observability/
```

</default-output>

<process>
1. Identify the repository root. If no path is provided, use the current working repository.
2. Detect whether `.arcanum/observability/` already exists.
3. Select storage model:
   - use `hybrid` by default,
   - use explicit user preference when provided,
   - do not infer a non-default model from unrelated folders.
4. Create missing directories:
   - `.arcanum/observability/`,
   - `.arcanum/observability/signals/`,
   - `.arcanum/observability/by-sigil/`,
   - `.arcanum/observability/hooks/`,
   - `.arcanum/observability/hooks/reflections/`,
   - `.arcanum/observability/runs/`,
   - `.arcanum/observability/reflections/`.
5. Create missing files:
   - `README.md`,
   - `config.json`,
   - `reflection-state.json`,
   - `signals/sigil-invocations.jsonl`,
   - `hooks/hook-operations.jsonl`,
   - `hooks/failures.jsonl`,
   - `hooks/dedupe.jsonl`,
   - `.gitkeep` files for empty optional folders.
6. If files exist, preserve user content unless `--repair` is provided and the file is invalid against the package contract.
7. Validate JSON files parse.
8. Return package path, storage model, files created, files preserved, and validation status.
</process>

<quality-bar>
A successful execution of this sigil must:

- create or verify the standard observability package path,
- preserve existing telemetry by default,
- produce valid JSON config and reflection-state files,
- create an append-only JSONL ledger path,
- state the selected storage model,
- avoid requiring a specific application framework or agent runtime.
  </quality-bar>

<anti-patterns>
Avoid:

- overwriting existing telemetry ledgers,
- storing telemetry inside the Arcanum repository when observing a different consuming repository,
- creating full duplicate per-sigil ledgers instead of rebuildable central-ledger indexes,
- treating setup as reflection,
- adding runtime-specific dependencies to the portable package contract.
  </anti-patterns>

<output-contract>
Return:

```markdown
## Observability Setup Result

- Repository: <path>
- Package path: <path>
- Storage model: central-ledger-reference-indexes
- Files created: <paths>
- Files preserved: <paths>
- Validation: <checks performed>
- Next step: <how sigils should append invocation telemetry>
```

</output-contract>

````
