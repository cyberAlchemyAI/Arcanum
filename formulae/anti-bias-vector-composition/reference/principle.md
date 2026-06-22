---
tags: [vault, discovery, multi-agent, bias, anti-bias, vector-composition, subagents-strategy]
node_type: discovery
is_session: false
layer: ontology
nature: explanatory
status: active
version: 0.2.0
last_updated: 2026-06-15
---

# Anti-Bias Vector Composition — Principle

> One of four files in this discovery: `principle.md` (this file) states the rule, `literature.md` records the prior art, `validator-check.md` operationalizes the rule as **Principle 5 (pairwise tension)** of the subagents-strategy constitution (v0.5.2), `examples.md` shows worked good/bad group shapes.

---

## Statement of the principle

When N agents share a macro goal — the same target question, the same artifact under investigation, the same hypothesis to test — their **micro vectors** (the per-agent angle, methodology, prior, source corpus) must be deliberately *tensioned* against each other, not merely *non-overlapping*.

The macro vector is the shared destination: "find prior art for X", "stress-test claim Y", "evaluate option Z against alternatives". The micro vectors are the lines of approach each agent runs. The principle says: pick the micro vectors so that, treated as vectors in a notional methodology-space, they point in structurally opposed directions whose component-wise bias terms cancel under composition.

Concretely: if four agents are dispatched to find prior art on a claim, do not give them four keyword searches that differ only in vocabulary. Give them four *axes* of approach (e.g., arXiv-categorical, physics-journals, dissent corpus, backward-citation tree) such that any bias internal to one axis is structurally absent from at least one of the others.

---

## Distinction from "diversity"

Diversity is necessary but insufficient. Two agents can hold diverse identities, diverse vocabularies, even diverse training distributions and still share the same blind spot — because the blind spot lives in the *direction of approach*, not in the surface presentation of the agent.

Diversity says: spread the agents apart on some axis. Tension says: spread them apart on an axis *that is load-bearing for the bias you are trying to cancel*. Random spread does not compose to cancellation; structural opposition does.

The cleanest test: ask, for each pair of agents `(a_i, a_j)`, *what bias internal to a_i would not survive a confrontation with a_j's output?* If the answer is "none, they would just produce two compatible findings", the pair is diverse but not tensioned. If the answer names a specific failure mode (a_i over-trusts modern papers, a_j is forced to read historical lineage; a_i takes the claim at face value, a_j attacks its definitions), the pair is tensioned.

---

## Why this matters

Ensemble averaging is a tool with two regimes. Average N estimators whose errors are independent and zero-mean: variance drops, bias is preserved. Average N estimators whose errors are *correlated*: variance drops less than expected and bias is reproduced at full strength.

Multi-agent dispatches sit in the second regime by default. Agents trained on the same corpus, prompted by the same operator, working on the same artifact, with no structural opposition between their angles, will produce correlated errors. The synthesizer that consumes their outputs sees a confident consensus and reports a biased finding with falsely high confidence.

The fix is not to add more agents (that does not break the correlation) and not to add more diversity in surface presentation (that does not break the correlation either). The fix is to choose angles such that the correlated bias term is *forced into the open* by at least one pair of agents disagreeing along the axis that carries the bias.

This is the operational form of Mill's "collision of adverse opinions" (see `literature.md` §Philosophy lineage) and of the error-decomposition identity in Krogh & Vedelsby (1995) where ensemble error decomposes as `accuracy − diversity` and the diversity term is exactly the structural opposition between members.

---

## Where this applies in a subagents-strategy dispatch

A dispatch (v0.5.2) is organized into **groups**, each with a group `role ∈ {investigate, evaluate, synthesize, meta-evaluate}` and agents with `role ∈ {explorer, skeptic, writer, auditor}`. The principle applies *group-locally*: it constrains the choice of `angle`s for the agents within a single **subject group** (`n ≥ 2`, role `investigate` or `evaluate`), not the relationship between groups. (The cross-group theme is `anti_bias_global`; the per-group axis is `anti_bias`.)

**Applies:**
- **`investigate` group (explorers).** N parallel agents gathering prior art / context. Angles must be tensioned along source corpus, methodology, or temporal prior. Bad: four LLM-paraphrase searches over arXiv with different keywords. Good: arXiv-categorical + physics-journals + dissent-corpus + backward-citation-tree.
- **`evaluate` group (skeptics).** N parallel agents attacking a claim. Angles must be tensioned along attack vector. Bad: three "find problems with the argument" agents. Good: precedent-attack (has this been done?) + vacuity-attack (does the claim reduce to a triviality?) + definitional-attack (do the terms hold under stress?).

> An `evaluator` role (N agents scoring an artifact against weighted criteria) was considered but **retired 2026-06-11**: it is not in the four-role set. Criteria-scoring, when needed, is a `skeptic` with a stated gate. Out of the subject-group set in [validator-check.md](./validator-check.md).

**Does not apply:**
- **`synthesize` group (writer).** Single agent by construction; nothing to tension against.
- **`meta-evaluate` group (auditor).** Single check, run after the other groups; the auditor's role is to enforce this principle, not to be subject to it.

The principle is *additional* to the existing `domainspec-subagents-strategy` partition check ("angles non-overlapping AND covering"). Non-overlapping-and-covering is a partition condition on the angle set; tensioned-pairwise is a *direction* condition on the partition. A group can pass the partition check and fail the tension check; the gate runs both.

---

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [literature.md](./literature.md) | `derives-from` | Prior art for the principle: Mill on collision of opinions, Kahneman-Klein adversarial collaboration, Hong-Page diversity theorem, Krogh-Vedelsby ensemble decomposition, Irving-Christiano-Amodei AI safety via debate. |
| [validator-check.md](./validator-check.md) | `operationalized-by` | The checklist that enforces this principle (constitution Principle 5) on the dispatch sheet at the confirm gate. |
| [examples.md](./examples.md) | `instances` | Worked good/bad layer shapes for explorer, skeptic, plus the false-consensus anti-pattern. |
| `multi-agent-implementation-strategy` (consuming repo) | `cites` | The investigation-vs-implementation framing this discovery extends: tensioned-pairwise applies to investigation-shaped fan-out (where N agents read one artifact from N stances). |
| `robot-talks` (consuming repo) | `cites` | Robot-talks already enforces declared-perspective-per-turn (D-2) and tension-not-aggregation (D-3); this discovery generalizes the same discipline to non-discussion dispatch shapes where perspectives are angles, not turns. |
