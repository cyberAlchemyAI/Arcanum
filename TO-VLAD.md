---
to: Vlad
from: Victor (multi-agent audit, synthesized)
re: cyberAlchemyAI/Arcanum — what to consider sharpening
date: 2026-05-20
status: draft for discussion
---

# To Vlad — Arcanum, where I'd push

This came out of a conversation that started somewhere else. I was working on the spine — the residue/iso-loss/reflection-tower thread — and the question came up whether Arcanum is operationally what the spine is mathematically. The short answer is yes, closely enough that the spine's vocabulary makes some real things visible in Arcanum that the engineering-only reading would miss. I had four agents do a deep slice-audit (method, sigils, observability, architecture), two more challenge the findings, and a third revise everything against the challenges. What survives is below.

I've been careful to cut anything that didn't survive devil's-advocate. The framework lens motivates *why* I noticed certain gaps, but every finding here stands on its own engineering merit. Where I retain the framework framing, it's because it predicts something the engineering-only reading would not.

---

## The three findings I think are load-bearing

### 1. Residue has no type at any layer

The framework's central unit of work — what an artifact *cannot* carry across its boundary — has no first-class representation anywhere in the repo. Three independent witnesses:

- **Method**: `CYBERALCHEMY-METHOD.md:82-83, 211` records "unresolved tensions" as work items to clear, never as durable artifacts to preserve.
- **Template**: `framework/templates/sigil-template.md` has no `<residue>`, no `<source-schema>`, no degradation block. `<inputs>` are labeled "if available." A sigil can ship without ever declaring what it needs.
- **Telemetry**: `observer.output_contract_drift` is a single bit. `workflow_gaps[].category` accepts free strings.

This is the load-bearing one because every downstream feature the framework wants — loss-based reflection, schema-join checks, cross-tier aggregation, the "governed library" claim — requires residue to be a typed object. Without it, the framework can't reason about itself or its own outputs.

Note this is also the cheapest credibility test the framework can pass. A doc that names "residue" and ships a template without a residue field is asking the reader to grant authority the artifact hasn't earned.

### 2. Phase joins are the leak site

When a spell composes sigil A → sigil B, nothing checks that B's input requirements are satisfied by A's output contract. The handoff is free-text-as-evidence.

- `spellcraft validate` checks structural completeness (every phase has input, output, gate, failure-policy) but not contract-join.
- `spell-run-report.md` has no "residue carried into next phase" slot.
- Telemetry records that a `recommendation` fired but not the gap that forced it.
- There is no machine-readable dependency graph across sigils.

This is the highest-leverage *engineering* finding. Catching schema-join mismatches at `spellcraft validate` time is a small change with an immediate effect on every spell, and it's the only chokepoint that already runs. Edit (2) below makes this enforceable.

### 3. The tower is documentary, not measured

The `tier` field (formulae / transmutations / arcana) is recorded per invocation, but no telemetry answers the obvious question: *does climbing tier reduce workflow_gaps per intent?*

- Reflection thresholds are activity-based (`meaningful_executions ≥ 5`), not loss-based.
- No cross-tier aggregation in `reflection-state.json`.
- The README treats tier as epistemic classification, not as a measured stack.

This is the lever that converts the framework from descriptive to operational. Once (1) lands and residue is typed, wiring reflection to fire on residue accumulation is a small change with structural payoff: the tower starts validating its own architecture from the data.

---

## A subtler finding worth keeping

### `arcana/` conflates three categorically different things

Right now `arcana/` holds:

- **Domain-orchestrators** (`scope-interview`, `task-session`) — operate on the user's work.
- **Meta-orchestrators** (`sigil-development`, `spellcraft`) — operate on the framework itself.
- **Registry-orchestrators** (`definitions-governance`, `signal-observer`) — operate on the registry.

Three epistemic targets, one folder, same template. The framework has an "epistemic nature" axis but no "epistemic target" axis. This is part of why (1) is unenforceable — sigils-about-sigils inherit a template designed for domain work.

**I am *not* recommending the obvious fix** (a new `meta/` tier). That's a re-shelving move that doesn't solve the deprecation-authority gap, and an earlier draft of this memo had it before B1 cut it. The fix is either the lifecycle-authority matrix (edit 4) or an explicit paragraph in the Method explaining why three things sit in one tier on purpose.

---

## What I'm leaving open for you

Three calls only you should make.

### Is the Quality Bar's iso framing deliberate or accidental?

Right now the Quality Bar has no slot for "successful-with-residue." Every output is either compliant or not. But the Validation Protocol has a richer alphabet (Pass / Flag / Block), and `flag` is exactly the shape of "the artifact landed but carried residue."

A1 read this as oversight (the two vocabularies should unify). A3 read this as deliberate (the harness explicitly disclaims deep semantic correctness). One of these is right. If deliberate, say so in the doc and stop using residue-vocabulary to describe what the framework validates. If accidental, unify the verdict alphabets.

