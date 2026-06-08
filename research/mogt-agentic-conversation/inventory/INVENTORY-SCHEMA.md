# MOGT Inventory Schema

Purpose: define the inventory chain for MOGT so source discovery, authority selection, extracted knowledge, and raw provenance stay connected.

## Required Chain

1. `sources/SOURCE-CATALOG.md`
2. `sources/REFERENCE-LEDGER.md`
3. `inventory/INVENTORY-INDEX.md`
4. `inventory/library/<source-id>.md`
5. `inventory/raw/<source-id>/...`

## Directory Layout

| Path                                          | Role                                                |
| --------------------------------------------- | --------------------------------------------------- |
| `inventory/INVENTORY-INDEX.md`                | lookup and coverage view                            |
| `inventory/INVENTORY-SCHEMA.md`               | local inventory contract                            |
| `inventory/library/<source-id>.md`            | per-source extracted knowledge artifact             |
| `inventory/raw/<source-id>/...`               | raw retrieved or user-provided provenance artifacts |
| `inventory/agentic-conversation-prior-art.md` | secondary thematic rollup                           |
| `inventory/methodology-authorities.md`        | secondary thematic rollup                           |
| `inventory/theory-baseline.md`                | secondary thematic rollup                           |

## Status Model

| Status          | Meaning                                                                                       |
| --------------- | --------------------------------------------------------------------------------------------- |
| `library-grade` | source has a library entry and raw provenance backing                                         |
| `partial`       | source has some inventory treatment but provenance or coverage is incomplete                  |
| `awaiting-raw`  | source needs user-provided raw files or later retrieval before a library entry can be trusted |

## Rules

1. The per-source library file is the content authority for extracted source knowledge.
2. The rollup files are convenience views; they are not substitutes for per-source entries.
3. If source content can be retrieved from the web, store a provenance-backed raw note under `inventory/raw/<source-id>/`.
4. If source content cannot be retrieved from the web or is paywalled, request user-provided raw files and track that dependency explicitly.
5. Every claim about source content in a library file should point to a raw path, a direct source location, or an unresolved-anchor note.

## Current Scope

This first pass prioritizes the open-access agentic-conversation prior-art sources and selected open methodology authorities.

Paywalled books and unresolved theory sources remain in the chain as `awaiting-raw` until raw files are supplied or retrieval improves.
