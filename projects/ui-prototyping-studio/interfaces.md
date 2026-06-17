---
id: ui-prototyping-studio-interfaces
project: ui-prototyping-studio
title: "UI Prototyping Studio — Interfaces (the `studio` CLI contract + internal boundaries)"
status: draft
node_type: interfaces
updatedAt: 2026-06-15
---

# UI Prototyping Studio — Interfaces

> The **primary interface is the `studio` CLI** — Claude Code-native (operated in VSCode),
> **no MCP server, no `@anthropic-ai/sdk`, no API key** (SPEC §2 interaction model). The CLI is the
> single operation surface for **both** Claude Code and the human; it wraps the shared **orchestration
> module**. Governance gates (INV-3/4/5/8) are enforced **server-side behind the CLI**, not in CLI args.

## 1. `studio` CLI command contract

Conventions: `<sid>` = session id. Every command prints a JSON result to **stdout** and a non-zero
exit on error; the error JSON is `{ code, message, details }` (the orchestration error shape, §3).
Exit map mirrors the HTTP status map (`errorStatusCode`): `2` = client/validation (401/403/404/409/422),
`1` = unexpected (500). Each gate is enforced in the orchestration module; a CLI flag can never bypass it.

| Command | Signature / flags | Does | Operation | Output (stdout JSON) | Errors / exit | Gate (INV) |
|---|---|---|---|---|---|---|
| `session open` | `--variants 1..3` (default 3) `--mode explore\|exploit` `[--by <user>]` | Create a session; validate/default `variantCount`; `count=1` ⇒ baseline `committed`, selection gate pre-satisfied. | `initializeSession` | `{ session }` (state `SessionInitialized`) | `VARIANT_COUNT_OUT_OF_RANGE` (2) | INV-1, INV-2 |
| `prompt submit <sid> <text>` | positional `<text>` | Store the non-empty, sanitized prompt. | `submitPrompt` | `{ session }` (`PromptCaptured`) | `PROMPT_REQUIRED`/`PROMPT_NOT_SET` (2) | INV-7 |
| `variants register <sid>` | `--from <dir>` (Claude Code HTML) \| `--fake` (deterministic fixture) | Register **exactly** `variantCount` HTML-first variants (`htmlArtifactRef`, `rationale`, `tradeoffs`, `risk`). The **only** generation seam. Changes no gate; fake↔Claude Code is contract-invariant. | `generateVariants` | `{ session, variants[] }` (`VariantsReady`) | `VARIANT_GENERATION_COUNT_MISMATCH` (1) | INV-1 (count) |
| `state <sid>` | — | Read-only snapshot for **agent + human**: session + current `StudioSessionState`, gates, baseline, revision head. | `getSessionSnapshot` (+ `listSessionVariants`) | `{ session, variants[] }` | `SESSION_NOT_FOUND` (2) | (read) |
| `baseline select <sid> <label>` | positional `<label>` | Select baseline when `variantCount>1`; record `BaselineProvenance(mode=selected)` + anchor + family. | `selectOrCommitBaseline` | `{ session, variants[] }` (`BaselineReady`) | `BASELINE_LABEL_INVALID` (2), `BASELINE_SELECTION_REQUIRED` (2) | INV-2 |
| `baseline commit <sid>` | — | Commit the single option (`variantCount=1`); `BaselineProvenance(mode=committed)`, selection gate satisfied without further input. | `selectOrCommitBaseline` (no label) | `{ session, variants[] }` (`BaselineReady`) | `BASELINE_GATE_UNSATISFIED` (2) | INV-2 |
| `comment add <sid>` | `--target <selector>` `--severity blocker\|high\|medium\|low` `--intent <text>` `--note <text>` `[--element-label]` `[--od-id]` `[--revision <id>]` | Append one canonical element-level `CommentEvent`; all of `{target, severity, intent, note}` required; note sanitized. | `captureCommentEvent` | `{ comment }` (`CommentsCaptured`, self-loops) | `COMMENT_SCHEMA_INVALID` (2), `SOURCE_REVISION_INVALID` (2) | INV-7 |
| `synthesize <sid>` | `[--source-revision <id>]` | Deterministically fold comments into a **draft** `MutationBatch` (`status=draft`); identical ordered comments ⇒ identical task IDs + checksum. | `synthesizeMutationBatch` | `{ session, batch }` (`MutationDrafted`) | `COMMENT_SET_EMPTY` (2), `SOURCE_REVISION_INVALID` (2) | (deterministic fold) |
| `batch approve <sid> <batchId>` | `--by <user>` `[--at <iso>]` | **Human-only.** Explicit approval `draft → approved`; sets approval metadata; satisfies apply gate. | `approveMutationBatch` | `{ session, batch }` (`MutationApproved`) | `BATCH_NOT_DRAFT` (2), `APPROVAL_METADATA_REQUIRED` (2), `BATCH_NOT_FOUND` (2) | **INV-3** |
| `apply <sid> <batchId>` `[PROPOSAL]` | `[--by <user>]` `[--max-propose-attempts <n>]` | **Human-only. First gate (approve-intent already passed).** Two-step, does **NOT** advance head: **propose** (Claude Code, impure) → **validate** (pure V1–V9b composite, fail-closed reject ⇒ no write, stays `MutationApproved`, bounded retry) → **stage** the candidate at a temp ref (`candidateHtmlHash` + `provenance`) and show the **honest diff** (`DiffSummaryHonest`). | `applyApprovedBatch` (propose+validate+stage) | `{ session, batch, candidate, diff }` (state `RevisionApplied`) | `BATCH_APPROVAL_REQUIRED` (2), `AUTO_APPLY_FORBIDDEN` (2), `APPROVAL_STALE`/`BATCH_STALE_FOR_HEAD` (2), `PROPOSE_RETRIES_EXHAUSTED` (1) | **INV-3/4/5/6/8** |
| `accept <sid> <batchId>` `[PROPOSAL]` | `[--by <user>]` | **Human-only. Second gate (accept-diff).** Commit **exactly** the staged `candidateHtmlHash` the human previewed (idempotency-at-verdict, seen == recorded), atomically all-or-nothing; append exactly one `RevisionManifestEntry`; **advance head**. | `acceptStagedRevision` `[PROPOSAL]` | `{ session, batch, revision }` (`RevisionRecorded`) | `NO_STAGED_CANDIDATE` (2), `CANDIDATE_HASH_MISMATCH` (2), `BATCH_STALE_FOR_HEAD` (2) | **INV-3/4/5/6/8** |
| `discard <sid> <batchId>` `[PROPOSAL]` | `[--by <user>]` | **Human-only. Reject the accept-diff gate.** Drop the staged candidate; stays `MutationApproved` (re-`apply` allowed). | `discardStagedRevision` `[PROPOSAL]` | `{ session, batch }` (`MutationApproved`) | `NO_STAGED_CANDIDATE` (2) | **INV-3** |
| `revisions <sid>` | `[--limit <n>]` `[--newest-first]` | List the append-only revision manifest (Revision Timeline). | `listRevisionManifest` | `{ entries[] }` | `SESSION_NOT_FOUND` (2) | INV-6 (read) |
| `handoff export <sid>` | `[--profile <name>]` `[--by <user>]` | Build the downstream-ready handoff bundle (story/requirement/acceptance/uiSpec/testSpec refs). | `exportDesignHandoff` | `{ session, bundle }` (`SessionCompleted`) | `HANDOFF_REVISION_REQUIRED` (2), `HANDOFF_REFERENCE_INCOMPLETE` (2), `HANDOFF_BUNDLE_NOT_READY` (2) | (terminal) |
| `preview <sid> [label\|revision] [--annotate]` | optional positional selector; `--annotate` | Serve the variant/revision HTML from an **ephemeral local server** and open it in the browser. With `--annotate` (default when a baseline exists), inject a **click-to-annotate overlay**: clicking a rendered element captures a robust selector + label and POSTs a `{severity,intent,note}` comment back to the local server, which calls `CaptureCommentEvent`. Read-only on variants; the overlay path is the only mutation (a gated `CommentEvent`, INV-2). | `getSessionSnapshot`/`listRevisionManifest` (read); `captureCommentEvent` (overlay) | `{ resolvedRef, openedUrl, annotate }` | `SESSION_NOT_FOUND` (2), `ANNOTATION_GATE_LOCKED` | (read + gated comment) |

