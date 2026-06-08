# Actions And Read Views: MOGT Agentic Conversation

Define state-changing actions and read-only views for the MOGT evidence model.

## Action: SelectPolicyAction

Type: Action (state-changing in the decision trace)

Initiator: research runner or policy evaluator

Trigger: a `DecisionState` has candidate actions and a selected `PolicyRegime`.

### Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `decision_state` | `DecisionState` | yes | Decision state to evaluate. |
| `policy_regime` | `PolicyRegime` | yes | Decision rule to apply. |
| `regime_parameters` | `object` | no | Weights, thresholds, negotiation limits, or Pareto options. |

### Constraints

| ID | Constraint | Formal Expression |
| --- | --- | --- |
| R1 | Candidate set must be non-empty. | `len(decision_state.candidate_actions) >= 1` |
| R2 | Every candidate must have an objective vector. | `forall a in A_t: objective_vector(a) exists` |
| R3 | Selected action must come from the candidate set. | `selected_action.action_id in candidate_actions.action_id` |
| R4 | Policy regime must be declared. | `policy_regime in PolicyRegime` |

### Derivations

| ID | Derivation | Formula |
| --- | --- | --- |
| C1 | Weighted score | `sum(weight_i * objective_i)` for `weighted_sum` regime. |
| C2 | Frontier membership | `not exists b: v(b) strictly dominates v(a)` for `pareto_guided` regime. |
| C3 | Dominated selection flag | `selected_action not in ParetoFrontier(candidate_actions)`. |

### State Update

Record: `PolicyTraceStep`

Transition: `decision_state_framed` -> `policy_action_selected`

### Success Guarantees

- The selected action is traceable to a candidate action.
- The policy trace records the regime and relevant derivation notes.
- No claim support is inferred from selection alone.

### Failure Outcomes

| Condition | Result |
| --- | --- |
| Missing policy regime | Block row capture. |
| Missing objective vector | Block selection or mark fixture invalid. |
| Selected action not in candidate set | Validation failure. |

---

## Action: CaptureRunRow

Type: Action (state-changing)

Initiator: research runner or fixture generator

Trigger: selected policy action is ready to be logged.

### Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `experiment_id` | `ExperimentId` | yes | Experiment receiving the row. |
| `decision_state` | `DecisionState` | yes | Decision state used for the policy action. |
| `selected_action` | `SelectedAction` | yes | Selected action and reason. |
| `policy_trace` | `PolicyTraceStep[]` | yes | Trace emitted by the policy regime. |
| `run_metadata` | `object` | yes | Model, prompt hash, operator, timestamp, token/latency metadata. |
| `evidence_class` | `EvidenceClass` | no | Fixture, dry-run, or live evidence marker. |

### Constraints

| ID | Constraint | Formal Expression |
| --- | --- | --- |
| R1 | Common required schema fields must be present. | `COMMON_REQUIRED subset row.keys` |
| R2 | Experiment-specific fields must be present. | `EXPERIMENT_FIELDS[experiment_id] subset row.keys` |
| R3 | Synthetic fixtures cannot update evidence status. | `evidence_class != live_experiment -> no claim upgrade` |

### Derivations

| ID | Derivation | Formula |
| --- | --- | --- |
| C1 | `token_cost` | `sum(tokens across decision episode)` |
| C2 | `latency_ms` | `end_time - start_time` |
| C3 | `protocol_deviations` | `observed deviations from protocol checklist` |

### State Update

Record: `MOGTRunRow`

Transition: `policy_action_selected` -> `run_row_captured`

### Success Guarantees

- Row can be appended to an experiment bundle data file.
- Row can be checked by `ValidateRunJsonl`.
- Evidence class remains explicit when available.

### Failure Outcomes

| Condition | Result |
| --- | --- |
| Missing run metadata | Validation failure. |
| Missing experiment-specific field | Validation failure. |
| Live-run field absent during live execution | Block claim adjudication. |

---

## Action: ValidateRunJsonl

Type: Action (state-changing in validation state, no experiment execution)

Initiator: operator, task-session, or research evidence harness

Trigger: JSONL fixture or run data is available for validation.

### Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `jsonl_path` | `Path` | yes | JSONL file to validate. |
| `schema_path` | `Path` | yes | `experiments/schema/mogt-run.schema.json`. |
| `mode` | `ValidationMode` | no | Fixture, dry-run, or live-data validation context. |

### Constraints

