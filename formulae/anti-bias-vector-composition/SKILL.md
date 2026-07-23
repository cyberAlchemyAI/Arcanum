---
name: anti-bias-vector-composition
description: The design principle behind Principle 5 (pairwise tension) of the subagents-strategy constitution. Use when designing the angle set for an n≥2 subject group (role investigate or evaluate) so the agents' micro-vectors are structurally opposed and their correlated bias cancels under composition — not merely non-overlapping. This is the design/theory layer; check-tension is the executable gate that enforces it before the human confirm.
---

# anti-bias-vector-composition — designing tensioned groups

> Arcanum library copy (public). Definition owner of the anti-bias principle, referenced by
> `formulae/dispatch-spec` (`anti_bias_composition` technique, rules R26–R29). The consuming
> repo also runs an executable gate, `check-tension`, that enforces this principle's Tests 1–4
> before the human confirm; `check-tension` is not part of this formulae package.

This skill is the **design layer**: it states *why* and *how* to pick the angles of a
multi-agent group so bias cancels. The **executable gate** that checks a sheet against this
principle is `check-tension` (two independent agents, Tests 1–4, before the human confirm) when
the consuming repo provides it. Author here; verify there.

## The principle (one sentence)

When N agents share a macro goal, their **micro vectors** (per-agent angle, methodology,
prior, source corpus) must be deliberately *tensioned* into structurally opposed directions —
so any bias internal to one is forced into the open by at least one other — not merely made
*non-overlapping*. Diversity of surface presentation is necessary but **insufficient**: agents
on the same corpus, same operator, same artifact produce **correlated errors**, and the
synthesizer reports a biased finding with falsely high confidence. More agents do not break the
correlation; structural opposition does.

**The clean test.** For each pair `(a_i, a_j)`: *what bias internal to a_i would not survive a
confrontation with a_j's output?* If the answer is "none — they'd just produce two compatible
findings", the pair is diverse but **not tensioned**. If it names a specific failure mode, it is.

## Where it applies

Group-locally, to a **subject group**: `n ≥ 2`, group role `investigate` (explorers) or
`evaluate` (skeptics). It constrains the per-group `anti_bias` axis and each agent's `angle`.
It does **not** apply to `synthesize` (single writer) or `meta-evaluate` (single auditor).

- **investigate / explorers** — tension along source-corpus, methodology, or temporal-prior.
  Bad: four arXiv keyword searches differing only in vocabulary. Good: arXiv-categorical +
  physics-journals + dissent-corpus + backward-citation-tree.
- **evaluate / skeptics** — tension along attack-vector. Bad: three "find problems" agents.
  Good: precedent-attack + vacuity-attack + definitional-attack.

## The four canonical axes (closed vocabulary for per-group `anti_bias`)

- **Methodology** — empirical / formal / adversarial / historical / computational
- **Source-corpus** — arXiv-categorical / journals / dissent-literature / canon / citation-tree
- **Attack-vector** (skeptics) — precedent / vacuity / definitional / scope / counter-example
- **Temporal-prior** — modern-only / historical-lineage / mixed-with-decade-bins

A composite is allowed only if **explicitly declared**. `anti_bias_global` (dispatch-wide
theme, present when ≥2 groups have `n≥2`) is free-text and never vocabulary-checked.

## Tensioned-pairwise is stronger than the partition check

The `subagent-strategy` chain already checks the angle set is **non-overlapping**
(no two agents cover the same concern) AND **covering** (together they span the goal). Those are
*partition* conditions — which subset each angle covers. Tensioned-pairwise is a *direction*
condition: a group can pass partition and fail tension (four explorers cleanly partitioning the
goal, all using one arXiv-keyword methodology). The gate runs **both**.
