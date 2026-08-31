# Regime: LIVE-DEFINE-DESIGN-PLAN-001

## Goal

Validate that live Codex execution can produce an inspectable define-to-design-to-plan chain where plan consumes design outputs without inventing upstream authority.

## Prompt

- Prompt: `example-prompts/invoke-define-design-plan-live-pass.md`

## Required Output Patterns

- `## Invoke Result`
- `Mode:.*define`
- `Mode:.*design`
- `Mode:.*plan`
- `Phase status:.*pass`
- `Spec|spec`
- `Glossary|glossary`
- `Define transport|define transport`
- `Context View|context view|View 1`
- `High-Level Structure View|high-level structure|View 2`
- `Low-Level Components View|low-level components|View 3`
- `Workflow Process View|workflow process|View 4`
- `Decision Flow View|decision flow|View 5`
- `Dependency Interface View|dependency interface|View 6`
- `Glossary consistency|glossary consistency`
- `Design transport|design transport`
- `Implementation layering|implementation layering`
- `Work-pack|work-pack`
- `Validation strategy|validation strategy`
- `Implementation detail|Implementation Detail Specs|implementation-detail`
- `Plan transport|plan transport`
- `consumes design|consume design|from approved design|approved design outputs`

## Quality Bar

- Output must include define evidence, design evidence, plan evidence, and clear handoff authority boundaries.
- Plan authority must come from approved design evidence.
- Plan must not execute implementation tasks.
- Plan must include implementation-detail specs or inline implementation details so the next execution worker is not handed vague bundle-level tasks.

## Anti-Patterns

- Avoid invented approvals.
- Avoid collapsing the chain into a one-line summary.
- Avoid routing directly to implementation without work-pack gates.
- Avoid omitting global implementation-layering evidence.
- Avoid vague plan tasks that do not describe how algorithmic or domain-logic work should be implemented.

## Observability

- Attempt telemetry must preserve workflow gaps across all three phases.

## Lessons To Capture

- Handoff drift.
- Missing plan companions.
- Layering or validation strategy gaps.
- Missing task-level implementation details.
