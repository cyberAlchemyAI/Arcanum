---
module: {module-name}
version: current
status: draft
updatedAt: {date}
docType: observability
---

# Observability: {Module Name}

Define measurable signals tied to source contracts.

## Signal Inventory

| Signal Family | Purpose | Source Contract |
| --- | --- | --- |
| Lifecycle Integrity | Detect invalid transitions and stalled states. | concept-model.md, flows-policies.md |
| Action Behavior | Measure action throughput, latency, and constraint violations. | operations.md |
| Operational Health | Track interface reliability and event lag. | interfaces.md, flows-policies.md |
| Outcome Effectiveness | Measure outcome quality and completion fitness. | module-spec.md, execution-pack.md |

## Lifecycle Integrity Signals

| Signal | Instrument Type | Attributes | Alert Rule |
| --- | --- | --- | --- |
| lifecycle.invalid_transition | Counter | module, record, from_state, attempted_action, error_code | Any increment is critical. |
| lifecycle.state_population | UpDownCounter | module, record, state | Non-terminal accumulation above threshold triggers warning. |
| lifecycle.invariant_violation | Counter | module, invariant_id | Any increment triggers investigation. |

## Action Behavior Signals

| Signal | Instrument Type | Attributes | Alert Rule |
| --- | --- | --- | --- |
| action.invocation | Counter | module, action, result | Investigate sustained error ratio. |
| action.duration | Histogram | module, action | Alert when p95 exceeds target. |
| action.constraint_violation | Counter | module, action, constraint_id | Review spikes by constraint. |
| action.postcondition_result | Counter | module, action, postcondition_id, result | Any violated result triggers audit. |

## Operational Health Signals

| Signal | Instrument Type | Attributes | Alert Rule |
| --- | --- | --- | --- |
| interface.request_count | Counter | module, interface, method, status_class | Monitor sudden drops or spikes. |
| interface.latency | Histogram | module, interface, method | Alert when p99 exceeds threshold. |
| event.consumer_lag | Histogram | module, event_type, consumer | Alert on sustained lag breaches. |

## Outcome Effectiveness Signals

| Signal | Instrument Type | Attributes | Alert Rule |
| --- | --- | --- | --- |
| outcome.completion_rate | Gauge | module, objective | Alert on significant regression. |
| outcome.rework_count | Counter | module, wave_or_stage | Alert when repeated rework grows. |
| outcome.blocker_age_hours | Gauge | module, blocker_id | Alert when blocker age exceeds policy. |

## Alert Runbook Index

| Alert | Severity | Investigation Entry | Owner |
| --- | --- | --- | --- |
| lifecycle.invalid_transition increment | critical | Validate transition rule and triggering action. | {owner-role} |
| action.postcondition violated | high | Trace action inputs and downstream state updates. | {owner-role} |
| interface latency breach | medium | Inspect dependency health and payload size. | {owner-role} |

## Dashboard Views

- Lifecycle view: transition health, state population, invariant violations.
- Action view: throughput, latency, error ratio, constraint violations.
- Interface view: request volume, latency percentiles, consumer lag.
- Outcome view: completion trend, blocker aging, rework pressure.

## Traceability Rules

1. Every alert must link to at least one source contract section.
2. Every action in operations.md should have invocation and duration signals.
3. Every lifecycle with transitions should have invalid transition monitoring.
4. Every completion gate should have at least one measurable signal.
