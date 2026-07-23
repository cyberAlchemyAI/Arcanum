## Spellcraft Result

- Mode: reflect
- Spell: Sigil Maintenance Loop
- Canonical ID: `sigil-maintenance-loop`
- Alias used: none
- Scope: library
- Spell file: `arcanum/spells/sigil-maintenance-loop/README.md`
- Profile ID: `spellcraft`
- Lifecycle owner: `spellcraft`
- Sigils referenced: required `inventory`, `signal-observer`, `workflow-reflect`, and `sigil-development`; optional `experiment-harness` and `observability-setup`
- Status: preserve the public spell and the corrected consumer route
- Inventory lookup: automatic, read-only, machine-index-first, and performed before reflection without an additional user prompt
- Mutation approval: preserved; `sigil-development` may mutate only after a reflection outcome and explicit approval of a bounded change scope
- Public/private leak: none; this result carries no consumer path, internal owner location, workspace identifier, or private operational detail into the public spell
- Phases: 5
- Validation: pass
- Observability: configured
- Next action: record a no-change reflection decision for the public spell, retain the consumer's canonical-spell invocation, and route future regressions through `sigil-maintenance-loop` instead of manually sequencing its inner sigils.

### Reflection decision

Preserve the public `sigil-maintenance-loop`; do not replace it and do not add consumer-specific behavior to it. The failure mode described by the reflection prompt is a consumer-routing defect, not a second spell purpose. The current bounded evidence shows that the private consumer hook has already been revised to use the canonical spell, so no additional public or private contract mutation is justified by this run.

### Public spell evidence

- Required Sigils composes the full chain: `inventory`, `signal-observer`, `workflow-reflect`, and `sigil-development`.
- Phase 1 always creates `inventory-lookup-packet` before observation and reflection, with `index.json` as the first machine view and explicit residue for unavailable, fallback, or no-match states.
- Automatic Inventory Exploration forbids an extra lookup prompt and forbids silently expanding lookup into `install`, `query`, `ingest`, `backfill`, or `sync`.
- Phase 2 records the current behavior signal instead of allowing reflection to bypass observation.
- Phase 3 consumes both telemetry and the Inventory packet, keeping retrieved evidence, inference, exclusions, and gaps distinguishable.
- Phase 4 requires user approval of the bounded change scope before `sigil-development` can update the target sigil.
- Authority Boundaries keeps Inventory non-authoritative, reflection proposal-only, and spell composition owned by Spellcraft.

### Consumer-route evidence

- The current hook routes maintenance through canonical `sigil-maintenance-loop` and explicitly rejects manual sequencing of only `workflow-reflect` and `sigil-development`.
- It passes the current correction or observer envelope, affected contract area, and relevant lookup terms into the spell rather than reconstructing inner phase contracts.
- It distinguishes read-only maintenance lookup from durable result ingestion, so retrieving prior evidence does not overwrite or masquerade as strategy-result recording.
- It retains `sigil-development` as the edit owner only after the spell produces a reflection outcome and the user approves the bounded scope.
- Its reflection signals remain local to the consumer. None need to be copied into the generic public spell.

### Boundary judgment

The public artifact contains only product-neutral composition rules. The private consumer owns its target identity, correction vocabulary, local paths, and result-recording conventions. The integration point is the canonical spell ID plus its declared inputs and handoffs; publishing the consumer's identifiers or operational paths would add no reusable behavior and would breach the evidence boundary.

### Future regression policy

If the consumer again bypasses Inventory exploration or signal observation, treat that as a consumer invocation regression. Preserve the public spell unless evidence identifies a generic contract gap. Any proposed consumer edit must come from the spell's `reflection-report`, remain within explicit approved scope, and produce a `change-receipt`; absent approval, the maintenance run stops before mutation.
