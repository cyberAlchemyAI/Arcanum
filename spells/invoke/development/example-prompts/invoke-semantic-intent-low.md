# Invoke Example Prompt: invoke-semantic-intent-low

## Codex Prompt

Author one machine-readable semantic-intent artifact for the existing mixed
Define-v3 example. This is a direct native Codex evidence run; do not invoke
Arcanum commands, lifecycle adapters, telemetry, or experiment-loop scripts.

Read only these semantic sources:

- `spells/invoke/development/define-v3-semantic-closure/fixtures/schema-family/positive-family.json`
- `spells/invoke/define-authoring-guide.md`

Do not open `development/fixtures/define-intent-coverage/` or any semantic
validator/oracle. Independently inventory the bounded subject, parts,
relationships, evidence/state, validation/gates, execution handoff, and
authority boundary before selecting probes. Include every domain concept the
source requires; do not merely describe the evidence shell.

The semantic subject is the mixed fixture's three declared semantic
applications. Use the guide to assess those applications and their facets,
not as a source of additional target-domain definitions. Record process-level
guide requirements in facets, evidence dispositions, topology, or boundaries;
do not turn generic Define control vocabulary into extra probes.

Return only one JSON object with this shape:

```json
{
  "schema_version": "invoke.define-intent-authored-artifact.v1",
  "target_id": "target:mixed-define-v3",
  "evidence_sources": [{"source_id":"...","source_class":"current-intent|current-contract|historical","semantic_disposition":"retain|retain-and-reassess","authority_disposition":"current|historical-only|none","rationale":"..."}],
  "facets": [{"facet_id":"subject|parts|relationships|evidence-state|validation-gates|execution-handoff|authority-boundary","status":"represented|not-applicable","evidence_source_ids":["..."],"rationale":"..."}],
  "definitions": [{"definition_id":"...","term":"...","aliases":[],"relations":[{"type":"references|depends-on|contrasts-with","target_id":"..."}],"boundary":{"includes":[],"excludes":[],"conditions":[]}}],
  "authority_bindings": [{"binding_id":"...","semantic_id":"...","term":"...","aliases":[]}],
  "probes": [{"probe_id":"...","term":"...","definition_id":"... or null","authority_binding_id":"... or null"}],
  "declared_uncovered": [],
  "consumer_topology": {"configured_roots":["..."],"enumerated_consumers":[],"declared_consumers":[],"no_consumers_evidence":"..."}
}
```

Assess all seven facets exactly once. Every definition or authority binding
must have one probe. Relation targets use definition `definition_id` or binding
`semantic_id`. Reused canonical meaning belongs in an authority binding rather
than a copied local definition. `enumerated_consumers` and
`declared_consumers` must be identical; count only independently confirmed
downstream semantic consumers, not discovery or evidence documents. Do not add
a closure snapshot. Do not include Markdown fences, commentary, or a save
summary.
