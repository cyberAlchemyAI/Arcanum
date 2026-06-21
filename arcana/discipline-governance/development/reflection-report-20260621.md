# Sigil Reflection Report

Manual reflection on `discipline-governance` after the curation run completed the 3-regime experiment harness.

## Reflection Context

- Sigil: discipline-governance
- Tier: arcana
- Reflection trigger: manual (operator asked to finish promotion; complex regime also emitted `reflect-now`)
- Signals reviewed: 3 meaningful executions — [.arcanum/observability/by-sigil/discipline-governance.jsonl](../../../.arcanum/observability/by-sigil/discipline-governance.jsonl)
- Period or usage window: 2026-06-15 → 2026-06-21
- Observer pass: local fallback

## Signal Summary

| Signal Type | Count | Notes |
| ----------- | ----- | ----- |
| Meaningful executions | 3 | gitignore (low), receipt-id-legend (medium), scan+curation (complex) |
| Generated outputs | 16 | cards, catalog rows, constitutions, private layer, harness/curation records |
| Quality Bar failures | 0 | all runs passed the catalog validator + boundary checks |
| Anti-Pattern hits | 0 | no one-off cataloged; no inline constitution authored beyond named route; no cross-owner promotion |
| Workflow gaps | 2 | (1) private practices had no home; (2) thin one-per-sigil cards were over-statused |
| Output-contract drift | 0 | every run returned the Discipline Governance Result contract |
| User corrections | 0 | operator confirmed scope; no rework of sigil behavior required |

## Patterns Found

- The sigil holds its **boundary** well under pressure: across formalize/route/scan/validate/deprecate it recommended routes and a private home, never promoted a sigil/spell/registry/ontology/glossary.
- The most valuable mode in practice was **`validate`+`deprecate` curation**, not `formalize` — a mature catalog's risk is proliferation, and the sigil's anti-pattern ("cataloging a one-off as a discipline") is exactly the lens that caught the thin one-per-sigil cards.
- The **public/private boundary** is a recurring, load-bearing concern the SKILL under-specified: a `scan` can surface practices that must NOT enter the public catalog, and the sigil had no explicit instruction to tag/home them privately.

## Gap Analysis

| Gap | Severity | Evidence | Affected Contract Area | Recommended Response |
| --- | -------- | -------- | ---------------------- | -------------------- |
| `scan` can surface private-parent practices with no public home | medium | curation run created `disciplines/` at the umbrella root | process / output-contract | Add a `scan` step + output field that tags each candidate public-safe vs private and names the target catalog |
| thin "one discipline per sigil" cards passed as active-pattern | medium | ontology/distillation/residuality downgraded to candidate | quality-bar / anti-pattern | Add a validate check: active-pattern requires ≥1 evidence ref OUTSIDE the owning sigil |
| no telemetry was emitted until now | low | jsonl created retroactively | observability | Wire the post-run hook so future runs emit automatically |

## Proposed Iterations

- Add to SKILL `scan`/`route`: each candidate carries a `public-safe | private-parent` tag and a target catalog (public arcanum vs a private home).
- Add to SKILL `validate`: an `active-pattern` discipline must cite cross-capability evidence beyond its own owning sigil, else it stays `candidate`.
- Note the private-catalog pattern in README (a private umbrella may keep its own `disciplines/`).

## Rejected Changes

- Adding a discipline-creation quota/cap — rejected: proliferation is better controlled by the evidence bar (curation) than an arbitrary limit.
- Auto-deprecating thin cards — rejected: the audit showed none were dead; downgrade-to-candidate is the honest, reversible response.

## Contract Preservation

- Core contract preserved: yes
- Compatibility impact: minor (the proposed iterations add tagging + a validate rule; they do not change the mode set or output contract shape)

## Updated Reflection Policy

- Next manual review condition: after the proposed SKILL iterations land, or on the next `deprecate`/merge.
- Usage threshold: 5
- Output threshold: 10
- Gap threshold: 3
- Severe gap rule: 1 severe (wrong invocation, cross-owner promotion, unreviewable catalog) triggers immediate reflection.

## Decision

- Outcome: targeted update — promote the sigil to v0.2.0 now (3/3 regimes + telemetry + this reflection); apply the two proposed SKILL iterations as the v0.2.x follow-up.
- Owner or reviewer: Constitution Governance / umbrella maintainer
- Next lifecycle step: promote (version bump + status), then apply the tagging + validate-rule iterations.
