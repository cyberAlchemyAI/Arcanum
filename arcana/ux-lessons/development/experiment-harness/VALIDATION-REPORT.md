# ux-lessons — Experiment Harness Validation Report

- **Run kind:** static conformance (native sigil; no Codex executor). Each example is a hand-run with a real output body.
- **Validated against:** `../../SKILL.md` `lesson`/`ux-pattern` schemas, the `evidence` enum, the anecdote→no-hard-gate honesty rule, the no-invented-consumer-fields guard, and the compose-don't-reimplement boundary.

## Per-example results

| # | Modes | Schema conformance | Evidence enum | Honesty rule | No invented consumer fields | Verdict |
| - | ----- | ------------------ | ------------- | ------------ | --------------------------- | ------- |
| 01 | capture | pass | pass (`screenshot_diff`) | pass (anecdote → `promoted_to: null`) | n/a | **pass** |
| 02 | distill + emit-validator | pass | pass | pass (anecdote → hard_gate is a *spec proposal*, not a gate) | pass (every claim names a `feeds_field`) | **pass** |
| 03 | capture + promote + emit-studio | pass | pass | pass (within-session `repeated` → no cross_session, no hard_gate) | pass (CommentEvent/MutationTask shape; variant intake deferred) | **flag** |

## Quality-bar coverage (SKILL `<quality-bar>`)
- [x] typed lesson/pattern artifacts conform to schemas
- [x] `evidence[]` within enum in all examples
- [x] anecdote→no-hard-gate honesty rule enforced (02 and 03)
- [x] every consumer-intake entry names the exact consumer field it feeds
- [x] composes the five owners; no re-implementation of capture/store/residue
- [x] never runs validation or mutates studio sessions (02 stops at `--mode spec`; 03 emits an intent only)
- [x] patterns held at `seed`/`calibrated` per evidence (no over-promotion)

## Promotion-gate status (SKILL `<promotion-gate>`)
| Gate criterion | Status |
| -------------- | ------ |
| ≥2 sessions captured with honest signal tagging | **blocked** — only 1 real session |
| ≥1 pattern emitted to BOTH consumers, zero invented fields | **pass** (`detail-beside-the-subject` → validator; `avoid-3d-rotation…` → studio) |
| anecdote→no-hard-gate enforced ≥once | **pass** |
| cross-session promotion demonstrated | **blocked** — within-session proxy only |
| validator claim map ingested by `--mode spec` | **pending** — handoff authored, live ingestion not run |
| studio intent validated against SPEC | **pass (shape)** — not applied to a live session |

## Verdict
**Harness status: `flag`.** Initialized with three conformance-passing examples and real output bodies. Two examples `pass`, one `flag`. **Promotion remains blocked** on: (1) a real second session to prove cross-session promotion, and (2) live consumer ingestion (validator calibrate + studio apply). This is reusable-behavior evidence at the contract level; it does not yet clear the promotion gate. Claim ≤ proof preserved.
