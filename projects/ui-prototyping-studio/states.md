---
id: ui-prototyping-studio-states
project: ui-prototyping-studio
title: "UI Prototyping Studio — StudioSessionState Machine (lean L0→L2)"
status: draft
node_type: states
updatedAt: 2026-06-15
---

# UI Prototyping Studio — StudioSessionState

> Lean states aspect for the L0→L2 release. Source of truth: `SPEC.md` §5 (10 states, INV-1..9).
> The `EvolutionCycleState` machine and all failure/recovery states are **deferred (L3+)** — see the
> Deferred note. The 10-state enum is confirmed in
> `implementation/domainspec/backend/src/modules/ui-prototyping-studio/domain/models.ts`
> (`StudioSessionState`); `IdentityEvidenceConfirmed` is the optional doc-level confirm branch and is
> not a code enum member at L0.
> The **two-gate apply** semantics for `RevisionApplied`/`RevisionRecorded` (INV-10..13, marked
> `[PROPOSAL]`) come from the mutation-execution-mechanics refine RESULT §5 and are not yet canonical.

## States

1. **SessionInitialized** — `variantCount` validated/defaulted (1..3, default 3).
2. **PromptCaptured** — non-empty prompt stored on the session.
3. **VariantsReady** — exactly `variantCount` variants generated and registered.
4. **BaselineReady** — baseline selected (`>1`) or committed (`=1`); anchor + family created.
5. **IdentityEvidenceConfirmed** — *optional branch*; identity/DNA suggestions confirmed durable.
6. **CommentsCaptured** — one or more canonical element-level comments appended (self-loop on more).
7. **MutationDrafted** — deterministic draft `MutationBatch` synthesized (`status=draft`).
8. **MutationApproved** — explicit human approval (`status=approved`; apply gate satisfied).
9. **RevisionApplied** — *staged preview / accept-diff gate* `[PROPOSAL]`. After `validate` admits, the proposed candidate HTML is staged at a **temp ref (NOT head)**, the honest diff is computed and shown (the saw-the-diff moment), and the session **waits for the human accept-diff gate**. Nothing has become head yet. (Resolves GAP-CONTRACT-DRIFT-004: distinct from RevisionRecorded.)
10. **RevisionRecorded** — human accepted the staged diff; the exact accepted candidate is atomically recorded (head advanced) and exactly one `RevisionManifestEntry` appended.

Terminal: **SessionCompleted** — session locked for handoff export.

## Transition table

| From | Event / operation (CLI · operation) | To | Guard / gate |
|---|---|---|---|
| SessionInitialized | `studio session open` · InitializeSession | SessionInitialized | `variantCount ∈ {1,2,3}`, default 3 (INV-1) |
| SessionInitialized | `studio session open` (prompt) · SubmitPrompt | PromptCaptured | prompt non-empty (INV-7) |
| PromptCaptured | `studio variants register` · GenerateVariants | VariantsReady | exactly `variantCount` HTML-first variants (INV-1) |
| VariantsReady | `studio baseline select` · SelectBaseline | BaselineReady | `variantCount > 1`, selected label valid (INV-2); creates anchor + family |
| VariantsReady | `studio baseline commit` · CommitBaseline | BaselineReady | `variantCount = 1`, mode `committed`, selection gate satisfied (INV-2) |
| BaselineReady | `studio baseline confirm` · ConfirmUIDecisionEvidence | IdentityEvidenceConfirmed | *optional*; human confirmation present |
| BaselineReady | `studio comment add` · CaptureCommentEvent | CommentsCaptured | comment payload `{target, severity, intent, note}` valid, sanitized (INV-7); selection gate satisfied (INV-2) |
| IdentityEvidenceConfirmed | `studio comment add` · CaptureCommentEvent | CommentsCaptured | comment payload valid + sanitized (INV-7) |
| CommentsCaptured | `studio comment add` · CaptureCommentEvent | CommentsCaptured | *(self-loop)* additional valid comment appended (INV-7) |
| CommentsCaptured | `studio synthesize` · SynthesizeMutationBatch | MutationDrafted | ordered comment set exists; `status=draft` |
| MutationDrafted | `studio batch approve` · ApproveMutationBatch | MutationApproved | explicit human approval; `status=approved`, apply gate satisfied (INV-3) |
| MutationApproved | `studio apply` · ProposeAndValidate `[PROPOSAL]` | RevisionApplied *(candidate staged)* | batch approved (INV-3), non-stale (INV-5), non-auto (INV-4), server-side (INV-8), no proof gate (INV-9); **all required validators pass** (INV-10) ⇒ candidate staged at temp ref |
| MutationApproved | `studio apply` · ProposeAndValidate (**required-fail**) `[PROPOSAL]` | MutationApproved *(no write)* | required validator fails ⇒ **REJECT, no write**, fail-closed (INV-12); bounded `maxProposeAttempts` retry then stays MutationApproved |
| RevisionApplied | `studio apply accept` · AcceptDiffAndRecord `[PROPOSAL]` | RevisionRecorded | **human accept-diff gate** (second gate); accept-time staleness re-check (INV-5); atomic all-or-nothing record (INV-11); exactly one `RevisionManifestEntry` appended (INV-6); commits exactly the accepted `candidateHtmlHash`, seen==recorded (INV-13) |
| RevisionApplied | `studio apply reject` · DiscardStagedCandidate `[PROPOSAL]` | MutationApproved | human rejects/discards staged candidate; temp ref dropped, no head change |
| RevisionRecorded | `studio comment add` · ContinueIteration | CommentsCaptured | *(iterate)* session not finalized; loop continues on active baseline |
| RevisionRecorded | `studio handoff export` · FinalizeSession | SessionCompleted | user finalizes; session locked for handoff |

