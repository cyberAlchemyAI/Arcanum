# Goal Handoff: Native Refine Orchestration

## Objective

Run the canonical Refine loop for `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/REFINE-SEED-PROPOSAL.md` without recursive Codex execution.

## Runtime Mode

- Preset: `compact`
- Research: `research-if-gap-appears`
- Stage dispatch owner: root `tools/arcanum` process

## Stage Dispatch Contract

The root process dispatches stage commands through:

```bash
tools/arcanum --exec --adapter <stage-adapter> --timeout <seconds> --output <stage-output> <command> <stage-request>
```

The Refine model is not asked to spawn child `codex-exec` processes from inside a Codex sandbox.

## Source Request

target=spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/REFINE-SEED-PROPOSAL.md; preset=compact; research=research-if-gap-appears; use existing run folder spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack; preserve text-intent-substrate.yaml as the schema control surface; primary reader default: AI-curious creative builders; do not execute task-session; produce/update RUN-MANIFEST.md, evidence-index.json, GOAL-HANDOFF.md, RESULT.md, and stages/ artifacts.
