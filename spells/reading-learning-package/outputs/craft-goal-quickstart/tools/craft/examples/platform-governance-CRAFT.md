# Platform Governance Craft Ledger

Human-readable view of `.craft/ledger.yml`. The ledger is
the source of truth; this page is a linked index for humans.

## Quick Links

- Current blocker decision: [DEC-AUTHORITY-MODEL-001](#decision-dec-authority-model-001).
- Active blockers: [BLK-AUTHORITY-VOCAB-001](#blocker-blk-authority-vocab-001), [BLK-RETENTION-POLICY-001](#blocker-blk-retention-policy-001).
- Active proposals: [DEC-ROLLOUT-GATE-001](#decision-dec-rollout-gate-001), [DEC-RETENTION-POLICY-001](#decision-dec-retention-policy-001).
- Active gaps: [GAP-ADOPTION-PLAYBOOK-001](#gap-gap-adoption-playbook-001), [GAP-AUDIT-SAMPLING-001](#gap-gap-audit-sampling-001).
- Main evidence: `docs/open-questions.md`, `docs/policy-map.md`, `docs/audit-sampling-note.md`.

## Contexts

### <a id="context-ctx-platform-gov-root"></a>CTX-PLATFORM-GOV-ROOT - Platform Governance Readiness

- Stage: `validate`
- Gate: `flag`
- Purpose: keep policy, rollout, retention, and adoption questions visible before platform mutation work begins.
- Current next move: resolve [DEC-AUTHORITY-MODEL-001](#decision-dec-authority-model-001) before executing policy mutation work.

### <a id="context-ctx-platform-gov-policy"></a>CTX-PLATFORM-GOV-POLICY - Policy Authority Model

- Stage: `validate`
- Gate: `flag`
- Summary: policy mutation must wait until approval authority and retention rules are explicit.
- Evidence: `docs/policy-map.md`, `docs/audit-sampling-note.md`.

### <a id="context-ctx-platform-gov-adoption"></a>CTX-PLATFORM-GOV-ADOPTION - Adoption Rollout

- Stage: `plan`
- Gate: `flag`
- Summary: human adoption can be drafted, but pilot use waits for the rollout gate decision.
- Evidence: `docs/adoption-playbook.md`.

## Decisions

### <a id="decision-dec-authority-model-001"></a>DEC-AUTHORITY-MODEL-001 - Approval Authority Vocabulary

- Question: Which approval authority vocabulary should govern platform policy mutation?
- Status: `active`, `blocking`
- Description: blocking decision for the governance root; it must close before mutation work starts.
- Current selection: pending.
- Default direction: `reviewer-plus-owner`
- Impact: keeps [BLK-AUTHORITY-VOCAB-001](#blocker-blk-authority-vocab-001) active and blocks platform mutation tasks.
- Evidence: `docs/policy-map.md`

### <a id="decision-dec-rollout-gate-001"></a>DEC-ROLLOUT-GATE-001 - Adoption Rollout Gate

- Question: What gate allows the adoption playbook to move from draft to pilot use?
- Status: `active`, non-blocking proposal
- Current selection: pending.
- Default direction: `paired-maintainer-validator-signoff`
- Impact: adoption work can draft, but pilot use waits for closure.
- Evidence: `docs/adoption-playbook.md`

### <a id="decision-dec-retention-policy-001"></a>DEC-RETENTION-POLICY-001 - Evidence Retention

- Question: Which retention rule applies to governance evidence?
- Status: `active`, non-blocking proposal
- Current selection: pending.
- Default direction: `durable-redacted-receipts`
- Impact: keeps [BLK-RETENTION-POLICY-001](#blocker-blk-retention-policy-001) active until retention expectations are explicit.
- Evidence: `docs/audit-sampling-note.md`

## Blockers

### <a id="blocker-blk-authority-vocab-001"></a>BLK-AUTHORITY-VOCAB-001

- Lane: `governance`
- Status: `active`, `refined`
- Role: `governance_reviewer`
- Allowed roles: `governance_reviewer`, `policy_owner`, `auditor`
- Human required: `true`
- Role confidence: `active-local`
- Closure: [DEC-AUTHORITY-MODEL-001](#decision-dec-authority-model-001) closes with selected approval vocabulary and evidence link.
- Linked decision: [DEC-AUTHORITY-MODEL-001](#decision-dec-authority-model-001)
- Role note: governance reviewer prepares the decision; authority closes only through the linked decision.

### <a id="blocker-blk-retention-policy-001"></a>BLK-RETENTION-POLICY-001

- Lane: `governance`
- Status: `active`, `typed`
- Role: `policy_reviewer`
- Allowed roles: `policy_reviewer`, `governance_reviewer`, `auditor`
- Human required: `true`
- Role confidence: `candidate`
- Closure: [DEC-RETENTION-POLICY-001](#decision-dec-retention-policy-001) closes or is explicitly deferred with audit rationale.
- Role note: retention policy can be proposed by policy review, but closure needs governance or audit rationale.

## Gaps

### <a id="gap-gap-adoption-playbook-001"></a>GAP-ADOPTION-PLAYBOOK-001

- Severity: `flag`
- Treatment: `plan`
- Owner: `operations`
- Summary: adoption playbook is planned but not drafted.

### <a id="gap-gap-audit-sampling-001"></a>GAP-AUDIT-SAMPLING-001

- Severity: `flag`
- Treatment: `plan`
- Owner: `auditor`
- Summary: audit sampling rule is proposed but not yet validated against a representative review set.

## Candidate Definitions

- **approval authority** - the owner, reviewer, or governance body allowed to convert a proposed policy change into approved platform behavior.
- **adoption gate** - the explicit decision that says a human rollout path is ready for use beyond the test group.

## Recomposition

[CTX-PLATFORM-GOV-POLICY](#context-ctx-platform-gov-policy) recomposed into
[CTX-PLATFORM-GOV-ROOT](#context-ctx-platform-gov-root) with a `flag` result.
Residue: [DEC-AUTHORITY-MODEL-001](#decision-dec-authority-model-001) remains
blocking and [DEC-RETENTION-POLICY-001](#decision-dec-retention-policy-001)
remains open.

## Artifacts

- `.craft/ledger.yml` - machine source of truth.
- `CRAFT.md` - this human view.
- `docs/open-questions.md`
- `docs/policy-map.md`
- `docs/adoption-playbook.md`
- `docs/audit-sampling-note.md`
