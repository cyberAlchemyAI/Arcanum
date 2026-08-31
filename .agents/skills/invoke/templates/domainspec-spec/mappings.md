# Mappings: {Feature Name}

<!-- Connective concepts: Data transformations between shapes.
     Each mapping documents field-by-field how data moves between
     domain entities, DTOs, API payloads, and external systems. -->
<!-- Linking rule: every referenced concept/type/field name must be a markdown link.
     Source/Target field refs should prefer [ConceptName](file.md#concept).fieldName form. -->

## {MappingName}

**From:** {SourceType} <!-- e.g., API Request, External System Response -->
**To:** {TargetType} <!-- e.g., Domain Entity, DTO -->
**Direction:** <!-- Inbound / Outbound / Bidirectional -->

### Field Mapping

| Source Field | Target Field | Transform                                      | Notes |
| ------------ | ------------ | ---------------------------------------------- | ----- |
|              |              | <!-- direct / computed / default / omitted --> |       |

### Defaults

<!-- Fields that get default values when not present in source -->

| Target Field | Default Value | Condition |
| ------------ | ------------- | --------- |
|              |               |           |

### Validation

<!-- Constraints checked during mapping -->

| Field | Validation | On Failure |
| ----- | ---------- | ---------- |
|       |            |            |
