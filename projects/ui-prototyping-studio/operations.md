---
id: ui-prototyping-studio-operations
project: ui-prototyping-studio
title: "UI Prototyping Studio — Lean Operations (L0 loop)"
status: draft
node_type: operations
updatedAt: 2026-06-15
---

# UI Prototyping Studio — Lean Operations

> The L0 operations of the deterministic governance loop, at SPEC altitude. Each block gives the
> `studio` CLI command, inputs, preconditions/gates (citing `INV-x` from `SPEC.md §5`), rules,
> postconditions (state transition + side effects), and owner. Gates are enforced **server-side in
> the orchestration module behind the CLI** (`INV-8`), not bypassable by any flag.
> **Agent proposes** (`GenerateVariants`, `SynthesizeMutationBatch` execution); **human disposes**
> (`SelectOrCommitBaseline`, `ApproveMutationBatch`, `ApplyApprovedBatch`). Verbatim op rules and
> error codes: `provenance/legacy-domainspec-spec/operations.md`. Confirmed against backend
> `application/*.ts`.

## L0 loop

`InitializeSession → SubmitPrompt → GenerateVariants → SelectOrCommitBaseline →
CaptureCommentEvent → SynthesizeMutationBatch → ApproveMutationBatch → ApplyApprovedBatch
[propose → validate → stage → accept-diff → record] → (append manifest) → ExportDesignHandoff`

---

## InitializeSession

- **CLI:** `studio session open [--variant-count N]`
- **Owner:** human
- **Inputs:** `requestedVariantCount?` (int), `requestedBy`.
- **Preconditions/gates:** none.
- **Rules:** default `variantCount = requestedVariantCount ?? 3` and bound to `{1,2,3}` (`INV-1`);
  open both gates as `pending` (`selectionGate`, `applyGate`).
- **Postconditions:** persists one `StudioSession` with `variantCount`, empty prompt, null baseline/
  revision head; state `[none] → SessionInitialized`. Reject `0`/`4` → `VARIANT_COUNT_OUT_OF_RANGE`.
- **Determinism:** pure given inputs (variant labels = `take(['A','B','C'], variantCount)`).

## SubmitPrompt

- **CLI:** (part of `session open`) — submit prompt to the open session.
- **Owner:** human.
- **Inputs:** `sessionId`, `prompt`, `submittedBy`.
- **Preconditions/gates:** session exists.
- **Rules:** prompt non-empty after trim; stored normalized (trimmed); notes/prompt sanitized before
  persist/render (`INV-7`).
- **Postconditions:** `StudioSession.prompt` set; state `SessionInitialized → PromptCaptured`.
  Reject: `SESSION_NOT_FOUND`, empty → `PROMPT_REQUIRED`.

## GenerateVariants

- **CLI:** `studio variants register` (Claude Code supplies the HTML; `--fake`/fixture for e2e).
- **Owner:** **agent proposes** (Claude Code generates the HTML-first variants and registers them).
- **Inputs:** `sessionId`, `requestedBy`; registered variants carry `htmlArtifactRef`,
  `componentsUsed`, `rationale`, `tradeoffs`, `risk`.
- **Preconditions/gates:** prompt set, else `PROMPT_NOT_SET`.
- **Rules:** emit **exactly** `variantCount` variants, else `VARIANT_GENERATION_COUNT_MISMATCH`;
  `variantCount = 1` ⇒ baseline `committed` and `selectionGate = satisfied` immediately;
  `variantCount > 1` ⇒ `selectionGate` stays `pending` (`INV-2`). Registering changes no gate
  beyond this `variantCount` semantic; swapping fake↔Claude Code changes no contract (AC-L0-9).
- **Postconditions:** `PrototypeVariant` rows persisted for the cycle; for count=1 the only variant
  is `committed`; state `PromptCaptured → VariantsReady`.
- **Determinism:** the studio fold is deterministic; HTML content itself is agent-generated and not a
  gate. (`explore`/`exploit` `GenerationMode` is an L0 name; `exploit` requires an existing baseline.)

## SelectOrCommitBaseline

- **CLI:** `studio baseline select <LABEL>` (multi) / `studio baseline commit` (single).
- **Owner:** **human disposes** (intentional baseline) — irreversible governance control (L2 target-size).
- **Inputs:** `sessionId`, `selectedLabel?` (required iff `variantCount > 1`), `requestedBy`.
- **Preconditions/gates:** variants generated (count matches `variantCount`).
- **Rules:** `variantCount > 1` ⇒ `selectedLabel ∈ variantLabels` (`INV-2`), provenance `mode=selected`;
  `variantCount = 1` ⇒ `mode=committed` (no input needed); selected variant marked `selected`/
  `committed`, the rest `candidate`.
