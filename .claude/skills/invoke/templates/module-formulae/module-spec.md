---
module: {module-name}
version: current
status: draft
updatedAt: {date}
docType: module-spec
---

# {Module Name}

## Mission

Describe the module purpose, ownership boundary, and expected outcomes in two to three sentences.

## Ownership Boundary

- Owns: {capabilities or artifacts this module is responsible for}.
- Does Not Own: {adjacent concerns handled elsewhere}.

## Capability Map

```mermaid
graph TD
    A[{Capability A}] --> B[{Capability B}]
    B --> C[{Capability C}]
```

## Capabilities

Use this table as the primary navigation surface.

| Capability | Outcome | Key Contracts | Detail |
| --- | --- | --- | --- |
| {CapabilityName} | {business or system outcome} | {actions, read views, flows, interfaces} | {complexity summary} |

### {Capability Name} (Inline Variant)

Use this subsection when capability detail stays inside the module spec.

| Contract Type | Contract Name | Summary |
| --- | --- | --- |
| Action | {ActionName} | {what changes} |
| Read View | {ReadViewName} | {what is read} |
| Flow | {FlowName} | {orchestration summary} |
| Policy | {PolicyName} | {decision strategy summary} |
| Interface | {InterfaceName} | {exposure summary} |
| Signal | {SignalGroupName} | {observability summary} |

## Concept Model

| Concept | Type | Key Constraints |
| --- | --- | --- |
| {ConceptName} | Record | {invariants, uniqueness, bounds} |
| {ConceptName} | Value Type | {allowed shape and validation} |
| {ConceptName} | Enumeration | {allowed values} |

## Concept Index

Keep identifiers stable and unique.

| Concept | ID | Type | Source |
| --- | --- | --- | --- |
| {ConceptName} | {module-name}.{ConceptName} | Record | concept-model.md |
| {ActionName} | {module-name}.{ActionName} | Action | operations.md |
| {ReadViewName} | {module-name}.{ReadViewName} | Read View | operations.md |
| {FlowName} | {module-name}.{FlowName} | Flow | flows-policies.md |
| {InterfaceName} | {module-name}.{InterfaceName} | Interface | interfaces.md |

## Relationship Map

Declare typed relationships and evidence references.

| From | Edge | To | Evidence | Notes |
| --- | --- | --- | --- | --- |
| {module-name}.ConstraintA | enforces | {module-name}.ActionA | operations.md section: {section-name} | {optional notes} |
| {module-name}.ActionA | produces | {module-name}.SignalA | operations.md section: {section-name} | {optional notes} |
| {module-name}.ReadViewA | reads | {module-name}.RecordA | operations.md section: {section-name} | {optional notes} |
| {module-name}.InterfaceA | exposes | {module-name}.ActionA | interfaces.md section: {section-name} | {optional notes} |

## Supporting Contracts

| Contract Document | Purpose |
| --- | --- |
| [glossary-ontology.md](glossary-ontology.md) | Terminology authority for business and system language. |
| [concept-model.md](concept-model.md) | Structural records, value types, and enumerations. |
| [operations.md](operations.md) | Actions and read views with constraints and outcomes. |
| [flows-policies.md](flows-policies.md) | Orchestration and policy decision contracts. |
| [interfaces.md](interfaces.md) | External and internal interface boundaries. |
| [research-brief.md](research-brief.md) | Evidence-first discovery inputs and decision options. |
| [architecture-bundle.md](architecture-bundle.md) | Required architecture views and design decisions. |
| [implementation-plan.md](implementation-plan.md) | Delivery slices and layer progression before execution gates. |
| [observability.md](observability.md) | Signal and alert derivation contract. |
| [execution-pack.md](execution-pack.md) | Execution planning, waves, and closure gates. |
| [bundle-profile.md](bundle-profile.md) | Composable profile selection for template bundle assembly. |

## External Dependencies

| Capability | Depends On | Via | Why |
| --- | --- | --- | --- |
| {CapabilityName} | {ExternalModuleOrSystem} | {Action, Read View, Interface, Event} | {reason} |

## Provides To

| Consumer | Consumes Capability | Via | Delivered Value |
| --- | --- | --- | --- |
| {ConsumerName} | {CapabilityName} | {Action, Read View, Interface, Event} | {artifact or outcome} |

## Scenario Coverage

List where scenario and acceptance behavior is documented.

- Primary scenarios: {path or artifact reference}
- Completion checks: {path or artifact reference}

## Change History

Track substantive module-level changes over time.
