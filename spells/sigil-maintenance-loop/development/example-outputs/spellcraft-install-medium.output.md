## Spellcraft Result

- Mode: install
- Spell: Sigil Maintenance Loop
- Canonical ID: `sigil-maintenance-loop`
- Alias used: none
- Scope: local
- Spell file: `.arcanum/spells/sigil-maintenance-loop/README.md`
- Sigils referenced: required `inventory`, `signal-observer`, `workflow-reflect`, and `sigil-development`; optional `experiment-harness` and `observability-setup`
- Phases: 5
- Validation: flag
- Observability: configured
- Next action: preserve `arcanum/spells/sigil-maintenance-loop/README.md` as the public canonical source, install only a path-local adaptation, and carry the state-specific Inventory residue into every maintenance report without prompting for Inventory mutation.

### Installation decision

Adapt the existing canonical spell locally; do not fork its workflow or revise the public contract for either degraded repository state. Local customization may select the Inventory root, thresholds, persistence paths, and validation commands, but it must preserve automatic read-only lookup, machine-index-first behavior, the named `inventory-lookup-packet`, and explicit approval before target-sigil mutation.

### Repository state 1: no Inventory package

- Automatic attempt: Phase 1 derives lookup terms from the target sigil ID, invocation envelope, and contract area, then attempts repository Inventory resolution without asking the user.
- Lookup packet: `inventory-lookup-packet` is returned with status `unavailable`, no asserted matches, no asserted exclusions, and the gap `repository Inventory package not found`.
- Residue: `inventory_unavailable`.
- Gate result: `flag`; continue to signal observation and, when the manual-trigger or evidence gate passes, workflow reflection.
- Authority result: reflection may use the target contract and telemetry evidence, but it cannot describe Inventory evidence as retrieved.
- Mutation boundary: no Inventory `install`, `query`, `ingest`, `backfill`, or `sync` action is proposed or executed; target-sigil mutation still requires explicit approved scope.

### Repository state 2: `index.md` exists without parseable `index.json`

- Automatic attempt: Phase 1 attempts the machine index first and records that no parseable `index.json` is available.
- Lookup packet: `inventory-lookup-packet` is returned with status `fallback`, no machine-index-backed matches, no asserted exclusions, and `index.md` identified only as human-orientation fallback evidence.
- Residue: `machine_index_gap` with the concrete condition `index.md present; index.json missing or unparsable`.
- Gate result: `flag`; continue to signal observation and, when the manual-trigger or evidence gate passes, workflow reflection.
- Authority result: any heading discovered through `index.md` remains fallback context and cannot be promoted to machine-index-backed or canonical evidence.
- Mutation boundary: no Inventory `install`, `query`, `ingest`, `backfill`, or `sync` action is proposed or executed; target-sigil mutation still requires explicit approved scope.

### Shared validation evidence

- Both states reach Inventory exploration before reflection and produce the same named handoff shape.
- Both state failures are visible, non-blocking residue; neither is silently treated as a successful lookup.
- Later reflection must distinguish telemetry, fallback context, inference, and unresolved Inventory gaps.
- Missing mutation approval blocks `sigil-development` in both states even when reflection proposes a targeted update.
- The canonical public spell remains unchanged; only repository-local paths and allowed customization values vary.

Validation is `flag` rather than `block` because the local adaptation can run its evidence and reflection phases in both states, while neither state provides a healthy machine-index-backed Inventory lookup. Resolving either gap is a separate, explicitly authorized Inventory lifecycle action, not an implicit part of spell installation.
