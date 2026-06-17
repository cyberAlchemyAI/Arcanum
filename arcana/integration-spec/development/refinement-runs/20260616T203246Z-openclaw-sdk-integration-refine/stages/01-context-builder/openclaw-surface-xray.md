# X-Ray: OpenClaw Integration Surface

Status: pass

```text
Host Operation/Query
  -> host-owned Integration Port
  -> OpenClaw Connector
  -> OpenClaw external agent-runtime resource
  -> provider-backed model/tool/session runtime
```

## Layers

| Layer | Owner | Notes |
| --- | --- | --- |
| Host application meaning | DomainSpec | Uses existing operations, queries, interfaces, mappings, policies, workflows, sagas, and events. |
| Integration boundary | IntegrationSpec L0 | Owns port, connector, trust, session, runtime-zone, failure, mapping, and evidence obligations. |
| OpenClaw external app surface | OpenClaw Gateway/RPC or CLI | Gateway/RPC is the current default for external apps; CLI is useful for one-shot probes and scripts. |
| OpenClaw plugin surface | OpenClaw Plugin SDK | For code running inside OpenClaw, not host application code. |
| Runtime/config state | OpenClaw runtime | `~/.openclaw` remains external runtime state, not workspace source. |

## Key Boundary Decision

The host system must not depend directly on OpenClaw command syntax, Gateway method details, or plugin SDK imports from domain/application code. It depends on a host-owned port; the connector absorbs OpenClaw details.