| ID | Constraint | Formal Expression |
| --- | --- | --- |
| R1 | JSONL must contain at least one object row. | `row_count >= 1` |
| R2 | Every row must pass common field checks. | `forall row: COMMON_REQUIRED subset row.keys` |
| R3 | Policy regime and objective vector are blocker fields. | `policy_regime exists and objective_vector exists` |
| R4 | Scores must be normalized. | `forall score: 0 <= score <= 1` |

### Derivations

| ID | Derivation | Formula |
| --- | --- | --- |
| C1 | Validation verdict | `pass if error_count == 0 else fail` |
| C2 | Error list | `ordered validation errors by line and field` |

### State Update

Record: `ValidationResult`

Transition: `run_row_captured` -> `validated` or `validation_failed`

### Success Guarantees

- Passing rows satisfy the first MOGT schema/validator contract.
- Failing rows produce field-level errors.
- Validation does not run live experiments.

### Failure Outcomes

| Condition | Result |
| --- | --- |
| Invalid JSON | Fail with line-level parse error. |
| Missing blocker field | Fail with field-level error. |
| Malformed score or metric | Fail with field-level error. |

---

## Read View: EvidenceReadinessView

Type: Read View (no mutation)

Consumer: operator, research evidence harness, publication pipeline.

### Query Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `experiment_id` | `ExperimentId` | no | Filter readiness by experiment. |
| `evidence_class` | `EvidenceClass` | no | Filter fixture/dry-run/live rows. |

### Read Rules

| ID | Rule | Formal Expression |
| --- | --- | --- |
| Q1 | Synthetic fixture readiness is not claim readiness. | `synthetic_fixture -> schema_ready only` |
| Q2 | Live evidence readiness requires validated data and result summary. | `live_experiment -> validated_data && result_summary` |
| Q3 | Claim upgrade requires approved analysis task. | `claim_status_change -> approved_analysis_result` |

### Output

| Field | Type | Description |
| --- | --- | --- |
| `schema_ready` | `boolean` | Whether schema and validator proof exists. |
| `fixture_ready` | `boolean` | Whether dry-run fixture mechanics are ready. |
| `live_run_approved` | `boolean` | Whether live experiment execution is approved. |
| `claim_update_allowed` | `boolean` | Whether evidence status may change. |

### Performance Notes

- Expected latency: local file scan only.
- Expected size: one project research pack.
- Cache or freshness contract: recompute after each SWU result.

---

## Action: MOGTDecide

Type: Action (state-changing in the agent runtime)

Initiator: orchestrator or agent runtime

Trigger: the agent loop reaches a conversation turn where multiple next actions
are available or where the next action needs an auditable tradeoff decision.

### Input

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `conversation_context` | `ContextHandle` | yes | Current conversation state. |
| `candidate_actions` | `CandidateAction[]` | yes | Actions the runtime can actually execute. |
| `objectives` | `ObjectiveName[]` | yes | Active objective dimensions. |
| `constraints` | `Constraint[]` | yes | Hard gates evaluated before optimization. |
| `policy_regime` | `PolicyRegime` | yes | Runtime selection rule. |
| `regime_parameters` | `object` | no | Weights, tie-breaker, or bargaining bounds. |

### Constraints

| ID | Constraint | Formal Expression |
| --- | --- | --- |
| R1 | Hard constraints run before policy selection. | `F_t = {a in A_t | K_t(a, s_t) == pass}` |
| R2 | Empty feasible set must not produce a normal action. | `len(F_t) == 0 -> runtime_status in {blocked, escalated}` |
| R3 | Runtime must emit a receipt. | `MOGTDecide -> RuntimeDecisionReceipt` |

### Derivations

| ID | Derivation | Formula |
| --- | --- | --- |
| C1 | Feasible set | `F_t = {a in A_t | constraints_pass(a, s_t)}` |
| C2 | Selected action | `(a_t*, trace_t) = pi(s_t, R_t, A_t, O_t, K_t, V_t, U_t)` |
| C3 | Runtime receipt | `receipt = record(state, regime, scores, selected_action, trace, overhead)` |

### State Update

Record: `RuntimeDecisionReceipt`

Transition: `conversation_turn_ready` -> `action_selected_for_execution`

### Success Guarantees

- Selected action is executable by the runtime.
- The policy regime and principal tradeoff are recorded.
- The receipt can be converted into a `MOGTRunRow` for experiments.

### Failure Outcomes

| Condition | Result |
| --- | --- |
| No feasible action remains | Emit `blocked` or `escalated` receipt. |
| Objective estimates are missing | Block selection or use declared fallback regime. |
| Policy-specific trace is missing | Receipt is invalid for fixture readiness. |
