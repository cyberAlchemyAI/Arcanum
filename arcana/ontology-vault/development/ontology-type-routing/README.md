# Ontology Type Routing Experiment

Status: reusable sigil lifecycle evidence; non-authoritative

## Question

Can Ontology Vault choose the model shape required by clear intent, preserve
project-local aliases, and stop for a bounded user selection when generic
ontology intent remains ambiguous?

## Regression Origin

Two sequential usage events showed one routing gap:

1. a request about ontology support for architecture enforcement was first
   modeled as cross-branch traceability;
2. a correction clarified that the ontology needed to describe architecture
   types, properties, relations, profiles, and observations.

The evidence supports a routing change, not a claim that the experiment's
project vocabulary belongs in Arcanum. The generalized regression prompt in
the fixture contains no project names or private project prose.

## Contract Under Test

Selection precedence is:

```text
explicit --ontology-type
  -> runtime profile ontology_type and local alias
  -> one high-confidence catalog match
  -> user choice among two or three candidates
```

Ontology type selects the model shape. Branch arguments select traversal scope
inside that shape. Architecture-property selection therefore derives a system
branch but does not become a generic system/runtime ontology and does not
imply a business-system bridge.

## Cases

[The routing fixtures](fixtures/routing-cases.json) cover:

- clear architecture-property intent;
- clear business/domain intent;
- clear system/runtime intent;
- clear business-system bridge intent;
- ambiguous generic package-ontology intent;
- a project-local type/profile alias;
- explicit type precedence over vague wording.

Clear cases must select without prompting. The ambiguous case must return two
or three catalog-backed, consequence-bearing choices. A project-local alias
must resolve through a catalog type without becoming a new catalog entry.

## Run

From the repository root:

```bash
node arcanum/arcana/ontology-vault/development/ontology-type-routing/validate-routing.mjs
```

The dependency-free validator checks the catalog shape, selection precedence,
derived branch arguments, fixture results, privacy-safe regression wording,
and the architecture-property versus bridge distinction.

## Evidence

- [Local observer report](LOCAL-OBSERVER-REPORT.md)
- [Reflection report](REFLECTION-REPORT.md)
- [Validation report](VALIDATION-REPORT.md)