## Invariants (SPEC §5) and enforcing transitions

| ID | Invariant | Enforced by |
|---|---|---|
| INV-1 | `variantCount ∈ {1,2,3}` in all states; default `3` when unset. | InitializeSession; GenerateVariants (and persisted in every state) |
| INV-2 | `variantCount > 1` ⇒ baseline selection mandatory before comment/synthesis/apply; `=1` ⇒ mode `committed`, gate satisfied without input. | SelectBaseline / CommitBaseline; the CaptureCommentEvent edges out of BaselineReady |
| INV-3 | Approval-before-apply: batch starts `draft`; only explicit approval ⇒ `approved`; apply rejected for non-approved. | ApproveMutationBatch; ApplyApprovedBatch (guard) |
| INV-4 | Auto-apply forbidden: `applyRequestedBy != 'system:auto'` in every state. | ApplyApprovedBatch (guard) |
| INV-5 | Stale check: apply rejected when batch is stale vs revision head / `BaselineRevisionAnchor`. | ApplyApprovedBatch (guard) |
| INV-6 | One manifest append per apply (append-only). | AppendManifest (RevisionApplied → RevisionRecorded) |
| INV-7 | Comment notes and prompt text escaped/sanitized before persist and render. | SubmitPrompt; every CaptureCommentEvent edge |
| INV-8 | Gate checks (selection, approval, staleness, non-auto actor) enforced server-side, not only UI. | ApplyApprovedBatch (guard); all gate transitions behind the CLI |
| INV-9 | Normal MVP apply MUST NOT depend on proof-gate evaluation. | ApplyApprovedBatch (no proof-gate dependency) |
| INV-10 `[PROPOSAL]` | Validate is **fail-closed**: candidate staged only if ALL required validators pass; any required fail ⇒ reject, no write. | ProposeAndValidate (composite admission rule) |
| INV-11 `[PROPOSAL]` | **Whole-batch all-or-nothing**: record commits the entire candidate atomically or nothing; no partial apply. | AcceptDiffAndRecord (single commit point) |
| INV-12 `[PROPOSAL]` | Reject leaves no trace: required-fail and human reject/discard both perform **no write** and keep the prior head. | ProposeAndValidate; DiscardStagedCandidate |
| INV-13 `[PROPOSAL]` | **Idempotency-at-verdict**: record commits exactly the accepted `candidateHtmlHash` (the diff the human saw); seen == recorded. | AcceptDiffAndRecord (hash-bound record) |

## Deferred (L3+)

Failure/recovery states — **GenerationFailed**, **SynthesisTimedOut**, **SourceStale**,
**ApplyConflicted** (and related interaction-flow recovery gates) — and the entire
**EvolutionCycleState** machine (genome/population/lineage/fitness/proof states) are **out of scope**
for this release. They require new states plus a failure-injection mock that does not exist in code.
See `development/deep-spec-dispatch/`.
