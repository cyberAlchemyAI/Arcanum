# Context Builder Handoff: Friend Graph Memory Ontology Summary

Status: pass
Mode: lean

## Evidence Baseline

The pasted conversation discusses:

- embedded graph/RAG database design,
- weighted relationships and pruning,
- a model that evaluates request/response copies,
- a bounded API that performs graph mutations,
- deterministic workers, audit, rollback, confidence thresholds, and provenance,
- portable/minimal database layers, including C libraries and bindings,
- platform-style multi-user systems versus device-local systems.

The local ontology work provides:

- branch context: `meaning | system | operational | bridge`,
- record kinds: `ontology_entry | promotion_record | evidence_input | bridge_validation`,
- lifecycle/role/outcome axis separation,
- evidence confidence versus commitment confidence,
- Inventory non-authority boundary,
- deterministic fixture validation and development JSON Schema,
- a current promotion blocker requiring decision-gate before canonical mutation.

## Controlling Interpretation

The shared idea is not just "use a graph". It is:

```text
model interprets semantic value
deterministic worker owns mutation
ontology records why a relation is allowed to matter
```

## Boundary

The external conversation is a candidate `evidence_input`. It can inspire a bridge explanation, but it does not promote local ontology conventions.
