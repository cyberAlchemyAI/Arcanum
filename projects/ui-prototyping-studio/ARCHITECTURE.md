---
id: ui-prototyping-studio-architecture
project: ui-prototyping-studio
title: "UI Prototyping Studio — Architecture Vision (Claude Code-native, CLI-operated)"
status: draft
node_type: architecture
updatedAt: 2026-06-15
---

# Architecture Vision

> Authored via `invoke design` from [SPEC.md](SPEC.md) + the aspect files. Lean, L0→L2, matching the
> spine altitude. Architecture decisions live in [.craft/ledger.yml](.craft/ledger.yml) (`DEC-*`); this
> document is the structure they imply, not a re-decision.

## 1. One sentence

**The studio is a governance harness around a single generation agent: Claude Code generates UI; a
`studio` CLI is the only seam; the orchestration core enforces the gates; the human disposes every
durable change.** The studio itself does *not* generate — it governs. Sharpened: the harness *admits at
a deterministic boundary* — generation is non-deterministic and expressive behind the seam, and
determinism is recovered in the pure core where the change is admitted (see §6a).

## 2. The shape

```
        ┌─────────────────────────── VSCode / Claude Code ───────────────────────────┐
        │  Human ──asks──▶ Claude Code ──generates HTML──▶ `studio variants register` │
        │    ▲                                                          │             │
        │    │ reviews (studio preview) + gates (CLI)                   ▼             │
        └────┼──────────────────────────────────────────────┐   ┌──────────────┐    │
             │                                               └──▶│  studio CLI  │    │
             │   operating SKILL.md teaches Claude Code           └──────┬───────┘    │
             └──────────────── the discipline ──────────────────────────┼────────────┘
                                                                         ▼
                                  ┌──────────────────── Orchestration Core ────────────────────┐
                                  │  application/ (use-cases + studio-orchestration-module)     │
                                  │  domain/ (StudioSession state machine, invariants INV-1..9, │
                                  │           deterministic synthesis)                          │
                                  │  ports: StudioSessionStorePort                              │
                                  └───────────────┬─────────────────────────────────────────────┘
                                                  ▼
                                  infrastructure/ file-backed session store (.data/)
```

There is **no MCP server, no web SPA, no API key, no in-process agent loop** in the MVP. Claude Code is
the engine; the CLI is the surface; the core is the governance.

## 3. Components & responsibilities

| Component | Responsibility | Boundary |
|---|---|---|
| **Claude Code** (in VSCode) | The generation/mutation engine: turns a prompt into 1–3 HTML variants; executes approved mutations. The *only* agentic actor. | External. Plugs in at the `variants register` / `batch apply` seams. Never approves/applies (skill-enforced + server-enforced). |
| **`studio` CLI** | The single operation surface for **both** Claude Code and the human (see [interfaces.md](interfaces.md)). Thin adapter over the orchestration module. | `interface/` layer. Holds no business rules. |
| **Operating skill** (`SKILL.md`) | Teaches Claude Code the `studio` discipline: generate → `variants register` → hand gates to the human. | Prompt-layer contract; carries no authority. |
| **Orchestration core** | The governance harness: the `StudioSession` state machine, invariants `INV-1..9`, deterministic comment→task synthesis, baseline/anchor logic. Owns *all* rule enforcement. | `application/` + `domain/`. Pure; no I/O. |
| **Session store** | Durable, file-backed session/variant/comment/batch/revision state. | `infrastructure/`, behind `StudioSessionStorePort`. `.data/`. |
| **`studio preview`** | Visual review: opens variant/revision HTML in a browser. The HTML *is* the output. | Read-only view; no gate authority. |

## 4. Layering & dependency rules (hexagonal — as it exists in code)

```
interface/  (studio CLI, [legacy] http-routes)   ── depends on ──▶ application/
application/ (use-cases, orchestration module, ports)             ── depends on ──▶ domain/
infrastructure/ (file store, newspaper adapter)  ── implements ──▶ application/ports
domain/      (models, state machine, invariants, errors)          ── depends on ──▶ nothing
```

- **Dependencies point inward.** `domain/` knows nothing of CLI, store, or Claude Code.
- **Gates live in the core, never in the adapter.** The CLI cannot bypass a gate with a flag; `batch apply` rejects non-approved / `system:auto` / stale server-side (INV-3/4/5/8).
- **Generation is external.** The core ingests *registered* variants; it does not own an LLM. This is what makes the runtime swappable.

## 5. The generator seam

The pivotal architectural choice: **generation is delegated, not embedded.**

