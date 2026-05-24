# Refine Validation

## Validation Summary

| Check | Result | Evidence |
| --- | --- | --- |
| Seven loop artifacts exist. | pass | `REFINE-CONTEXT-PACK.md` through `REFINE-SIGIL-DEVELOPMENT-HANDOFF.md` are present. |
| Research decision records offered/selected/deferred state. | pass | `REFINE-RESEARCH-DECISION.md` selects `research-if-gap-appears`. |
| Distill selects seed/preflight controller. | pass | `REFINE-DISTILL-REVIEW.md` rejects Task Session fallback mode, Invoke wrapper, and new engine. |
| Sigil Development owns lifecycle. | pass | `REFINE-SIGIL-DEVELOPMENT-HANDOFF.md`, `README.md`, and `SKILL.md` route promotion to Sigil Development. |
| Codex Goal is default and unsafe handoff blocks. | pass | `SKILL.md` process and `examples/goal-blocked.md`. |
| Task Session owns execution through Codex Goal. | pass | README, SKILL, work-pack, and examples include `--runtime codex --via goal`; `REFINEMENT-LOOP.md` says Task Session executes the approved loop. |
| Existing work-pack preflight skips seed creation. | pass | `examples/existing-work-pack-preflight.md` shows `Seed needed: no` for an existing SWU. |
| Required skills are mandatory during execution. | pass | `SKILL.md` defines `<required-sigils>` and `<execution-plan-contract>`; `REFINEMENT-LOOP.md` defines the execution rule. |
| Experiment Harness is initialized. | pass | `EXPERIMENT-PROFILE.md` and regimes exist; generic harness validation passes. |
| Refine live-output gate distinguishes proposal from final refinement. | pass | `run-validation-fixtures.sh` reports `REFINE_LIVE_VALIDATION=pass` because `sigil-new-low.output.md` now includes Task Session/Codex Goal execution status and a final refinement output section. |
| Promotion evidence exists. | flag | `sigil-new-low.output.md` reports `Promotion evidence: no` and `Status: block` because Task Session/Codex Goal execution could not complete in the current environment. |
| Observability and reflection templates exist. | pass | `templates/usage-telemetry.md` and `templates/reflection-report.md`. |
| Registry discoverability exists. | pass | `registry/SIGILS.md` and `arcana/README.md` include `refine`. |

## Validation Commands

```bash
find arcana/refine -type f | sort
rg -n "required-sigils|execution-plan-contract|Planned execution stages|research-if-gap-appears|--runtime codex --via goal|Sigil Development|seed/preflight controller|REFINEMENT-LOOP" arcana/refine registry/SIGILS.md arcana/README.md
arcana/refine/development/run-validation-fixtures.sh
git diff --check -- arcana/refine registry/SIGILS.md arcana/README.md
```

## Promotion Status

Status: pilot.

The initial package is usable, but not promotion-ready. Promotion requires realistic experiment-harness examples for:

- vague target to seed proposal,
- existing work-pack to preflight,
- research mode selection,
- blocked Codex Goal handoff,
- confirmed route to Task Session,
- at least one final refinement result produced through Task Session/Codex Goal rather than only a proposed route.
