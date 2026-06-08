# Concept Model: {Module Name}

Define structural concepts and constraints.

## Records

### {RecordName}

Describe what this record represents and why it exists.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| id | {IdType} | yes | Unique identifier. |
| {field-name} | {TypeName} | {yes or no} | {field purpose} |

Lifecycle Reference: {optional lifecycle or state machine reference}

Related Actions: {actions that create or update this record}

---

## Value Types

### {ValueTypeName}

Use value types for immutable or comparison-sensitive shapes.

| Field | Type | Constraint |
| --- | --- | --- |
| {field-name} | {TypeName} | {validation rule} |

Equality Rule: {how two values are compared}

---

## Enumerations

### {EnumName}

| Value | Description |
| --- | --- |
| {ValueA} | {meaning} |
| {ValueB} | {meaning} |
