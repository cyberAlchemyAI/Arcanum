# {Feature Name}

## What This Module Owns

<!-- 2-3 sentences: domain ownership boundary, core capabilities, and design intent -->

## Module Map

<!-- Visual concept flow by capability. Keep concise and capability-oriented. -->

```mermaid
graph TD
     A[{Capability A}] --> B[{Capability B}]
     B --> C[(Entity/State)]
```

## Capabilities

<!--
Primary navigation is capability-driven.

Governance thresholds:
- SPEC < 120 lines: keep capability details inline as subsections.
- SPEC 120-200 lines: keep capability summary in SPEC and move stories to STORIES.md.
- SPEC > 300 lines OR any capability section > 15 rows: create capabilities/{capability-name}.md and keep only summary links in SPEC.
-->

| Capability                                             | What               | Key Aspects                               | Detail                      |
| ------------------------------------------------------ | ------------------ | ----------------------------------------- | --------------------------- |
| {CapabilityName} (`capabilities/{capability-name}.md`) | {business outcome} | {main operations/queries + states/events} | {counts/complexity summary} |

### {Capability Name} (inline variant)

<!-- Use this subsection format when capability details stay inline. -->

{One-sentence capability summary.}

| Aspect      | Concept                                          | Summary               |
| ----------- | ------------------------------------------------ | --------------------- |
| Operation   | [{OperationName}](operations.md#{anchor})        | {what it changes}     |
| Query       | [{QueryName}](queries.md#{anchor})               | {what it reads}       |
| Interface   | [{Endpoint or Contract}](interfaces.md#{anchor}) | {how it is exposed}   |
| Mapping     | [{MappingName}](mappings.md#{anchor})            | {data transformation} |
| State/Event | [{StateOrEvent}](states.md#{anchor})             | {lifecycle effect}    |

## Domain Concepts

<!-- Structural concepts and key constraints for quick human understanding. -->

| Concept                            | Type        | Key Constraints                  |
| ---------------------------------- | ----------- | -------------------------------- |
| [{EntityName}](domain.md#{anchor}) | Entity      | {invariants, uniqueness, bounds} |
| [{EnumOrType}](domain.md#{anchor}) | Enum / Type | {allowed values}                 |

## Concept Registry

<!-- Source of truth for registry sync. Keep compact: no Description column. -->

| Concept                                 | ID                      | Type      |
| --------------------------------------- | ----------------------- | --------- |
| [{ConceptName}](domain.md#{anchor})     | {feature}.{ConceptName} | Entity    |
| [{ConceptName}](operations.md#{anchor}) | {feature}.{ConceptName} | Operation |
| [{ConceptName}](queries.md#{anchor})    | {feature}.{ConceptName} | Query     |
| [{ConceptName}](interfaces.md#{anchor}) | {feature}.{ConceptName} | Interface |

## Feature Concept Graph

<!--
Declare typed relationships with canonical edge names from RELATIONSHIPS.md.
Use one relationship per row and include an evidence anchor when available.
-->

| From                 | Edge     | To                   | Evidence                 | Notes            |
| -------------------- | -------- | -------------------- | ------------------------ | ---------------- |
| {feature}.RuleA      | enforces | {feature}.OperationA | operations.md#operationa | {optional notes} |
| {feature}.OperationA | produces | {feature}.EventA     | operations.md#operationa | {optional notes} |
| {feature}.QueryA     | queries  | {feature}.EntityA    | queries.md#querya        | {optional notes} |
| {feature}.InterfaceA | exposes  | {feature}.OperationA | interfaces.md#interfacea | {optional notes} |

## Aspect Docs

<!-- Link only to aspect files that exist for this feature. Delete unused lines. -->

| Aspect                          | Contains                                                | Key Concepts   |
| ------------------------------- | ------------------------------------------------------- | -------------- |
| [Architecture](architecture.md) | Architecture-level explanation of the feature contracts | {top concerns} |
| [Glossary](glossary.md)         | Distilled definitions for feature concepts              | {top concepts} |
| [Domain](domain.md)             | Entities, value objects, enums                          | {top concepts} |
| [Operations](operations.md)     | Mutations, rules, calculations                          | {top concepts} |
| [Interfaces](interfaces.md)     | External/internal contracts                             | {top concepts} |
| [Queries](queries.md)           | Read models                                             | {top concepts} |
| [Mappings](mappings.md)         | Data transformations                                    | {top concepts} |
| [Workflows](workflows.md)       | Multi-step orchestrations and policies                  | {top concepts} |
| [States](states.md)             | State machines and transitions                          | {top concepts} |
| [Events](events.md)             | Domain events and consumers                             | {top concepts} |

## Cross-Feature Dependencies

<!-- Capability-to-capability dependencies. -->

| Capability       | Depends On                                                       | Via                           | Why      |
| ---------------- | ---------------------------------------------------------------- | ----------------------------- | -------- |
| {CapabilityName} | {other-feature}.{OtherCapability} (`../{other-feature}/SPEC.md`) | Query / Operation / Interface | {reason} |

## Produces For

<!-- Capability-aware outputs for downstream consumers. -->

| Consumer                     | Consumes Capability | Via                       | What             |
| ---------------------------- | ------------------- | ------------------------- | ---------------- |
| {consumer-feature or system} | {CapabilityName}    | Query / Interface / Event | {artifact/value} |

## Stories

See [User Stories](STORIES.md) for acceptance scenarios and BDD coverage.

## Change History

See [Changelog](CHANGELOG.md) for a dated record of domain-level changes to this feature.

## References

- Implementation tasks: `TASKS.md`
- Architecture decisions: `DECISIONS.md`
- Test specification: `TEST-SPEC.md`
