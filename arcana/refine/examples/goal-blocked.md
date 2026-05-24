# Example: Codex Goal Blocked

## Refine Seed Proposal

- Target: `arcana/refine`
- Seed needed: no
- Proposed task: `TASK-REFINE-001 - Create refine sigil package`
- Source context: `arcana/refine/development/WORK-PACK.md`
- Write scope: `arcana/refine/README.md`, `arcana/refine/SKILL.md`, `arcana/refine/examples/`
- Done criteria: initial sigil package and examples exist
- Validation surface: markdown link review and required-term grep
- Preset: standard
- Loop count: one loop plus repair/synthesis
- Research: no-research
- Planned execution stages:
  - context-builder: blocked, missing persisted handoff pack
  - invoke-define: skipped until context-builder block is resolved
  - interrogation: skipped until context-builder block is resolved
  - distill: skipped until context-builder block is resolved
  - invoke-design-plan: skipped until context-builder block is resolved
  - sigil-development: not_applicable until refinement can run
- Runtime default: codex-goal
- Goal eligibility: block
- Blocked handoff fields: missing persisted context pack Markdown, missing context pack JSON/index, strict coverage not recorded
- Proposed Task Session route: blocked until Context Builder produces strict handoff evidence
- Confirmation required: yes

## Blocked Fallback

Refine does not silently route to local Task Session. The user may explicitly request local fallback, or the missing handoff fields must be produced first.
