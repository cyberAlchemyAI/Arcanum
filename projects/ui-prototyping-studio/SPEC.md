---
id: ui-prototyping-studio-spec
project: ui-prototyping-studio
title: "UI Prototyping Studio — Lean Feature Spec (L0→L2 survival/trust floor)"
status: draft
node_type: spec
updatedAt: 2026-06-15
---

# UI Prototyping Studio — Lean Feature Spec

> Lean replacement for the 79KB full-vision spec. Scoped to the **buildable** floor the
> deep-spec readiness verdict authorized: the working L0 loop, hardened to L1 (accessibility)
> and L2 (layout integrity). Everything past L2 is deferred and named, not designed in here.
> Full vision lives in `provenance/legacy-domainspec-spec/` and `development/deep-spec-dispatch/`.

## 2. What this is

UI Prototyping Studio is a tool for **accountable UI exploration**: a human gives a prompt, the
agent generates 1–3 HTML-first variants, the human chooses an intentional baseline, annotates it
with canonical element-level comments, the agent deterministically synthesizes a draft mutation
batch, the human explicitly approves it, the batch is applied, and one append-only revision entry
is recorded — then the work is handed off downstream. **Governance is a feature, not friction**:
the agent has an accountable opinion but never an unaccountable action, and the human disposes
every durable change. The design is **ergonomics-first** — the agent earns its keep on reversible
work so the human's attention is spent only at the named, irreversible checkpoints.

### Interaction model & where the agent acts

**Runtime: Claude Code-native (operated in VSCode), via a `studio` CLI — no MCP server.** The embedded
assistant *is* Claude Code — the studio has **no separate LLM integration, API key, or agent loop**.
The studio is the **governance harness**; Claude Code is the generation/mutation engine. Components:

- **`studio` CLI** (wraps the orchestration module) — the single operation surface for **both** Claude
  Code and the human: `session open`, `variants register`, `state`, `baseline select|commit`,
  `comment add`, `synthesize`, `batch approve`, `batch apply`, `handoff export`, `preview`. Governance
  invariants are enforced in the orchestration module **behind** the CLI (auto-apply forbidden,
  approval-before-apply, stale check) — server-side, not in any UI and not bypassable by a flag.
- **Operating skill** (`SKILL.md`) — teaches Claude Code the `studio` commands + discipline: generate
  on request, `variants register`, never self-approve/apply, hand the gates to the human.
- **Visual review + in-prototype annotation** — `studio preview` renders the variant/revision HTML and
  **injects a click-to-annotate overlay**: clicking a rendered element captures its **stable component id**
  (`data-od-id` → `AnnotationTarget.odId`, with the CSS selector as fallback) + label and opens a
  `{severity, intent, note}` comment that feeds `CaptureCommentEvent`. Comments are captured **directly on
  the components** — no hand-typed selectors, no separate React SPA. (`studio comment add` remains the
  scriptable/headless path; both produce the identical `CommentEvent` contract.)
- **Stable annotation targets (light component identity).** The generator stamps annotatable elements with a
  stable `data-od-id` on a minimal component-role convention, so a comment's target **survives regeneration**
  (Explore→Exploit, applied mutations) instead of breaking with the DOM. The full atomic-design taxonomy
  (atoms→organisms), component registry, and `UIElementIdentity`/conformance-delta are the **L4** realization
  of this same idea — deferred (see `BLK-IDENTITY-TYPES-002`, `GAP-COMPONENT-REGISTRY-002`).

The loop: human asks Claude Code for a UI → Claude Code generates 1–3 HTML variants and
`studio variants register`s them → human `studio preview`s and runs the gate commands
(`baseline select`, `comment add`, `batch approve`, `batch apply`) → the studio deterministically
synthesizes the draft batch → Claude Code executes the approved mutation → one manifest entry is
appended. **Agent proposes (generate / mutate), human disposes (select / approve / apply) via the CLI;
synthesis stays deterministic** so the agent can never reinterpret the human's intent.

