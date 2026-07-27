# Define Transport: Distill Runtime-Event Emission

- Mode: `invoke define`
- Target: Distill sigil lifecycle
- Template: `invoke.sigil` candidate handoff profile
- Discovery: satisfied by the completed DEE package and live Distill contract
- Define status: pass
- Layering: seed carried into `IMPLEMENTATION-LAYERING.md`
- Distill sanity check: not required; the approved scope is already one bounded
  lifecycle gap and introduces no competing definition units
- Owner boundary: Invoke authors; Sigil Development accepts and mutates
- Next route: `invoke design`

## Define Dispatch Techniques

| Technique | Effect |
| --- | --- |
| `sequence` | Preserves define → design → plan order. |
| `owner_boundary_check` | Separates Distill, Invoke, observer, and bootstrap authority. |
| `artifact_contract_bridge` | Connects producer behavior to the accepted consumer schema. |
| `residue_ledger` | Preserves `GAP-DEE-002` until runtime proof closes it. |
| `concrete_path_evidence` | Requires exact source, fixture, receipt, and mirror paths. |
