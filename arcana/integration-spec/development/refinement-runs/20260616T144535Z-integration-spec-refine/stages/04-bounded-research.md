# Bounded Research: IntegrationSpec Comparisons

Status: pass
Mode: bounded-research
Owner: refine

## Research Decision

Bounded external research was selected by the operator. External sources are comparison evidence only; local Arcanum and DomainSpec artifacts remain authoritative for this run.

## Findings

| Source | Finding | IntegrationSpec Implication |
| --- | --- | --- |
| OpenAPI Initiative, `https://www.openapis.org/` | OpenAPI is a formal standard for describing HTTP APIs and supports understanding, code generation, tests, and design standards. | Reuse it for HTTP wire contracts. IntegrationSpec should decide when an HTTP boundary needs OpenAPI and what application-layer policies/evidence surround it. |
| AsyncAPI, `https://www.asyncapi.com/docs/concepts/asyncapi-document` | AsyncAPI documents describe event-driven APIs and serve as communication contracts between senders and receivers. | Reuse it for channels, messages, and protocol bindings. IntegrationSpec should govern ownership, retries, ordering, dead letters, and domain mapping. |
| CloudEvents, `https://cloudevents.io/` | CloudEvents describes event data in a common way across services, platforms, and systems. | Reuse it for event envelopes where portability matters. DomainSpec `Event` remains the domain fact; CloudEvents owns transport metadata. |
| Ports and Adapters, `https://alistair.cockburn.us/hexagonal-architecture` | The application communicates over ports to external agencies, with multiple adapters per port and tests/mocks as substitutes. | IntegrationSpec should protect application-owned ports and keep vendor SDK/database clients outside the application core. |
| Azure Cache-Aside, `https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside` | Cache-aside improves performance but needs explicit consistency, lifetime, stale-data, local/shared cache, and sensitivity decisions. | Cache strategy records are first-class integration decisions. |
| Azure Data Store Choices, `https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/data-stores-getting-started` | Store choice depends on data format, purpose, access method, relationships, consistency, schema flexibility, concurrency, lifecycle, and movement. | Database selection must be a decision record, not a technology label. |
| AWS Well-Architected purpose-built data stores, `https://docs.aws.amazon.com/wellarchitected/latest/framework/perf_data_use_purpose_built_data_store.html` | Data stores should fit workload needs rather than one-size-fits-all database habits. | IntegrationSpec should record store family fit and accepted trade-offs. |
| Google Cloud Application Integration, `https://cloud.google.com/application-integration` | Integration platforms connect applications, systems, APIs, and data with workflow automation. | iPaaS belongs as an external integration resource or workflow host, not as Arcanum lifecycle authority. |

## Research Synthesis

The space has strong standards for protocol and wire description, and strong architecture guidance for ports, adapters, caches, and data stores. What is missing locally is a governed application-layer envelope that composes them:

```text
use case -> port -> adapter/resource -> standard contract -> policy -> mapping -> evidence
```

## Boundary Decision

Borrow carefully from standards and architecture sources. Do not replace them. Do not promote new Arcanum vocabulary from this research alone.
