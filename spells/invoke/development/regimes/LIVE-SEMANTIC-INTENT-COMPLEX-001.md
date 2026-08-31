# Regime: LIVE-SEMANTIC-INTENT-COMPLEX-001

## Goal

Validate that direct native Codex authoring retains and reassesses the complete
Plan domain model while discarding historical execution authority.

## Prompt

- Prompt: `example-prompts/invoke-semantic-intent-complex.md`

## Required Output Patterns

- `"schema_version":"invoke.define-intent-authored-artifact.v1"`
- `"target_id":"target:invoke-plan-successor"`

## Quality Bar

- The repository-owned semantic validator passes the expanded Plan corpus,
  required relations, boundaries, historical dispositions, and topology.
- Two consecutive independent attempts pass.

## Anti-Patterns

- Avoid discarding historical semantics with historical authority.
- Avoid reducing Plan to an authoring/admission evidence shell.
- Avoid opening the hidden fixture oracle or incident directory.

## Observability

- Evidence records the raw prompt, complete artifact, and semantic receipt.

## Lessons To Capture

- Missing Plan parts, relations, boundaries, historical dispositions, or handoff semantics.