- **Postconditions:** `BaselineProvenance` persisted; `revisionHeadId` anchored to `rev-0000` if unset
  (the `BaselineRevisionAnchor` / staleness oracle); `selectionGate → satisfied`, `applyGate → pending`;
  state `VariantsReady → BaselineReady`. (`BaselineGenealogyFamily` is an L0 name; rich genealogy is L4.)
  Reject: missing selection → `BASELINE_SELECTION_REQUIRED`; bad label → `BASELINE_LABEL_INVALID`.

## CaptureCommentEvent

- **CLI:** `studio comment add --target <sel> --severity <s> --intent <i> --note <n>`
- **Owner:** human (annotation).
- **Inputs:** `sessionId`, `revisionId`, `target {selector, elementLabel, odId?}`, `severity`,
  `intent`, `note`, `createdBy`.
- **Preconditions/gates:** `selectionGate = satisfied`, else `BASELINE_GATE_UNSATISFIED` (`INV-2`);
  `revisionId` must match `revisionHeadId` when set, else `SOURCE_REVISION_INVALID`.
- **Rules:** canonical schema mandatory — all of `{target.selector, target.elementLabel, severity,
  intent, note}` present, else `COMMENT_SCHEMA_INVALID`; `severity ∈ {blocker,high,medium,low}`;
  note/intent trimmed and sanitized (`INV-7`).
- **Postconditions:** one `CommentEvent` appended (append-only, the durable synthesis source); state
  `BaselineReady → CommentsCaptured` (self-loop on more comments).

## SynthesizeMutationBatch

- **CLI:** `studio synthesize`
- **Owner:** **agent / system executes** (deterministic fold — agent never reinterprets human intent).
- **Inputs:** `sessionId`, `sourceRevisionId`, `requestedBy`.
- **Preconditions/gates:** `sourceRevisionId` matches `revisionHeadId` when set, else
  `SOURCE_REVISION_INVALID`; ≥1 ordered comment for that revision, else `COMMENT_SET_EMPTY`.
- **Rules:** fold the **ordered** comments into `MutationTask`s; batch starts `status=draft` with
  `approval.required=true` (`INV-3`). `applyGate` stays `pending`. `[PROPOSAL]` each task copies
  `comment.target.odId` into the task and emits `changeType: MutationChangeType` (the
  `"add"|"remove"|"change"` union, replacing the free `string`).
- **Determinism (load-bearing, AC-L0-4):** identical ordered comments + same `sourceRevisionId` ⇒
  **identical task IDs and checksum**. `taskId = "task-" + sha1(sourceRevisionId:commentId:selector:index)[:10]`;
  `checksum = sha256({sourceRevisionId, generatedFromCommentIds, tasks})`. No randomness, no timestamps
  in the fold. `[PROPOSAL]` the checksum now incorporates `odId`, so it is **re-baselined** with a
  checksum **version stamp** (old batches must not read as tampered).
- **Postconditions:** one `draft` `MutationBatch` persisted with `generatedFromCommentIds` and `tasks`;
  state `CommentsCaptured → MutationDrafted`.

## ApproveMutationBatch

- **CLI:** `studio batch approve <batchId> --by <actor>`
- **Owner:** **human disposes** (explicit approval) — irreversible governance control (L2 target-size).
- **Inputs:** `sessionId`, `batchId`, `approvedBy`, `approvedAt` (ISO-8601).
- **Preconditions/gates (server-side, `INV-8`):** batch must be `draft`, else `BATCH_NOT_DRAFT`
  (re-approval rejected); `approvedBy` non-empty and `approvedAt` a parseable timestamp, else
  `APPROVAL_METADATA_REQUIRED`; batch `sourceRevisionId` must equal `revisionHeadId`, else
  `APPROVAL_STALE` (stale rejected, `INV-5`).
- **Rules:** approval is the **only** path `draft → approved` (`INV-3`); records approver identity +
  timestamp.
- **Postconditions:** `MutationBatch.status = approved`; `applyGate → satisfied`; state
  `MutationDrafted → MutationApproved`.

## ApplyApprovedBatch

> `[PROPOSAL]` No longer bookkeeping. This is the **produce → validate → stage → accept → record**
> machine (chosen model: Approach C — agentic-propose behind the CLI seam, deterministic-validate in
> the pure core). Generation is non-deterministic and expressive in the one impure lane (Claude Code);
> determinism is recovered at the **admission boundary** in the pure core. Split into two CLI-facing
> operations: **`studio batch apply`** (propose → validate → stage) and **`studio batch accept`**
> (accept-diff → record). **Auto-apply remains forbidden** (`INV-4`); nothing becomes head without a
> human accepting the exact staged candidate they previewed.

