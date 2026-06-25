# Artifact Constitution

This repository treats every created file as an artifact with an owner, a retention
class, and a validation obligation. The goal is to keep source, durable evidence,
generated output, and local runtime state from collapsing into one unreviewable
pile.

## Classes

### Source Artifacts

Source artifacts define reusable behavior, process, templates, command surfaces,
scripts, schemas, documentation, or tests. They are versioned by default.

Examples:

- `arcana/**`
- `spells/**`
- `transmutations/**`
- `framework/**`
- `disciplines/**`
- `registry/**`
- `.codex/commands/**`
- `tools/**`

### Durable Evidence Artifacts

Durable evidence artifacts are run outputs that are intentionally promoted as
proof, examples, or benchmark records. They may be versioned only when a nearby
document names why the evidence is durable.

Examples:

- curated fixture inputs and expected outputs
- validation reports referenced by a work-pack
- benchmark summaries that support a committed decision

### Generated Artifacts

Generated artifacts are reproducible run output, temporary experiment evidence,
lookup indexes, logs, or cache-like files. They are ignored by default. A
generated artifact may be force-added only when it is promoted to durable
evidence.

Examples:

- `**/development/runs/**`
- `**/development/example-runs/**`
- `**/development/example-outputs/**`
- `.arcanum/observability/runs/**`
- `.arcanum/observability/reflections/**`
- `.arcanum/observability/by-sigil/*.jsonl`
- `.arcanum/observability/by-capability/**/*.jsonl`
- `.arcanum/observability/hooks/*.jsonl`
- `.arcanum/observability/signals/*.jsonl`
- `.arcanum/observability/reflection-state.json`
- `benchmark/artifacts/**`
- `benchmark/logs/**`

### Local Runtime Artifacts

Local runtime artifacts are machine-specific state. They must never become
versioned source or durable evidence.

Examples:

- `.arcanum/codex-home/**`
- `.arcanum/codex-home-smoke/**`
- `.arcanum/runtime/**`
- `tmp/**`
- `*.sqlite`, `*.sqlite-shm`, `*.sqlite-wal`
- `auth.json`
- `installation_id`

## Rules

1. Every new artifact must be classified before it is committed.
2. Source artifacts must remain visible to Git unless they are intentionally
   deleted.
3. Generated artifacts must be ignored unless promoted to durable evidence with
   an explicit reason in adjacent documentation, a work-pack, or a validation
   report.
4. Local runtime artifacts must be ignored and must not be force-added.
5. Observability indexes, hook ledgers, signals, reflection state, run folders,
   and reflection reports are generated artifacts. Keep only the package
   skeleton and explicit configuration under version control by default.
6. Adding a new artifact-producing path requires updating `.gitignore` and this
   constitution when the path belongs to generated or local runtime state.
7. Validation must run after file-creating tools and before handoff.

## Promotion Boundary Rules

| Rule ID | Selector | Rule | Validation mode | Status |
| --- | --- | --- | --- | --- |
| `artifact.promotion.development-to-canonical` | A source artifact change derives from a development artifact, run package, runtime observation, validation report, glossary candidate, architecture draft, or other non-authoritative evidence. | The change must be framed as a promotion patch that names the source evidence, target canonical artifact, owning route, selected durable claim or structure, omitted candidate material, validation surface, approval state, and required index or generated-surface sync. Raw development content must not be bulk-copied into canonical source. | hybrid: artifact constitution validation plus source-review against [Development To Canonical Promotion](DEVELOPMENT-TO-CANONICAL-PROMOTION.md) | canonical |

### Examples

- A task-session result proposes a new rule for `framework/`; the final source
  change extracts only the accepted rule, cites the task-session path as
  evidence, updates affected lookup surfaces, and records validation.
- An architecture development artifact proposes a dependency rule; the canonical
  architecture artifact receives a normalized rule, companion indexes are
  updated, and unselected draft notes stay in `development/`.
- A local glossary candidate becomes Arcanum-wide terminology only after
  `definitions-governance` patches `definitions/DEFINITIONS.md` and syncs
  `definitions/DEFINITIONS-INDEX.md`.

### Non-Examples

- Committing an entire refinement-run folder because one result looked useful.
- Copying development prose into a canonical README without naming omitted
  candidate material, owner route, or validation surface.
- Treating a validation report as direct authority instead of evidence for a
  reviewed source change.

## Rendering Rules

1. Charts and visual artifacts must not rely on literal `\n` sequences for label,
   legend, title, annotation, or tooltip line breaks. Use HTML markup such as
   `<br>` or structured renderer-supported rich text instead.
2. When an artifact renderer has inconsistent newline handling, prefer explicit
   HTML or structured markup that survives export, screenshot, and browser
   rendering.

## Related Constitutions

- [Schema Constitution](SCHEMA-CONSTITUTION.md) governs canonical
  machine-readable schema artifact format.
- [Artifact Metadata Constitution](ARTIFACT-METADATA-CONSTITUTION.md) governs
  artifact intent/type tags used to select constitutions and validation
  profiles.
- [Markdown Linking Constitution](MARKDOWN-LINKING-CONSTITUTION.md) governs
  Markdown link hygiene, source references, and relation-like edge declarations.

## Validation Contract

Run:

```bash
tools/validate-artifact-constitution.sh
```

Fixture self-test:

```bash
tools/validate-artifact-constitution.sh --self-test
```

The validator checks the current Git working tree for new local/generated
artifacts that are not ignored, plus tracked local runtime state that should
never be versioned. It also validates schema constitution format boundaries for
new machine-readable schemas and schema-shaped Markdown under template/source
paths. Hook integrations run the same validator after file-writing tools so
violations are caught close to creation time.

Current limitation: validation still relies heavily on path and filename
heuristics. Metadata-driven constitution selection is governed by the Artifact
Metadata Constitution and remains candidate until its validation adapter is
implemented.
