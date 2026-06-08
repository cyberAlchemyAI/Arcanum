---
module: inventory-interface-link-index
version: current
status: draft
updatedAt: 2026-06-05
docType: architecture
owner: inventory
---

# Inventory Interface Architecture

## Purpose

Design the Inventory interface as a JSON + Markdown knowledge system that can be
called from any chat session, infer what should be inventorized, ask for
confirmation, then create or update a bounded inventory slice.

This architecture corrects the prior strategy focus. The priority is not
repository sweep research. The priority is an interface and indexing model that
makes inventorization ergonomic, traceable, and reusable.

## Product Contract

Calling `$inventory` with no explicit mode should start this flow:

```text
user intent
  -> target inference
  -> confirmation proposal
  -> inventory slice execution
  -> JSON indexes + Markdown records
  -> lookup-ready result
```

The user should not need to know internal modes like `install`, `ingest`,
`backfill`, or `sync`.

## Interface Modes

Keep the existing technical modes, but add an interface layer above them.

| Interface Mode | Trigger | Purpose | Internal Route |
| --- | --- | --- | --- |
| `auto` | `$inventory` or vague request | infer target and ask confirmation | target-resolution -> confirmation |
| `inventorize` | explicit source or scope | create/update a bounded slice | ingest/backfill |
| `lookup` | user asks for known context | retrieve records/cards/selectors | lookup/query |
| `status` | user asks what exists or what is missing | summarize indexes, gaps, stale cards | validate/lint |
| `continue` | user wants next inventory work | resume from tracker/backlog | task-session handoff |
| `explain` | user is lost | show package state and next action | index/status read |

The interface layer should be documented in `arcana/inventory/SKILL.md`, while
the implementation details can remain in package-local architecture docs.

## Auto Mode Flow

### 1. Intent Capture

Inputs:

- current user prompt,
- current working directory,
- mentioned paths,
- named skills/sigils/spells/projects,
- recent Inventory tracker or backlog if present.

Output:

```json
{
  "intent_id": "inv-intent-<timestamp>",
  "raw_prompt": "...",
  "inferred_action": "inventorize | lookup | status | explain | continue",
  "confidence": "high | medium | low",
  "reason": "Why this action was inferred.",
  "residue": []
}
```

### 2. Target Resolution

Resolve the smallest safe target.

Target types:

| Target Type | Example | Confirmation Needed |
| --- | --- | --- |
| explicit path | `cyberAlchemy/ontology/README.md` | yes |
| named zone | `whole domainspec-core` | yes, then narrow |
| named capability | `inventory skill` | yes |
| current conversation | "what we just discussed" | yes, source as session-derived synthesis |
| tracker/backlog item | next pilot slice | yes |
| lookup question | "what exists for X?" | no mutation; confirm only if filing synthesis |

Output:

```json
{
  "target_id": "sigils-library-arcanum-authority",
  "target_label": "Arcanum vs Sigils Library Authority",
  "target_type": "pilot-slice",
  "source_anchors": [
    "arcanum/README.md",
    "sigils-library/README.md"
  ],
  "excluded_sources": [
    ".arcanum/",
    ".codex/"
  ],
  "proposed_inventory_root": "arcana/inventory/development",
  "risk_tags": [
    "risk:authority-conflict"
  ],
  "confidence": "medium",
  "residue": [
    "Authority conflict must be recorded, not resolved."
  ]
}
```

### 3. Confirmation Proposal

The interface must show one concise confirmation before mutation:

```text
I inferred you want to inventorize:

Target: Arcanum vs Sigils Library Authority
Sources: arcanum/README.md, arcanum/registry/SIGILS.md, sigils-library/README.md
Output: arcana/inventory/development/pilot/interface-link-index/sigils-library-arcanum-authority/
Will create: cards.json, index.json, retrieval.json, COVERAGE.md
Will not do: decide canonical authority, edit source files, ingest whole repo

Confirm?
```

If confidence is low, ask a targeted clarification instead of offering a
mutation proposal.

### 4. Slice Execution

Execution writes:

```text
slices/<slice-id>/
  cards.json
  index.json
  retrieval.json
  COVERAGE.md
```

Then updates, if present:

```text
indexes/repository-index.json
indexes/zone-index.json
indexes/tag-index.json
indexes/surface-index.json
indexes/link-index.json
indexes/selector-index.json
log.md
```

## Interface Screens As CLI/Chat Views

The first interface does not need a web UI. It needs stable views that can be
rendered in chat and later by a browser/HTML viewer.

| View | Purpose | Backing Files |
| --- | --- | --- |
| Inventory Home | show inventory root, status, next slice | `repository-index.json`, `log.md` |
| Target Proposal | show inferred target and confirmation | transient JSON + Markdown prompt |
| Slice Workspace | show source anchors, cards, coverage, gaps | `slices/<slice-id>/*` |
| Tag Browser | show tag families and counts | `tag-index.json` |
| Link Browser | show source/card/record relationships | `link-index.json` |
| Lookup Result | show selected records, excluded records, gaps | `retrieval.json` or lookup output |
| Gap/Risk Queue | show unresolved residue and blockers | `COVERAGE.md`, `lint/latest.md` |

## Data Ownership

Use JSON for machine-stable indexes and Markdown for human-readable surfaces.

| Data | Format | Owner | Rule |
| --- | --- | --- | --- |
| source files | existing repo files | source owner | read-only |
| evidence cards | JSON | Inventory | source-backed records |
| indexes | JSON | Inventory | deterministic lookup structures |
| coverage reports | Markdown | Inventory | human explanation and omissions |
| interface proposals | Markdown plus optional JSON | Inventory | confirmation before mutation |
| definitions | Markdown/source owner | Definitions Governance | Inventory may link only |
| ontology relations | Markdown/JSON/source owner | Ontology Vault | Inventory may hand off only |

## Minimum Viable Interface

Build this first:

1. `$inventory` defaults to `auto`.
2. Auto mode emits a target confirmation proposal.
3. Confirmed run creates one slice folder.
4. Slice contains `cards.json`, `index.json`, `retrieval.json`, and `COVERAGE.md`.
5. `status` reads indexes and tells the user what exists, what is missing, and
   what the next safe slice is.

Do not build a complex UI before this works in chat.

## Required Skill Contract Changes

Update `arcana/inventory/SKILL.md` to add:

- default/no-mode behavior,
- target inference process,
- confirmation proposal process,
- interface modes,
- linking/indexing discipline,
- JSON/Markdown storage rule,
- status/explain behavior.

## Stop Conditions

Block or ask when:

- target confidence is low,
- source scope is broad enough to become a repository dump,
- the user asks for authority promotion instead of inventory evidence,
- the slice would write inside a submodule,
- tag or link vocabulary would become canonical definitions,
- source anchors cannot be resolved to existing paths or durable session
  evidence.

## Architecture Decision

Recommended decision:

```text
Use chat-first Inventory interface with JSON indexes and Markdown records.
Defer database, full web UI, and vector index until slice/card/query behavior is proven.
```

Rationale:

- JSON + Markdown matches existing Inventory contracts.
- It is git-friendly and reviewable.
- It supports shell/JQ validation.
- It keeps raw source authority visible.
- It can later project into SQLite, HTML, or vector search without changing the
  source-of-truth package.
