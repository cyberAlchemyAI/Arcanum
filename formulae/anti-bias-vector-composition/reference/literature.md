---
tags: [vault, discovery, multi-agent, bias, literature, prior-art]
node_type: discovery
is_session: false
layer: ontology
nature: reference
status: active
version: 0.1.0
last_updated: 2026-05-26
---

# Anti-Bias Vector Composition — Literature

> Annotated references for the principle stated in `principle.md`. Status field on each entry: `verified` (citation form is standard and the source is well-known enough to attest), `inferred` (the work exists and the framing is correct, but the exact title/year is reconstructed and should be checked against the original before citing in print).

---

## Philosophy lineage

**Mill, J. S. (1859). *On Liberty*. Chapter 2: "Of the Liberty of Thought and Discussion".** — *verified*.
Mill's argument that truth emerges from the collision of adverse opinions, not from any single opinion's purity, is the textual ancestor of this discovery. The relevant move: "He who knows only his own side of the case, knows little of that." Reframed for multi-agent dispatch: an agent whose angle is not confronted by a structurally opposed angle has produced output that "knows little of the case". The principle is Mill's discipline applied to ensemble composition.

**Hegel, G. W. F. *Phenomenology of Spirit* (1807) and *Science of Logic* (1812–1816).** — *verified* (works), *inferred* (specific section reference).
The dialectical pattern thesis → antithesis → synthesis is the structural template. The qualifier this discovery adds: not every dialectic produces useful synthesis. The antithesis must be *load-bearing* against the specific bias of the thesis, not merely a verbal negation. Hegel's caution against empty negation (the "abstract negation" that produces nothing new) is the precursor of the "diversity vs tension" distinction in `principle.md` §Distinction from "diversity".

---

## Cognitive science

**Kahneman, D., & Klein, G. (2009). Conditions for intuitive expertise: A failure to disagree. *American Psychologist*, 64(6), 515–526.** — *verified*.
The paper is itself an instance of adversarial collaboration: two researchers who held publicly opposed positions on expert intuition agreed to co-author a piece resolving where they actually disagreed and where they agreed. Method is the load-bearing artifact, not the conclusion. Tensioned-pairwise dispatch is the same method applied to N agents within a single session: each pair must produce a "failure to disagree" — an explicit map of which axes they share and which they oppose — not a confident consensus.

**Tetlock, P. E., & Mellers, B. A. (multiple, c. 2014–2017). Superforecaster pairing and aggregation in the Good Judgment Project.** — *inferred* (the body of work is verified; specific paper titles for the "pairing" mechanism are reconstructed).
The empirical finding from the Good Judgment Project: pairing forecasters with opposed-prior models — one who anchors high, one who anchors low; one who weights base rates heavily, one who weights recent signals heavily — produces ensembles with measurably lower Brier scores than ensembles of forecasters drawn from the same prior. The mechanism is precisely the structural-opposition cancellation invoked in `principle.md` §Why this matters.

---

## Decision science / management

**Janis, I. L. (1972, revised 1982). *Victims of Groupthink*. Houghton Mifflin.** — *verified*.
The "groupthink" diagnosis is the negative case of this discovery: agents who share macro vector *and* micro vectors converge on biased consensus precisely because no structural opposition is present in the room. Janis's prescriptions (assign a devil's advocate, invite outside experts, encourage open dissent) are early operationalizations of tensioned-pairwise composition. Treat the auditor-layer post-dispatch dissent check (in `validator-check.md`) as Janis's devil's advocate slot, formalized.

---

## Formal results

**Hong, L., & Page, S. E. (2004). Groups of diverse problem solvers can outperform groups of high-ability problem solvers. *Proceedings of the National Academy of Sciences*, 101(46), 16385–16389.** — *verified*.
The "diversity beats ability" theorem: under stated conditions, a randomly selected diverse group outperforms a group of the highest-individual-ability solvers on a function-optimization task. The mechanism is that high-ability solvers cluster in heuristic space (correlated errors), while diverse solvers cover orthogonal heuristics (cancelling errors). Caveat for this discovery: the theorem requires diversity in *heuristic*, which is the load-bearing kind — not surface diversity. Hong-Page therefore supports the principle but does *not* support reading "diversity" loosely; their diversity is exactly the tensioned-pairwise sense.

**Krogh, A., & Vedelsby, J. (1995). Neural network ensembles, cross validation, and active learning. *Advances in Neural Information Processing Systems 7*, 231–238.** — *verified*.
The error-decomposition identity: ensemble generalization error = average member error − ensemble diversity, where "diversity" is the variance of member outputs around the ensemble mean. The identity makes the principle quantitative: the ensemble cancels member bias *exactly* to the extent that members disagree on the relevant axis. A layer of N agents whose outputs are highly correlated has near-zero diversity term and therefore inherits member bias undiminished. This is the formal foundation of `principle.md` §Why this matters.

**Dietterich, T. G. (2000). Ensemble methods in machine learning. *Multiple Classifier Systems*, LNCS 1857, 1–15.** — *verified*.
Survey of bagging, boosting, and error-correcting output codes. The boosting case is particularly relevant: AdaBoost actively *constructs* tension between weak learners by reweighting examples to force each learner to err on examples the previous one got right. This is the in-training analog of the dispatch-time tensioning enforced by `validator-check.md`.

---

## AI safety

**Irving, G., Christiano, P., & Amodei, D. (2018). AI safety via debate. *arXiv:1805.00899*.** — *verified*.
The proposal: have two AI agents argue opposing sides of a question in front of a human judge. The safety mechanism is precisely the tensioned-pairwise principle: a single AI's bias is hard to detect, but two AIs forced into structural opposition are forced to expose each other's weaknesses to win the debate. The `theorem-research` skeptic layer is a multi-agent generalization (N ≥ 3) of the same idea: each skeptic runs a different *attack vector*, not just a different attack instance.

**Christiano, P., et al. (various, 2018–2022). Eliciting Latent Knowledge / debate variants.** — *inferred* (the line of work is verified; specific paper citation reconstructed).
Subsequent work refining the debate proposal addresses the failure mode where two debaters collude on a shared bias. The fix proposed in that literature — vary the *priors* and *capability profiles* of the debaters — is the same fix this discovery applies one level up: vary the *angles* of the agents within a layer.

---

## Cross-cutting note on citation discipline

This discovery does not require any of the above to be the *first* statement of tensioned-pairwise composition. The framework's contribution is operationalizing the principle as a mechanical validator check on a dispatch spec (see `validator-check.md`), not claiming originality. The literature is cited so a reader can verify the principle is well-grounded, not so the discovery can claim novelty. Per the project's standing rule (memory entry `feedback_cite_dont_rediscover.md`): name prior art in the first section, not as a footnote.

---

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [principle.md](./principle.md) | `derives-from` | The principle this literature grounds. Every claim in `principle.md` §Why this matters traces to either Krogh-Vedelsby (ensemble decomposition) or Hong-Page (heuristic diversity). |
| [validator-check.md](./validator-check.md) | `cites` | The validator's red-flag rules cite Irving-Christiano-Amodei (single-bias collusion) and Janis (groupthink) as the failure modes being detected. |
