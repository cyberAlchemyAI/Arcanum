---
module: {module-name}
version: current
status: draft
updatedAt: {date}
docType: architecture-bundle
---

# Architecture Bundle: {Module Name}

Use this template to translate approved module scope into structural and process design views.

## Design Intent

Summarize architecture goals and constraints in two to three sentences.

## Inputs

- [module-spec.md](module-spec.md)
- [glossary-ontology.md](glossary-ontology.md)
- [research-brief.md](research-brief.md) (when available)

## Required View Set

### 1. Context View

```mermaid
graph TD
    User[Actor] --> Module[{Module}]
    Module --> External[External Dependency]
```

### 2. High-Level Structure View

```mermaid
graph TD
    A[Interface Layer] --> B[Application Layer]
    B --> C[Core Rules Layer]
    C --> D[Storage or Integration Layer]
```

### 3. Low-Level Components View

```mermaid
graph TD
    C1[Component A] --> C2[Component B]
    C2 --> C3[Component C]
```

### 4. Workflow Process View

```mermaid
graph TD
    S1[Start] --> S2[Action]
    S2 --> S3{Decision}
    S3 -->|Path A| S4[Outcome A]
    S3 -->|Path B| S5[Outcome B]
```

### 5. Decision Flow View

```mermaid
graph TD
    D1[Input] --> D2{Policy}
    D2 --> D3[Decision]
    D3 --> D4[Effect]
```

### 6. Dependency Interface View

```mermaid
graph TD
    M[Module] --> I1[Interface A]
    M --> I2[Interface B]
    I1 --> X1[External System]
```

## Assumptions

- {assumption 1}
- {assumption 2}

## Open Risks

| Risk ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| R-ARCH-1 | {risk summary} | high, medium, low | {mitigation} |

## Unresolved Decisions

| Decision | Options | Current Status |
| --- | --- | --- |
| {decision summary} | {A, B, C} | open, selected, blocked |

## Planning Notes

- Direct implementation constraints: {constraints}
- Boundary rules: {rules}
- Testability implications: {notes}

## Handoff Targets

- [implementation-plan.md](implementation-plan.md)
- [execution-pack.md](execution-pack.md)
