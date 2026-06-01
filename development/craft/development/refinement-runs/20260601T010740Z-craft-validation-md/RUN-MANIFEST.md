# Refine Run Manifest

## Status

- Run id: `20260601T010740Z-craft-validation-md`
- Status: `block`
- Target: `development/craft/CRAFT-VALIDATION.md`
- Preset: `standard`
- Research: `no-research`
- Runtime topology: native root orchestration
	- Stage adapter: `local-skill`

## Source Request

development/craft/CRAFT-VALIDATION.md --preset standard --research no

## Stage Evidence

| Stage | Owner | Status | Verdict |
| --- | --- | --- | --- |
| Task Zero Observer Envelope | refine | `pass` | observer envelope prepared |
| Context Builder evidence baseline | context-builder | `flag` | Stage produced a runtime-native handoff stub only; owner-stage execution receipt is still required. |
| Invoke Define | invoke | `block` | Dependency blocked. Context Builder evidence baseline did not produce pass evidence. |
| Interrogation refine-review | interrogation | `block` | Dependency blocked. Invoke Define did not produce pass evidence. |
| Research decision | refine | `pass` | no-research recorded; external research not executed |
| Distill | distill | `block` | Dependency blocked. Refine review did not produce pass evidence. |
| Invoke Redefine / Design | invoke | `block` | Dependency blocked. Distill did not produce pass evidence. |
| Interrogation refine-design-review | interrogation | `block` | Dependency blocked. Invoke Design did not produce pass evidence. |
| Distill Repair | distill | `block` | Dependency blocked. Design review did not produce pass evidence. |
| Invoke Plan | invoke | `block` | Dependency blocked. Distill Repair did not produce pass evidence. |
| Final Interrogation and Synthesis | interrogation | `block` | Dependency blocked. Invoke Plan did not produce pass evidence. |

## Next Route

If status is `pass`, route the resulting plan to Task Session or the requested downstream owner. If status is `block`, inspect the first blocked stage artifact and its log under `stages/.logs/`.
