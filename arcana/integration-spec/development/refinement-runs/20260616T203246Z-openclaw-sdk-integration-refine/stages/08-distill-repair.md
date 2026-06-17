# Distill Repair

Status: pass
Owner capability: distill

## Repairs

- Changed external host-app default from SDK-first to Gateway/RPC-first.
- Scoped plugin SDK to inside-OpenClaw plugins.
- Preserved CLI subprocess as a supported minimal probe/script connector.
- Added mandatory failure contracts and evidence fixtures.
- Kept local relation syntax outside canonical DomainSpec relationships.

## Residue Ledger

| Residue | Owner | Next route |
| --- | --- | --- |
| Should L0 name `AgentRuntimeResource` or only `ExternalResource`? | integration-spec governance | decision-gate or definitions-governance after examples stabilize |
| Should first public example be Gateway/RPC or CLI? | integration-spec authoring | default Gateway/RPC, include CLI as secondary fixture |
| Should this become an `integrations.md` aspect? | DomainSpec authoring route | after L0 field schema is stable |
| Should a validator exist now? | formula route | after one filled example and fixtures exist |