### ApplyApprovedBatch — apply/propose (produce → validate → stage)

- **CLI:** `studio batch apply <batchId> --by <actor>`
- **Owner:** **human triggers**, **agent proposes** (Claude Code), **core validates/stages**.
- **Inputs:** `sessionId`, `batchId`, `applyRequestedBy`.
- **Preconditions/gates (server-side, `INV-8`, all rejected regardless of CLI flags):**
  - `applyRequestedBy != 'system:auto'` (case-insensitive), else `AUTO_APPLY_FORBIDDEN` (`INV-4`).
  - `selectionGate = satisfied` and baseline present, else `BASELINE_GATE_UNSATISFIED` (`INV-2`).
  - batch `status = approved`, else `BATCH_APPROVAL_REQUIRED` (non-approved rejected, `INV-3`).
  - batch `sourceRevisionId = revisionHeadId`, else `BATCH_STALE_FOR_HEAD` (stale rejected, `INV-5`).
- **Rules `[PROPOSAL]`:**
  - **Propose (impure, behind the CLI seam):** read `currentHtml` (via the artifact-content port);
    call Claude Code as a **value-in/value-out** engine — a frozen `ProposeInput` envelope in,
    `candidateHtml + ExecutionProvenance` out. The engine is forbidden the store/clock/append path
    (it never writes). Bounded by `maxProposeAttempts`.
  - **Validate (pure, clock-free):** run the **V1–V9b** deterministic validator suite (see
    *Deterministic validator suite* below) in fixed order over a canonical parse, yielding an
    `AdmissionVerdict`. **Composite fail-closed admission:** all *required* validators pass ⇒ admit;
    any required fails ⇒ **reject** (no write), stay `MutationApproved`, **bounded retry** of propose
    up to `maxProposeAttempts`, then fail.
  - **Stage (no head change):** on admit, compute the **`DiffSummaryHonest`** (per-od-id
    `OdDiffFragment` units derived from `odIndex` set-diff) and stage the `candidateHtml` at a temp ref
    (NOT head) as the **`RevisionApplied`** preview — the real "saw-the-diff" artifact. Record the
    `candidateHtmlHash` and `ExecutionProvenance` (proposer record + per-validator verdicts /
    `verdictHash`) for replay-by-verdict.
- **Postconditions `[PROPOSAL]`:** on admit, candidate staged + honest diff computed; state
  `MutationApproved → RevisionApplied` (preview, head unchanged, `applyGate` still `pending`). On
  reject, no state change. Honors `INV-3/4/5/8` and auto-apply-forbidden.

### ApplyApprovedBatch — accept-diff (accept → record)

- **CLI:** `studio batch accept <batchId> --by <actor>` `[PROPOSAL]`
- **Owner:** **human disposes** (the irreversible durable change) — L2 target-size control.
- **Inputs:** `sessionId`, `batchId`, `acceptRequestedBy`, the previewed `candidateHtmlHash`.
- **Preconditions/gates (server-side, `INV-8`):** a `RevisionApplied` preview exists for the batch;
  `acceptRequestedBy != 'system:auto'` (`INV-4`); batch `sourceRevisionId = revisionHeadId` still
  (re-checked, `INV-5`); the accepted `candidateHtmlHash` equals the staged one — the **accept-diff
  gate**, the human accepts the exact candidate they previewed.
- **Rules `[PROPOSAL]`:** **atomic, all-or-nothing record** — commit the staged HTML (via the
  artifact-content port), allocate next revision off `parentRevisionId = revisionHeadId ?? 'rev-0000'`,
  build `RevisionManifestEntry` carrying `variantCount`, baseline provenance, `parentRevisionId`,
  `appliedBatchId`, `appliedTaskIds`, `unresolvedCommentIds`, `htmlArtifactRef`, `candidateHtmlHash`,
  `provenance: ExecutionProvenance`, and `DiffSummaryHonest`. No partial apply. **Idempotency-at-verdict:**
  record commits *exactly* the accepted `candidateHtmlHash` so **seen == recorded**.
- **Postconditions:** batch `status = applied`; staged HTML committed; **exactly one**
  `RevisionManifestEntry` appended (`INV-6`, guarded post-write — count must be `prev+1` or the record
  throws); `revisionHeadId` advances; `applyGate → pending`; state `RevisionApplied → RevisionRecorded`.
  Then `RevisionRecorded → CommentsCaptured` (iterate) or `→ SessionCompleted` (finalize). Normal apply
  does **not** depend on any proof gate (`INV-9`).
