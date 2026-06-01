# Refine Seed Proposal

## Target

- Target: `/home/vrondelli/projects/domainspec-core/arcanum/framework/observability/development`
- Request: refine observability solutions and include `Arize-ai/openinference` (`https://github.com/Arize-ai/openinference`) as an option.
- Preset: `standard`
- Research mode: `bounded-research`

## Source Context

Local source surface:

- `framework/observability/ARCHITECTURE-OVERVIEW.md`
- `framework/observability/README.md`
- `framework/observability/SIGIL-OBSERVABILITY-HOOK.md`
- `framework/observability/REPOSITORY-PACKAGE.md`
- `framework/observability/development/*.md`
- `framework/observability/scripts/*.sh`
- `.codex/commands/refine.md`
- `arcana/refine/SKILL.md`
- `arcana/refine/REFINEMENT-LOOP.md`

External option included by request:

- `Arize-ai/openinference`: OpenInference presents itself as OpenTelemetry-compatible AI observability conventions and instrumentation, with semantic conventions and instrumentation libraries across Python, JavaScript, Java, and Go, and support for OTEL-compatible collectors.

## Write Scope

This blocked refinement run may write only the refine-owned evidence folder:

```text
framework/observability/development/refinement-runs/arcanum-refine-20260525T153651Z/
```

It does not mutate canonical observability architecture, scripts, templates, or command files.

## Done Criteria

- The `/refine` command bridge resolves.
- The command-backed execution attempt is preserved.
- The target-local run folder includes `RUN-MANIFEST.md`, `evidence-index.json`, `REFINE-SEED-PROPOSAL.md`, `GOAL-HANDOFF.md`, `RESULT.md`, and `stages/`.
- Every canonical stage records either an artifact path or blocked reason.
- The OpenInference option is recorded as bounded external research input, not promoted repository architecture.
- Observability closeout status is reported.

## Validation Surface

- `tools/arcanum --resolve /refine`
- `tools/arcanum --resolve context-builder`
- `tools/arcanum --resolve invoke`
- `tools/arcanum --resolve interrogation`
- `tools/arcanum --resolve distill`
- `tools/arcanum --exec --output .arcanum/observability/runs/session-20260525T153651Z/arcanum-refine-20260525T153651Z/refine-command-output.md refine "..."`
- `jq empty framework/observability/development/refinement-runs/arcanum-refine-20260525T153651Z/evidence-index.json`

## Planned Stage Configuration

1. Context Builder evidence baseline: `context-builder`, `standard`, `--strict --emit both --handoff codex-goal`.
2. Invoke Define: `invoke`, `define`.
3. Interrogation refine-review: `interrogation`, `refine-review`.
4. Research decision: `refine`, `bounded-research`.
5. Distill: `distill`, `standard`.
6. Invoke Redefine / Design: `invoke`, `design`.
7. Interrogation refine-design-review: `interrogation`, `refine-design-review`.
8. Distill Repair: `distill`, `validate`.
9. Invoke Plan: `invoke`, `plan`.
10. Final Interrogation and Synthesis: `interrogation`, `refine-final`, followed by refine-owned synthesis.
