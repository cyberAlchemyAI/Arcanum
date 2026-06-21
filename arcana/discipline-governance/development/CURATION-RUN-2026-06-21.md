# Discipline Governance - Complex Regime Run: Scan + Curation (2026-06-21)

The **complex** experiment-harness regime for the `discipline-governance` sigil. It exercises the modes neither earlier example touched: `scan` (discover) over the private umbrella root, and `validate` + `deprecate` (curation) over the existing arcanum catalog. Read-only discovery + audit by two parallel subagents; mutations applied by the parent after operator approval.

## Part A - `scan` over the private umbrella root

Found that the root needs almost no new disciplines (confirming the proliferation suspicion). Genuine private-parent candidates, formalized in a NEW **private** catalog (kept out of public arcanum per the open/private boundary):

| Discipline | Status | Home | Evidence |
| --- | --- | --- | --- |
| `submodule-orchestration` | candidate (full card) | `disciplines/` (umbrella root, private) | SUBMODULE-DISCIPLINE.md + Makefile bump-check/doctor |
| `asset-ownership-propagation` | candidate | private | ops/ASSET-OWNERSHIP-POLICY.md + check_github_drift.sh |
| `session-closure` | candidate | private | sessions/ + close-session skill |

Non-disciplines (correctly NOT minted): `agent-signal-emission` = private profile of public `observability`; `subagent-dispatch-registration` = public-safe but cross-references (not merges) `dispatch`; frontmatter / GitNexus / code-tags = domainspec-internal profiles.

## Part B - `validate` + `deprecate` curation over arcanum's 22

Catalog is schema-clean (`VALIDATION=pass`). Verdicts: **KEEP 17 · FIX 4 · MERGE 1 · DEPRECATE 0.** No standalone deprecations warranted — nothing was dead; the bloat was a thin one-per-sigil pointer smell.

Applied:

| Action | Disciplines | What changed |
| --- | --- | --- |
| FIX (status drift) | `quality-bar` | validation mode prose-review → mixed; canonical backing on the Quality Bar constitution made explicit; next hardening = deterministic card validator |
| FIX (thin one-per-sigil) | `ontology`, `distillation`, `residuality` | downgraded active-pattern → candidate (cross-capability recurrence unproven); honest next-hardening move added |
| MERGE | `implementation-readiness` → `planning` | deprecated with superseding route; planning absorbed the smallest-responsible-layer readiness rule |

Validator after edits: `VALIDATION=pass`, `DISCIPLINE_COUNT=22` (count unchanged — merge used deprecation-with-supersede, not row deletion).

## Outcome

- Result: pass. Boundary preserved: scan recommended routes and a private home, never promoted a sigil/spell/registry/ontology/glossary; curation fixed/merged but deprecated nothing dead.
- Modes exercised across the three regimes: formalize, route, validate, scan, deprecate (merge) — the full set.

## Promotion status after this run

- Regimes: **3/3 exercised** (low=gitignore, medium=receipt-id-legend, complex=this run).
- Meaningful executions: **3+** (gitignore formalize; receipt-id-legend formalize+route; scan+curation).
- Still gated on: **telemetry** (no signals emitted yet) and a **reflection pass** (`sigil-development --reflect`). Promotion to v0.2.0 after those two.
