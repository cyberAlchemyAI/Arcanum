# Subagent Receipt: Data Resource Selection Mapper

role_id: data-resource-selection-mapper
agent_id: 019ed231-6bb8-7fa3-96a5-d09212d74bee
dispatch_id: refine-20260616T204823Z-database-selection-migration-commands
status: pass-with-residue
spawn_status: spawned
join_status: completed
close_status: closed

## Sources Considered

- Prior public IntegrationSpec refinement and gap review.
- Prior OpenClaw integration refine result.
- DomainSpec taxonomy and definitions.
- Official AWS and Microsoft/Azure data-store selection guidance.

## Findings

- Data-store selection should be workload-led: access patterns, data shape, consistency, latency, throughput, volume/growth, durability, retention, and governance come before technology choice.
- IntegrationSpec should support polyglot choices only when access patterns, lifecycle, or latency/throughput needs diverge.
- Cache, search, analytics, vector, object/archive, time-series, stream/log, graph, ledger, document, key-value, relational, and wide-column choices should be resource-family roles with authority and evidence obligations, not canonical DomainSpec meta-types.

## Recommended Model

Add an IntegrationSpec-local `Integration Data Resource Decision Record` with fields for resource role/family, source-of-truth role, workload access patterns, data shape, consistency, atomicity, latency/throughput, growth, lifecycle, migration/backfill, cache/search/analytics/vector role, security/governance, failure modes, alternatives rejected, and evidence anchors.

## Boundary Warnings

- Do not mutate DomainSpec definitions.
- Do not let cache/search/analytics/vector stores silently become source-of-truth.
- Validator checks required fields and evidence anchors only.

## Residue

Fixture set needed: missing source-of-truth, cache without invalidation, search as primary store, vector index without rebuild/versioning, analytics store without lineage, and unsupported taxonomy promotion.
