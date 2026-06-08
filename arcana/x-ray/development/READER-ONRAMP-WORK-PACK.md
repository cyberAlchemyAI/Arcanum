# WORK-PACK: x-ray Reader On-Ramp

## Objective

Improve `x-ray` outputs so they explain the target to readers who do not already know the domain vocabulary.

The motivating user signal is that current explanations can feel too expert-oriented: they expose structure, but they sometimes expect the reader to already know why a component, dependency, queue, validator, lifecycle state, or policy matters.

## Current Branch

- Worktree: `/home/vrondelli/projects/domainspec-core/arcanum-x-ray-reader-explanations`
- Branch: `codex/x-ray-reader-explanations`
- Source package: `arcana/x-ray/`
- Current lifecycle status: seed

## Reader Problem

An x-ray page can be structurally correct and still fail as an explanation when it:

- labels concepts without defining them,
- shows arrows without saying what changes across the arrow,
- names dependencies without saying what would break if the dependency changed,
- separates evidence and inference without explaining why that distinction matters,
- assumes the reader already knows the target's domain.

## Required Output Behavior

Every meaningful x-ray run should identify a reader baseline:

| Baseline | Meaning |
| --- | --- |
| `newcomer` | The reader may not know the domain or target vocabulary. |
| `working-reader` | The reader knows the domain category but not this target. |
| `expert` | The reader knows the domain and wants compact structural inspection. |
| `unknown` | Audience is not supplied; default prose to newcomer-friendly. |

For each important concept, the generated page should follow this local order:

1. Plain name.
2. Why it matters in this target.
3. What changes, moves, depends on it, or can fail because of it.
4. Local term, handle, diagram label, or technical vocabulary.

## Candidate Changes

- Keep `reader-onramp` in the canonical `SKILL.md` contract.
- Add `Reader baseline` and `Reader on-ramp` to result envelopes and examples.
- Add optional lane-model fields for `reader_baseline` and `reader_onramp` after at least one example proves the shape.
- Add validator checks once the schema is updated:
  - page declares reader baseline,
  - technical labels used in visuals have nearby explanatory text,
  - each important lane has at least one plain-language bridge or an explicit omitted reason.

## Validation Surface

```bash
python3 arcana/x-ray/scripts/validate-xray-example.py --lanes arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json --html arcana/x-ray/examples/visual-layered-order-ingestion.html
python3 arcana/x-ray/scripts/validate-xray-library.py
git diff --check -- arcana/x-ray
rg -n "reader baseline|Reader baseline|reader on-ramp|Reader on-ramp|newcomer|working-reader" arcana/x-ray
```

## Promotion Boundary

This work should not promote `x-ray`. It strengthens the seed contract and prepares the next experiment evidence pass.

Promotion still requires live Experiment Harness evidence for component, process, architecture or codebase, generated L0 HTML/SVG, insufficient-context handling, and validation.