- **Determinism `[PROPOSAL]`:** the *admission verdict* is replayable (clock-free, replay-by-verdict
  via V8); revision-id allocation and the honest diff are deterministic given the staged candidate and
  head. The *proposal itself* is not reproducible — determinism lives at admission, not production.

### Deterministic validator suite `[PROPOSAL]`

Pure, clock-free, run over a canonical parse in **fixed order** (V6 → V1 → V2/V4 → V3 → V7 → V9 →
V9b → V5 → V8), so the first failure code is itself reproducible. **Composite rule:** all *required*
pass ⇒ admit; any required fails ⇒ reject (fail-closed).

- **V6 well-formed-HTML** (required) — parse + parse-reparse fixpoint.
- **V1 target-exists** (required) — anchor resolves to exactly one element in `currentHtml`.
- **V2 target-changed** (required) — addressed subtree hash differs current→candidate.
- **V4 od-id-preserved** (required) — dropped/appeared od-ids ⊆ owned removal/addition tasks.
- **V3 no-out-of-scope-change** (required, the crux) — **whole-tree od-id-attributed diff**: any change
  not dominated by a `TaskScope` od-id is rejected (odIndex is the attribution/display key, not the
  detection domain — repairs the TG-1 un-anchored-markup blindness).
- **V7 text-escaped/sanitized** (required) — no *new* injection vector vs current; escaped round-trip.
- **V9 diff-bounded** (required) — `changeMagnitude <= B(taskCount)`, fixed monotone bound.
- **V9b ops-vs-output-reconciliation** (optional, skipped if no ops) — A-subset reconciliation.
- **V5 acceptanceText-satisfiable-proxy** (**soft/pivotal**) — a structural shadow proxy keyed on
  `changeType`; it is a SOFT proxy, **NOT** a machine check of the acceptance text. Quantitative intent
  (e.g. `44x44px`) is judged only by the human eye at the accept-diff gate, never by the pure lane.
- **V8 idempotency** (required) — double-run verdict-hash equality, clock-free (what makes
  replay-by-verdict true).

### Artifact-content port dependency `[PROPOSAL]`

Apply/accept depend on **artifact-content port methods that do not exist today** — `StudioSessionStorePort`
has zero HTML read/write methods and `htmlArtifactRef` is currently a dangling path. To add:
`readHtml` / `stageHtml` / `commitHtml` / `discardStagedHtml` (read current, stage candidate, commit on
accept, discard on reject) and `removeRevision` (atomic compensation). Until these land, the validator
and recorder lanes have no input and nothing to commit.

## ExportDesignHandoff

- **CLI:** `studio handoff export [--profile mvp]`
- **Owner:** human or system.
- **Inputs:** `sessionId`, `exportProfile?` (default `mvp`), `requestedBy`.
- **Preconditions/gates:** ≥1 `RevisionManifestEntry` and a `revisionHeadId`, else
  `HANDOFF_REVISION_REQUIRED`; baseline present and required downstream files exist
  (`SPEC.md`, `STORIES.md`, `UI-SPEC.md`, `TEST-SPEC.md`), else `HANDOFF_REFERENCE_INCOMPLETE`.
- **Rules:** bundle carries `revisionHeadId`, baseline, `variantCount`, and story/requirement/
  acceptance/UI-spec/test-spec refs; integration flags align with artifact presence.
- **Postconditions:** `HandoffBundle` persisted and queryable; `IntegrationReadiness` flags set true;
  state `RevisionRecorded → RevisionRecorded` (terminal-side projection).

---

## Optional / deferred operations

- **ConfirmUIDecisionEvidence** — *optional L0 branch* (`BaselineReady → IdentityEvidenceConfirmed`).
  Human confirms proposed identity/visual-DNA/decision evidence as durable; requires
  `confirmedBy != 'system:auto'`. Skippable: `BaselineReady → CommentsCaptured` is valid without it.
  Rich identity/DNA types are **L4** (not in code) — see `SPEC.md §3` DEFERRED.
- **RecordFitnessSignal** — **DEFERRED (L5)**. Not detailed; net-new fitness types, gated by OQ-3.
- **EvaluateProofGate** — **DEFERRED (L5+)**. Not detailed; normal MVP apply must not depend on it (`INV-9`).
- **PromoteEvolutionRule** — **DEFERRED (L3+/L5)**. Not detailed; runtime promotion rejected in MVP.
