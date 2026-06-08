---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: formulae/observability-setup/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
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