**Generator seam = the CLI.** Claude Code generates the HTML and registers it through
`studio variants register`; a **deterministic fake** (`--fake` / fixture) drives e2e. No MCP server,
no `@anthropic-ai/sdk`, no API key. (An MCP adapter and a standalone Anthropic-SDK adapter both remain
future options behind the same orchestration core if ever needed.)

### Mutation-execution model (Approach C — part of L0 scope) `[PROPOSAL]`

How an approved batch becomes a recorded revision (DEC-MUTATION-EXEC-015, Approach C). The model
keeps generation expressive in one impure lane and **recovers determinism at the admission boundary**
inside the pure core — four lanes, the seam between lane 2 and lanes 3–4 being load-bearing:

| Lane | Owner | Purity | Responsibility |
|---|---|---|---|
| 1. Synthesis | core | pure | comments → `MutationBatch` (checksummed) — unchanged |
| 2. Proposer (engine) | Claude Code | impure (LLM) | `propose(currentHtml, tasks, context) → candidateHtml + provenance`, behind the `studio` CLI seam |
| 3. Validator suite | core | pure, clock-free | `validate(...) → AdmissionVerdict` (V1–V9b) |
| 4. Recorder | core | pure-effectful | admit ⇒ persist HTML + append exactly-one revision + advance; reject ⇒ persist nothing |

**Admission-boundary determinism (not producer, not persist-step alone).** Determinism is *relocated*:
validator purity (no `Date.now`/`Math.random`/fs/network; structural validators run over a canonical
parse), **one shared canonicalizer used on both sides of the seam**, and **replay-by-verdict** — the
*decision to admit* is replayable, the *proposal* is not. (A and B reachable as config — C→B if the
validator proves unbuildable, C→A if the workload is enumerable — not redesign.)

**Two-gate apply.** First gate = approve-intent (existing). The proposer runs, the validator admits or
rejects fail-closed; on admission the candidate is **staged at a temp ref (NOT head)** and the honest
diff is shown — the saw-the-diff moment. Second gate = the human **accept-diff** on the exact staged
candidate; only then does the recorder commit. Whole-batch all-or-nothing; commit binds the previewed
`candidateHtmlHash` (seen == recorded).

## 3. Scope: L0→L2 (this release)

### IN

- **L0 — the working loop + governance invariants.** The implemented spine: `InitializeSession →
  SubmitPrompt → GenerateVariants → SelectOrCommitBaseline → CaptureCommentEvent →
  SynthesizeMutationBatch → ApproveMutationBatch → ApplyApprovedBatch → (append manifest) →
  ExportDesignHandoff`, the 10-state `StudioSessionState` machine, and the load-bearing governance
  invariants (auto-apply forbidden, approval-before-apply, stale-source rejection, append-only
  manifest, `variantCount` 1..3). This already exists in code (`models.ts`, `mock-api.ts`, e2e).
- **L1 — accessibility.** Keyboard operability of every gate, ARIA roles/names on all controls,
  visible/managed focus on selection and approval transitions, explicit form labels and severity
  semantics, and non-color-only state cues.
- **L2 — layout integrity.** No overflow/clip/overlap of studio surfaces; WCAG 2.2 target-size
  (≥24×24) on irreversible governance controls; responsive at the supported breakpoints.
- **`studio` CLI + operating skill (the Claude Code seam) — no MCP.** Wrap the orchestration module in
  a `studio` CLI that Claude Code and the human both drive; Claude Code registers generated HTML via
  `studio variants register`; a deterministic fake drives tests. Ship the operating `SKILL.md`.
  Generation/mutation are the *only* agentic actions; all gates are enforced server-side behind the CLI.

### DEFERRED (named, not designed here)

