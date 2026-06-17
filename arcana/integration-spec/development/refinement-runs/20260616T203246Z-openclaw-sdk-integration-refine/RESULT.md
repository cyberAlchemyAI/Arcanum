# Refine Result: OpenClaw Integration Modeling

Status: pass-with-residue
Run ID: 20260616T203246Z-openclaw-sdk-integration-refine
Dispatch ID: refine-20260616T203246Z-openclaw-sdk-integration
Preset: full
Research: bounded-research

## Final Synthesis

Model OpenClaw as an **IntegrationSpec external agent-runtime resource** behind a host-owned integration port and connector.

Use DomainSpec for the host application's meaning:

- `Operation` or `Query`: why the host needs OpenClaw.
- `Interface`: how host users/jobs/API routes trigger the work.
- `Mapping`: how host requests/results/events transform.
- `Policy`: retry, timeout, auth, routing, fail-closed, redaction, and session rules.
- `Workflow`, `Saga`, `Event`: orchestration and observable state transitions.

Use IntegrationSpec-local vocabulary for the boundary machinery:

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

## OpenClaw-Specific Decision

Gateway/RPC is the recommended default for external apps. Use it when the host needs agent lifecycle, events, result waiting, cancellation, sessions, or runtime inspection.

CLI subprocess is still valid for one-shot automation and smoke probes, especially `openclaw infer ... --json` or CLI agent/message commands.

Plugin SDK belongs to code running inside OpenClaw. Do not model it as the default SDK dependency for an arbitrary host app.

## Required Decision Record Fields

| Field | Required decision |
| --- | --- |
| OpenClaw surface | Gateway/RPC, CLI subprocess, or plugin SDK inside OpenClaw. |
| Invocation mode | Raw infer, agent turn, gateway smoke, status check, cancellation, inspection, or domain workflow. |
| Host-owned port | Stable application contract such as `RunAgentTurn` or `CheckGatewayStatus`. |
| Connector strategy | `gateway_rpc`, `cli_subprocess`, or `plugin_sdk_inside_openclaw`. |
| Resource kind | `AgentRuntimeResource` as local specialization of `ExternalResource`, unless governance chooses the smaller term. |
| Trust boundary | Single trusted operator, trusted team, mixed trust, or external users. |
| Session policy | Fresh, durable, per-user, no-session, or explicit session mapping. |
| Runtime zone | OpenClaw-owned runtime/config state, not workspace source. |
| Auth/config policy | Gateway auth, provider credentials, config validation, and repair owner. |
| Timeout/cancellation | Timeout, cancellation/kill method, retry, stuck-run behavior. |
| Output contract | Gateway events, JSON envelope, stdout/stderr, exit code, normalized result/error. |
| Failure contract | Gateway down, auth missing, invalid config, timeout, malformed output, nonzero exit, redaction failure. |
| Evidence anchors | Version/status, health, smoke, contract fixtures, failure fixtures, observability, redaction checks. |

## Validator Scope

A future validator may check required fields, local relation shape, links, and evidence anchors. It must not claim runtime truth, architecture correctness, or DomainSpec taxonomy promotion.

## Bridge Decisions

| Claim | Decision |
| --- | --- |
| OpenClaw needs explicit integration modeling | promotion-candidate |
| Gateway/RPC as default external-app example | promotion-candidate |
| CLI subprocess as minimal probe path | borrow-carefully |
| Plugin SDK as arbitrary host-app dependency | block |
| `AgentRuntimeResource` local specialization | future-work |
| Canonical DomainSpec `Adapter` for OpenClaw connector | block |
| Runtime receipts as canonical spec truth | block |
| Runtime receipts as task evidence | borrow-carefully |

## Recommended Next Route

Build L0 first:

1. Draft `INTEGRATION-BOUNDARY-DISCIPLINE.md`.
2. Include a filled OpenClaw Gateway/RPC example.
3. Include a secondary CLI probe example.
4. Add pass/flag/block fixtures for missing host port, missing trust/session policy, runtime-zone leakage, missing failure contract, missing evidence anchors, canonical `Adapter` misuse, and runtime-truth promotion.
5. Route `integrations.md` and formula validator work only after the L0 fields stabilize.

## Stage Evidence

| Stage | Status | Artifact |
| --- | --- | --- |
| Context Builder evidence baseline | pass | `stages/01-context-builder/context-pack.md` |
| Invoke Define | pass | `stages/02-invoke-define.md` |
| Interrogation refine-review | pass | `stages/03-refine-review.md` |
| Research decision | pass | `stages/04-bounded-research.md` |
| Distill | pass | `stages/05-distill.md` |
| Invoke Redefine / Design | pass | `stages/06-invoke-design.md` |
| Interrogation refine-design-review | pass-with-residue | `stages/07-refine-design-review.md` |
| Distill Repair | pass | `stages/08-distill-repair.md` |
| Invoke Plan | pass | `stages/09-invoke-plan.md` |
| Final Interrogation | pass-with-residue | `stages/10-final-interrogation.md` |

## Subagent Receipts

| Role | Status | Receipt |
| --- | --- | --- |
| `openclaw-runtime-mapper` | pass | `stages/subagent-receipts/openclaw-runtime-mapper.md` |
| `domainspec-boundary-guardian` | pass | `stages/subagent-receipts/domainspec-boundary-guardian.md` |
| `integration-operability-planner` | pass | `stages/subagent-receipts/integration-operability-planner.md` |

## Residue

- Decide later whether `AgentRuntimeResource` is an IntegrationSpec-local type or only a resource label.
- Do not mutate `arcanum/definitions/*` from this run.
- Do not execute OpenClaw runtime work inside Refine; use task-session for runtime proof.
