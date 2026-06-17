# Paid CUDA Runner Fallback

Status: planned-fallback
Date: 2026-06-12

## Question

Does this challenge need guaranteed GPU resources, or will a free Google/Kaggle
runner suffice?

## Answer

For the next PoC and correctness checks, free hosted GPUs should suffice.

For final performance claims, zero-allocation claims, and repeatable benchmark
evidence, a paid on-demand GPU is safer because free notebook resources are not
guaranteed and may change during the run.

## Guarantee Levels

| Level | Runner | Use For | Good Enough? |
| --- | --- | --- | --- |
| L0 | Local CPU `.venv` | PyTorch reference, gradcheck, baseline math | yes |
| L1 | Free Kaggle or Google Colab GPU | CUDA/Triton probe, first kernel correctness smoke | yes |
| L2 | Paid on-demand GPU pod | final Triton parity, FP16 tolerance, memory checks, benchmark report | recommended |
| L3 | Dedicated cloud VM | only needed for long/repeated benchmarking | unnecessary for this challenge unless L2 is unstable |

## Current Pricing Snapshot

Checked on 2026-06-12.

| Provider | Current signal | Practical reading |
| --- | --- | --- |
| Google Colab Pay As You Go | Official Colab pricing lists `$9.99` for `100 Compute Units`. | Good low-friction fallback, but GPU type/availability is still dynamic. |
| RunPod | Official pricing lists options including RTX A5000 at `$0.27/hr`, L4 at `$0.39/hr`, RTX 3090 at `$0.46/hr`, RTX 4090 at `$0.69/hr`. | Best balance for repeatable paid validation without a monthly commitment. |
| Vast.ai | Marketplace prices can be cheaper, including low-cost consumer GPUs. | Cheapest pure price, but reliability and image quality vary by host. Good if budget is the only constraint. |
| Lambda Cloud | Official pricing skews toward larger reserved clusters in current public listing. | Not the cheapest fit for this small validation task. |

## Recommended Paid Fallback

Use RunPod with the cheapest currently available CUDA GPU that supports PyTorch
and Triton, preferring:

1. RTX A5000 if available around `$0.27/hr`.
2. L4 if A5000 is unavailable.
3. RTX 3090 if L4/A5000 images are unavailable or slow.

Why:

- no monthly subscription is required for a pod-style validation run;
- per-hour cost is low enough for a short test window;
- 24 GB VRAM class GPUs are more than enough for this kernel challenge;
- more repeatable than free notebook allocation.

## Maximum Budget Recommendation

For this challenge, start with a strict cap:

```text
2 hours maximum, stop/delete immediately after validation.
```

At the listed RunPod prices, that means roughly:

- RTX A5000: about `$0.54` for 2 hours;
- L4: about `$0.78` for 2 hours;
- RTX 3090: about `$0.92` for 2 hours.

Storage, network, or provider minimum-balance rules may add overhead, so treat
these as compute-only estimates.

## Decision

Use free Google/Kaggle first for `TASK-W0-008`. If free GPU availability blocks
or flakes twice, switch to the paid fallback task:

```text
TASK-W0-009: Provision paid on-demand CUDA runner.
```