| Layer | What | Why deferred | Pointer |
|---|---|---|---|
| L3 | Interaction-flow failure/recovery gates (`GenerationFailed`, `SynthesisTimedOut`, `SourceStale`, `ApplyConflicted`, `DeterminismDrift`, …) | Needs 7 new states + failure-injection mock that **does not exist in code**; provenance fingerprint (`Inv-1`) is proposed-not-calibrated | `development/deep-spec-dispatch/` (L3) |
| L4 | Identity/DNA + conformance-delta (`UIElementIdentity`, `UIVisualSignature`, `previewRef`, signed `DiffSummary.fieldDeltas`) | The identity/conformance types **do not exist in code** (`DiffSummary` is bare `{added,changed,removed}` counts); net-new build | `development/deep-spec-dispatch/` (L4) |
| L5 | Domain/fitness scoring, concurrency atomicity, bounded stores (`FitnessSignal`/`FitnessVector`, `Inv-3..5,8`) | Net-new types + backend serialization; **OQ-3** blocks it | `development/deep-spec-dispatch/` (L5) |
| L6 | Human-evidence / trust ergonomics (`WorkflowStep` projection, plain-language copy, trust meter) | Ergonomics payoff is **unproven and human-study-gated**; **OQ-1/OQ-2** block it | `development/deep-spec-dispatch/` (L6) |

### Deferred open questions (carried)

- **OQ-1** — trust-meter design (blocks L6; do not ship unvalidated).
- **OQ-2** — "saw-the-diff" proxy before irreversible apply (blocks L6).
- **OQ-3** — operator-handoff carry/reset/prompt policy (blocks L5).
- **OQ-4** — import-integrity MVP boundary (forged-provenance scope, out of L1).

## 4. Domain model (what exists in code)

Only the domainspec UI types that back the L0 loop. (Identity/DNA, conformance, fitness, and proof
types exist as *names* in the legacy domain but carry no working code yet — they are L4/L5 deferrals.)

| Type | Kind | Role at L0 |
|---|---|---|
| `StudioSession` | Entity | Root: persists `variantCount`, baseline provenance, revision head, gate state, current `StudioSessionState`. |
| `PrototypeVariant` | Entity | One row per generated candidate in the current cycle (HTML-first + metadata). |
| `CommentEvent` | Entity | Canonical element-level comment; append-only durable source for synthesis. |
| `MutationBatch` | Entity | Deterministic draft from comments; starts `draft`, requires approval before apply. |
| `RevisionManifestEntry` | Entity | Exactly one append-only record per successful apply. `[PROPOSAL]` gains `htmlArtifactRef`, `candidateHtmlHash`, and `provenance: ExecutionProvenance` (model, `promptHash`, input/output hashes [non-replayable] + `verdictHash` + per-validator results [replayable]). |
| `BaselineGenealogyFamily` | Entity | Durable family created when one baseline survives the generated population. |
| `VariantCount` | Value Object | Allowed `{1,2,3}`, session default `3`. |
| `GenerationMode` | Value Object | `explore` (new directions) or `exploit` (baseline-conforming; requires existing baseline). |
| `BaselineProvenance` | Value Object | `mode ∈ {selected, committed}`; the intentional-baseline record. |
| `BaselineRevisionAnchor` | Value Object | Explicit anchor created at baseline resolution; staleness oracle for apply. |
| `AnnotationTarget` | Value Object | Stable target reference a `CommentEvent` points at. |
| `MutationTask` | Value Object | One deterministic task folded from comments into a `MutationBatch`. `[PROPOSAL]` gains `odId: string \| null` (copied from `comment.target.odId`) and `changeType: MutationChangeType = "add"\|"remove"\|"change"`; batch `sha256` re-baselined with a checksum version stamp. |
| `DiffSummaryHonest` / `OdDiffFragment` | Value Object | `[PROPOSAL]` replaces `DiffSummary` (and deletes `buildDiffSummary`): per-od-id `OdDiffFragment` units; counts **derived** from a real before/after `odIndex` set-diff, never from `changeType`. |
| `TypedReference` | Value Object | Wire-level ref for domain/artifact/handoff links. |
| `CommentSeverity` | Enum | `blocker / high / medium / low`. |
| `MutationBatchStatus` | Enum | `draft / approved` (apply forbidden until `approved`). |
| `GateState` | Enum | Selection/apply gate state (`satisfied` / blocked). |
| `StudioSessionState` | State Machine | The 10-state deterministic loop (see §5). |

