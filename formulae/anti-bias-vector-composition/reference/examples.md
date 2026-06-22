---
tags: [vault, discovery, multi-agent, examples, theorem-research]
node_type: discovery
is_session: false
layer: application
nature: instances
status: active
version: 0.1.0
last_updated: 2026-05-26
---

# Anti-Bias Vector Composition — Examples

> Worked good/bad layer shapes for the `theorem-research` skill. Each example shows a candidate spec, classifies it under the validator rules in `validator-check.md`, and names the failure mode (or absence thereof). Use as a template library when authoring a new dispatch spec.

---

## Example 1 — Explorer layer (N = 4)

**Macro goal:** Find prior art for the claim "ensemble error decomposes as accuracy minus diversity" in the context of multi-agent LLM dispatch.

### Bad — fails R1 (same noun phrase) and R3 (same source corpus)

```yaml
layer: explorer
agents:
  - id: e1
    angle: "search literature on ensemble error decomposition (keywords: ensemble, error, decomposition)"
  - id: e2
    angle: "search literature on ensemble error decomposition (keywords: bagging, boosting, variance)"
  - id: e3
    angle: "search literature on ensemble error decomposition (keywords: diversity, accuracy, members)"
  - id: e4
    angle: "search literature on ensemble error decomposition (keywords: voting, averaging, classifiers)"
```

**Why it fails.** Four keyword searches against the same corpus (web/arXiv generic). All four agents will surface ML papers from the 2000s on bagging/boosting; none will surface the philosophy-of-science lineage (Mill), the cognitive-science adversarial-collaboration lineage (Kahneman-Klein), or the AI-safety debate lineage (Irving-Christiano-Amodei). The bias — "this is a machine-learning problem with a machine-learning answer" — is uncancelled.

### Good — passes G1 (pairwise tension) and G2 (≥ 2 axes)

```yaml
layer: explorer
agents:
  - id: e1
    angle: "search arXiv stat.ML / cs.LG (modern formal lineage)"
    axes: {methodology: formal, source_corpus: arxiv-categorical, temporal_prior: modern}
  - id: e2
    angle: "search physics journals + Phys Rev (older statistical-mechanics lineage of ensemble averaging)"
    axes: {methodology: formal, source_corpus: physics-journals, temporal_prior: historical}
  - id: e3
    angle: "search dissent / critical AI corpus (Cognition blog, lesswrong, Christiano on debate failures)"
    axes: {methodology: adversarial, source_corpus: dissent-corpus, temporal_prior: modern}
  - id: e4
    angle: "backward-citation tree from Krogh-Vedelsby 1995 and Hong-Page 2004"
    axes: {methodology: empirical, source_corpus: citation-tree, temporal_prior: mixed}
```

**Why it passes.** Six pairs, each tensioned along a nameable axis: (e1,e2) modern vs historical; (e1,e3) formal vs adversarial; (e1,e4) primary vs derivative search; (e2,e3) physics vs critical AI; (e2,e4) historical vs derivative; (e3,e4) dissent vs canon. Two tension axes (methodology, source-corpus, temporal-prior) appear across the layer, satisfying G2 with margin.

---

## Example 2 — Skeptic layer (N = 3)

**Macro goal:** Stress-test the claim "the residue functor is the canonical entropy carrier in the framework".

### Bad — fails R4 (same attack vector)

```yaml
layer: skeptic
agents:
  - id: s1
    angle: "find problems with the residue-as-entropy argument"
  - id: s2
    angle: "argue against the residue-as-entropy claim"
  - id: s3
    angle: "identify weaknesses in residue-as-entropy"
```

