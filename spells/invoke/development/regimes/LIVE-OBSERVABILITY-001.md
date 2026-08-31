# Regime: LIVE-OBSERVABILITY-001

## Goal

Validate that experiment loop reports can be observed and converted into telemetry without recursive hook observation.

## Prompt

- Prompt: `example-prompts/invoke-observability-live-pass.md`

## Required Output Patterns

- `## Invoke Result`
- `semantic receipt|Semantic receipt`
- `claim ceiling|Claim ceiling`

## Quality Bar

- Observer telemetry must expose `quality_bar_status`, `anti_pattern_hits`, `workflow_gaps`, and `reflection_trigger`.

## Anti-Patterns

- Avoid observing hook operation rows as capability telemetry.
- Avoid duplicate telemetry emissions for the same report.

## Observability

- Hook ledger rows must carry `observe: false`.

## Lessons To Capture

- Missing telemetry fields.
- Dedupe behavior.
- Hook loop risks.