## 5. State machine + invariants (the L0 acceptance contract)

### The 10 `StudioSessionState` states (deterministic loop)

1. `SessionInitialized` — `variantCount` validated/defaulted.
2. `PromptCaptured` — non-empty prompt stored.
3. `VariantsReady` — exactly `variantCount` variants generated.
4. `BaselineReady` — baseline selected (`>1`) or committed (`=1`); anchor + family created.
5. `IdentityEvidenceConfirmed` — optional branch; identity/DNA suggestions confirmed durable.
6. `CommentsCaptured` — one or more canonical comments appended (self-loop on more).
7. `MutationDrafted` — deterministic draft `MutationBatch` (`status=draft`).
8. `MutationApproved` — explicit human approval (`status=approved`, apply gate satisfied).
9. `RevisionApplied` — `[PROPOSAL]` **the staged preview / accept-diff state** (no longer dead): the
   admitted candidate is staged at a temp ref (NOT head) and the honest diff is shown for human review.
10. `RevisionRecorded` — exactly one `RevisionManifestEntry` appended; revision head updated.

**Two-gate apply transitions `[PROPOSAL]`** (DEC-MUTATION-EXEC-015): `MutationApproved` → [propose]
(impure) → [validate] (pure; **required-fail ⇒ reject, no write, stay `MutationApproved`**) →
`RevisionApplied` (candidate staged at temp ref + honest diff shown) → human **accept-diff** → [record]
(atomic, whole-batch all-or-nothing, commits exactly the previewed `candidateHtmlHash`) →
`RevisionRecorded`. Bounded `maxProposeAttempts`.

> This **resolves the old `RevisionApplied`/`RevisionRecorded` contract-drift** (§8): the two states now
> carry distinct meaning — `RevisionApplied` = staged-but-not-head preview gate, `RevisionRecorded` = committed.

Terminal: `RevisionRecorded → SessionCompleted` (finalize) or `RevisionRecorded → CommentsCaptured`
(continue iteration). `BaselineReady → CommentsCaptured` is also valid (identity confirm is optional).

### Load-bearing invariants (verbatim intent from the implemented governance)

| ID | Invariant |
|---|---|
| INV-1 | `variantCount` MUST stay in `{1,2,3}` in all states; default `3` when unset. |
| INV-2 | `variantCount > 1` ⇒ baseline selection is mandatory before any comment/synthesis/apply; `variantCount = 1` ⇒ baseline mode is `committed` and the selection gate is satisfied without further input. |
| INV-3 | **Approval-before-apply.** A `MutationBatch` starts `draft`; only explicit human approval transitions it to `approved`; `ApplyApprovedBatch` is rejected for a non-approved batch. |
| INV-4 | **Auto-apply forbidden.** `applyRequestedBy != 'system:auto'` in every state. |
| INV-5 | **Stale check.** Apply is rejected when the batch is stale relative to the current revision head / `BaselineRevisionAnchor`. |
| INV-6 | **One manifest append per apply.** Every successful apply appends exactly one `RevisionManifestEntry` (append-only). |
| INV-7 | Comment notes and prompt text are **escaped/sanitized** before persistence and render. |
| INV-8 | Gate checks (selection, approval, staleness, non-auto actor) are enforced **server-side**, not only in the UI. |
| INV-9 | Normal MVP apply MUST NOT depend on proof-gate evaluation. |

## 6. Surfaces (7 panels)

1. **Session Controls** — capture prompt, set `variantCount` (1..3, default 3).
2. **Variant Canvas** — show generated candidates + metadata for review/selection.
3. **Identity Evidence** — review/confirm identity & visual-DNA evidence (L0: optional confirm branch; rich preview is L4).
4. **Annotation Panel** — capture canonical element-level comments on the active baseline.
5. **Mutation Approval Panel** — present deterministic draft tasks before explicit approval.
6. **Revision Timeline** — display the immutable, append-only revision history.
7. **Handoff Summary** — publish downstream-ready links and evidence.

