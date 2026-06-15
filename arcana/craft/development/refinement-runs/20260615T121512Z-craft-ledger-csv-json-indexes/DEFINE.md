# Define: Craft Ledger CSV And JSON Projections

## Problem

Craft ledgers are YAML-first, which is good for authority and review, but
expensive for repeated agent reads and awkward for bulk human edits. Existing
embedded indexes help navigation, but positional pointers can drift when rows
move.

## Definition

Add a generated projection layer:

- `.craft/index.json` is the fast machine lookup and freshness manifest.
- `.craft/projections/*.csv` are flat review/import staging files.
- `.craft/ledger.yml` remains the only source of truth.

## Done Criteria

- The projection contract names authority, generated status, freshness, and
  import safety.
- JSON index shape supports common status and lookup paths.
- CSV projections cover current live row families or explicitly flag unsupported
  families.
- Import/writeback is dry-run gated until a round-trip fixture proves safety.

## Non-Goals

- Do not replace the YAML ledger.
- Do not make CSV authoritative.
- Do not introduce SQLite or a long-lived service.
- Do not mutate canonical Craft source files in this refine run.
