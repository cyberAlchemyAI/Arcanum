# Regime: LIVE-SEMANTIC-INTENT-LOW-001

## Goal

Validate that direct native Codex authoring represents all bounded semantic
obligations in the mixed Define-v3 source.

## Prompt

- Prompt: `example-prompts/invoke-semantic-intent-low.md`

## Required Output Patterns

- `"schema_version":"invoke.define-intent-authored-artifact.v1"`
- `"target_id":"target:mixed-define-v3"`

## Quality Bar

- The repository-owned semantic validator passes parsed artifact structure.
- Two consecutive independent attempts pass.

## Anti-Patterns

- Avoid heading or keyword-only validation.
- Avoid opening the hidden fixture oracle.

## Observability

- Evidence records the raw prompt, complete artifact, and semantic receipt.

## Lessons To Capture

- Missing bounded concepts, orphan probes, or unjustified facet exclusions.
