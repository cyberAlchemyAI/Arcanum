# Example: Existing Work-Pack Preflight

## User Target

```text
refine to arcana/refine/development/WORK-PACK.md --swu SWU-REFINE-002
```

## Refine Seed Proposal

- Target: `arcana/refine/development/WORK-PACK.md`
- Seed needed: no
- Proposed task: `SWU-REFINE-002` Add examples and validation evidence
- Source context: `arcana/refine/development/WORK-PACK.md`, `arcana/refine/SKILL.md`, `arcana/refine/REFINEMENT-LOOP.md`
- Write scope: `arcana/refine/examples/`, `arcana/refine/development/VALIDATION.md`
- Done criteria: examples cover seed proposal, existing work-pack preflight, and blocked goal handoff
- Validation surface: `rg` required route and research terms, then `git diff --check`
- Preset: compact
- Loop count: 1
- Research: research-if-gap-appears
- Planned execution stages:
  - context-builder: required, selected SWU has source context and validation surface
  - invoke-define: required after confirmation
  - interrogation: required after invoke define
  - distill: required after interrogation
  - invoke-design-plan: skipped by compact preset unless repair is required
  - sigil-development: not_applicable unless the run changes reusable sigil behavior
- Runtime default: codex-goal
- Goal eligibility: pass
- Blocked handoff fields: none
- Proposed Task Session route: `/task-session to arcana/refine/development/WORK-PACK.md --swu SWU-REFINE-002 --runtime codex --via goal`
- Confirmation required: yes

## Expected Behavior

Refine does not create a new seed work-pack because the selected SWU already has write scope, done criteria, and validation surface. It records the research choice, confirms the budget, and prepares the Task Session route.
