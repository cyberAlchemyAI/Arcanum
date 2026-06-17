# Work Pack - Math Boundary Hardening

Status: `ready-for-task-session`
Owner: `research/triton-top2-backward-kernel`

## Objective

Turn exact 2-sparsity and dynamic-load questions into explicit tests,
definitions, and proof-roadmap decisions.

## Source Evidence

- `stages/subagents/math-relaxation-reviewer.md`
- `CAP2-CANDIDATE-SPEC.md`
- `CAP2-REFERENCE.md`
- `CAP2-W6-PARITY-REPORT.md`
- `FORMAL-MATH-SPEC.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`

## Task Board

| Task ID | Layer | Task | Status |
| --- | --- | --- | --- |
| TASK-MATH-001 | L0 | Add CAP2 exact-2-sparsity non-claim fixture. | ready |
| TASK-MATH-002 | L1 | Define dynamic-load design menu. | ready |
| TASK-MATH-003 | L2 | Add fixed-load vs dynamic-load contract tests/design split. | ready-after-002 |
| TASK-MATH-004 | L3 | Add Lean roadmap for full softmax VJP and CAP2 calculus slices. | ready-after-003 |

## SWU Manifest

| SWU ID | Parent | Goal | Write Scope | Validation |
| --- | --- | --- | --- | --- |
| SWU-MATH-001 | TASK-MATH-001 | Add tiny fixture showing CAP2 can have more than two active entries above tolerance. | tests or `CAP2-EXACT-SPARSITY-NONCLAIM.md` | pytest or fixture review |
| SWU-MATH-002 | TASK-MATH-002 | Compare `f_j(P)`, `f_j(G)`, and thresholded `f_j(A)` load definitions. | `CAP2-DYNAMIC-LOAD-DESIGN-MENU.md` | design review |
| SWU-MATH-003 | TASK-MATH-003 | Ensure fixed-load path cannot silently include dynamic-load gradients. | reference/tests or contract doc | pytest or review |
| SWU-MATH-004 | TASK-MATH-004 | State theorem roadmap and non-goals. | formal roadmap doc/paper formal notes | `lake build` not required unless proofs are edited |

## Gates

- Do not imply CAP2-v0 exact 2-sparsity.
- Do not derive dynamic-load gradients before choosing load definition.
- Lean claims must remain real-valued theorem-specific.

## Next Route

`task-session` beginning with `SWU-MATH-001`.
