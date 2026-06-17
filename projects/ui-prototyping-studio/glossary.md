---
id: ui-prototyping-studio-glossary
project: ui-prototyping-studio
title: "UI Prototyping Studio — Lean Glossary (L0→L2 scope)"
status: draft
node_type: glossary
updatedAt: 2026-06-15
---

# UI Prototyping Studio — Lean Glossary

> Lean companion to the lean [SPEC.md](SPEC.md). Defines only the terms used by the buildable
> L0→L2, Claude Code-native, `studio`-CLI design. SPEC.md is the source of truth for canonical
> names and the contract; this glossary teaches the words. Anything past L2 is marked
> **(deferred L3+)** and is named, not defined here. Full vision: `provenance/legacy-domainspec-spec/`.

## 1. Domain types (SPEC §4)

These are the only domainspec UI types that back the L0 loop in code.

| Term | Kind | Definition |
|---|---|---|
| `StudioSession` | Entity | Session root that persists `variantCount`, baseline provenance, revision head, gate state, and current `StudioSessionState`. |
| `PrototypeVariant` | Entity | One generated HTML-first candidate in the current cycle, with label, artifact ref, rationale, tradeoffs, and risk. |
| `CommentEvent` | Entity | One canonical element-level comment on the active baseline; the append-only durable source for synthesis. |
| `MutationBatch` | Entity | Deterministic draft change set folded from comments; starts `draft`, requires explicit approval before apply. |
| `MutationTask` | Value Object | One deterministic change task (target, intent, change type) folded from comments into a `MutationBatch`. |
| `RevisionManifestEntry` | Entity | Exactly one append-only record written per successful apply; carries provenance, batch link, and diff summary. |
| `BaselineGenealogyFamily` | Entity | Durable family record created when one baseline survives the generated population; anchors later mutation ancestry. |
| `BaselineProvenance` | Value Object | The intentional-baseline record: `mode ∈ {selected, committed}` plus the variant it points at. |
| `BaselineRevisionAnchor` | Value Object | Explicit anchor set at baseline resolution; the staleness oracle the apply gate checks against. |
| `AnnotationTarget` | Value Object | Stable element reference (selector + label) that a `CommentEvent` points at. |
| `DiffSummary` | Value Object | Apply diff; at L0 a bare `{added, changed, removed}` count summary (signed field deltas are **(deferred L3+)**). |
| `TypedReference` | Value Object | Wire-level reference for domain / artifact / handoff links. |
| `VariantCount` | Value Object | Bounded selector constrained to `{1, 2, 3}`; session default `3`. |
| `GenerationMode` | Value Object | `explore` (new directions) or `exploit` (baseline-conforming; requires an existing baseline). |
| `CommentSeverity` | Enum | Annotation priority scale: `blocker / high / medium / low`. |
| `MutationBatchStatus` | Enum | Batch lifecycle at L0: `draft / approved` (apply forbidden until `approved`). |
| `GateState` | Enum | Selection/apply gate state: `satisfied` or blocked. |
| `StudioSessionState` | State Machine | The 10-state deterministic loop, from `SessionInitialized` through `RevisionRecorded` (SPEC §5). |

## 2. CLI verbs (`studio` command surface)

The single operation surface for both Claude Code and the human; gates are enforced behind the CLI.

| Command | Definition |
|---|---|
| `studio session open` | Create a new session with a bounded `variantCount`; gates start pending. |
| `studio prompt submit` | Capture the non-empty prompt text for the session. |
| `studio variants register` | Register exactly `variantCount` Claude-Code-generated HTML-first variants (the generator seam). |
| `studio state` | Print the current session state, gate states, baseline provenance, and revision head. |
| `studio baseline select` | Human chooses the baseline from multiple variants (`variantCount > 1`). |
| `studio baseline commit` | Single-variant path (`variantCount = 1`): the only option becomes the committed baseline. |
| `studio comment add` | Append one canonical element-level `CommentEvent` to the active baseline. |
| `studio synthesize` | Deterministically fold ordered comments into a draft `MutationBatch`. |
| `studio batch approve` | Explicit human approval transitioning the batch `draft → approved` (satisfies the apply gate). |
| `studio batch apply` | Apply an approved, non-stale, non-auto batch; appends exactly one `RevisionManifestEntry`. |
| `studio revisions` | List the append-only revision manifest for the session. |
| `studio handoff export` | Publish downstream-ready links and evidence for UI / test / implementation stages. |
| `studio preview` | Open the variant/revision HTML in a browser; the HTML *is* the visual output. |

## 3. Governance & runtime terms

