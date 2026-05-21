# Arcanum Transmutation: codex goal profile

<!-- arcanum:capability-id codex-goal-profile -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier transmutations -->
<!-- arcanum:command codex-goal-profile -->
<!-- arcanum:runtime codex -->

## Objective

Run the installed Arcanum transmutation `codex-goal-profile` using the canonical package at `transmutations/codex-goal-profile/`.

## Process

1. Read `transmutations/codex-goal-profile/SKILL.md`.
2. Resolve exactly one work-pack task or SWU from the user request.
3. Check readiness before producing a runnable native Codex Goal.
4. Return either a paste-ready `/goal` command or a blocked profile with the exact unblock action.

## Guardrails

- Do not implement a competing Arcanum `/goal`.
- Do not claim runtime ownership; Codex native Goals own `/goal`, pause, resume, clear, continuation, and completion.
- Do not generate a goal for an unselected task bundle.
- Preserve source work-pack, selected unit, write scope, validation surface, and stop condition.