> **Apply-gate note:** `apply`/`accept` refuse non-approved (INV-3), `applyRequestedBy='system:auto'`
> (INV-4), and stale (INV-5) applies **server-side regardless of CLI flags** (AC-L0-10). The CLI passes
> the real actor; it cannot assert `system:auto` to skip a gate, and cannot force-approve via a flag.
> `[PROPOSAL]` **Two-gate split (D7/D8):** `apply` runs propose→validate→stage and shows the diff but
> **never advances head**; `accept` is the second human gate that commits exactly the staged
> `candidateHtmlHash` (D13), `discard` drops it. The single old `applyApprovedBatch` is split so the
> saw-the-diff moment (`RevisionApplied`) is real, not a passthrough to `RevisionRecorded`.

## 2. REST → CLI mapping (the 14 existing endpoints)

The orchestration module is **shared**; the REST layer (`http-routes.ts`) and the CLI are two adapters
over the same operations. **Open choice:** the REST layer MAY be retained (web-UI / CI) or dropped once
the CLI is the sole driver — not decided here.

| # | REST endpoint (`http-routes.ts`) | Operation | `studio` CLI command |
|---|---|---|---|
| 1 | `POST /sessions` | `initializeSession` | `session open --variants --mode` |
| 2 | `POST /sessions/:sid/prompt` | `submitPrompt` | `prompt submit <sid> <text>` |
| 3 | `POST /sessions/:sid/variants/generate` | `generateVariants` | `variants register <sid> --from\|--fake` |
| 4 | `POST /sessions/:sid/baseline` | `selectOrCommitBaseline` | `baseline select <sid> <label>` / `baseline commit <sid>` |
| 5 | `POST /sessions/:sid/comments` | `captureCommentEvent` | `comment add <sid> --target --severity --intent --note` |
| 6 | `POST /sessions/:sid/mutation-batches/synthesize` | `synthesizeMutationBatch` | `synthesize <sid>` |
| 7 | `POST /sessions/:sid/mutation-batches/:batchId/approve` | `approveMutationBatch` | `batch approve <sid> <batchId> --by` |
| 8 | `POST /sessions/:sid/mutation-batches/:batchId/apply` | `applyApprovedBatch` (propose+validate+stage) `[PROPOSAL]` | `apply <sid> <batchId>` |
| 8b | `POST /sessions/:sid/mutation-batches/:batchId/accept` `[PROPOSAL]` | `acceptStagedRevision` `[PROPOSAL]` | `accept <sid> <batchId>` |
| 8c | `DELETE /sessions/:sid/mutation-batches/:batchId/staged-candidate` `[PROPOSAL]` | `discardStagedRevision` `[PROPOSAL]` | `discard <sid> <batchId>` |
| 9 | `POST /sessions/:sid/handoff/export` | `exportDesignHandoff` | `handoff export <sid>` |
| 10 | `GET /sessions/:sid` | `getSessionSnapshot` | `state <sid>` |
| 11 | `GET /sessions/:sid/variants` | `listSessionVariants` | `state <sid>` (folded into snapshot) / `preview` |
| 12 | `GET /sessions/:sid/mutation-batches/draft` | `getDraftMutationBatch` | `state <sid>` (draft surfaced in snapshot) |
| 13 | `GET /sessions/:sid/revisions` | `listRevisionManifest` | `revisions <sid>` |
| 14 | `GET /sessions/:sid/handoff` | `getHandoffBundle` | `handoff export <sid>` (idempotent read after build) |

