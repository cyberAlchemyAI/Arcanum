# Interfaces: {Feature Name}

<!-- Connective concepts: API boundaries — external (REST, GraphQL) and internal (module contracts).
     Each interface exposes operations or queries and documents the mapping
     between API shape and domain concepts. -->
<!-- Linking rule: every referenced concept/type/field name must be a markdown link.
     Field mappings should use: [OperationName](operations.md#operationname-lowercase).fieldName -->

## External: {API Name} ({Protocol})

### {METHOD} {/path}

**Exposes:** [{OperationName}](operations.md#{operationname-lowercase})
**Auth:** <!-- Bearer token, API key, public, etc. -->

**Request:**

| Field | Type | Maps To                                                        |
| ----- | ---- | -------------------------------------------------------------- |
|       |      | [OperationName](operations.md#operationname-lowercase).{field} |

**Responses:**

| Status | Condition      | Body |
| ------ | -------------- | ---- |
| 2xx    | Success        |      |
| 4xx    | Rule violation |      |

---

## Internal: {ModuleName} Interface

**Consumers:** <!-- Which modules call this interface -->

| Method | Maps To                   | Description |
| ------ | ------------------------- | ----------- |
|        | {OperationName} operation |             |
|        | {QueryName} query         |             |
