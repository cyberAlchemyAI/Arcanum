# Actions And Read Views: {Module Name}

Define state-changing actions and read-only views.

## Action: {ActionName}

Type: Action (state-changing)

Initiator: {user, system, scheduler, or service}

Trigger: {what starts this action}

### Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| {field-name} | {TypeName} | {yes or no} | {purpose} |

### Constraints

| ID | Constraint | Formal Expression |
| --- | --- | --- |
| R1 | {constraint text} | {formal expression} |

### Derivations

| ID | Derivation | Formula |
| --- | --- | --- |
| C1 | {derived value} | {formula} |

### State Update

Record: {RecordName}

Transition: {FromState} -> {ToState}

### Success Guarantees

- {guarantee 1}
- {guarantee 2}

### Failure Outcomes

| Condition | Result |
| --- | --- |
| {failure condition} | {error or fallback behavior} |

---

## Read View: {ReadViewName}

Type: Read View (no mutation)

Consumer: {who reads this view}

### Query Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| {filter-name} | {TypeName} | {yes or no} | {purpose} |

### Read Rules

| ID | Rule | Formal Expression |
| --- | --- | --- |
| Q1 | {rule text} | {formal expression} |

### Output

| Field | Type | Description |
| --- | --- | --- |
| {field-name} | {TypeName} | {meaning} |

### Performance Notes

- Expected latency: {target}
- Expected size: {target}
- Cache or freshness contract: {target}
