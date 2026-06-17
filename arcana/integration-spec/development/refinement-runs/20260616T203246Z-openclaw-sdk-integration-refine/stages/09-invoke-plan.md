# Invoke Plan: Next Routes

Status: pass
Owner capability: invoke
Mode: plan

## Recommended Sequence

1. Create a public-safe `INTEGRATION-BOUNDARY-DISCIPLINE.md` L0 artifact.
2. Fill an OpenClaw example using Gateway/RPC as the default external-app path and CLI as a probe path.
3. Add fixture sketches for pass/flag/block validation.
4. Only then consider a candidate DomainSpec `integrations.md` aspect.
5. Only after one or two examples stabilize, route formula-level validator design.

## Minimum OpenClaw Example

| Port | Connector | Evidence |
| --- | --- | --- |
| `CheckGatewayStatus` | Gateway health or CLI status wrapper | status/version/health receipt |
| `RunGatewaySmoke` | Gateway/RPC or `openclaw infer model run --gateway --json` probe | gateway routing smoke |
| `RunModelProbe` | CLI `openclaw infer ... --json` | normalized JSON envelope fixture |
| `RunAgentTurn` | Gateway/RPC agent run or CLI agent command | result/error/event contract |

## Validator Fixture Candidates

- pass: complete Gateway/RPC integration record.
- pass: complete CLI subprocess probe record.
- block: missing host-owned port.
- block: missing trust boundary.
- block: session IDs treated as auth.
- block: runtime zone treated as workspace source.
- block: canonical DomainSpec `Adapter` used for OpenClaw connector.
- flag: no cancellation behavior.
- flag: no malformed-output fixture.
- flag: evidence anchors named but not linked.