### Where does deprecation authority live?

Right now nobody owns retirement. Authoring, validation, observation, reflection all have owning sigils. Deprecation, archiving, re-tiering, replacement — no owner. Combined with `tools/install_arcanum.sh` installing from `main` (unpinned, unsigned), the "governed library" claim is currently aspirational. What's the retirement contract for a sigil that a consuming repo already pulled?

### Is `arcana/` one tier or three?

See the subtler finding above. Either co-location is intentional (then the Method owes a paragraph explaining why), or the "epistemic target" axis needs to be added.

---

## Concrete edits, ordered by leverage

I'd do these in this order. Each item: file → change → effect. I've cut three I almost included; see "what I deliberately did not recommend" below.

1. **`framework/templates/sigil-template.md`** — add `<source-schema>` with `required:` and `degrades-on:` sub-fields. *Effect:* makes the schema-join check possible; closes the `<inputs> "if available"` leak.

2. **`arcana/spellcraft/SKILL.md` (validate mode)** — check that phase N's `<output-contract>` covers phase N+1's `<source-schema>.required`; emit `BLOCK` on mismatch. *Effect:* turns the leak-site finding from observation into enforcement at the only chokepoint that already runs.

3. **`framework/observability/config.json`** — type `workflow_gaps[].category` as enum; replace `output_contract_drift: boolean` with `output_contract_drift_detail: {field, expected_shape, actual_shape}[]`. *Effect:* materializes typed residue at the telemetry layer without touching any sigil.

4. **`framework/LIFECYCLE-AUTHORITY.md`** (new) — matrix mapping {author, validate, observe, reflect, deprecate, retire, re-tier, re-name} to owning sigil. *Effect:* closes the deprecation-authority gap without re-shelving anything.

5. **`framework/observability/config.json`** — add `residue_accumulated_by_sigil` to reflection-state; let reflection fire on residue threshold in addition to execution count. *Effect:* turns the tower from documentary to measured. Depends on edits 1 and 3.

6. **`registry/SIGILS.md`** — add `version:`, `status: {active | deprecated | experimental | archived}`, `replaced-by:` columns (empty rows are fine for now). *Effect:* schema-first pinning surface; required for any deprecation contract.

7. **Repo root** — glossary pinning the overloaded vocabulary: "capability" (3 meanings across docs), "harness" (4), "lifecycle" (3). Reference from README. *Effect:* removes a recurring source of cross-doc drift.

8. **`BUSINESS-ONTOLOGY.md`** — move to `arcana/ontology-vault/CONCEPTS.md`. *Effect:* fixes a named instance-leak (sigil-scoped content at framework-scope path); demonstrates the framework can perform self-correction.

9. **`CYBERALCHEMY-METHOD.md:22`** — split the Tension anchor into `Tension (engineering)` and `Tension (residue)`. *Effect:* small, makes the stratified vocabulary usable in the body prose.

---

## What I deliberately did not recommend

For honesty about what was considered and cut:

- **`<residue>` block on every sigil** — triggers a residue-about-residue spiral. If we want it, scope it to Arcana tier only, never universal.
- **Cross-sigil baseline replay** — combinatorial blowup; replays cost real model calls; premature without (1).
- **A `degenerate` verdict** — depended on the cross-sigil replay; compound speculation.
- **A new `meta/` tier** — re-shelving move that doesn't solve the actual authority gap. The diagnosis stands; the rename was the wrong fix.
- **Heavy Lawvere/categorical framing in the memo body** — the framework lens was useful for *noticing* gaps but every finding here is defensible in plain engineering terms. The framework discussion belongs in a separate doc we're already drafting (the tower companion to lost-in-translation.md).

---

## One observation that's beyond the audit

The single thing the framework lens predicts that the engineering lens does not: **Arcanum is currently a worked instance of the framework, but it's not yet measured against it.** The tower exists structurally (three tiers, reflection state, observability). The information-theoretic claim that climbing the tower reduces conditional entropy of intent-given-vocabulary is currently untestable against the live `sigil-invocations.jsonl` because intent isn't fingerprinted and residue isn't typed. Edits 1, 3, 5 together would close that gap. At that point Arcanum stops being an instance of the framework by analogy and starts being one by measurement.

That's the bridge worth building if we want the two repos to talk to each other in something stronger than vocabulary.

---

## Three sharpest questions, in order

1. **Is the Quality Bar's iso framing deliberate or oversight?** (Determines whether edit 1 + 3 are extensions or corrections.)
2. **Where does deprecation authority live, and what is the retirement contract for a consumer pinned to `main`?** (Determines whether "governed library" is a near-term goal or a long-term one.)
3. **Is `arcana/` one tier or three?** (Determines whether (1)'s template needs to be tier-aware or whether `arcana/` splits.)

— V.
