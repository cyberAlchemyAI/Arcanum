# Implementation Layering

| Layer | Decision | Minimum working unit | Exit evidence |
| --- | --- | --- | --- |
| L0 | Can one operation receipt be canonical, digest-bound, and byte-reproducible? | schema, serializer, fingerprint/digest rules, deterministic fixtures | repeated byte identity and schema validation |
| L1 | Can package-local dry-run attribute baseline, candidate, warning delta, and zero mutation? | full no-write append transition | named dry-run receipts and unchanged filesystem digests |
| L2 | Can sequential apply and faceted new-entry admission preserve conformance? | apply observation plus facet/path/projection validation | failure receipts, legacy compatibility, exact projections |
| L3 | Can the runtime be installed and reproduced without touching consumer-owned state? | manifest sync plus isolated consumer proof | managed-set receipt and installed-consumer proof |

## Non-Regression Guardrails

- Later layers preserve L0 byte determinism.
- Apply remains explicitly sequential and non-atomic.
- New facet fields apply only to new faceted records.
- Legacy entries remain valid and unmoved.
- Generated sync never owns consumer Inventory state.
- No receipt proves currentness or promotion.

## Current Window

Closed. L0 through L3 and terminal recomposition passed; no Task Session unit
is selected. The exclusions and non-regression guardrails remain binding.
