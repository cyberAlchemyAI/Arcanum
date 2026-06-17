# Refine Seed Proposal: OpenClaw SDK Integration Modeling

Status: strategy-proposal
Run ID: 20260616T203246Z-openclaw-sdk-integration-refine
Dispatch ID: refine-20260616T203246Z-openclaw-sdk-integration
Target: `arcanum/arcana/integration-spec`
Preset: full
Research mode: bounded-research

## Operator Intent

Refine how we would model an integration where a system wants to use the OpenClaw SDK or CLI/gateway surface to perform AI-agent or inference work.

The concrete question is:

> If I want to use OpenClaw SDK to do some integration in any system, how would we model this?

## Target Resolution

This run is scoped as an Integration Boundary modeling refinement, not an implementation.

Allowed now:

- Create refinement evidence under this run folder.
- Model OpenClaw as an external integration resource / provider boundary.
- Reuse prior IntegrationSpec findings and DomainSpec taxonomy boundaries.

Deferred:

- Creating `arcanum/arcana/integration-spec/SKILL.md`.
- Mutating `arcanum/definitions/*`.
- Adding a DomainSpec `integrations.md` template.
- Implementing an OpenClaw connector in any product.

## Local Evidence

- Prior IntegrationSpec review selected **Integration Boundary Discipline first** and found that DomainSpec does not currently model provider/resource topology, `Port -> Adapter -> External Resource`, cache/source-of-truth, data-store selection, or evidence/proof relationships as canonical graph vocabulary.
- Operator-supplied local bridge evidence models OpenClaw as a subprocess/gateway bridge. It mints fresh session ids, checks gateway health at `127.0.0.1:18789/health`, runs `openclaw agent --agent ... --session-id ... -m ... --json`, streams stdout/result/exit/error events, and exposes `openclaw infer model run --gateway`.
- Operator-supplied local UI evidence states the UI never owns LLM logic: it watches files, shells out to OpenClaw, and streams results back.
- Operator-supplied local Node bridge evidence models `runOpenClaw(args)`, status via `openclaw --version`, gateway smoke via `openclaw infer model run --gateway --model ... --prompt ... --json`, normalized JSON output, timeout handling, and status/run API handlers.
- Operator-supplied runtime-zone evidence states `~/.openclaw/` is the runtime zone and does not contain workspace files.

## Bounded External Research Baseline

- OpenClaw docs say external apps should use Gateway WebSocket/RPC today, and warn that there is no public npm client package yet.
- OpenClaw docs scope `openclaw/plugin-sdk/*` to plugin code running inside OpenClaw, not external apps, scripts, dashboards, CI jobs, or IDE extensions.
- OpenClaw docs describe `openclaw infer` as a canonical headless surface for provider-backed inference workflows, with `--json` useful for scripts and automation.
- OpenClaw docs say local `model run` is a lean one-shot provider completion, while `model run --gateway` exercises gateway routing, saved auth, provider selection, and embedded runtime without full agent context, tools, memory, or session transcript.
- OpenClaw security docs define the trust model as one trusted operator boundary per gateway; mixed-trust teams should split gateways or OS users/hosts.
- OpenClaw configuration docs say `~/.openclaw/openclaw.json` is strictly schema-validated, invalid config prevents gateway boot or hot reload, and `doctor --fix` repairs/restores last-known-good config.

## Provisional Model

Do not model OpenClaw as a DomainSpec `Adapter`. In DomainSpec, `Adapter` is UI-boundary vocabulary.

Model it as:

```text
DomainSpec Operation/Query
  -> Integration Boundary: OpenClaw AI Runtime Boundary
  -> Integration Port: RunAgentTurn / RunModelProbe / RunGatewaySmoke / CheckGatewayStatus
  -> Integration Adapter or Connector: OpenClawConnector
  -> Integration Resource: OpenClaw Gateway/RPC or CLI + configured agent/model runtime
  -> Integration Decision: gateway vs CLI vs inside-OpenClaw plugin, agent turn vs raw infer, session policy, trust boundary
  -> Integration Policies: timeout, auth, session isolation, retry, output parsing, tool-authority, fail-closed behavior
  -> Integration Mapping: host request -> OpenClaw RPC call or CLI args; OpenClaw events/JSON/stdout -> host result/event model
  -> Integration Evidence: status check, gateway smoke, e2e smoke, contract fixtures, error fixtures, observability
```

## DomainSpec Reuse

Use DomainSpec for the host application semantics:

- `Operation`: user/system action that asks for OpenClaw work, such as `RunScout`, `DraftSection`, `GatewaySmoke`, or `RunAgentTurn`.
- `Query`: status/read model such as `GetOpenClawStatus` or `GetAgentRunResult`.
- `Interface`: host API surface such as `POST /api/openclaw/run` or `GET /api/openclaw/status`.
- `Mapping`: request/response/event transformations between host shapes and OpenClaw CLI JSON/stdout.
- `Policy`: timeout, retry, auth, routing, fail-closed, and session policy.
- `Workflow`: multi-step orchestration around OpenClaw invocation.
- `Event`: `OpenClawRunStarted`, `OpenClawStdoutReceived`, `OpenClawRunCompleted`, `OpenClawRunFailed`.

Keep local to Integration Boundary Discipline:

- OpenClaw connector / integration adapter.
- External resource / gateway runtime / CLI runtime.
- Session namespace.
- Trust boundary.
- Config ownership.
- Evidence anchors and smoke-test obligations.

## Integration Decision Record Fields

For any OpenClaw integration, require:

| Field | Why it matters |
| --- | --- |
| OpenClaw surface | Gateway/RPC for external apps, CLI for probes/scripts, plugin SDK only inside OpenClaw. |
| Invocation mode | One-shot raw inference, sessionful agent turn, gateway smoke, or domain-specific workflow. |
| Host-owned port | The application dependency contract, independent of OpenClaw implementation details. |
| Connector strategy | Subprocess wrapper, SDK client, gateway HTTP client, or plugin bridge. |
| Trust boundary | Single operator, company team, mixed trust, or external users; determines gateway split. |
| Runtime zone | `~/.openclaw` or configured runtime root; must not become workspace source. |
| Session policy | Fresh session per request, durable session, per-user session, or explicit no-session. |
| Auth/config policy | Provider credentials, gateway auth, config path, strict validation, repair path. |
| Timeout/cancellation | Timeouts, kill behavior, retry policy, and stuck-run handling. |
| Output contract | JSON envelope, stdout lines, SSE events, result/error/exit model. |
| Failure contract | Gateway down, invalid config, auth missing, timeout, malformed JSON, nonzero exit. |
| Evidence | Version/status check, health check, smoke test, e2e integration test, failure fixtures. |

## Candidate Refinement Questions

1. Should OpenClaw be modeled as a generic `ExternalResource` or as a specialized `AgentRuntimeResource`?
2. Is the recommended connector surface CLI-first, gateway HTTP-first, or SDK-first?
3. Which OpenClaw operations are generic enough for IntegrationSpec examples: `status`, `gateway_smoke`, `run_agent_turn`, `run_model_probe`?
4. What is the smallest useful `integrations.md` example for a host application using OpenClaw?
5. What validator fixtures prove the model catches the important mistakes?

## Done Criteria For This Proposal Step

- Seed proposal is written.
- Dispatch route is written and validator-checked.
- Runtime handoff records awaiting confirmation.
- Response asks for confirmation before running native stages or spawning subagents.