## 7. Acceptance criteria (L0→L2)

### L0 — the working loop + governance (tie to existing e2e: `wp01`, `wp02`/`wp03`, `mock-api.ts`)

- **AC-L0-1** Session created without `variantCount` persists `variantCount = 3`; `0` and `4` are rejected. (INV-1)
- **AC-L0-2** For `variantCount = 3`, an apply attempt before baseline selection is blocked with a gate error; for `variantCount = 1` the single option is committed and the selection gate is satisfied. (INV-2)
- **AC-L0-3** Full happy-path cycle completes end-to-end via `getByRole`, exercising both the `variantCount=3` selected branch and the `variantCount=1` committed branch (the mock auto-commits `rev-0000` for count=1). (covered by `wp01`/`wp02`/`wp03`)
- **AC-L0-4** Re-running `SynthesizeMutationBatch` on identical ordered comments yields identical task IDs and payload (deterministic fold).
- **AC-L0-5** Applying a `draft` batch without approval is rejected; applying an `approved` batch creates the next revision and appends exactly one manifest entry including `variantCount`, baseline provenance (`selected`/`committed`), and `baselineRevisionId`. (INV-3, INV-6)
- **AC-L0-6** A direct network apply with `applyRequestedBy='system:auto'` is rejected (`AUTO_APPLY_FORBIDDEN`); the UI never reaches an applied state. (INV-4, INV-8)
- **AC-L0-7** Applying a stale batch (head moved) is rejected. (INV-5)
- **AC-L0-8** Comment missing any of `{target, severity, intent, note}` is rejected; persisted notes are escaped. (INV-7)
- **AC-L0-9** Variant generation flows through the `studio variants register` command (Claude Code supplies the HTML); e2e uses a deterministic fake; the command accepts exactly `variantCount` HTML-first variants with `rationale`/`tradeoffs`/`risk` and changes no gate. Swapping fake↔Claude Code changes neither the session contract nor any gate.
- **AC-L0-10** The `studio` CLI exposes the full session loop (`open`/`variants register`/`state`/`baseline`/`comment`/`synthesize`/`batch approve`/`batch apply`/`handoff`/`preview`); a Claude Code session drives generate→register→(human CLI gates)→apply, and `batch apply` refuses non-approved, auto (`system:auto`), or stale applies server-side (INV-3/4/5/8) regardless of CLI flags.
- **AC-L0-11** `studio preview` serves the prototype HTML with a click-to-annotate overlay: clicking a rendered element captures its **`data-od-id` (stable component id) as the primary target**, with the CSS selector + label as fallback, and submits a `CommentEvent` with `{severity, intent, note}` — no manual selector entry. The overlay path and `studio comment add` produce the identical `CommentEvent` contract (`{target:{odId,selector,elementLabel}, severity, intent, note}`), and annotation stays gated (blocked until a baseline exists, INV-2).
- **AC-L0-12** Generated variant HTML stamps annotatable elements with a stable `data-od-id`; a comment captured on a variant resolves to the same `odId` after the baseline is regenerated/mutated (target survives regeneration). Where no `data-od-id` is present, the overlay falls back to the CSS selector and flags the target as non-durable.
- **AC-L0-13** `[PROPOSAL]` The V1–V9b validator suite admits **server-side and fail-closed**: a proposed candidate is recorded only if every required validator passes; any required failure rejects with a reproducible first-failure code, writes nothing, and the session stays `MutationApproved`. (DEC-MUTATION-EXEC-015)
- **AC-L0-14** `[PROPOSAL]` The accept-diff gate commits **exactly the previewed `candidateHtmlHash`** (seen == recorded): the recorded `RevisionManifestEntry.candidateHtmlHash` equals the hash of the candidate staged at `RevisionApplied`; a mismatch aborts the commit.
- **AC-L0-15** `[PROPOSAL]` Recording is **whole-batch all-or-nothing**: either the full candidate HTML is persisted with exactly one revision appended and head advanced, or nothing is written — no partial apply.
- **AC-L0-16** `[PROPOSAL]` `acceptanceText` is **NOT machine-checked**: admission means "anchored, in-scope, well-formed, safe, bounded change occurred," not "acceptance met." Quantitative intent (e.g. `button >= 44x44px`) is human-judged at the accept-diff gate; the pure lane performs no geometry/CSS-layout check.

