# Codex Goal Profile: SWU-GOAL-001 Spellcraft Validate

## Codex Goal Profile Result

- Source work-pack: `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/WORK-PACK.md`
- Selected unit: `SWU-GOAL-001`
- Readiness: pass
- Goal budget: 4000 characters, pass
- Decision profile: none; consumed fields n/a
- One-shot mode: no
- Capability policy: Spellcraft lifecycle validation only; no subagents, runtime
  SWUs, active Craft mutation, generated surface authoring, promotion claims, or
  ambient approval.
- Sidecar profile: `arcanum/spells/goal/development/goals/swu-goal-001-spellcraft-validate/CODEX-GOAL-PROFILE.md`
- Native Goal:

```text
/goal Outcome: execute SWU-GOAL-001 for arcanum/spells/goal by producing a Spellcraft validation report for the source/design/plan packet. Use sidecar arcanum/spells/goal/development/goals/swu-goal-001-spellcraft-validate/CODEX-GOAL-PROFILE.md and strict handoff pack arcanum/spells/goal/development/goals/swu-goal-001-spellcraft-validate/handoff-pack.md plus handoff-index.json before reading broader context. Verification: report pass|flag|block with evidence covering README.md, decision-profile.schema, define SPEC/DEFINITIONS, design ARCHITECTURE/RULES/CONTRACTS/SCHEMAS, WORK-PACK.md, and PLAN-DISPATCH.json. Boundaries: write only validation report/receipt under arcanum/spells/goal/development/spellcraft-runs/ or equivalent public-safe validation path; do not implement runtime SWUs, mutate Craft ledger, copy filled decision profiles, generate SKILL.md, publish, commit, push, PR, or move parent gitlinks. Iteration: work pack first, fallback exploration only for named gaps G-GOAL-SCHEMA-HOME or G-GOAL-CRAFT-SYNC, and report every extra source with gap and effect. Stop blocked if lifecycle authority, public/private boundary, generated-surface boundary, schema home, or validation evidence is unclear; return blockers, residue, and reroute.
```

- Verification surface: `spellcraft validate arcanum/spells/goal` or
  reviewable lifecycle validation report.
- Boundaries: write only validation report/receipt under
  `arcanum/spells/goal/development/spellcraft-runs/` or equivalent public-safe
  validation path; source context is limited to strict handoff pack and indexed
  source contracts.
- Handoff pack:
  - Markdown: `arcanum/spells/goal/development/goals/swu-goal-001-spellcraft-validate/handoff-pack.md`
  - JSON/index: `arcanum/spells/goal/development/goals/swu-goal-001-spellcraft-validate/handoff-index.json`
- Strict coverage: pass
- Fallback exploration: named gaps only (`G-GOAL-SCHEMA-HOME`,
  `G-GOAL-CRAFT-SYNC`)
- Extra-source reporting: required
- Stop condition: stop blocked and report blocker, evidence inspected, owner,
  exact unblock action, residue, and reroute whenever lifecycle authority,
  public/private boundary, generated-surface boundary, schema home, validation
  evidence, or runtime-implementation dependency is unclear.
- Validation: pass; JSON parse, goal budget, strict coverage, selected-unit,
  markdown links, public-boundary, trailing whitespace, and diff hygiene checks.

## Readiness Notes

- Dependencies are satisfied: none for `SWU-GOAL-001`.
- Write scope is bounded.
- Done criteria are concrete.
- Validation surface is available.
- Handoff Markdown and JSON/index are present.
- One-shot mode is not active.
- Private decision profile was not read or consumed.
