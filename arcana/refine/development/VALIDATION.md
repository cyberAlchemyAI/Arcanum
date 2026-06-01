# Refine Validation

## Validation Summary

| Check | Result | Evidence |
| --- | --- | --- |
| Refine is discovery/design oriented. | pass | `README.md`, `SKILL.md`, and `REFINEMENT-LOOP.md` define seed design, dispatch route validation, command-stage dispatch, and final synthesis. |
| Canonical ten-stage loop exists. | pass | `REFINEMENT-LOOP.md` defines Context Builder, Invoke Define, Interrogation, Research decision, Distill, Invoke Redefine/Design, Interrogation, Distill Repair, Invoke Plan, and Final Interrogation/Synthesis. |
| Deterministic command dispatch is required. | pass | `SKILL.md` and `REFINEMENT-LOOP.md` require `tools/arcanum --resolve` and `tools/arcanum --exec`. |
| Dispatch Spec route validation is required. | pass | `SKILL.md`, `REFINEMENT-LOOP.md`, and templates require `REFINE-DISPATCH.json` before command-backed stage execution. |
| Task Session and Sigil Development are not loop stages. | pass | Core contract keeps them as optional recommended next routes only. |
| Dispatch route replaces ad hoc orchestration. | pass | Templates and loop contract use `REFINE-DISPATCH.json`; runtime handoff references the validated dispatch route. |
| Research decision records offered/selected/deferred state. | pass | `SKILL.md` and `REFINEMENT-LOOP.md` preserve `no-research`, `bounded-research`, and `research-if-gap-appears`. |
| Experiment Harness is initialized. | pass | `EXPERIMENT-PROFILE.md` and regimes exist; generic harness validation passes. |
| Refine live-output gate distinguishes proposal from manifest-backed loop evidence. | pass | `run-validation-fixtures.sh` checks run manifest, evidence index, dispatch route, runtime handoff, canonical stage names, and command evidence. |
| Dispatch overlay fixture coverage exists. | pass | `formulae/dispatch-spec/development/run-validation-fixtures.sh` covers route-menu, dialectic, tournament, x-ray, toy-game, memory, and protected-context overlays. |
| Deterministic dispatch generation exists. | pass | `arcana/refine/scripts/generate-refine-dispatch.py` renders a seed-based `REFINE-DISPATCH.json` and validates it through dispatch-spec. |
| Dispatch strategy permission gate exists. | pass | `REFINE-DISPATCH.json` now carries `subagent_strategy`, a human approval gate, role ownership, join policy, receipt requirements, and `requires_user_permission` authorization before delegated execution. |
| Promotion evidence exists. | flag | `sigil-new-low.output.md` and the x-ray run manifest report `Status: block`; this is valid blocked evidence, not promotion evidence. |
| Observability and reflection templates exist. | pass | `templates/usage-telemetry.md` and `templates/reflection-report.md`. |
| Registry discoverability exists. | pass | `registry/SIGILS.md`, `arcana/README.md`, and `.codex/commands/refine.md` include `refine`. |

## Validation Commands

```bash
tools/arcanum --resolve refine
tools/arcanum --resolve /refine
tools/arcanum --resolve context-builder
tools/arcanum --resolve invoke
tools/arcanum --resolve interrogation
tools/arcanum --resolve distill
python3 -m json.tool formulae/dispatch-spec/dispatch.schema.yml
python3 -m json.tool arcana/refine/templates/refine-dispatch.json
python3 -m py_compile arcana/refine/scripts/generate-refine-dispatch.py
python3 arcana/refine/scripts/generate-refine-dispatch.py --seed arcana/refine/development/fixtures/refine-dispatch-seed.json --output /tmp/refine-generated-dispatch.json --validate
formulae/dispatch-spec/scripts/validate-dispatch.py /tmp/refine-generated-dispatch.json
formulae/dispatch-spec/development/run-validation-fixtures.sh
formulae/dispatch-spec/scripts/validate-dispatch.py arcana/refine/templates/refine-dispatch.json
arcana/refine/development/run-validation-fixtures.sh
rg -n "stale execution-owner wording" arcana/refine
git diff --check -- arcana/refine .codex/commands/refine.md .codex/commands/arcanum-sigil-refine.md registry/SIGILS.md arcana/README.md
```

## Promotion Status

Status: pilot.

The package is usable for blocked and proposal-level evidence. Promotion requires a non-blocked live run that validates `REFINE-DISPATCH.json`, completes the canonical loop through deterministic `tools/arcanum` command dispatch, and writes final synthesis evidence.
