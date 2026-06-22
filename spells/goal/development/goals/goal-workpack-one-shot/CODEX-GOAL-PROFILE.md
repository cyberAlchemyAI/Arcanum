# Codex Goal Profile: Goal Work-Pack One-Shot

## Codex Goal Profile Result

- Source work-pack: `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/WORK-PACK.md`
- Selected unit: `GOAL-WORKPACK-ONE-SHOT` (`SWU-GOAL-001` through `SWU-GOAL-010`)
- Readiness: pass
- Goal budget: 4000 characters, pass
- Decision profile: none; consumed fields n/a
- One-shot mode: yes
- Capability policy: allowed lanes are Spellcraft, local fallback for staged
  sync proposal, Task Session, Decision Gate for approval/blocker decisions,
  Experiment Harness, and runtime installer; subagents are not authorized;
  every attempted SWU requires a receipt.
- Sidecar profile: `arcanum/spells/goal/development/goals/goal-workpack-one-shot/CODEX-GOAL-PROFILE.md`
- Native Goal:

```text
/goal Outcome: execute the full arcanum/spells/goal work-pack stream from arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/WORK-PACK.md, covering SWU-GOAL-001..010 in W0->W3 order. Use sidecar arcanum/spells/goal/development/goals/goal-workpack-one-shot/CODEX-GOAL-PROFILE.md plus handoff-pack.md and handoff-index.json before broader context. Verification: produce receipts for each attempted SWU and a final report proving W0 Spellcraft validation, W1 read-only goal bind/frontier/risk/result, W2 dispatch/receipt/audit/staged-delta, W3 approval/gap/telemetry/Experiment Harness evidence, and installer readiness when allowed. Boundaries: keep public/private split; no filled profile content in public files; no active Craft mutation without staged proposal plus batch-specific approval token; no generated surfaces except installer output; no publication, commit, push, PR, or parent gitlink movement. Iteration: run pack-first, one SWU at a time, obey wave gates, stop for blocker decisions or missing write scope, and report extra sources with gap and effect. Stop blocked if W0 fails, runtime source scope is unclear, approval is missing, reusable evidence is absent, generated-surface ownership is unclear, or validation cannot prove the current layer.
```

- Verification surface: per-SWU receipts plus final stream report; profile
  validation covers JSON parse, markdown links, goal budget, strict coverage,
  public-boundary scan, trailing whitespace, and diff hygiene.
- Boundaries: write only within current SWU scope; protected operations require
  their owner gates; no private profile content; no generated surfaces except
  installer output; no commit/push/PR/gitlink movement.
- Handoff pack:
  - Markdown: `arcanum/spells/goal/development/goals/goal-workpack-one-shot/handoff-pack.md`
  - JSON/index: `arcanum/spells/goal/development/goals/goal-workpack-one-shot/handoff-index.json`
- Strict coverage: pass
- Fallback exploration: named gaps only (`G-GOAL-SCHEMA-HOME`,
  `G-GOAL-CRAFT-SYNC`, `G-GOAL-RUNTIME-SOURCE`, `G-GOAL-FIXTURE-SET`,
  `B-GOAL-PROMOTION-EVIDENCE`)
- Extra-source reporting: required
- Stop condition: stop blocked and report wave, SWU, evidence inspected, owner,
  exact unblock action, residue, reroute, and prior-SWU validity whenever a
  wave gate, write scope, approval, generated-surface, public/private,
  promotion-evidence, or terminal-receipt requirement is unclear.
- Validation: pass; JSON parse, all-SWU/source-path coverage, dispatch
  validation, native goal budget, markdown links, public-boundary scan,
  trailing whitespace scan, and diff hygiene checks.

## Readiness Notes

- The selected stream is explicit and covers the whole work-pack.
- W0 is the mandatory first gate.
- Runtime source/write scope is allowed only after Spellcraft or the current
  Task Session selects it for the active SWU.
- Approval and Craft mutation remain protected.
- Registry readiness remains evidence-gated.
- Private decision profile was not read or consumed.
