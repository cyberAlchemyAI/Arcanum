# Concept Model: MOGT Agentic Conversation

Define structural concepts and constraints for MOGT decision evidence.

## Records

### DecisionState

Represents a bounded conversation decision point.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | `DecisionStateId` | yes | Unique decision-state identifier. |
| `conversation_context` | `ContextHandle` | yes | Context available at turn `t`. |
| `candidate_actions` | `CandidateAction[]` | yes | Finite action set available at the decision point. |
| `active_objectives` | `ObjectiveName[]` | yes | Objectives considered by the policy regime. |
| `active_constraints` | `Constraint[]` | yes | Constraints that may block or shape action selection. |

Lifecycle Reference: framed before policy selection and captured in the run row.

Related Actions: `SelectPolicyAction`, `CaptureRunRow`.

---

### CandidateAction

Represents one action available to a policy regime.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `action_id` | `ActionId` | yes | Stable action identifier. |
| `description` | `string` | no | Human-readable action summary. |
| `objective_vector` | `ObjectiveVector` | yes | Normalized scores for active objectives. |

Lifecycle Reference: belongs to `DecisionState.candidate_actions`.

Related Actions: `SelectPolicyAction`.

---

### MOGTRunRow

Represents one append-only JSONL evidence row for a policy-regime decision.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `experiment_id` | `ExperimentId` | yes | One of `E1`, `E2`, `E3`, `E4`. |
| `run_id` | `RunId` | yes | Stable run identifier. |
| `timestamp` | `DateTime` | yes | ISO 8601 capture time. |
| `project_id` | `ProjectId` | yes | Must be `mogt-agentic-conversation`. |
| `scenario_id` | `ScenarioId` | yes | Stable scenario fixture or live scenario identifier. |
| `policy_regime` | `PolicyRegime` | yes | Operational decision rule used. |
| `objective_vector` | `ObjectiveVector` | yes | Selected action objective vector. |
| `candidate_actions` | `CandidateAction[]` | yes | Available candidate actions. |
| `selected_action` | `SelectedAction` | yes | Chosen action and selection reason. |
| `policy_trace` | `PolicyTraceStep[]` | yes | Auditable policy trace. |
| `reviewer_scores` | `ScoreMap` | yes | Reviewer or rubric scores. |
| `token_cost` | `NonNegativeInteger` | yes | Token cost observed or estimated. |
| `latency_ms` | `NonNegativeInteger` | yes | Latency observed or estimated. |
| `turn_count` | `NonNegativeInteger` | yes | Number of conversation turns. |
| `tool_calls` | `NonNegativeInteger` | yes | Tool-call count. |
| `protocol_deviations` | `string[]` | yes | Deviations from protocol, empty if none. |
| `evidence_class` | `EvidenceClass` | no | Fixture/dry-run/live evidence marker. |

Lifecycle Reference: created by `CaptureRunRow`, validated by
`ValidateRunJsonl`.

Related Actions: `CaptureRunRow`, `ValidateRunJsonl`.

## Value Types

### ObjectiveVector

Use value types for immutable comparison-sensitive objective scores.

| Field | Type | Constraint |
| --- | --- | --- |
| `quality` | `Score` | Required, 0..1, higher is better. |
| `cost` | `Score` | Required, 0..1, normalized with higher meaning more preferred after cost adjustment. |
| `latency` | `Score` | Required, 0..1, normalized with higher meaning more preferred after latency adjustment. |
| `safety` | `Score` | Required, 0..1, higher is better. |
| `escalation_risk` | `Score` | Required, 0..1, normalized with higher meaning lower unacceptable escalation risk. |

Equality Rule: equal only when all active objective keys and values match.

---

### SelectedAction

| Field | Type | Constraint |
| --- | --- | --- |
| `action_id` | `ActionId` | Must match one `candidate_actions[].action_id`. |
| `selection_reason` | `string` | Non-empty. |

Equality Rule: equal when both action id and selection reason match.

---

### Score

| Field | Type | Constraint |
| --- | --- | --- |
| `value` | `number` | 0 <= value <= 1. |

Equality Rule: numeric equality.

## Enumerations

### PolicyRegime

| Value | Description |
| --- | --- |
| `heuristic` | Baseline implicit or rule-of-thumb arbitration. |
| `weighted_sum` | Scalarized objective scoring with explicit weights. |
| `pareto_guided` | Frontier/dominance-aware action filtering or selection. |
| `bargaining_guided` | Negotiation or equilibrium-inspired coordination policy. |

### ExperimentId

| Value | Description |
| --- | --- |
| `E1` | Tradeoff traceability baseline. |
| `E2` | Pareto arbitration quality. |
| `E3` | Negotiation stability under conflict. |
| `E4` | Overhead feasibility envelope. |

### EvidenceClass

| Value | Description |
| --- | --- |
| `synthetic_fixture` | Synthetic row used to prove schema/validator behavior. |
| `dry_run` | Non-live rehearsal data used to validate fixture mechanics. |
| `live_experiment` | Evidence from an approved experiment execution. |
