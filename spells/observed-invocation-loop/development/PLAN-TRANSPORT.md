# Plan Transport: Observed Invocation Loop

## Transport Summary

- Source spell: `invoke`
- Source modes: define, design, plan
- Target lifecycle authority: `spellcraft`
- Planned artifact: `observed-invocation-loop`
- Recommended next route: execute work-pack by SWU through a mutation-capable task session after approval.
- Latest refresh: hook-first interrogation incorporated and planning gaps resolved.

## Produced Artifacts

| Artifact | Path |
| --- | --- |
| spell contract | `spells/observed-invocation-loop/README.md` |
| define spec | `spells/observed-invocation-loop/development/DEFINE-SPEC.md` |
| glossary | `spells/observed-invocation-loop/development/GLOSSARY.md` |
| design bundle | `spells/observed-invocation-loop/development/DESIGN.md` |
| implementation layering | `spells/observed-invocation-loop/development/IMPLEMENTATION-LAYERING.md` |
| implementation plan | `spells/observed-invocation-loop/development/IMPLEMENTATION-PLAN.md` |
| work-pack | `spells/observed-invocation-loop/development/WORK-PACK.md` |
| interrogation report | `spells/observed-invocation-loop/development/INTERROGATION.md` |

## Handoff Notes

- This is a spell, not a sigil, because it composes observation, reflection, runtime wrappers, and lifecycle routing.
- `signal-observer` should receive the generic observation extraction.
- `workflow-reflect` should receive deterministic script support.
- Experiment harness should delegate to the generic observer rather than own the global path.
- The implementation is hook-first: telemetry append must be enforced by runtime adapters, wrappers, or deterministic closeout hooks, not by agent attention.
- L3 now requires a hook-driven local adapter pilot for one skill, one sigil, and one spell path.
- Generic telemetry must preserve legacy `sigil` compatibility while adding `capability.id`, `capability.kind`, and `by-capability/<kind>/<id>.jsonl` fanout.

## Refresh Review

| Check | Status | Notes |
| --- | --- | --- |
| Define/design/plan alignment | pass | Hook-first principle appears in define, design, plan, layering, and work-pack. |
| Transport freshness | refreshed | Interrogation and hook-first handoff notes added. |
| Execution readiness | pass | L0 can start; L2/L3 are specified as implementation tasks with no planning ambiguity. |
| User goal coverage | pass | The pack distinguishes hook-enforced telemetry from manual observer calls and selects concrete pilot adapters. |

## Open Refresh Items

| Item | Severity | Route |
| --- | --- | --- |
| Select local adapter files for the L3 pilot. | resolved | Use the pilot adapter targets in `IMPLEMENTATION-PLAN.md`. |
| Add concrete validation scripts after implementation starts. | resolved for planning | Validation behavior is specified; command files are implementation work. |

## Pilot Adapter Targets

| Kind | Pilot Adapter |
| --- | --- |
| skill | `.arcanum/runtimes/github-copilot/skills/arcanum-orchestrate/SKILL.md` |
| sigil | `.arcanum/runtimes/github-copilot/skills/arcanum-sigil-signal-observer/SKILL.md` |
| spell | `.arcanum/runtimes/github-copilot/skills/arcanum-spell-invoke/SKILL.md` |
