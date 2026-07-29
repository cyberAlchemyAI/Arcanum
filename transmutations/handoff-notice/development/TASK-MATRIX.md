# Task Matrix

| ID | Complexity | Scenario | Expected Output | Status |
| --- | --- | --- | --- | --- |
| HN-LOW-001 | low | Publish and resolve a complete product-neutral handoff. | Exact code/path/digest round-trip, open call preserved, authority disclaimer present. | automated |
| HN-LOW-NEG-001 | low | Publish without a boundary. | Fail before allocating a locator or index. | automated |
| HN-MED-001 | medium | Resolve malformed, unknown, artifact-drifted, index-drifted, or wrong-repository locators. | Distinct fail-closed diagnostics. | automated |
| HN-MED-002 | medium | Create a resolution that supersedes an open notice. | Old notice stays immutable and reports the new superseding code. | automated |
| HN-MED-003 | medium | Commit a notice locally and inspect it. | `committed-local`; remote availability remains `unverified`. | automated |
| HN-COMPLEX-001 | complex | Force a locator-prefix collision. | Deterministically extend the code without overwriting the first entry. | automated |
| HN-COMPLEX-002 | complex | Include a next-route hint with no authorization. | Preserve the hint and return its owner without dispatch or execution. | automated |
| HN-COMPLEX-003 | complex | Request commit, push, or external notification through this sigil. | Return the separate owner boundary; do not perform delivery. | lifecycle fixture |