> REST auth (`x-scopes` read/write) has no CLI analogue — the CLI runs in the operator's local trust
> boundary; the scope check is a REST-adapter concern, not a core gate.

## 3. Internal boundaries

```
Claude Code / human ── studio CLI (adapter) ──┐
                                              ├─► orchestration module ──► StudioSessionStorePort ──► .data/*.json
web UI / CI ───────── REST routes (adapter) ──┘   (gates INV-3/4/5/6/8       (file-backed store)
                                                    enforced HERE)
```

- **Orchestration module** (`application/studio-orchestration-module.ts`) — the single source of behavior:
  the 10-state `StudioSessionState` machine, deterministic synthesis fold, and **all gate enforcement**.
  Gates (approval-before-apply, auto-apply-forbidden, stale-check, server-side enforcement, one-manifest-
  per-apply) live **here, behind the CLI** — never in CLI argument parsing (INV-8). A CLI flag is input,
  not authority.
- **`StudioSessionStorePort`** (`application/ports.ts`) — the persistence boundary the orchestration module
  depends on: id allocation (`allocateSessionId/CommentId/BatchId/RevisionId`), session/variant/comment/
  batch/revision/handoff read+write, append-only comment & revision appends. **File-backed** implementation
  (`infrastructure/file-studio-session-store.ts`) persists under **`.data/`** (default
  `.data/ui-prototyping-studio-session-store.json`); `createInMemoryStudioSessionStore` backs e2e/tests.
  The CLI selects file-backed by default; the port keeps storage swappable without touching gates.
