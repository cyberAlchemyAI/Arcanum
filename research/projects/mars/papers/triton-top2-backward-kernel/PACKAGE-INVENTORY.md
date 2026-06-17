# Package Inventory - Triton Top2 Backward Kernel Paper

Status: `draft-audited`
Date: 2026-06-15

## Purpose

Define what belongs in a shareable paper package and what must stay out until
reviewed.

## Package Roots

| Root | Role | Include By Default |
| --- | --- | --- |
| `research/projects/mars/papers/triton-top2-backward-kernel/` | Paper, appendices, formal package, claim guards | yes |
| `research/triton-top2-backward-kernel/` | Research tower, implementation, tests, run evidence | yes, filtered |
| `research/projects/mars/development/` | Planning and task-session receipts for paper/formal work | selected receipts only |

## Include - Paper Package

- `paper.md`
- `PAPER-SPEC.md`
- `PAPER-STORIES.md`
- `PAPER-TEST-SPEC.md`
- `PAPER-REVIEW.md`
- `CLAIM-GUARDS.md`
- `EVIDENCE-MANIFEST.md`
- `REFERENCE-LEDGER.md`
- `MATH-APPENDIX.md`
- `DATA-APPENDIX.md`
- `PRESENTATION-PACKAGE.md`
- `formal/`

## Include - Tower Evidence

Include the tower files listed in:

- `research/triton-top2-backward-kernel/ARTIFACT-AUDIT.md`

The tower provides executable references, Triton kernels, tests, benchmark
scripts, RunPod receipts, and challenge-specific research reports.

## Include - Selected MARS Development Evidence

Include only receipts that support this paper package:

- `research/projects/mars/development/invoke-runs/20260614T075231Z-triton-paper-package-plan/`
- `research/projects/mars/development/invoke-runs/20260614T083000Z-triton-appendix-proof-plan/`
- `research/projects/mars/development/invoke-runs/20260614T102500Z-lean-softmax-cap2-proof-plan/`
- `research/projects/mars/development/invoke-runs/20260614T142000Z-softmax-coordinate-derivative-proof-plan/`
- paper/formal task-session receipts that mention `triton`, `softmax`, or
  `cap2` in their run folder names.

## Exclude

- local Python environments and caches;
- Lean build artifacts if present;
- runner bundle tarballs unless explicitly approved;
- generated Arcanum skill/runtime surfaces;
- unrelated project folders;
- parent worktree modifications outside approved package roots;
- hostnames, credentials, tokens, or provider-specific private details.

## Publication Tiers

| Tier | Contents | Intended Use |
| --- | --- | --- |
| `internal-full` | Paper package, tower, selected development receipts, raw benchmark JSON | internal review and reproducibility |
| `reviewer-clean` | Paper package plus curated code/tests/reports and sanitized benchmark evidence | external technical reviewer |
| `public-minimal` | Paper, appendices, references, selected code snippets or repo link | public-facing share |

## Required Pre-Share Checks

1. Re-run or verify `lake build` status for the formal package.
2. Verify CPU tests and RunPod/Triton evidence paths still exist.
3. Reconcile `EVIDENCE-MANIFEST.md` path warnings from `ARTIFACT-AUDIT.md`.
4. Review `development/runner-bundles/` and notebook outputs before including.
5. Run a pathspec status check:

```sh
git status --short -- \
  research/projects/mars/papers/triton-top2-backward-kernel \
  research/triton-top2-backward-kernel
```

6. Confirm no unrelated dirty project or generated runtime surface is staged.
