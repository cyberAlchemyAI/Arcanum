# Regime: LIVE-SEMANTIC-INTENT-MEDIUM-001

## Goal

Validate that direct native Codex authoring preserves the complete semantic
contract of Complexity Example Ladder rather than only its three rungs.

## Prompt

- Prompt: `example-prompts/invoke-semantic-intent-medium.md`

## Required Output Patterns

- `"schema_version":"invoke.define-intent-authored-artifact.v1"`
- `"target_id":"target:complexity-example-ladder"`

## Quality Bar

- The repository-owned semantic validator passes parsed concepts, relations,
  boundaries, facets, and authority preservation.
- Two consecutive independent attempts pass.

## Anti-Patterns

- Avoid treating Low, Medium, and Complex as the whole intent denominator.
- Avoid opening the hidden fixture oracle.

## Observability

- Evidence records the raw prompt, complete artifact, and semantic receipt.

## Lessons To Capture

- Lost invariant, progression, evidence separation, option balance, or authority.
