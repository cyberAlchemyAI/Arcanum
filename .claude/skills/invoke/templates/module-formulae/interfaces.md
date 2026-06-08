# Interfaces: {Module Name}

Define external and internal integration contracts.

## External Interface: {InterfaceName} ({Protocol})

### {Method} {Path}

Exposes: {ActionName or ReadViewName}

Auth: {auth model}

### Request

| Field | Type | Maps To |
| --- | --- | --- |
| {field-name} | {TypeName} | {action or read view field} |

### Responses

| Status | Condition | Body |
| --- | --- | --- |
| 2xx | Success | {response contract} |
| 4xx | Constraint violation | {error contract} |
| 5xx | System failure | {fallback contract} |

---

## Internal Interface: {InternalInterfaceName}

Consumers: {calling modules or services}

| Method | Maps To | Description |
| --- | --- | --- |
| {method-name} | {ActionName} | {purpose} |
| {method-name} | {ReadViewName} | {purpose} |

## Data Mapping Notes

- Keep field naming deterministic between transport and contract layers.
- Keep enum and status translation rules explicit.
- Record backward compatibility constraints when endpoint changes are introduced.
