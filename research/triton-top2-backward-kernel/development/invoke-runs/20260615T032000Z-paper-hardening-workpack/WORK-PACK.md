# Work Pack - Triton Paper Hardening

Status: `ready-for-task-session`
Owner: `research/triton-top2-backward-kernel/paper`

## Objective

Harden the paper package so a reviewer can trace each claim to evidence,
reproduce core checks, and see exactly what is not claimed.

## Source Evidence

- `research/triton-top2-backward-kernel/development/refinement-runs/20260615T025930Z-review-hardening-refine/stages/subagents/paper-evidence-reviewer.md`
- `research/triton-top2-backward-kernel/FINAL-PRIOR-ART-NOVELTY-REPORT.md`
- `research/triton-top2-backward-kernel/paper/CLAIM-GUARDS.md`
- `research/triton-top2-backward-kernel/paper/EVIDENCE-MANIFEST.md`
- `research/triton-top2-backward-kernel/paper/PAPER-TEST-SPEC.md`

## Task Board

| Task ID | Layer | Task | Status |
| --- | --- | --- | --- |
| TASK-PAPER-001 | L0 | Refresh stale formal non-claims in `CLAIM-GUARDS.md`. | ready |
| TASK-PAPER-002 | L1 | Add reproducibility command table to paper/test appendix. | ready |
| TASK-PAPER-003 | L1 | Add theorem-to-claim table. | ready |
| TASK-PAPER-004 | L2 | Add FP16 and CAP2 zero-allocation boundary paragraphs. | ready |
| TASK-PAPER-005 | L2 | Add appendix "proves / does not prove" boxes. | ready |
| TASK-PAPER-006 | L3 | Validate evidence manifest paths and update package review notes. | ready |

## SWU Manifest

| SWU ID | Parent | Goal | Write Scope | Validation |
| --- | --- | --- | --- | --- |
| SWU-PAPER-001 | TASK-PAPER-001 | Rewrite `NC-008`/`NC-009` to match current Lean evidence. | `CLAIM-GUARDS.md` | review diff against `FORMAL-VALIDATION-REPORT.md` |
| SWU-PAPER-002 | TASK-PAPER-002 | Add CPU, Triton, RunPod, benchmark, JSON, and Lean commands. | `PAPER-TEST-SPEC.md`, `paper.md` or appendix | commands are syntactically copyable |
| SWU-PAPER-003 | TASK-PAPER-003 | Map theorem names to supported and unsupported claims. | `paper.md`, `MATH-APPENDIX.md`, or new table file | every theorem row has evidence ID |
| SWU-PAPER-004 | TASK-PAPER-004 | Add FP16/CAP2 zero-allocation boundary text. | `paper.md`, `CLAIM-GUARDS.md`, `DATA-APPENDIX.md` | non-claims remain explicit |
| SWU-PAPER-005 | TASK-PAPER-005 | Add appendix scope boxes. | `MATH-APPENDIX.md`, `DATA-APPENDIX.md` | each box includes "does not prove" |
| SWU-PAPER-006 | TASK-PAPER-006 | Check manifest paths and update review note. | `EVIDENCE-MANIFEST.md`, `PAPER-REVIEW.md` | path check output recorded |

## Gates

- Do not introduce CAP2 novelty.
- Do not claim FP16 formal proof.
- Do not claim CAP2 W7 zero-allocation until systems work-pack passes.

## Next Route

`task-session` one SWU at a time.
