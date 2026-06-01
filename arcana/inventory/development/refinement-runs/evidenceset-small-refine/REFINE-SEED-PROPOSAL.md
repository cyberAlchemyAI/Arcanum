# Refine Seed Proposal: EvidenceSet Candidate

## Target

`arcana/inventory/development` EvidenceSet candidate.

## Source Context

- `POC-VALIDATION.md` defines EvidenceSet as a candidate intermediate artifact only if grouped evidence proves reusable.
- `pilot-retrieval.json` contains a `candidate_evidence_set` with 4 included cards and 2 excluded cards.
- `pilot-handoff-ontology.json` and `pilot-handoff-definitions.json` reuse related card groups for downstream packets.
- `POC-CANDIDATES.md` identifies selected Craft sections as the best second-pass stressor for EvidenceSet.

## Refinement Question

Should Inventory promote `EvidenceSet` into a first-class artifact now, keep it as a candidate pending a Craft stressor, or drop it back to retrieval output?

## Research Mode

`no-research`: local POC evidence is enough for this gate.

## Validation Surface

- `bash arcana/inventory/scripts/validate-evidence-card-fixtures.sh arcana/inventory/development/pilot/evidence-card`
- inspection of retrieval selected/excluded groups,
- inspection of handoff packet reuse,
- decision-gate record for the unresolved promotion choice.
