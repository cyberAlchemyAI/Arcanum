# Regime: LIVE-PLAN-001

## Goal

Validate that live Codex execution can run `invoke plan` from approved design outputs and produce governed planning artifacts with global implementation layering and work-pack handoff.

## Prompt

- Prompt: `example-prompts/invoke-plan-live-pass.md`

## Required Output Patterns

- `## Invoke Result`
- `Mode:.*plan`
- `Phase status:.*pass`
- `Implementation plan|implementation plan`
- `Implementation layering|implementation layering`
- `Work-pack|work-pack`
- `Validation strategy|validation strategy`
- `Implementation detail|Implementation Detail Specs|implementation-detail`
- `Smallest working units|Smallest Working Units|SWU-`
- `Algorithm|algorithm|pseudocode|step-by-step|transition rules|classification`
- `Blocker ledger|blocker ledger|Unresolved gaps`
- `Plan transport|plan transport|Transport report|transport report`
- `Complexity:.*low|Complexity:.*medium|Complexity:.*high`
- `Per-layer planning:.*compact|Per-layer planning:.*L0`
- `Next route:.*task-session|Next route:.*full|Next route:.*deferred`

## Quality Bar

- Output must include implementation plan, global implementation-layering artifact, work-pack, validation strategy, blocker ledger, plan transport, and next route evidence.
- Medium/high outputs must include implementation-detail specs for execution tasks, including algorithm or rule details for domain-logic tasks.
- Medium/high outputs must include a SWU manifest and task-local SWU lists with parent task, write scope, acceptance evidence, and verification command or reviewable check.
- Output must remain non-mutating and must not claim task execution.

## Anti-Patterns

- Avoid planning without approved design refs.
- Avoid skipping required implementation layering or work-pack companions.
- Avoid treating layer promotion as preference-only.
- Avoid vague task descriptions such as "implement this bundle" without implementation details.
- Avoid task-level handoffs without SWUs for medium/high work-packs.
- Avoid omitting algorithm, state-transition, classification, or data-flow details for domain-logic tasks.
- Avoid executing implementation tasks in plan mode.

## Observability

- Attempt telemetry must record planning validation gaps and anti-pattern hits.

## Lessons To Capture

- Missing companion artifacts.
- Work-pack mode mismatch.
- Per-layer planning missing when complexity is medium/high.
- Missing SWU manifest or task-local SWU mappings.
