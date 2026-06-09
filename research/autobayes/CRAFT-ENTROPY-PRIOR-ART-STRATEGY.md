---
profile: autobayes-research
name: Craft Entropy / SCU — Prior-Art & Novelty Audit Strategy
description: Adversarial prior-art search that tests whether the Craft translation-entropy / SCU-U-curve / measurement design is a novel synthesis or a restatement of existing work.
type: prior-art-strategy
status: draft
parent_run: arcanum/research/autobayes/development/refinement-runs/refine-scu-entropy-experiment-20260608
dispatch: arcanum/research/autobayes/craft-entropy-priorart.dispatch.json
last_updated: 2026-06-08
---

# Craft Entropy / SCU — Prior-Art & Novelty Audit

## Why this exists

The refine run produced a sharp, attractive claim bundle. Attractive claims are exactly
the ones that are most often **already in the literature under a different name**. Before
any experiment is funded, this audit asks one adversarial question:

> Is any of this novel, or are we restating bias-variance, MDL, the information
> bottleneck, semantic entropy, lost-in-the-middle, and task-decomposition research with
> Craft vocabulary?

The audit's **default stance is prosecutorial**: assume restatement until a specific,
citable gap is shown. A "novel" verdict requires naming what is *not* in the cited art.

## Claims under audit

| ID | Claim from the refine run | Most likely prior art |
| --- | --- | --- |
| C1 | Uncertainty/error is U-shaped in unit complexity with an interior minimum (the SCU). | Bias-variance trade-off (Geman 1992); double descent (Belkin 2019). |
| C2 | The SCU is a description-length minimizer (model bits + residual bits). | MDL / two-part codes (Rissanen 1978); model selection by MDL. |
| C3 | A spread-vs-fidelity tradeoff governs unit sizing. | Information bottleneck (Tishby, Pereira, Bialek 1999); rate-distortion. |
| C4 | `H_spread` = semantic-cluster entropy of an LLM's conditional, measured by sampling. | Semantic uncertainty (Kuhn, Gal, Farquhar 2023); self-consistency (Wang 2022). |
| C5 | There is an optimal task/unit decomposition granularity for LLM work. | Decomposed prompting (Khot 2022); least-to-most (Zhou 2022); agent task decomposition. |
| C6 | Translation fidelity decays as the unit grows (attentional decay, `A_att`). | Lost-in-the-middle (Liu 2023); long-context degradation studies. |
| C7 | schema→data→residue is functorial Bayesian inversion with composed local losses. | AutoBayes / GVI / statistical games (tower); Spivak functorial data migration. |
| C8 | Optimal work-unit size empirically minimizes defects/residue. | SE literature: method/change size vs defect density; review-effectiveness vs diff size. |

## Search lanes

Each lane is one bounded web+local search unit. Each returns: the closest prior work
(with citation/URL), and a verdict mark — `restatement`, `partial-overlap`, or
`novel-synthesis` — plus, for any non-restatement, the specific gap the prior art leaves.

1. **L1 bias-variance / double descent** — C1.
2. **L2 MDL / rate-distortion / information bottleneck** — C2, C3.
3. **L3 semantic entropy / LLM uncertainty** — C4.
4. **L4 LLM task-decomposition granularity & long-context decay** — C5, C6.
5. **L5 functorial / categorical Bayesian inversion** — C7.
6. **L6 empirical unit-size vs defect/residue (software & agents)** — C8.

## Convergence

A two-role dialectic — **restatement-prosecutor** vs **novelty-defender** — converges on a
per-claim verdict and one overall honest statement of the form:

> Components C1–C8 are [mostly] prior art. The only candidate-novel element, if any, is
> the *specific synthesis*: [name it precisely], which the cited art does not already do
> because [specific gap]. If no such gap survives, the honest verdict is **restatement**.

## Boundaries

- This audit may write only under `research/autobayes`. It does not edit the Craft definition.
- External sources are flagged protected context; web findings are candidate, not canonical.
- The full-mode web fanout uses delegated subagents and requires operator approval.

## Artifacts

- [craft-entropy-priorart.dispatch.json](craft-entropy-priorart.dispatch.json) — validated audit route.
- `sessions/craft-entropy-priorart-receipts.md` — per-lane prior-art receipts (on run).
- `tracks/craft-entropy-novelty-verdict.md` — converged novelty verdict card (on run).
- `residue/craft-entropy-priorart-residue.md` — open residue (on run).
