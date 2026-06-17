# TOWER.md - Structure & File Roles

**Lane:** triton-top2-backward-kernel
**Subject:** Zero-allocation Triton backward kernel for a top-2 relaxed MoE/router objective.

## Tower Layers

| Layer | File | Role |
| --- | --- | --- |
| L0 - Corpus | `L0-corpus.md` | Source records for Triton, PyTorch autograd/custom ops, MoE top-2 routing, and load-balancing losses. |
| L1 - Glossary | `glossary.md` | Plain-language terms for the problem. |
| L1 - Governed defs | `definitions.md` | Canonical definitions used inside the tower. |
| L2 - Claims | `claim-ledger.md` | Source-backed claims, local inferences, risks, and ambiguity labels. |
| L3 - Derivation | `derivation.md` | Mathematical interpretation and likely backward equations. |
| L3 - Formal spec | `FORMAL-MATH-SPEC.md` | Lean-suitable proof obligations for the fixed-mask real-number graph. |
| L3 - Rigor map | `RIGOR-VALIDATION-MAP.md` | Separates proof, test, numerical, and systems validation. |
| L3 - Relaxation candidates | `RELAXATION-CANDIDATES.md` | Candidate continuous Top2 relaxations, source records, and decision matrix. |
| L3 - Prior art | `PRIOR-ART-MAP.md` | Known solution families and novelty warnings. |
| L3 - Novelty search | `NOVELTY-SEARCH-MAP.md` | Hypothesis space for trying a novel solution without overclaiming. |
| L3 - Implementation | `implementation-notes.md` | Triton/PyTorch kernel strategy, zero-allocation constraints, and validation plan. |
| L4 - Pack | `LEARNING-PACK.md` | Short synthesis for dispatching a full research or implementation pass. |
| Brief | `SAFE-EXPLANATION-BRIEF.md` | Safe explanation language and no-overclaiming boundaries. |
| Residue | `open-residue.md` | Decisions and missing facts that block honest implementation. |
| Decisions | `OPEN-QUESTIONS-DECISION-LEDGER.md` | Interrogation decisions splitting V0 baseline, CAP2 design, and hard blockers. |
| Final assumptions | `FINAL-QUESTION-RESOLUTION.md` | Resolved execution assumptions for the full work pack. |
| CAP2 candidate | `CAP2-CANDIDATE-SPEC.md` | Capacity-aware pairwise relaxed Top-2 hypothesis, with claims and non-claims. |
| CAP2 reference | `CAP2-REFERENCE.md` | Implemented CAP2-v0 standard-library/PyTorch reference and fixed-load gradcheck summary. |
| CAP2 comparison | `CAP2-PRIOR-ART-COMPARISON.md` | CAP2-v0 comparison against local prior-art baselines before kill/promote/defer decision. |
| Work pack | `WORK-PACK.md` | End-to-end task matrix, wave gates, SWU manifest, and validation criteria. |
| Tooling plan | `TOOLING-PLAN.md` | Dependency and runtime plan for CPU reference, formal checks, and GPU Triton validation. |
| CUDA runner plan | `CUDA-RUNNER-PLAN.md` | Runner acquisition and validation contract for CUDA/Triton work. |
| Free CUDA runner kit | `FREE-CUDA-RUNNER-KIT.md` | Kaggle/Colab/SageMaker free runner path, bootstrap script, and probe notebook. |
| Google Colab PoC | `GOOGLE-COLAB-POC.md` | Google-specific free/low-friction CUDA PoC path. |
| Paid fallback | `PAID-CUDA-RUNNER-FALLBACK.md` | Cheapest sensible paid fallback and guarantee boundary. |
| Convex top-k blocker | `CONVEX-SPARSE-TOPK-BLOCKED.md` | Blocked report for implementation-ready convex sparse top-k baseline details. |
| Convex top-k research pack | `CONVEX-SPARSE-TOPK-RESEARCH-PACK.md` | Source-backed extraction decision for official sparse soft top-k PAV mask path. |
| Convex top-k dispatch | `convex-sparse-topk-extraction-20260612.dispatch.json` | Governed route for extracting the convex sparse top-k operator. |
| Convex top-k extraction | `CONVEX-SPARSE-TOPK-EXTRACTION.md` and `CONVEX-SPARSE-TOPK-FIXTURES.md` | Extracted PAV p=4/3 sparse top-k mask contract, selected router compositions, fixtures, and boundary policy. |
| Convex top-k JVP blocker | `CONVEX-SPARSE-TOPK-JVP-BLOCKED.md` | Blocked report for source-backed PyTorch/custom-JVP parity through the PAV mask. |
| Convex top-k JVP feasibility | `CONVEX-SPARSE-TOPK-JVP-FEASIBILITY.md` | Source-backed feasibility report for a narrow PyTorch custom-autograd PAV mask parity oracle. |
| Convex top-k JVP parity | `CONVEX-SPARSE-TOPK-JVP-PARITY.md` | Narrow PyTorch custom-autograd parity report for the p=4/3 PAV sparse top-k mask. |
| Dispatch | `top2-backward-research.dispatch.json` | Route-shaped research plan validated by Dispatch Spec. |
| Execution | `development/dispatch-runs/20260612T121416Z-top2-backward-research/` | Artifact-backed execution receipts and closeout for the research dispatch. |
| Invoke | `development/invoke-runs/20260612T123402Z-baselines-tdd-math-validation/` | Define/design/plan/handoff for baselines, TDD, math validation, and CAP2 design gate. |
| Invoke full work pack | `development/invoke-runs/20260612T124255Z-full-workpack/` | Define/design/plan/handoff for executing all remaining waves to final report. |
| Invoke tooling plan | `development/invoke-runs/20260612T131715Z-tooling-plan/` | Plan for adding dependencies and runtime gates after W0 blocker evidence. |
| Invoke refresh | `development/invoke-runs/20260612T133737Z-refresh-cuda-runner-task/` | Refresh adding CUDA runner acquisition and validation tasks. |
| Refine refresh | `development/refinement-runs/20260612T140546Z-cuda-runner-refresh/` | Refined free-first, paid-fallback CUDA runner strategy. |
| Dispatch extraction | `development/dispatch-runs/20260612T-convex-topk-extraction-research/` | Validated dispatch for convex sparse top-k extraction research. |
| Interrogation closeout | `development/interrogation-runs/20260612T124255Z-resolve-to-workpack/` | Final open-question resolution and CAP2 candidate framing. |
| Reference harness | `reference/router_reference.py`, `reference/router_torch.py`, `tests/test_router_reference.py`, and `tests/test_router_torch.py` | Standard-library V0 fixed-mask oracle, PyTorch autograd mirror, raw-vs-normalized selected-pair comparison, soft-routing/sparsemax/ReLU baselines, and finite-difference validation. |
| Task Session | `development/task-sessions/20260612T-task-reference-tdd/` | Execution evidence for the first reference/TDD/math-validation scaffold. |
| Task Session | `development/task-sessions/20260612T-w0-environment-gate/` | Environment gate evidence for PyTorch, pytest, Triton, and GPU availability. |
| Task Session | `development/task-sessions/20260612T1318Z-w0-004-tooling-manifests/` | Dependency manifests and environment test evidence. |
| Task Session | `development/task-sessions/20260612T1320Z-w0-005-cpu-env/` | CPU PyTorch/pytest environment provisioning evidence. |
| Task Session | `development/task-sessions/20260612T1322Z-w0-006-gpu-triton-gate/` | GPU/Triton blocker evidence for local machine. |
| Task Session | `development/task-sessions/20260612T135008Z-w0-007-cuda-runner-selection/` | CUDA runner selection blocker and decision gate. |
| Task Session | `development/task-sessions/20260612T140949Z-w1-001-pytorch-v0-parity/` | PyTorch V0 fixed-mask reference and autograd parity evidence. |
| Task Session | `development/task-sessions/20260612T-w2-003c-jvp-blocked/` | Convex sparse top-k differentiable parity blocked report evidence. |
| Task Session | `development/task-sessions/20260612T-w2-003d-rg-feasibility/` | Convex sparse top-k PAV JVP/backward feasibility gate evidence. |
| Task Session | `development/task-sessions/20260612T-w2-003d-pav-jvp-parity/` | Convex sparse top-k PAV mask-level PyTorch custom-autograd parity evidence. |
| Task Session | `development/task-sessions/20260612T-w3-001-cap2-reference/` | CAP2-v0 standard-library/PyTorch reference and fixed-load gradcheck evidence. |
| Task Session | `development/task-sessions/20260612T-w3-002-cap2-comparison/` | CAP2-v0 prior-art comparison evidence and decision blocker handoff. |

## Source-Kind Labels

- **primary-source** - official documentation or original paper.
- **related-source** - reputable derivative or ecosystem source.
- **local-inference** - reasoned from sources and the prompt; not directly stated by a source.
- **operator-reading** - practical reading for the engineer who will implement.
- **open-residue** - unresolved ambiguity or missing evidence.

## Build Provenance

Sources were checked on 2026-06-12. The tower cites public documentation and papers
only; no private implementation code was inspected for this topic.
