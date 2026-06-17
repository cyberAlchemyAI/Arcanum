# Subagent Receipt: OpenClaw Runtime Mapper

role_id: openclaw-runtime-mapper
agent_id: 019ed227-abd5-7933-ae8e-3738144f82da
dispatch_id: refine-20260616T203246Z-openclaw-sdk-integration
status: pass-readonly
spawn_status: spawned
join_status: completed
close_status: closed

## Sources Considered

- Current refine seed and dispatch route.
- Official OpenClaw inference CLI, Gateway external apps, Plugin SDK, Gateway security, and Gateway configuration docs.
- Private local OpenClaw evidence was not opened by the subagent.

## Findings

- OpenClaw should be modeled as an IntegrationSpec external runtime/resource behind a host-owned port and connector.
- External applications should use Gateway protocol/RPC today when they need run lifecycle, events, cancellation, sessions, or resource inspection.
- CLI shell-out is valid for one-shot scripts and probes.
- Plugin SDK is for code running inside OpenClaw, not external host apps.
- Session IDs are routing selectors, not authorization.
- Runtime/config ownership belongs to OpenClaw.

## Recommended Model

- `resource.kind`: `AgentRuntimeResource` as a specialized `ExternalResource`.
- `connector.strategy`: `gateway_rpc`, `cli_subprocess`, or `plugin_sdk_inside_openclaw`.
- `ports`: `RunRawInference`, `RunAgentTurn`, `RunGatewaySmoke`, `CheckGatewayStatus`, `CancelRun`, `InspectRuntime`.

## Boundary Warnings

- Do not add fictional OpenClaw npm SDK dependencies.
- Do not vendor OpenClaw config, credentials, runtime state, transcripts, or private receipts into public examples.

## Residue

- Parent should decide whether examples default to Gateway/RPC or CLI. Recommendation: Gateway/RPC for external apps; CLI for minimal probes.
