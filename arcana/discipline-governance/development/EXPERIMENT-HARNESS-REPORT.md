# Experiment Harness Report - Discipline Governance

Status: promoted v0.2.0 (3/3 regimes + telemetry + reflection complete 2026-06-21)
Date: 2026-06-21
Sigil: `arcana/discipline-governance` (v0.1.0, candidate)
Profile: sigil-development

## Purpose

Accrue the low/medium/complex worked examples + validation evidence the `discipline-governance` sigil needs before promotion beyond v0.1.0. Promotion gate (from sigil-development): experiment harness with low/medium/complex examples, observability signals, a reflection pass, and the sigil's own Growth Rule (owner + evidence + validation surface + mutation boundary).

## Regime Set

| Regime | Scenario | Modes exercised | Example | Result |
| --- | --- | --- | --- | --- |
| **low** | Formalize one recurring practice + route to a constitution | formalize, route, validate | [TEST-GITIGNORE-DISCIPLINE.md](TEST-GITIGNORE-DISCIPLINE.md) | pass |
| **medium** | Formalize + route + author the enforcing constitution, public-boundary clean | formalize, route, validate | [TEST-RECEIPT-ID-LEGEND-DISCIPLINE.md](TEST-RECEIPT-ID-LEGEND-DISCIPLINE.md) | pass |
| **complex** | `scan` over the private umbrella root (discover) + `validate`/`deprecate` curation audit over the 22 arcanum disciplines | scan, validate, deprecate (merge) | [CURATION-RUN-2026-06-21.md](CURATION-RUN-2026-06-21.md) | pass |

## Evidence Summary

- Catalog validator: `VALIDATION=pass`, `DISCIPLINE_COUNT=22` (was 21 before the receipt-id-legend run).
- Both worked examples keep the layer boundary: a discipline recommends a route and never promotes a sigil, spell, registry, ontology, or glossary entry.
- Both cards cite concrete, locally-resolving evidence; the receipt-id-legend card stays inside public arcanum (no private cross-submodule paths).

## Observability

Telemetry from these runs (per the sigil's `<observability>` contract) should record: mode, target discipline id, card created/updated, catalog row added, route + owner, status before/after, validator result, decisions required, pass/flag/block. No repository telemetry package has been wired for this sigil yet — this is a named gap (below).

## Gaps Before Promotion

1. ~~Complex regime unrun~~ — **DONE** ([CURATION-RUN-2026-06-21.md](CURATION-RUN-2026-06-21.md)): scan over the private root + validate/deprecate curation over arcanum's 22, exercising scan + validate + deprecate(merge).
2. ~~No telemetry collected~~ — **DONE**: 3 signals emitted to [.arcanum/observability/by-sigil/discipline-governance.jsonl](../../../.arcanum/observability/by-sigil/discipline-governance.jsonl).
3. ~~Reflection pass~~ — **DONE** (manual): [reflection-report-20260621.md](reflection-report-20260621.md). Note: executions = 3 (manual reflection, below the 5-execution auto-threshold — honest caveat).
4. **Constitutions still `review`-only** — gitignore + receipt-id-legend constitutions lack validators; promotion of those *disciplines* to `canonical` still waits on a validation surface (separate from the sigil's own promotion).

## Verdict

- Sigil promotion: **PROMOTED to v0.2.0** (2026-06-21) — 3/3 regimes + telemetry + reflection; Growth Rule met (owner=Constitution Governance/maintainer, evidence=harness+curation, validation surface=catalog validator + boundary review, mutation boundary=disciplines layer only).
- Honest caveat: this is a v0.1.0→v0.2.0 hardening, not a claim of "canonical." Execution count is 3 (manual reflection), and the reflection named two v0.2.x SKILL iterations (public/private tagging in `scan`/`route`; an `active-pattern` evidence rule in `validate`).

## Next Move

Apply the two reflection-named SKILL iterations (v0.2.x); let telemetry accrue to ≥5 executions for the next threshold-triggered reflection.
