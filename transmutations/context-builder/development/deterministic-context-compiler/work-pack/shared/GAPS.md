# Cross-Task Gaps

| Gap ID | State | Description | Owning SWU Or Route | Closure Evidence |
| --- | --- | --- | --- | --- |
| G-001 | open | No compiler, schemas, or deterministic fixtures exist. | SWU-DCC-001 through SWU-DCC-004 | passing deterministic fixture receipts |
| G-002 | open | Current packs do not require per-excerpt hashes or cache receipts. | SWU-DCC-002 and SWU-DCC-008 | validated receipt plus lifecycle-owned contract diff |
| G-003 | open | Exact tokenizer/runtime usage baseline is absent. | SWU-DCC-005 and SWU-DCC-007 | separated measurement and paired live receipts |
| G-004 | deferred | Provider-specific prompt-cache behavior is unspecified. | future runtime-adapter route | separately approved adapter contract |
| G-005 | open | Reusable behavior and lifecycle readiness are unproven. | SWU-DCC-007 and Sigil Development | experiment and lifecycle receipts |
| G-006 | deferred | Cache cleanup and long-term retention policy are unspecified. | future consumer-owned route | data-lifecycle decision |

Open gaps prevent corresponding claims. Deferred gaps do not block L0 because
their behavior is excluded from the layer.
