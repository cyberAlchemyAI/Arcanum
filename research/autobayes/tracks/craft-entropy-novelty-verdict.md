---
profile: autobayes-research
name: Craft Entropy / SCU — Novelty Verdict Card
description: Converged adversarial verdict on whether the Craft entropy / SCU claim bundle is novel or restatement.
type: novelty-verdict
status: candidate
dispatch: arcanum/research/autobayes/craft-entropy-priorart.dispatch.json
dispatch_id: craft-entropy-priorart-20260608
last_updated: 2026-06-08
---

# Novelty Verdict Card (candidate)

> **Candidate reading.** Output of the prior-art audit. Does not edit the Craft
> definition or promote canonical vocabulary. External sources are protected context.

## Overall verdict (updated after second pass)

**Full restatement.** The first pass left one narrow surviving gap (a falsification
protocol) and two exposed ones (the unit-size axis, the two-arm decomposition). The
**second pass collapsed all three.** The honest answer to "are we just restating?" is
**yes.** The bundle's only residual value is *applying* known machinery to the agentic-LLM
craft-unit domain — and even that application is now substantially anticipated.

> First-pass verdict (superseded): "restatement with one narrow surviving gap." Retained
> below for the audit trail; corrected by the [second-pass section](#second-pass-collapse).

> Plain statement: "SCU is the local minimum of (composite) entropy" is **bias-variance /
> rate-distortion / MDL restated** on a translation-unit axis. The semantic-entropy proxy
> **is** Kuhn/Farquhar. The functorial schema→data→residue framing **is** Spivak +
> St Clere Smithe. We should claim none of these as ours.

## Per-claim verdicts

| Claim | Verdict | Killing citation |
| --- | --- | --- |
| C1 U-curve / interior minimum | restatement (form) | Geman 1992; Wu et al. 2025 (LLM CoT-length U already exists) |
| C2 SCU = bits(schema)+bits(residue) | **restatement** | Rissanen 1978 (two-part code, verbatim) |
| C3 spread-vs-fidelity tradeoff | **restatement** | Tishby et al. 1999 (information bottleneck) |
| C4 semantic-entropy proxy | **restatement** | Kuhn/Gal/Farquhar 2023; Farquhar 2024 (Nature) |
| C5 decomposition interior optimum | restatement (phenomenon) | Dense X Retrieval (interior optimum already shown) |
| C6 attentional / per-unit fidelity decay | partial-overlap | Liu 2023 covers *positional*, not *per-unit* decay |
| C7 functorial Bayesian inversion | **restatement, no gap** | Spivak 2012; Cho–Jacobs; St Clere Smithe |
| C8 empirical unit-size optimum | partial-overlap | SmartBear/Cisco (diff-size) — but module-size contested (El Emam/Koru) |

## The compositional core is also restatement

"Compose a descending spread arm + an ascending overload arm into a U with a measurable
minimum" is the **bias-variance decomposition** (bias↓+variance↑) and the **rate-distortion
decomposition** (rate vs distortion) restated. Decomposing a loss into a monotone-down term
and a monotone-up term and locating the crossing is the canonical move in both fields. The
U is *derived*, not discovered.

## What narrowly survives (state only this, narrowly)

Ranked by defensibility:

1. **(Strongest) The measurement/falsification protocol** — `r*` **codebook-invariance**
   (the MDL minimizer *location* must be invariant across reference models/serializations)
   **+ blind-rubric co-location** as the test that the U is not an encoding artifact.
   Standard MDL reports a code length; it does not routinely demand minimizer-location
   invariance across codebooks as a built-in artifact-falsifier. Affirmatively uncovered by
   the search. **This, not the U-curve, is the only thing worth claiming — and only as a
   protocol, not a discovery.**
2. **(Medium, exposed) The translation-unit-size axis** as the control variable with model
   and task fixed. Closest threat: Wu 2025 (CoT length) and RAG granularity — adjacent axes,
   not this one. Falsified by any paper plotting fixed-model fixed-task loss/entropy vs
   semantic-unit size with a named interior optimum.
3. **(Weak) Two independent semantic instruments** (semantic entropy for spread, residual
   energy for fit) that compose into the U, neither individually U-shaped. Exposed to the
   information-bottleneck rate/distortion pair; defensible only at the narrowest framing.
4. **(Weakest, hold in reserve) A unit-agnostic interior-minimum law** spanning module +
   diff + LLM-subtask. One pillar (module size) is actively contested; one (agent decomp) is
   thin. Do not lead with this.

## Second-pass collapse

Three targeted searches, each built to *kill* a surviving claim, succeeded:

### #1 protocol (`r*` codebook-invariance + blind co-location) → **restatement**

Each component is a named established method; the bundle is ordinary triangulation.

- **NML / universal codes** (Rissanen 1996, *Fisher Information and Stochastic Complexity*;
  Myung, Navarro & Pitt 2006) make MDL selection **codebook-invariant by construction** — the
  reparameterization-invariant minimax-optimal code. "Test `r*` invariance across codebooks"
  is, in proper MDL, "use a code-independent code." The protocol patches naive two-part
  codes with a property NML already gives for free.
- **Stability selection** (Meinshausen & Bühlmann 2010, JRSS-B) makes "the selected optimum
  must be invariant across perturbations" the standard selection-validity criterion.
- **Multiverse / specification-curve analysis** (Steegen et al. 2016; Simonsohn et al. 2020)
  is the named method for "an effect/optimum is real only if invariant across analytic choices."
- **Convergent validity** (Campbell & Fiske 1959) is co-location with a blind criterion.

Only the *packaging* of these three for a U-curve minimizer is unnamed — composition
novelty, not conceptual novelty. **Revised mark: restatement.**

### #2 translation-unit-size axis → **restatement**

Wu et al. 2025 (arXiv:2502.07266) is **axis-agnostic by its own statement**: per-step error
`A(N)=α[(1−T/C)(1−T/(NM))]^N` depends only on model `M` and subtask difficulty `T/N`, with
**no** CoT/token-specific term. Its interior optimum (easier-units vs multiplicative
error-accumulation, optimal `N* = T·Z/[M(Z+1)]`) is exactly "split a fixed-difficulty unit
into N sub-units." "Translation-unit size" is a relabel of their `N`. Echoed by divide-and-
conquer noise decomposition (arXiv:2506.16411), multi-agent subtask-count optima, and METR
task-horizon work. **Revised mark: restatement.**

### #3 module-size pillar of C8 → **drop**

The module-size interior optimum is **likely a spurious-ratio artifact**: El Emam/Koru
(EMSE 2008; TSE 2009) show defect-density-vs-size induces correlation with size's own
reciprocal; modeling raw counts gives a *monotonic* power law (smaller modules
proportionally more defect-prone), no interior minimum. Hatton's large-size upturn was
thinly replicated and self-flagged as speculative. **Drop module-size**; restrict C8 to
diff-size (SmartBear/Cisco) + LLM-subtask — a narrower 2-domain claim, and the ~200–400 LOC
numerical coincidence is now suspect, not corroboration.

## Honesty boundary

- We are **not** entitled to claim the U-curve, the entropy metric, the MDL framing, the
  rate-distortion tradeoff, or the functorial framing. Each is prior art.
- The only stake-worthy contribution is the **falsification protocol** (#1), and even the
  axis (#2) is exposed. Positioning must be "operationalization + protocol," never "new law."
- This verdict is candidate; promotion to any positioning/publication claim needs owner
  review. See [residue](../residue/craft-entropy-priorart-residue.md).
