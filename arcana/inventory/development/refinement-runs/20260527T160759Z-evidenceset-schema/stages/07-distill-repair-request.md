# Distill Repair Request

Repair the EvidenceSet design by reducing it to the minimum useful shape.

Prefer:

- flat JSON;
- small required field set;
- explicit exclusions;
- short rationale strings;
- references to evidence-card IDs instead of duplicating card content.

Avoid:

- nested multi-document packages;
- prose-heavy schema fields;
- UI-only fields;
- ontology or definition authority claims.