- **Artifact content port** `[PROPOSAL]` (the design needs it; **currently MISSING**) — `StudioSessionStorePort`
  has **zero HTML read/write methods today**, so `htmlArtifactRef` is a dangling path never written or read;
  this is the unbuildable assumption the design closes in **Layer 0**. The mutation lanes require five
  methods on the store port: `readHtml` (load current HTML for the proposer/validators), `stageHtml`
  (persist the candidate at a temp ref — the `RevisionApplied` preview), `commitHtml` (atomically promote the
  staged candidate and advance head — the `accept` gate), `discardStagedHtml` (drop the staged candidate —
  the `discard` gate), and `removeRevision` (compensating rollback for `VARIANT_GENERATION_COUNT_MISMATCH`,
  Layer 3 RESIDUE-A — atomic compensation is not even *expressible* against the current port).
- **Engine (proposer) contract at the seam** `[PROPOSAL]` — the load-bearing boundary between the impure
  proposer (Claude Code) and the pure core is **value-in / value-out (D15)**: a frozen `ProposeInput`
  envelope in → `ProposeOutput` (candidate HTML + `ExecutionProvenance`) out. Claude Code is **forbidden the
  store/clock/append path** — it returns a value; the pure validator suite admits it and the pure-effectful
  recorder records it. The proposer never touches persistence, never advances head, never sees the clock.

## 4. Operating skill seam

Claude Code operates **only the reversible, generative half** of the loop through the CLI: it reads
`studio state <sid>` for the current state and gates, **generates the 1–3 HTML variants**, registers them
with `studio variants register --from <dir>`, and may run `synthesize` to produce the draft batch — then
hands the irreversible **disposition** gates to the human. Claude Code **never** runs `batch approve`,
`apply`, or `accept` (human-only, INV-3/INV-4); those refuse a non-human/`system:auto` actor server-side
even if invoked. `[PROPOSAL]` Within `apply`, Claude Code acts only as the **proposer engine** (value-in/
value-out, §3) — it returns candidate HTML, it does not stage, accept, or advance head. Agent proposes
(generate / register / synthesize / propose), human disposes (select / approve / apply / accept); the
operating `SKILL.md` teaches exactly this discipline.

## 5. Deferred surfaces (future options behind the same core)

An **MCP adapter** and a **standalone Anthropic-SDK / REST** surface are both **future options** sitting
behind the same orchestration core — not built here. They reuse the identical operations and the same
server-side gates; only the transport changes. Design/scope lives in `development/` (MCP +
`standalone-extraction/`); see also `development/deep-spec-dispatch/` for the L3–L6 deferrals.
