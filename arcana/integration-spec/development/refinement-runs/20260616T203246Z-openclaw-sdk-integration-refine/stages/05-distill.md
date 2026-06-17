# Distill: Coherent Unit

Status: pass
Owner capability: distill

## Selected Unit

The smallest coherent unit is a filled Integration Boundary Discipline example for OpenClaw, not a new canonical taxonomy mutation and not a production connector.

## Distilled Model

```text
Host Operation/Query
  -> Integration Boundary
  -> Integration Port
  -> OpenClaw Connector
  -> OpenClaw AgentRuntimeResource
  -> Integration Decision Record
  -> Policies + Mappings
  -> Evidence Anchors + Failure Fixtures
```

## Rejected Alternatives

| Alternative | Reason rejected for this run |
| --- | --- |
| Mutate DomainSpec definitions | The required resource/session/evidence vocabulary is not canonical DomainSpec today. |
| Build connector implementation | Refine is design/planning; runtime implementation belongs to task-session. |
| Default to plugin SDK | Official docs scope plugin SDK to code inside OpenClaw. |
| CLI-only model | Useful for probes, but external apps with lifecycle/events/cancel/session needs should use Gateway/RPC. |

## Recomposition

This unit can later recompose into an `integrations.md` aspect, a validator fixture set, or a small `integration-spec` package proof.
