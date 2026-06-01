# Refine Run Manifest

## Status

- Run id: `20260601T015216Z-craft-validation-md`
- Status: `block`
- Target: `development/craft/CRAFT-VALIDATION.md`
- Preset: `standard`
- Research: `no-research`
- Dispatch route: `development/craft/development/refinement-runs/20260601T015216Z-craft-validation-md/REFINE-DISPATCH.json`
- Dispatch validation: `pass`
- Runtime topology: native root orchestration
	- Stage adapter: `local-skill`

## Source Request

development/craft/CRAFT-VALIDATION.md --preset standard --research no

## Stage Evidence

| Stage | Owner | Status | Evidence Kind | Verdict |
| --- | --- | --- | --- | --- |
| Task Zero Observer Envelope | refine | `pass` | `observer_envelope` | observer envelope prepared |
| Context Builder evidence baseline | context-builder | `flag` | `handoff_prepared` | Stage produced a runtime-native handoff stub only; owner-stage execution receipt is still required. |
| Invoke Define | invoke | `block` | `blocked` | Dependency blocked. Context Builder evidence baseline did not produce pass evidence. |
| Interrogation refine-review | interrogation | `block` | `blocked` | Dependency blocked. Invoke Define did not produce pass evidence. |
| Research decision | refine | `pass` | `decision_record` | no-research recorded; external research not executed |
| Distill | distill | `block` | `blocked` | Dependency blocked. Refine review did not produce pass evidence. |
| Invoke Redefine / Design | invoke | `block` | `blocked` | Dependency blocked. Distill did not produce pass evidence. |
| Interrogation refine-design-review | interrogation | `block` | `blocked` | Dependency blocked. Invoke Design did not produce pass evidence. |
| Distill Repair | distill | `block` | `blocked` | Dependency blocked. Design review did not produce pass evidence. |
| Invoke Plan | invoke | `block` | `blocked` | Dependency blocked. Distill Repair did not produce pass evidence. |
| Final Interrogation and Synthesis | interrogation | `block` | `blocked` | Dependency blocked. Invoke Plan did not produce pass evidence. |

## Next Route

If status is `pass`, route the resulting plan to Task Session or the requested downstream owner. If status is `block`, inspect the first blocked stage artifact and its log under `stages/.logs/`.