| Term | Definition |
|---|---|
| Governance gate | A checkpoint that blocks the loop until required human or rule conditions are met; enforced server-side, not in any UI. |
| Baseline selection gate | The gate requiring a resolved baseline (`select` or `commit`) before any comment, synthesis, or apply (INV-2). |
| Apply gate | The gate that admits `batch apply` only for an `approved`, non-stale, non-auto batch (INV-3/4/5/8). |
| Auto-apply (forbidden) | Applying without explicit human action; `applyRequestedBy = 'system:auto'` is always rejected (INV-4). |
| Deterministic synthesis | Folding identical ordered comments always yields identical task IDs and payloads, so the agent can never reinterpret intent (AC-L0-4). |
| Stale check | Rejection of an apply when the batch is stale relative to the current revision head / `BaselineRevisionAnchor` (INV-5). |
| Generator seam | The boundary where generated HTML enters the system — the CLI (`studio variants register`); a deterministic `--fake` fixture drives e2e. |
| Operating skill | The `SKILL.md` that teaches Claude Code the `studio` commands and discipline: generate, register, never self-approve/apply. |
| Claude Code-native | The runtime model: the embedded assistant *is* Claude Code — no separate LLM integration, API key, agent loop, or MCP server. |
| Human disposes / agent proposes | The governing principle: the agent proposes reversible work (generate, mutate); the human disposes every durable change (select, approve, apply). |

## 4. Mutation execution mechanics (refine-run `20260615-mutation-execution-mechanics`, Approach C)

The propose-validate-record model that turns an approved batch into head. Source: `development/refinement-runs/20260615-mutation-execution-mechanics/RESULT.md`.

### The seam and its lanes

| Term | Definition |
|---|---|
| Admission boundary | Where determinism is recovered — the pure validator/recorder lane — not the producer. |
| Proposer / engine | Claude Code (impure) behind the `studio` CLI seam: `propose(currentHtml, tasks, context) → candidateHtml + provenance`. |
| Validator suite (V1–V9b) | Pure, clock-free admission checks run in fixed order; composite fail-closed. |
| Shared canonicalizer | One module (Dom/odIndex/version) used on both sides of the seam, killing accidental non-determinism. |

### Contract types (schema / behavior changes)

| Term | Definition |
|---|---|
| `AdmissionVerdict` | The `admit | reject` result of the validator suite. |
| `DiffSummaryHonest` / `OdDiffFragment` | Per-od-id diff derived from real before/after, replacing the counts-only `DiffSummary`. **[PROPOSAL]** |
| `ExecutionProvenance` | Record of how `candidateHtml` was produced (model, `promptHash`, hashes) plus the replayable verdict. **[PROPOSAL]** |
| `candidateHtmlHash` | Hash of the staged candidate the human accepts; record commits exactly it (`seen == recorded`). |
| `MutationChangeType` | The `add | remove | change` union replacing the bare `changeType` string. **[PROPOSAL]** |
| `odId` on `MutationTask` | Stable component id threaded from the comment target. **[PROPOSAL]** |
| Artifact content port | `readHtml/stageHtml/commitHtml/discardStagedHtml/removeRevision` — currently missing. **[PROPOSAL]** |

### Apply state machine

| Term | Definition |
|---|---|
| `RevisionApplied` (staged preview) | Candidate staged at a temp ref with the honest diff shown — the saw-the-diff moment, not head. |
| accept-diff gate | The human's second gate; commits the previewed candidate. |
| two-gate apply | Approve-intent then accept-diff. |
| replay-by-verdict | The admit decision is replayable; the proposal is not. |

## Deferred families (named, not defined here)

The following legacy domain families are **(deferred L3+)** — they exist as names but carry no
working code in this release. See `development/deep-spec-dispatch/`.

- **Identity / visual DNA** (L4) — `UIElementIdentity`, `UIVisualSignature`, `previewRef`, signed `DiffSummary.fieldDeltas`. **(deferred L3+)**
- **Fitness scoring** (L5) — `FitnessSignal`, `FitnessVector`, genome/evolution-cycle modeling. **(deferred L3+)**
- **Proof gate** (L5/L6) — `ProofObligation`, `EvaluateProofGate`, self-improvement promotion; normal MVP apply MUST NOT depend on it (INV-9). **(deferred L3+)**

## Maintenance rules

- Derive every term from [SPEC.md](SPEC.md) (§4 domain model, §2 CLI surface, §5 invariants). Do not introduce new canonical behavior here.
- Keep each definition to one declarative sentence; update SPEC.md first, then this glossary.
- Mark any term escaping L0→L2 scope as **(deferred L3+)** rather than defining it.
