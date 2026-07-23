## Spellcraft Result

- Mode: design
- Spell: Sigil Maintenance Loop
- Canonical ID: `sigil-maintenance-loop`
- Alias used: none
- Scope: library
- Spell file: `arcanum/spells/sigil-maintenance-loop/README.md`
- Sigils referenced: required `inventory`, `signal-observer`, `workflow-reflect`, and `sigil-development`; optional `experiment-harness` and `observability-setup`
- Phases: 5
- Validation: flag
- Observability: configured
- Next action: retain the revision in the canonical spell, do not create a second spell, and run the remaining Inventory and approval-gate experiment cases before claiming reusable promotion readiness.

### Design decision

Revise the canonical `sigil-maintenance-loop`; do not create a new spell. Automatic Inventory exploration strengthens the existing evidence-to-reflection maintenance lifecycle and does not introduce a separate workflow purpose. A second spell would duplicate the same target, triggers, reflection phase, and mutation gate.

### Contract evidence

- `inventory` is a required sigil in `lookup` mode and runs in Phase 1 before observation or reflection.
- Phase 1 produces the named `inventory-lookup-packet`, which is shared with `signal-observer`, `workflow-reflect`, and the maintenance report.
- The automatic exploration contract requires `index.json` first, permits `index.md` only as a flagged fallback, and returns selected matches, exclusions, source references, and unresolved gaps.
- Read-only lookup proceeds without another user prompt and may not silently expand into `install`, `query`, `ingest`, `backfill`, or `sync`.
- Inventory absence, an invalid machine index, and no matching entry remain explicit residue rather than silently skipped work.
- Inventory is declared non-authoritative: lookup evidence may inform reflection but cannot approve or promote a sigil change.
- Phase 4 preserves explicit user approval before `sigil-development` may mutate the target contract and blocks missing approval or scope expansion.
- The spell names its prerequisites, shared state, handoff artifacts, gates, failure policies, local customization boundary, observability, Quality Bar, Anti-Patterns, and output contract.

### Validation boundary

The canonical design satisfies this prompt structurally and preserves Spellcraft ownership without copying the internal processes of its referenced sigils. Validation remains `flag` because this low-complexity native example establishes one design result, while the spell's declared reusable-evidence boundary still requires runtime coverage for relevant `index.json`, no-match, `index.md` fallback, unavailable Inventory, insufficient signal, and rejected mutation approval cases.
