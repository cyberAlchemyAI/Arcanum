# Validation: Schema Discipline Package

## Summary

This validation plan checks that schema discipline remains lightweight, reviewable, and dependency-free through the first implementation slice.

## Package Checks

```bash
test -f tools/development/schema-discipline/DEFINE.md
test -f tools/development/schema-discipline/DESIGN.md
test -f tools/development/schema-discipline/IMPLEMENTATION-LAYERING.md
test -f tools/development/schema-discipline/SCHEMA-DISCIPLINE-CONTRACT.md
test -f tools/development/schema-discipline/WORK-PACK.md
test -f tools/development/schema-discipline/VALIDATION.md
git diff --check -- tools/development/schema-discipline
```

## Runtime Family Checks

Use runtime as the first artifact-family proof.

```bash
test -f framework/runtime/README.md
test -f framework/runtime/templates/RUNTIME-HANDOFF.md
test -f framework/runtime/templates/RUN.json
test -f framework/runtime/templates/STATUS.json
jq empty framework/runtime/templates/RUN.json
jq empty framework/runtime/templates/STATUS.json
jq -e '.schema_version == "arcanum.runtime.run.v1"' framework/runtime/templates/RUN.json
jq -e '.adapter_profile_path == "artifacts/adapter-profile.json"' framework/runtime/templates/RUN.json
jq -e '.schema_version == "arcanum.runtime.status.v1"' framework/runtime/templates/STATUS.json
```

If the runtime runner is in scope for the slice:

```bash
tools/arcanum-runtime-run --adapter dry-run --handoff framework/runtime/development/fixtures/dry-run/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-dry-run
jq empty /tmp/arcanum-runtime-dry-run/RUN.json
jq empty /tmp/arcanum-runtime-dry-run/STATUS.json
jq -e '.adapter_profile_path == "artifacts/adapter-profile.json"' /tmp/arcanum-runtime-dry-run/RUN.json
jq -e '.validation_grade == "contract"' /tmp/arcanum-runtime-dry-run/STATUS.json
test -f /tmp/arcanum-runtime-dry-run/RESULT.md
test -f /tmp/arcanum-runtime-dry-run/events.jsonl
```

## Review Checks

A successful design/refinement pass must:

- define schema discipline as a governance and validation pattern, not a heavy framework;
- answer the nine handoff questions in `DEFINE.md`, `DESIGN.md`, `IMPLEMENTATION-LAYERING.md`, and `WORK-PACK.md`;
- identify artifact families that need schema discipline first;
- separate Markdown templates, JSON templates, and shell/`jq` validators;
- document inline enum rules;
- define how `schema_version`, `status`, provenance, and validation grades appear across artifacts;
- integrate with refine, invoke, context-builder, task-session, experiment-harness, observability, and ontology promotion;
- name first implementation slices;
- name explicit non-goals.

## Candidate-Vs-Canonical Checks

CyberAlchemy validation must confirm:

- ontology promotion work remains candidate unless explicitly accepted;
- `PromotionRecord` has one primary claim;
- source inputs are pointers, not raw dumps;
- evidence confidence and commitment confidence remain separate;
- observability signals are review inputs, not truth;
- operational use requires visible status, use scope, owner, contradiction path, and bridge validation when cross-branch.

## Dependency Checks

The first three layers pass only if they add no new dependency.

Allowed:

- Markdown templates;
- JSON templates;
- `jq`;
- shell checks;
- fixture review;
- quality-bar review.

Deferred:

- JSON Schema;
- Zod;
- YAML/frontmatter parser dependencies;
- graph database;
- taxonomy repository dependency.

## Current Validation Run

Date: 2026-05-25

Result: pass.

Checks run:

- `test -f` for all schema discipline package files.
- `git diff --check -- tools/development/schema-discipline`.
- `jq empty framework/runtime/templates/RUN.json`.
- `jq empty framework/runtime/templates/STATUS.json`.
- `jq -e '.schema_version == "arcanum.runtime.run.v1"' framework/runtime/templates/RUN.json`.
- `jq -e '.adapter_profile_path == "artifacts/adapter-profile.json"' framework/runtime/templates/RUN.json`.
- `jq -e '.schema_version == "arcanum.runtime.status.v1"' framework/runtime/templates/STATUS.json`.
- `tools/arcanum-runtime-run --adapter dry-run --handoff framework/runtime/development/fixtures/dry-run/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-schema-discipline-dry-run`.
- `jq empty /tmp/arcanum-schema-discipline-dry-run/RUN.json`.
- `jq empty /tmp/arcanum-schema-discipline-dry-run/STATUS.json`.
- `jq -e '.adapter_profile_path == "artifacts/adapter-profile.json"' /tmp/arcanum-schema-discipline-dry-run/RUN.json`.
- `jq -e '.validation_grade == "contract"' /tmp/arcanum-schema-discipline-dry-run/STATUS.json`.
- `test -f /tmp/arcanum-schema-discipline-dry-run/RESULT.md`.
- `test -f /tmp/arcanum-schema-discipline-dry-run/events.jsonl`.

Dry-run evidence:

```text
RUN_DIR=/tmp/arcanum-schema-discipline-dry-run
STATUS=passed
RESULT=/tmp/arcanum-schema-discipline-dry-run/RESULT.md
```
