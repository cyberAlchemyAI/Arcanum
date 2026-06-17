# Invoke Define: OpenClaw Integration Boundary

Status: pass
Owner capability: invoke
Mode: define

## Definition

An OpenClaw integration is an application-owned dependency boundary in which a host `Operation` or `Query` invokes an external agent-runtime resource through a local integration port and connector.

## Required Components

| Component | Description |
| --- | --- |
| Host use case | The application meaning, expressed through DomainSpec concepts. |
| Integration port | The stable host-owned contract, such as `RunAgentTurn`, `RunModelProbe`, `RunGatewaySmoke`, or `CheckGatewayStatus`. |
| Connector | The implementation boundary that talks to OpenClaw through Gateway/RPC, CLI subprocess, or inside-OpenClaw plugin SDK. |
| Resource | OpenClaw as external runtime, preferably `AgentRuntimeResource` as a specialization of `ExternalResource`. |
| Decision record | The selected surface, trust/session/runtime/config/output/failure/evidence choices. |
| Evidence anchors | Tests, smoke checks, fixtures, and observability records that prove obligations were checked. |

## Non-Goals

- Do not model OpenClaw as canonical DomainSpec `Adapter`.
- Do not make plugin SDK the default for external host apps.
- Do not treat runtime receipts as canonical spec truth.