**Why it fails.** All three agents will produce the same shape of critique — "the argument is X, here are objections to X". They will likely converge on the most visible objection (probably definitional ambiguity of "entropy" in the framework's sense) and miss the precedent objection (has someone already done this in stat-mech literature?) and the vacuity objection (does the claim reduce to "entropy is what we labeled entropy"?).

### Good — passes G1 with three distinct attack vectors

```yaml
layer: skeptic
agents:
  - id: s1
    angle: "precedent-attack: find existing constructions in stat-mech / categorical thermodynamics that already do this; if found, the framework's claim is at best a restatement"
    axes: {attack_vector: precedent-attack, source_corpus: physics-journals}
  - id: s2
    angle: "vacuity-attack: assume the framework's definitions; show whether the claim reduces to a definitional tautology or genuinely constrains the residue functor"
    axes: {attack_vector: vacuity-attack, methodology: formal}
  - id: s3
    angle: "definitional-attack: stress-test the term 'entropy' in the framework; produce two natural alternative formal definitions of entropy and show whether the residue functor remains canonical under each"
    axes: {attack_vector: definitional-attack, methodology: formal}
```

**Why it passes.** Three pairs, each tensioned along the attack-vector axis. (s1,s2) external-precedent vs internal-vacuity; (s1,s3) external-precedent vs internal-definitional; (s2,s3) vacuity vs definitional (vacuity assumes definitions fixed; definitional varies them). Two axes (attack-vector, source-corpus) present.

---

## Example 3 — Mixed layer with dissent surfacing

**Scenario.** A three-skeptic layer is dispatched on the claim "the C₀-semigroup PR is genuinely missing from Mathlib". Pre-dispatch, all three angles are tensioned (precedent-attack, vacuity-attack, scope-attack). Initial returns:

- s1 (precedent-attack): "I searched Mathlib and found no exact match. Claim looks safe."
- s2 (vacuity-attack): "The claim is non-trivial — the definition is load-bearing for QM applications."
- s3 (scope-attack): "Scope is appropriate for a first PR; not too narrow, not too broad."

All three reach the same bottom-line ("the PR is good"). The post-dispatch validator (Item 10) flags this as a candidate false consensus and prompts each skeptic with a layer-specific tension prompt: "What is the strongest argument the *other two* skeptics could raise against your finding?"

After the tension prompt:

- s1 revises: "On re-search with looser keywords, I find a 2023 PR draft on the Mathlib Zulip that proposed a partial version of this; it stalled. Worth citing in the PR body."
- s2 holds.
- s3 revises: "The scope is borderline narrow — if the PR is rejected, the obvious fallback is to bundle it with the Hille-Yosida statement, which would double the PR size."

The hidden disagreement (s1 found a near-collision, s3 had a scope concern) surfaces only after the layer-specific tension prompt is run. This is the principle working as designed: tensioned-pairwise dispatch *plus* the dissent-surfacing post-check together produce the disagreement that flat consensus would have hidden.

---

## Example 4 — Anti-pattern: false consensus

**Scenario.** Five-agent skeptic layer dispatched on "is this PR description ready to ship?" (each skeptic on a distinct gate). All five return "yes, ship it". No dissent records. No pair-level differentiation noted.

**Correct response.** This is **not** a success. Five agents converging with zero dissent against a stated tensioned-pairwise spec means one of three things:

1. The pre-dispatch tensioning was nominal but not load-bearing — the angles were declared distinct but the agents implemented them similarly.
2. The artifact is genuinely uncontroversial along all five tension axes.
3. The agents are correlated through shared prompt / shared training distribution and the tensioning never engaged.

The validator cannot distinguish (1)/(2)/(3) from output alone. Default action: treat as **failure to apply the principle** and either (a) re-dispatch the skeptic layer with one agent explicitly instructed to argue the opposite conclusion (debate-style fallback, per Irving-Christiano-Amodei), or (b) accept the consensus but record in the audit trail that the layer did not produce dissent, so future readers can weight the finding appropriately.

The wrong response is to take the unanimous "yes, ship it" as five times more evidence than a single agent's "yes". Correlated unanimity is *not* multiplicative evidence. Treating it as such is the failure mode the principle exists to prevent.

---

## How to use these examples

When authoring a new `theorem-research` spec, find the example whose layer shape matches yours (explorer / skeptic / mixed) and use its "good" angles as a template. Replace the angle values with the ones appropriate to your macro goal, keep the axis classification, and run the spec past `validator-check.md`.

When reviewing a returned dispatch and noticing unanimous findings, consult Example 4 before treating the unanimity as confirmation.

---

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [principle.md](./principle.md) | `derives-from` | The principle these examples instantiate. |
| [validator-check.md](./validator-check.md) | `derives-from` | The validator rules each example is classified under. |
| [literature.md](./literature.md) | `cites` | Example 4's debate-style fallback cites Irving-Christiano-Amodei (AI safety via debate); the correlated-unanimity warning cites Janis (groupthink). |
