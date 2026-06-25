# Task Session Context - SWU-WHISPER-READABILITY-001

- Task: `SWU-WHISPER-READABILITY-001`
- Mode: lean
- Strict coverage: pass
- Handoff pack: none
- Runtime: local
- Session evidence: this file

## Obligation Matrix

| Obligation | Coverage | Evidence |
| --- | --- | --- |
| Execute exactly one SWU. | covered | `WORK-PACK.md` selects `SWU-WHISPER-READABILITY-001` as the only ready L0 unit. |
| Keep mutation non-breaking. | covered | `DESIGN.md` says `readability_dynamics` is optional and old substrates must behave unchanged. |
| Keep renderer and canonical spell promotion out of scope. | covered | `SPELLCRAFT-RESULT.md` rejects immediate README and renderer mutation. |
| Implement validator-only readability checks. | covered | `WORK-PACK.md` names `validate-whisper-draft.py` and one substrate fixture as the write scope. |
| Validate old draft behavior and dense readability flags. | covered | `WORK-PACK.md` requires old draft validation plus a dense fixture producing readability flags. |

## Included Context

| Source | Selectors | Why Included |
| --- | --- | --- |
| `WORK-PACK.md` | Control fields; SWU execution handoff; implementation detail; expected receipt | Authoritative task contract, write scope, and validation surface. |
| `SPELLCRAFT-RESULT.md` | Lifecycle decision; accepted execution boundary; promotion boundary | Owner gate for mutating a reusable library spell. |
| `DESIGN.md` | Proposed schema shape; validator design; decision flow | Field names and intended `PASS`/`FLAG`/`BLOCK` behavior. |
| `../20260531T164421Z-readability-dynamics/RUNTIME-HANDOFF.md` | Handoff objective; next executable route | Prior refinement selecting validator-only L0 before renderer work. |
| `../20260526T204134Z-language-ai-substack/text-intent-substrate.yaml` | Existing old-style substrate | Regression source for compatibility validation. |
| `../../tools/validate-whisper-draft.py` | `prose_paragraphs`; `validate`; CLI output | Implementation target and existing validator behavior. |

## Execution Assumptions

- No blocker-level human decision remains; Spellcraft accepted L0 execution.
- `FLAG whisper draft validation` should exit successfully when only readability findings exist, because readability warnings are advisory until tuned.
- Invalid `readability_dynamics` schema type is a hard configuration error.
- New session/report artifacts in this refinement-run folder are execution evidence and do not expand the implementation write scope.

## Excluded Candidates

| Candidate | Reason Excluded |
| --- | --- |
| `build-whisper-review-html.py` | Renderer support is deferred to `SWU-WHISPER-READABILITY-002`. |
| `arcanum/spells/whisper/README.md` | Canonical spell promotion remains blocked until experiment evidence. |
| Public/review HTML artifacts | Browser review validation is deferred to `SWU-WHISPER-READABILITY-003`. |
