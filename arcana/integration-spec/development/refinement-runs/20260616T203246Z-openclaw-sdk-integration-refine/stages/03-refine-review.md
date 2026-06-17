# Interrogation Review: Define

Status: pass
Owner capability: interrogation
Mode: refine-review

## Review Verdict

The definition is useful if it keeps the dependency contract host-owned and keeps OpenClaw details behind an integration connector.

## Confirmed

- DomainSpec should model host/application semantics.
- IntegrationSpec L0 should model provider/resource/session/runtime/evidence mechanics.
- `Adapter` is overloaded and risky because DomainSpec currently uses it for UI-boundary shape transformation.
- OpenClaw plugin SDK is not a host-app dependency path.

## Repairs Applied

- Prefer `Connector`, `Provider Adapter`, or `Integration Adapter` for local implementation vocabulary.
- State Gateway/RPC as the richer external-app default.
- Keep CLI subprocess as a minimal probe/script path.
- Require trust boundary and session policy explicitly.

## Residue

Whether `AgentRuntimeResource` should become an IntegrationSpec-local specialization or remain only a labeled `ExternalResource` is a later governance decision.
