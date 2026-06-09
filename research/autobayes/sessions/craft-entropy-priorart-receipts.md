---
profile: autobayes-research
name: Craft Entropy / SCU — Prior-Art Lane Receipts
description: Per-lane prior-art receipts (web search) for the Craft entropy / SCU novelty audit.
type: prior-art-receipts
status: complete
dispatch: arcanum/research/autobayes/craft-entropy-priorart.dispatch.json
dispatch_id: craft-entropy-priorart-20260608
run_date: 2026-06-08
---

# Prior-Art Lane Receipts

Six role-bound lanes searched external literature (web) under a prosecutorial default.
External sources are protected context: cited, not promoted.

## Mark summary

| Lane | Claims | Closest prior work | Mark |
| --- | --- | --- | --- |
| L1 | C1 U-curve | Geman 1992; Belkin 2019; Wu et al. 2025 (CoT length U) | partial-overlap |
| L2 | C2, C3 | Rissanen 1978 (MDL two-part code); Tishby et al. 1999 (information bottleneck) | restatement |
| L3 | C4 | Kuhn/Gal/Farquhar 2023; Farquhar et al. 2024 (Nature) | restatement |
| L4 | C5, C6 | Dense X Retrieval; Khot 2022; Zhou 2022; Liu 2023 (lost in the middle) | partial-overlap |
| L5 | C7 | Spivak 2012; Cho–Jacobs 2019; Braithwaite–Hedges–Smithe; St Clere Smithe | restatement |
| L6 | C8 | SmartBear/Cisco review study; Hatton 1997; El Emam/Koru 2008/2009 | partial-overlap |

## L1 — bias-variance / double descent (partial-overlap)

- Closest: Geman, Bienenstock & Doursat 1992, *Neural Networks and the Bias/Variance Dilemma*, Neural Computation 4(1) — https://direct.mit.edu/neco/article/4/1/1/5624 ; Belkin et al. 2019, *Reconciling modern ML practice and the classical bias-variance trade-off*, PNAS — https://arxiv.org/abs/1812.11118 ; Wu et al. 2025, *When More is Less: Understanding Chain-of-Thought Length in LLMs*, arXiv:2502.07266.
- Establishes the U-shape *form* with interior minimum, but on the **model-capacity** axis (fixed task); Belkin undercuts "interior minimum = optimal." **Wu 2025 already shows an interior-optimum inverted-U on an LLM granularity axis (CoT length)**, without invoking bias-variance.
- Surviving gap: the U-curve on the **translation-unit-size** axis (fixed model) + SCU formalization — narrow; the neighboring CoT-length U already exists.

## L2 — MDL / rate-distortion / information bottleneck (restatement)

- Closest: Rissanen 1978 *Modeling by shortest data description* (two-part code); Grünwald MDL tutorial — https://arxiv.org/pdf/math/0406077 ; Tishby, Pereira & Bialek 1999 *The Information Bottleneck Method* — https://www.princeton.edu/~wbialek/our_papers/tishby+al_99.pdf
- C2 ("bits(schema)+bits(residue) minimizer") **is** Rissanen's two-part code `L(M)+L(D|M)`; C3 (spread-vs-fidelity) is the rate-distortion / IB tradeoff. Minimizer and tradeoff are forced by MDL/RD with no new math.
- Surviving gap: only the application surface (LLM unit sizing). Too narrow to carry theoretical novelty.

## L3 — semantic entropy / LLM uncertainty (restatement)

- Closest: Kuhn, Gal & Farquhar 2023 *Semantic Uncertainty*, ICLR — https://arxiv.org/abs/2302.09664 ; Farquhar, Kossen, Kuhn & Gal 2024 *Detecting hallucinations… using semantic entropy*, Nature 630 — https://www.nature.com/articles/s41586-024-07421-0
- The metric (sample N → bidirectional-entailment clusters → discrete entropy) **is** theirs, validated even on machine translation. Proxy A is a literal restatement.
- Surviving gap: using it as a curve over unit-size — absence-of-evidence, not a methodological gap.

## L4 — task decomposition / long-context decay (partial-overlap)

- Closest: Chen et al. 2023 *Dense X Retrieval* — https://arxiv.org/abs/2312.06648 ; Khot et al. 2022 *Decomposed Prompting* — https://arxiv.org/abs/2210.02406 ; Zhou et al. 2022 *Least-to-Most* — https://arxiv.org/abs/2205.10625 ; Liu et al. 2023 *Lost in the Middle* — https://arxiv.org/abs/2307.03172
- Decomposition-helps and long-context-decay are established. **RAG retrieval-granularity already shows an interior optimum (~100–200 words) with both failure modes.** Task-decomposition literature defaults to "decompose more" and names optimal granularity OPEN.
- Surviving gap: a quantified interior optimum for **task/work-unit** (not retrieval-chunk) granularity, and **per-unit** fidelity decay distinct from **positional** lost-in-the-middle. Real but thinly evidenced.

## L5 — functorial / categorical Bayesian inversion (restatement, no gap)

- Closest: Spivak 2012 *Functorial Data Migration* — https://arxiv.org/abs/1009.1166 ; Cho & Jacobs 2019 *Disintegration and Bayesian Inversion* — https://arxiv.org/abs/1709.00322 ; Braithwaite–Hedges–St Clere Smithe 2023 — https://arxiv.org/abs/2305.06112 ; St Clere Smithe 2023 — https://arxiv.org/abs/2306.17009
- schema→data (Spivak), data→residue (Cho–Jacobs/BHS), local-losses-compose / residue = free-energy laxness gap (St Clere Smithe). The autobayes tower already imports this. **No surviving gap.**

## L6 — empirical unit-size vs defect/residue (partial-overlap)

- Closest: SmartBear/Cisco code-review study (2,500 reviews) — https://static0.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf ; Hatton 1997 *U-bend* — https://www.leshatton.org/Documents/Ubend_IS697.pdf ; Koru & El Emam 2008/2009 *Theory of Relative Defect Proneness* — https://link.springer.com/article/10.1007/s10664-008-9080-x
- The **diff/review-size interior optimum (~200–400 LOC)** is strongly established. **Module-size U is contested**: El Emam/Koru call it a measurement artifact, claim monotonic relative defect proneness. Agent-decomposition optimum (arXiv:2511.01149, ~4–5 modules) thinly evidenced.
- Surviving gap: a **unit-agnostic** interior-minimum law spanning module + diff + LLM-subtask as one phenomenon. Real but one pillar is contested.

## Missing-source residue

- Full text of Wu et al. 2025 (2502.07266) theoretical model not parsed — cannot fully rule out that its proof already generalizes beyond CoT length. Recorded as residue.
