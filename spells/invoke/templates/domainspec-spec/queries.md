# Queries: {Feature Name}

<!-- Behavioral concepts: Read operations that retrieve data without side effects.
     Each query documents its input, output shape, filters, and which entities it reads from. -->
<!-- Linking rule: every referenced concept/type/field name must be a markdown link.
     Output source format: [EntityName](domain.md#entityname).fieldName -->

## {QueryName}

**Type:** Query (read-only)
**Actor:** <!-- Who can execute: Authenticated User, Admin, System, etc. -->

### Input

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
|       |      |          |             |

### Filters

<!-- Optional filtering/pagination parameters -->

| Field | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
|       |      |         |             |

### Output

| Field | Type | Source                                       | Description |
| ----- | ---- | -------------------------------------------- | ----------- |
|       |      | [EntityName](domain.md#entityname).fieldName |             |

### Reads From

<!-- Which entities/projections this query accesses -->

| Entity | Relationship | Fields Used |
| ------ | ------------ | ----------- |
|        | queries      |             |
