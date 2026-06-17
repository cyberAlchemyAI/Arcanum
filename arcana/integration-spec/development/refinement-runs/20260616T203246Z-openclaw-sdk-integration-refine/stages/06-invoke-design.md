# Invoke Design: OpenClaw Integration L0

Status: pass
Owner capability: invoke
Mode: design

## Authoring Shape

Every OpenClaw integration record should include:

| Field | Required content |
| --- | --- |
| `host_operation_or_query` | DomainSpec `Operation` or `Query` that needs OpenClaw work. |
| `host_interface` | Host API, command, job, UI action, or event consumer that triggers the port. |
| `integration_port` | Stable host contract such as `RunAgentTurn`, `RunModelProbe`, `RunGatewaySmoke`, `CheckGatewayStatus`, `CancelRun`, or `InspectRuntime`. |
| `resource.kind` | `AgentRuntimeResource` as a local specialization of `ExternalResource`, unless governance chooses a smaller term. |
| `connector.strategy` | `gateway_rpc`, `cli_subprocess`, or `plugin_sdk_inside_openclaw`. |
| `openclaw_surface` | Gateway/RPC, CLI agent/message/infer, or plugin SDK subpath. |
| `invocation_mode` | Raw infer, agent turn, gateway smoke, status check, cancellation, inspection, or domain workflow. |
| `trust_boundary` | Single operator, trusted team, mixed-trust, or external users. |
| `session_policy` | Fresh session, durable session, per-user session, no-session, or explicit session mapping. |
| `runtime_zone` | OpenClaw-owned config/runtime state such as `~/.openclaw`, never workspace source. |
| `auth_config_policy` | Who owns provider credentials, Gateway auth, config validation, and repair. |
| `timeout_cancellation` | Timeout, kill/cancel method, retry behavior, and stuck-run handling. |
| `output_contract` | JSON envelope, Gateway events, stdout/stderr, exit code, normalized result/error. |
| `failure_contract` | Gateway down, auth missing, invalid config, timeout, malformed output, nonzero exit, redaction failure. |
| `mappings` | Host request to OpenClaw command/RPC and OpenClaw result/events to host DTO/event model. |
| `policies` | Retry, idempotency, rate limit, circuit breaker, fallback, redaction, observability. |
| `evidence_anchors` | Status, health, smoke, contract fixtures, failure fixtures, observability, redaction checks. |

## Local Relations

These relations are IntegrationSpec-local only:

- `operation_uses_integration_port`
- `integration_port_implemented_by_adapter`
- `adapter_connects_to_resource`
- `resource_governed_by_decision`
- `policy_attaches_to_boundary`
- `mapping_transforms_external_shape`
- `evidence_anchor_covers_obligation`

Do not add them to DS-D2 in this run.
