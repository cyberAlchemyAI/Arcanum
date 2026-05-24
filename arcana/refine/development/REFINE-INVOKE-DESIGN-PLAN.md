# Invoke Redefine + Design/Plan: Refine

## Redefined Capability

`refine` is an Arcana seed controller that prepares refinement work for Task Session. It proposes the first executable seed, makes research and loop budget explicit, and defaults later execution to Codex Goal through Task Session when strict handoff coverage passes.

## Architecture View

```text
User target
  -> refine
    -> seed proposal
    -> research offer
    -> preset and loop count
    -> confirmation gate
    -> seed work-pack
      -> task-session --runtime codex --via goal
        -> context-builder handoff pack
        -> codex-goal-profile / native Codex Goal
        -> task-session evidence review
          -> sigil-development or target lifecycle owner
```

## Interface View

Expected user forms:

```text
refine <target>
refine <target> --preset compact|standard|full|deep
refine <target> --research no|bounded|if-gap
refine to <work-pack-path> --task <TASK-ID>
```

The implementation may expose these forms through skill instructions first; CLI or command-surface flags can come later.

## Preflight Output Contract

`refine` returns a proposal before mutation:

```markdown
## Refine Seed Proposal

- Target: <target>
- Seed needed: yes | no
- Proposed task: <task id and title>
- Source context: <paths or selectors>
- Write scope: <paths or none yet>
- Done criteria: <criteria>
- Validation surface: <command or review evidence>
- Preset: compact | standard | full | deep
- Loop count: <n>
- Research: no-research | bounded-research | research-if-gap-appears
- Runtime default: codex-goal
- Goal eligibility: pass | block
- Blocked handoff fields: <items or none>
- Proposed Task Session route: <command shape>
- Confirmation required: yes
```

## Preset Mapping

| Preset | Loop Use | Default Runtime |
| --- | --- | --- |
| compact | One refinement loop without research unless requested. | Codex Goal when strict coverage passes. |
| standard | One loop plus one repair/synthesis pass. | Codex Goal when strict coverage passes. |
| full | Full Refine Loop path with research offer, tournament or repair as needed, and final synthesis. | Codex Goal when strict coverage passes. |
| deep | Full path plus checkpoint before mutation-heavy delegation. | Codex Goal when strict coverage passes. |

## Implementation Layers

| Layer | Decision Question | Minimum Working Unit | Exit Evidence |
| --- | --- | --- | --- |
| L0 | Can `refine` express a seed proposal without executing? | README/SKILL preflight contract and examples. | Proposal example validates. |
| L1 | Can `refine` create or point to a minimal seed work-pack? | Development work-pack and seed behavior. | Seed work-pack has one task/SWU with write scope, done criteria, and validation. |
| L2 | Can `refine` delegate safely to Task Session and Codex Goal by default? | Task Session route contract and blocked handoff behavior. | Unsafe goal handoff blocks with exact fields. |
| L3 | Can `refine` be reusable? | Examples, observability, and validation report. | Sigil Development can assess promotion readiness. |

## Work-Pack Seed

This design produces [WORK-PACK.md](WORK-PACK.md) as the initial executable development manifest.

## Design Verdict

Pass for Sigil Development handoff.
