# Bounded Research: OpenClaw Surfaces

Status: pass
Owner capability: refine
Research mode: bounded-research

## Findings

| Source | Finding | IntegrationSpec Implication |
| --- | --- | --- |
| OpenClaw Gateway integrations for external apps | External apps should use Gateway WebSocket/RPC; there is no public npm client package yet; plugin SDK is for code inside OpenClaw. | Default external app examples to Gateway/RPC. Do not invent an SDK package dependency. |
| OpenClaw Inference CLI | `openclaw infer` is a headless automation surface and `--json` emits a stable envelope with `ok`, `capability`, `transport`, `provider`, `model`, `attempts`, `outputs`, and `error`. | CLI connector examples should normalize the JSON envelope and treat stdout parsing as secondary. |
| OpenClaw Gateway security | Gateway host/config state is trusted; mixed-trust teams should split gateways, OS users, or hosts; session ids are routing selectors, not auth tokens. | Trust boundary and session policy are mandatory fields. |
| OpenClaw Gateway configuration | `~/.openclaw/openclaw.json` is the config root; invalid config blocks startup/reload and repair belongs to OpenClaw validation/doctor flows. | Runtime zone and config/auth ownership must stay outside workspace source. |

## Research Decision

External research is sufficient for the modeling question. A live OpenClaw runtime check is deferred to a future task-session.
