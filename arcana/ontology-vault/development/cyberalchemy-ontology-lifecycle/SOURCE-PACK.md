# CAOL Source Pack For Ontology Vault

Status: source evidence pack
Date: 2026-05-27
Source root: `development/cyberalchemy-ontology-lifecycle/`

## Source Manifest

| Source file | CAOL status | Use in Ontology Vault development |
| --- | --- | --- |
| `README.md` | `final-audit-pass` | Package verdict, source artifact map, candidate authority caveat. |
| `CONTEXT-HANDOFF.md` | `strict-context-pack` | Obligation coverage, selected source evidence, contradictions. |
| `context-pack.json` | `strict-context-pack` | Structured obligation/source/gap inventory. |
| `SOURCE-MAP.md` | `final-source-map` | Authority precedence and evidence coverage across Arcanum, CyberAlchemy, DomainSpec. |
| `DEFINITIONS-GLOSSARY.md` | `candidate-definition-baseline` | Candidate vocabulary for ontology branches, confidence, promotion, signals, axiom/constitution. |
| `external-research-appendix.md` | `complete` | External pressure only; not authority. |
| `CONCEPT-TOURNAMENT.md` | `complete` | Selection of `PromotionRecord` as smallest coherent governance object. |
| `ONTOLOGY-ARCHITECTURE.md` | `candidate-design` | Branches, node types, edge types, authority levels, adapters, owner matrix, PromotionRecord boundary. |
| `PROMOTION-LIFECYCLE.md` | `candidate-design` | Lifecycle states, transition gates, evidence requirements, bridge outcomes, operational-use gates. |
| `INTERROGATION-VERDICT.md` | `caol-010-final-pass` | Flags, repairs, final audit, residual review items. |
| `ROADMAP.md` | `plan-ready` | Layered implementation path and validation strategy. |
| `FIRST-WORKING-SLICE.md` | `plan-ready` | L0 review-only PromotionRecord fixture scenario and checklist. |
| `TASKS.md` | `complete-ledger` | Staged CAOL task ledger. |
| `TASK-STRATEGIES.md` | `active-ledger` | Per-task routes, budgets, and gates. |
| `GOALS.md` | `draft` | Native-goal prompt candidates; useful as execution hints only. |
| `EXECUTION-STRATEGY.md` | `draft` | Full package execution workflow. |
| `SUBSTACK-ARTICLE.md` | `final-candidate` | Public explanation, not schema authority. |
| `PRESENTATION.html` | `contributor-presentation` | Contributor onboarding, not schema authority. |
| `index.json` | `final-audit-pass` | Machine-readable package index, obligations, decisions, next recommended goal. |
| `first-slice/promotion-record-fixture.md` | source artifact | Existing L0 fixture evidence, if present. |
| `first-slice/validation-result.md` | source artifact | Existing fixture validation evidence, if present. |

## Authority Precedence To Preserve

CAOL uses this authority order:

1. Canonical local source files in Arcanum, CyberAlchemy, and DomainSpec.
2. Existing CyberAlchemy ontology source digests and entries, treated as candidate evidence.
3. Curated development/provenance plans.
4. Runtime signal docs and feature packs.
5. External research, only as vocabulary/design pressure.
6. Raw memory or telemetry, never authority by itself.

Ontology Vault should preserve that ordering when using this package.

## Selected Claims

### Candidate Versus Promoted Knowledge

CAOL repeatedly preserves:

```text
candidate knowledge may guide review
promoted knowledge may guide operation
```

Ontology implication:

- candidate branch-aware entries can guide validation,
- promoted branch-aware entries require owner, evidence, confidence, bridge, and governance gates.

### Signals Are Review Inputs

CAOL repairs "Verified Signal" into `ReviewableSignal` to avoid signal-as-truth drift.

Ontology implication:

- signal-derived entries should target `operational` or `bridge` only after review,
- signals may affect evidence confidence,
- signals must not directly increase commitment confidence.

### PromotionRecord Is A Boundary Object

CAOL selects `PromotionRecord` as the smallest cross-lane unit.

Ontology implication:

- PromotionRecord should not replace ontology entries,
- PromotionRecord should record governed change to one claim,
- each independent claim needs its own record,
- raw source dumps and raw telemetry payloads stay outside the record.

### Operational Ontology Remains Candidate

CAOL treats Operational Ontology as a candidate extension, not a permanent top-level branch.

Ontology implication:

- current Ontology Vault work may test `operational` as top-level-with-context,
- canonical acceptance still needs validation and governance review.

### Axiom And Constitution Semantics Are Useful But Not Settled

CAOL's working model:

```text
axiom = behavior invariant or load-bearing principle
constitution = enforceable form/model/structure/process governance that preserves axioms, transformations, and review gates
```

Ontology implication:

- use as candidate role semantics,
- route canonical definition changes through Definitions Governance or decision gate.

## Residual Review Items

CAOL final audit leaves these non-blocking review items:

1. Decide whether Operational Ontology becomes a permanent fourth branch or remains an extension across System and Bridge.
2. Normalize PromotionRecord into an implementation-ready schema/template.
3. Assign named review owners rather than role placeholders.
4. Choose default signal recurrence/severity thresholds.
5. Define bridge-validation evidence templates.
6. Route canonical ontology acceptance through user review, ontology-vault, ontology-harness, or decision-gate.

## Source Use Rule

Use the CAOL package as reviewed candidate evidence, not as canonical ontology authority.