- **Real adapter (MVP):** Claude Code produces HTML and calls `studio variants register --from <dir>`. The core validates count/shape and records `PrototypeVariant`s.
- **Test adapter:** `studio variants register --fake` (deterministic fixture) drives e2e — stable IDs, no model, no network.
- **One seam, many futures:** because the core only sees *registered variants*, alternative engines (an in-process Anthropic-SDK generator, an MCP tool, a different agent) are future adapters behind the same seam — none required now.

## 6. Data flow (the governed loop)

`session open` → `prompt submit` → **Claude Code generates** → `variants register` → `baseline select|commit`
→ `comment add` (human intent) → `synthesize` (**deterministic** fold, core-owned) → `batch approve` (human)
→ **Claude Code executes** the mutation → `batch apply` (core appends exactly one `RevisionManifestEntry`)
→ iterate or `handoff export`. Full transition contract in [states.md](states.md); semantics in [operations.md](operations.md).

**Agent proposes (generate, execute-mutation); human disposes (select, approve, apply); the core arbitrates (synthesis, invariants).**

## 6a. Mutation execution — the admission boundary

Refines §5 (the generator seam) and §7 (trust/governance) with the *apply path*. Ref `DEC-MUTATION-EXEC-015`
(Approach C: agentic-propose behind the seam, deterministic-validate in the pure core).

The apply path is **propose → validate → stage → accept → record**. The core *admits*; the engine only
*proposes* (value-in / value-out). Four lanes, with the load-bearing seam **between lane 2 and lanes 3–4**:

| Lane | Owner | Purity | Responsibility |
|---|---|---|---|
| 1. Synthesis | core | pure | comments → `MutationBatch` (checksummed) |
| 2. Proposer (engine) | Claude Code | **impure (LLM)** | `propose(currentHtml, tasks, context) → candidateHtml + provenance`, behind the `studio` CLI seam |
| 3. Validator suite | core | **pure, clock-free** | `validate(...) → AdmissionVerdict` (V1–V9b) |
| 4. Recorder | core | pure-effectful | admit ⇒ persist HTML + append exactly one revision + advance; reject ⇒ persist nothing |

**Architectural principle:** generation is non-deterministic and expressive *behind the seam*;
**determinism is recovered at the admission boundary in the pure core.** Three commitments make it
enforceable: validator purity (no clock/random/IO; structural checks run over a canonical parse),
**one shared canonicalizer used on both sides of the seam**, and **replay-by-verdict, not
replay-by-production** — the *decision to admit* is replayable, the *proposal* is not.

**A and B are reachable as config**, not redesign — the same machine, different lane behavior (C→A when the
workload is enumerable; C→B when the validator cannot be made deterministic), consistent with the
generator-port framing of §5.

### Contract deltas `[PROPOSAL]`

Each is a named extension point; nothing here is canonical until operator-approved.

- `[PROPOSAL]` **Artifact content port (Layer 0 — the currently-missing substrate).** `StudioSessionStorePort`
  has no HTML read/write methods; `htmlArtifactRef` is a dangling path. Add `readHtml / stageHtml /
  commitHtml / discardStagedHtml` (and `removeRevision` for atomic compensation). Until this lands, lanes
  3/4 have no input and the recorder has nothing to commit.
- `[PROPOSAL]` **Schema (`domain/models.ts`).** Add `odId` + `MutationChangeType` union to `MutationTask`
  (batch `sha256` re-baselined); delete `buildDiffSummary`, replace with `DiffSummaryHonest` /
  per-od-id `OdDiffFragment` (counts derived from `odIndex` set-diff); add `htmlArtifactRef`,
  `candidateHtmlHash`, and `ExecutionProvenance` to `RevisionManifestEntry`.
- `[PROPOSAL]` **Apply state machine.** Two gates (approve-intent + accept-diff) via the activated dormant
  `RevisionApplied` preview state; fail-closed reject + bounded retry; whole-batch all-or-nothing record;
  idempotency-at-verdict (the human accepts a specific `candidateHtmlHash`; record commits exactly that hash,
  so seen == recorded).

## 6b. Operating-model update — reversibility + two modes (DEC-026 / DEC-027)

> Current model; supersedes "human disposes every durable change" (§1, §6) where they conflict.

- **Reversibility, not gating (DEC-026).** The append-only revision log + content-addressed HTML make every
  durable action undoable (`revert` appends an inverse revision — head moves forward, content goes back, never
  a destructive rewind). So the agent may drive the whole loop, including `accept`. The **one irreversible
  edge is `handoff export`** (downstream consumption), guarded by an explicit human `--confirm`. The
  human-vs-agent identity gate is **dropped, not built**.
