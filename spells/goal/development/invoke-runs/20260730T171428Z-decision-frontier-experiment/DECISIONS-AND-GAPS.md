# Decisions And Gaps

## Decisions

| ID | Decision | Basis |
| --- | --- | --- |
| DFE-D-001 | Model a decision-discovery DAG, not an execution DAG. | preserves Task Session and Goal execution ownership |
| DFE-D-002 | Place the fixture experiment under Goal development. | Goal currently consumes a frontier and is the smallest bounded host |
| DFE-D-003 | Keep Craft authoritative; use candidate fixtures and proposal outputs only. | prevents a second ledger |
| DFE-D-004 | Use digest-bound compare-and-set claims. | makes stale and competing work observable |
| DFE-D-005 | Treat fog and out-of-scope as retained states, not deletion. | preserves uncertainty and scope history |
| DFE-D-006 | Route lifecycle review to Spellcraft. | the target is an existing spell extension |
| DFE-D-007 | Defer tracker projection entirely. | it adds integration risk without testing the core hypothesis |
| DFE-D-008 | Use a serial work graph. | planned units touch shared schemas and reducer contracts |

## Open Gaps

| ID | Gap | Effect | Owner / route |
| --- | --- | --- | --- |
| DFE-G-001 | No fixture behavior has been implemented or observed. | blocks adoption claims | selected Task Sessions after Spellcraft approval |
| DFE-G-002 | Canonical Craft representation of claim/fog remains undecided. | blocks canonical integration | later Define/Design refresh if fixtures pass |
| DFE-G-003 | Claim expiry and recovery policy is intentionally absent from L0. | blocks concurrent production use | later lifecycle design |
| DFE-G-004 | No evidence shows developer-time or quality improvement. | blocks capability-benefit claim | later Experiment Harness comparison |
| DFE-G-005 | No SWU is selected. | blocks all implementation mutation | user plus Spellcraft |
| DFE-G-006 | Current Craft and Goal contracts lack the candidate claim, fog, and dependency shape needed for meaningful adapters. | blocks adapter implementation in this work pack | later Spellcraft-owned Invoke Design refresh |
