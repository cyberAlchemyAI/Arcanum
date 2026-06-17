# Refine Result - Review Hardening

Status: `pass-with-flags`
Run ID: `20260615T025930Z-review-hardening-refine`

## Summary

The approved review-hardening route ran with six subagents. All six subagents
completed, wrote receipts, were joined, and were closed. No kernel, paper,
glossary, work-pack, or canonical evidence artifact was mutated by this run.

The result is not "everything is finished." The result is sharper:

```text
The implementation package is review-ready under guarded claims.
The novelty, math-extension, systems-strength, paper-polish, and packaging
gaps are now task-ready.
```

## Subagent Closeout

| Role | Receipt | Status | Main Residue |
| --- | --- | --- | --- |
| `novelty-prior-art-reviewer` | `stages/subagents/novelty-prior-art-reviewer.md` | flag | CAP2 novelty not established. |
| `math-relaxation-reviewer` | `stages/subagents/math-relaxation-reviewer.md` | flag | Exact 2-sparsity and dynamic-load gradients remain future work. |
| `systems-validation-reviewer` | `stages/subagents/systems-validation-reviewer.md` | flag | CAP2 needs dedicated zero-allocation, FP16, and larger benchmark checks. |
| `baseline-coverage-reviewer` | `stages/subagents/baseline-coverage-reviewer.md` | flag | Entmax and full convex top-k router backward remain baseline gaps. |
| `paper-evidence-reviewer` | `stages/subagents/paper-evidence-reviewer.md` | flag | Paper needs claim guards, reproducibility, theorem mapping, and appendix polish. |
| `artifact-inventory-reviewer` | `stages/subagents/artifact-inventory-reviewer.md` | pass-with-packaging-warnings | Dirty worktree needs include/exclude manifest before sharing. |

## Final Synthesis

### Supported Now

- Fixed-mask Triton backward and W7 evidence are strong enough for guarded
  implementation claims.
- CAP2 fixed-load backward parity is supported for the named smooth graph.
- The paper can present CAP2 as a validated candidate relaxation.
- The package can say Lean validates real-valued theorem slices, not GPU/FP16
  behavior.

### Must Remain Non-Claims

- CAP2 novelty.
- Exact backward through hard Top2.
- Exact 2-sparsity for CAP2-v0.
- Dynamic-load gradients.
- CAP2 W7-level zero-allocation acceptance.
- Production-scale benchmark or tuning claims.
- Formal proof of FP16, Triton, CUDA memory behavior, or zero allocation.

### Task-Ready Gaps

1. Novelty/baseline hardening:
   - CAP2 novelty comparison matrix.
   - Entmax baseline or explicit deferral.
   - Convex sparse top-k full-router backward status.
   - CAP2 kill/promote checklist.

2. Math-boundary hardening:
   - CAP2 exact-2-sparsity non-claim fixture.
   - Dynamic-load definition menu.
   - Fixed-load vs dynamic-load contract tests.
   - Optional Lean theorem roadmap for full softmax VJP and CAP2 slices.

3. Systems hardening:
   - CAP2 CUDA memory-stat zero-allocation acceptance test.
   - CAP2 FP16 parity/tolerance test.
   - Larger benchmark sweep with environment capture.

4. Paper hardening:
   - Rewrite stale formal non-claim wording.
   - Add reproducibility command table.
   - Add theorem-to-claim table.
   - Add FP16 and CAP2 zero-allocation boundary paragraphs.
   - Add "proves / does not prove" boxes to appendices.

5. Artifact inventory:
   - Add package include/exclude manifest.
   - Add artifact audit.
   - Validate evidence manifest paths.
   - Avoid broad parent-level staging.

## Recommended Next Routes

1. `task-session`: artifact inventory first, because the parent worktree is dirty
   and the tower/paper roots are untracked.
2. `invoke`: paper-hardening work-pack, so claim guard edits happen as a bounded
   plan instead of ad hoc patching.
3. `invoke`: systems-hardening work-pack for CAP2 zero-allocation, FP16, and
   benchmark sweep.
4. `invoke`: novelty/baseline hardening work-pack for entmax and prior-art matrix.
5. `invoke`: math-boundary hardening work-pack for exact-sparsity and
   dynamic-load decisions.

## Verdict

`pass-with-flags`: the route executed, subagents were closed, and the remaining
work is now explicit. The flags are not blockers to guarded review; they are
blockers to stronger novelty, exact-sparsity, dynamic-load, CAP2 systems, and
publication-grade claims.
