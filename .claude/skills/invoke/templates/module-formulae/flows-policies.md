# Flows And Policies: {Module Name}

Define multi-step flows and policy decisions.

## Flow: {FlowName}

Type: Flow

Trigger: {event, schedule, manual request, or upstream action}

Orchestrates: {ActionA, ActionB, ActionC}

Compensation Strategy: {reverse action, rollback, notify-only, none}

Idempotency: {yes, no, conditional}

### Steps

```mermaid
graph TD
    A[Step 1: {description}] --> B{Decision Point}
    B -->|{condition-a}| C[Step 2A: {description}]
    B -->|{condition-b}| D[Step 2B: {description}]
    C --> E[Step 3: {description}]
    D --> E
```

### Step Table

| Step | Description | Actor | Action | On Success | On Failure | Compensation |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | {step summary} | {actor} | {ActionName} | {next step} | {failure path} | {none or action} |
| 2 | {step summary} | {actor} | {ActionName} | {next step} | {failure path} | {none or action} |

### Invariants

| ID | Invariant | Formal Expression |
| --- | --- | --- |
| I1 | {invariant text} | {formal expression} |

---

## Policy: {PolicyName}

Type: Policy

Applies To: {flow step or action}

Trigger Conditions: {when to evaluate this policy}

### Decision Table

| Condition | Selected Behavior | Notes |
| --- | --- | --- |
| {condition} | {behavior} | {notes} |

### Formula (Optional)

{formula or scoring expression}

### Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| {parameter-name} | {TypeName} | {default} | {purpose} |
