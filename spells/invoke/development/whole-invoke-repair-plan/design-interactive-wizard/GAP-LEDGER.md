# Interactive Design Wizard Gap Ledger

| Gap | State | Severity | Owner | Repair route | Effect |
| --- | --- | --- | --- | --- | --- |
| `GAP-WIZ-001`: no admitted Wizard Design exists | open blocker | critical | Invoke Design owner | W0 through `invoke design` | Blocks Plan v2 authoring and all implementation. |
| `GAP-WIZ-002`: current Invoke package closure still has mixed-owner history | open blocker | high | Invoke package-closure owner | Fresh selective preview and exact owner classification in W0 | Blocks a fresh implementation baseline and later generated sync. |
| `GAP-WIZ-003`: historical thread evidence may be missing, compacted, or unreadable | permanent condition | high | evidence-boundary owner | Classify expected refs as unavailable and route affected questions | Blocks finalize only when the missing evidence class is required. |
| `GAP-WIZ-004`: direct chat push transport is not owned | deferred | medium | future chat-integration owner | Separate post-v1 Design | Does not block v1 native-agent rendering; no direct transport claim. |
| `GAP-WIZ-005`: retention and destructive cleanup policy is not selected | deferred | medium | session-policy owner | Separate policy decision before adding purge commands | V1 keeps caller-owned session roots and performs no automatic deletion. |
| `GAP-WIZ-006`: exact future schema and target baselines are not frozen | open blocker | high | Wizard Design and Plan owners | Freeze after W0 Design admission | Blocks Task Session or other mutation-capable handoff. |

## Resolved Design Tensions

| Tension | V1 resolution |
| --- | --- |
| Should the deterministic CLI write semantic questions? | No. The native agent authors them; the CLI validates and persists them. |
| How does the question appear in chat? | The native agent renders the exact canonical CLI question record. |
| Should the wizard replace the stateless Design pipeline? | No. It freezes a complete request for the existing `check` and explicit `author` stages. |
| Where is session state stored? | Only in an explicit caller-selected session root. |
| How are terminal/chat races handled? | Expected revisions plus immutable revisions; stale writers fail closed. |
| Can evidence completeness be universal? | No. Completeness is always relative to a declared finite boundary. |

No gap is waived. Deferred gaps cannot be silently pulled into v1 implementation.