### L1 — accessibility (axe + keyboard checks)

- **AC-L1-1** Every interactive control (variant cards, comment targets, gate buttons) has an accessible name + role; an axe scan reports zero `button-name`/`label` violations on each panel.
- **AC-L1-2** The full happy-path cycle is operable by keyboard alone; tab order across the 7 panels follows reading order.
- **AC-L1-3** The `ApplyApprovedBatch` confirmation is a `role=dialog`/`aria-modal` with focus trap + return-focus; Escape closes it.
- **AC-L1-4** Each disabled governance control exposes its reason via `aria-describedby`; session-state transitions announce once via `aria-live="polite"`.
- **AC-L1-5** Severity and gate states are distinguishable without color alone.

### L2 — layout integrity (layout/measurement checks)

- **AC-L2-1** At each supported breakpoint, no studio surface overflows, clips, or overlaps its container (measured bounding-box assertions).
- **AC-L2-2** Irreversible governance controls (`SelectOrCommitBaseline`, `ApproveMutationBatch`, `ApplyApprovedBatch`) meet WCAG 2.2 SC 2.5.8 target size (≥24×24), with a product-context exception for low-risk secondary controls.
- **AC-L2-3** The 7 panels remain reachable and legible (no off-viewport content, no horizontal scroll trap) across the responsive range.

> "Done" for this release = all L0 ACs green against the existing e2e harness, plus the L1 and
> L2 ACs green. No L3–L6 behavior is required to ship.

## 8. Non-goals / carried residue

- **L3 deferred** — failure/recovery gates: needs new states + failure-injection mock not in code. See `development/deep-spec-dispatch/`.
- **L4 deferred** — identity/DNA + conformance-delta: types do not exist in code; `DiffSummary` is counts-only. See `development/deep-spec-dispatch/`.
- **L5 deferred** — fitness scoring + concurrency atomicity + bounded stores: net-new; gated by OQ-3. See `development/deep-spec-dispatch/`.
- **L6 deferred** — human-evidence / trust ergonomics: unproven, human-study-gated; gated by OQ-1/OQ-2. See `development/deep-spec-dispatch/`.
- **OQ-1** trust meter · **OQ-2** saw-the-diff proxy · **OQ-3** operator-handoff carry/reset · **OQ-4** import-integrity MVP boundary — all open; resolve via `decision-gate` before the layer they block. See `development/deep-spec-dispatch/RESULT.md`.
- **Contract drift — RESOLVED** `[PROPOSAL]` — the `RevisionApplied`/`RevisionRecorded` two-state split is now load-bearing (staged-preview vs committed); see §5. No longer pending reconciliation.
- **`GAP-ACCEPTANCE-CHECK-007`** `[PROPOSAL]` — intent-fidelity ceiling: admission ≠ `acceptanceText` satisfied. Quantitative criteria are judged only by the human eye at accept-diff; the pure lane never checks geometry/CSS layout. Accepted as a ceiling, priced into the determinism budget — not closed. See `development/refinement-runs/20260615-mutation-execution-mechanics/RESULT.md`.
- **C-1 spike (RESIDUE-B)** `[PROPOSAL]` — single gating action between "C designed" and "C trusted": build/stress-test the whole-tree od-id-attributed V3 fence, decide V2 (R2-a vs R2-b), and commit/report calibration constants `S`/`B`/`k`/`c` on real comment workloads before mutation-execution implementation. `GAP-R1` (external deterministic-validation pass) is the named fallback if it stalls.
- **Proposed-not-calibrated invariants** — the 8 residuality invariants (`Inv-1..8`) from the deep-spec are NOT part of this release's contract; they belong to L3–L5. See `development/deep-spec-dispatch/DEEP-SPEC-PROPOSAL.md`.