- **Two modes (DEC-027).** HUMAN-in-the-loop (human selects/accepts) and AUTO exploit/explore `cycle`
  (agent generates + self-critique-scores; the core gates via the scope fence and auto-accepts the top score).
  New core use-cases: `run-cycle`, `revert-revision`, `list-pending-comments`; new CLI/preview surface:
  `cycle · watch · pending · revert · preview (+ annotate /comment, /state) · handoff export --confirm`.
- **Admission boundary unchanged.** AUTO still passes the same pure scope fence (§6a); exploit refines within
  head od-ids, explore may diverge with integrity. Determinism-at-admission + replay-by-verdict still hold.

## 6c. Known architecture gaps — gap-audit 2026-06-18

- **F1 (HIGH) — the export gate is in the wrong layer.** The `--confirm` edge is enforced only in the CLI
  adapter; the mounted Fastify route `POST /…/handoff/export` (`interface/http-routes.ts`) calls
  `exportDesignHandoff` with no confirm, on `0.0.0.0:8787` (`src/index.ts`). This **violates §4's "gates live
  in the core, never in the adapter."** Fix: move the confirm requirement into the `exportDesignHandoff`
  use-case so every adapter inherits it. (Tracked in `development/PLAN-NEXT.md`.)
- **F7 (MED) — the legacy HTTP surface is ungated + untested.** Decide: bring it to CLI parity (gates + tests)
  or remove the bootstrap, since §1 names the CLI as the surface.
- **F2 (MED) — `cycle` carries no `system:auto` guard.** Sanctioned under DEC-026 (reversibility is the
  control); a literal-`system:auto` smoke-guard is queued for parity with the apply path.

## 7. Trust & governance architecture

Governance is the product, not a constraint bolted on:
- **Server-side gates.** Selection, approval, staleness, and non-auto-actor checks are enforced in the orchestration core (INV-3/4/5/8) — the CLI and Claude Code are untrusted callers.
- **Determinism where intent is sacred.** Comment→task synthesis is deterministic (sha1 task IDs, no timestamps), so the agent can never reinterpret the human's comments. The *apply* path extends this with the **admission boundary** (§6a): the impure proposer is gated by a pure, clock-free validator suite, so a non-deterministic generation becomes head only by passing a replayable verdict.
- **Append-only lineage.** Exactly one `RevisionManifestEntry` per apply; revision head is the staleness oracle.
- **Ergonomics-first.** The agent earns its keep on reversible work (generation); the human spends attention only at the named irreversible checkpoints.

## 8. Runtime & deployment

- **Claude Code-native, local.** Runs inside VSCode with Claude Code. No service to deploy, no key to manage, no agent loop to operate.
- **State:** file-backed under `.data/` (gitignored). Single-user, local-first.
- **Packaging:** the orchestration core + CLI ship as one backend package (`tsx`/`tsc`, fastify only if the legacy REST surface is retained); the operating skill ships as `SKILL.md`.

## 9. Extension points (deferred, each behind a named seam)

| Future | Seam it plugs into | Tracked as |
|---|---|---|
| Standalone product (own the model) | Anthropic-SDK adapter behind the generator seam | `DEC-CLI-NOT-MCP-012` note |
| Multi-client / typed tools | MCP adapter behind the same core | `DEC-RUNTIME-CLAUDE-CODE-011` note |
| Click-to-annotate web view | UI over `comment add` | `GAP-ANNOTATION-UX-006` |
| Identity/DNA + conformance-delta | new domain types + `IdentityEvidence` surface | L4 (`BLK-IDENTITY-TYPES-002`) |
| Failure/recovery states | new states + store failure-injection | L3 (`BLK-FAILURE-STATES-003`) |

## 10. Architecture decisions (pointers, not re-decisions)

`DEC-FRESH-MINIMAL-008` (lean spine, archive the rest) · `DEC-INTERFACE-MODEL-009` (human workbench +
embedded assistant) · `DEC-GENERATOR-PORT-010` (generation is a seam, not embedded) ·
`DEC-RUNTIME-CLAUDE-CODE-011` (Claude Code-native) · `DEC-CLI-NOT-MCP-012` (CLI, not MCP) ·
`DEC-MUTATION-EXEC-015` (mutation execution: agentic-propose / deterministic-admit — see §6a). Full text and
rationale in [.craft/ledger.yml](.craft/ledger.yml); human view in [CRAFT.md](CRAFT.md).
