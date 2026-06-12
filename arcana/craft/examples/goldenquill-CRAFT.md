# CRAFT - GoldenQuill Promotion Governance

Human-readable view of [.craft/ledger.yml](.craft/ledger.yml). The ledger is the
source of truth; this page is a linked index for humans.

## Quick Links

- Current blocker decision: [DEC-OQ4](#decision-dec-oq4).
- Active blockers: [BLK-OQ4-VOCAB](#blocker-blk-oq4-vocab), [BLK-B001-TESTSPEC](#blocker-blk-b001-testspec), [BLK-D5A-THRESHOLD](#blocker-blk-d5a-threshold), [BLK-OQ13-EDGES](#blocker-blk-oq13-edges).
- Active architecture proposals: [DEC-D2-FLIP](#decision-dec-d2-flip), [DEC-D3-SHARED-GATE](#decision-dec-d3-shared-gate), [DEC-D4-VERIFY](#decision-dec-d4-verify).
- Main evidence: [OPEN-QUESTIONS-LEDGER.md](docs/features/goldenquill-promotion-governance/integration/OPEN-QUESTIONS-LEDGER.md), [whole-system-architecture-design.md](docs/features/goldenquill-promotion-governance/integration/whole-system-architecture-design.md), [impl-architecture README](docs/features/goldenquill-promotion-governance/discovery/impl-architecture/README.md).

## Contexts

### <a id="context-ctx-gq-promo-gov"></a>CTX-GQ-PROMO-GOV - GoldenQuill Promotion-Governance Readiness

- Stage: `validate`
- Gate: `flag`
- Purpose: track open questions, blockers, gaps, and decisions for the promotion-governance feature and its Victor learning loop.
- Current next move: resolve [DEC-OQ4](#decision-dec-oq4), then route L1 candidate-shape work.

### <a id="context-ctx-gq-impl-arch"></a>CTX-GQ-IMPL-ARCH - Implementation-Architecture Discovery

- Stage: `validate`
- Gate: `pass`
- Summary: derived the implementation architecture and model read-only from spec, rendered four Victor-pattern views, and drift-checked load-bearing claims.
- Evidence: [impl-architecture README](docs/features/goldenquill-promotion-governance/discovery/impl-architecture/README.md), [drift-check-ledger.md](docs/features/goldenquill-promotion-governance/discovery/impl-architecture/drift-check-ledger.md).

### <a id="context-ctx-gq-arch-design"></a>CTX-GQ-ARCH-DESIGN - Whole-System Architecture Design

- Stage: `validate`
- Gate: `flag`
- Summary: consolidated integration and promotion-governance architecture; proposed D2-D4 designs for team discussion.
- Evidence: [whole-system-architecture-design.md](docs/features/goldenquill-promotion-governance/integration/whole-system-architecture-design.md).

## Decisions

### <a id="decision-dec-oq4"></a>DEC-OQ4 - Promotion Decision Vocabulary

- Question: Should GoldenQuill keep three typed decision surfaces or collapse them into one unified enum?
- Status: `active`, `blocking`
- Description: blocking vocabulary decision for L1 candidate shape and promotion-authority semantics.
- Current selection: pending; operator is weighing three surfaces versus a single enum.
- Proposed direction: three typed surfaces, with `OwnerDecision` as the sole promotion vocabulary.
- Impact: keeps [BLK-OQ4-VOCAB](#blocker-blk-oq4-vocab) active until the vocabulary model is locked.
- Evidence: [OPEN-QUESTIONS-LEDGER.md](docs/features/goldenquill-promotion-governance/integration/OPEN-QUESTIONS-LEDGER.md)

### <a id="decision-dec-d2-flip"></a>DEC-D2-FLIP - L0 To L1 Activation

- Question: How should GoldenQuill authorize the L0 to L1 `mutation_allowed` flip?
- Status: `active`, non-blocking proposal
- Proposed selection: operator-signed per-org Ed25519 flip, journaled; shared-card mutation remains separately gated.
- Impact: turns L0 to L1 activation into an explicit operator event instead of an implicit runtime transition.
- Evidence: [whole-system-architecture-design.md](docs/features/goldenquill-promotion-governance/integration/whole-system-architecture-design.md)

### <a id="decision-dec-d3-shared-gate"></a>DEC-D3-SHARED-GATE - Shared-Card Guardpost

- Question: What gate keeps shared cards general and prevents metric hill-climbing?
- Status: `active`, non-blocking proposal
- Proposed selection: structural generality rule plus operator Ed25519 card-edit review; requires `consent_tier=composable_with_others`.
- Impact: gives [BLK-D5A-THRESHOLD](#blocker-blk-d5a-threshold) a machine-checkable closure path.
- Evidence: [whole-system-architecture-design.md](docs/features/goldenquill-promotion-governance/integration/whole-system-architecture-design.md)

### <a id="decision-dec-d4-verify"></a>DEC-D4-VERIFY - Improvement Verification

- Question: How should GoldenQuill verify an improvement without overfitting to one funder or metric?
- Status: `active`, non-blocking proposal
- Proposed selection: diverse held-out set with rejection on negative primary-KPI delta or significant guardrail-KPI decrease; descriptive stats only.
- Impact: creates an evidence rule without turning promotion into metric optimization.
- Evidence: [whole-system-architecture-design.md](docs/features/goldenquill-promotion-governance/integration/whole-system-architecture-design.md)

## Blockers

### <a id="blocker-blk-oq4-vocab"></a>BLK-OQ4-VOCAB

- Lane: `governance`
- Status: `active`, `refined`
- Closure: operator confirms three-surface model versus single unified enum; canonical promotion vocabulary is locked before L1 candidate shape.
- Linked decision: [DEC-OQ4](#decision-dec-oq4)

### <a id="blocker-blk-b001-testspec"></a>BLK-B001-TESTSPEC

- Lane: `validator`
- Status: `active`, `raw`
- Closure: TEST-SPEC T1-T35 are confirmed authored and stable before TASK-FIX.

### <a id="blocker-blk-d5a-threshold"></a>BLK-D5A-THRESHOLD

- Lane: `governance`
- Status: `active`, `raw`
- Closure: encode a machine-checkable "general guardpost" threshold and "no metric hill-climb" assertion in `PromotionAuthorityPolicy`.
- Related proposal: [DEC-D3-SHARED-GATE](#decision-dec-d3-shared-gate)

### <a id="blocker-blk-oq13-edges"></a>BLK-OQ13-EDGES

- Lane: `governance`
- Status: `active`, `raw`
- Closure: file GQ-AMD-001/002 and author edge-amendments discovery so the 16 coined edges plus `gq_kind` can graduate to the vault.

## Gaps

| ID | Severity | Owner | Summary |
| --- | --- | --- | --- |
| GAP-DESIGNED-NOT-BUILT | block | grant-runtime | Learning loop is designed, not built; humans edit cards by hand today. |
| GAP-PROMO-ENFORCE | block | grant-runtime | No centralized enforcement test proves adapter-side `approved_allowed_uses` is rejected. |
| GAP-L0L1-FLIP | flag | governance | No gate spec for flipping per-org `mutation_allowed` at L0 to L1. |
| GAP-REDACTION-TABLES | flag | governance | Per-CIC redaction/generalization rule tables are unauthored. |
| GAP-KPI-COUNT | flag | grant-runtime | Spec prose says 47 KPIs but enum currently verifies 44. |
| GAP-EVENT-COUNT | flag | grant-runtime | Event-count "13 vs 12" remains unresolved. |

## Candidate Definitions

- **promotion authority** - `OwnerDecision` is the only setter of `approved_allowed_uses`.
- **L0 fixture-only / audit-only** - only C2/C3/C8; `mutation_allowed=false`; no org-vault, card, or dashboard write.

## Recomposition

- [CTX-GQ-IMPL-ARCH](#context-ctx-gq-impl-arch) -> [CTX-GQ-PROMO-GOV](#context-ctx-gq-promo-gov): pass. Residue: KPI 47-vs-44, event 13-vs-12, and [DEC-OQ4](#decision-dec-oq4).
- [CTX-GQ-ARCH-DESIGN](#context-ctx-gq-arch-design) -> [CTX-GQ-PROMO-GOV](#context-ctx-gq-promo-gov): pass. Residue: D2-D4 remain team proposals; [DEC-OQ4](#decision-dec-oq4) remains blocking.

## Artifacts

- [.craft/ledger.yml](.craft/ledger.yml) - machine source of truth.
- [CRAFT.md](CRAFT.md) - this human view.
- [OPEN-QUESTIONS-LEDGER.md](docs/features/goldenquill-promotion-governance/integration/OPEN-QUESTIONS-LEDGER.md)
- [whole-system-architecture-design.md](docs/features/goldenquill-promotion-governance/integration/whole-system-architecture-design.md)
- [impl-architecture README](docs/features/goldenquill-promotion-governance/discovery/impl-architecture/README.md)
- [open-questions-and-blockers.pdf](docs/features/goldenquill-promotion-governance/team-review/open-questions-and-blockers.pdf)
- [whole-system-architecture-design.pdf](docs/features/goldenquill-promotion-governance/team-review/whole-system-architecture-design.pdf)
