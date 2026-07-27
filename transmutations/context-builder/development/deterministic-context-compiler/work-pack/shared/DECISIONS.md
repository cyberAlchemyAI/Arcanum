# Cross-Task Decisions

| Decision ID | Decision | Applies To | Revisit Trigger |
| --- | --- | --- | --- |
| PD-001 | Python standard-library tooling is the L0 implementation default. | SWU-DCC-001 and SWU-DCC-002 | repository runtime constraints reject it |
| PD-002 | Canonical JSON uses sorted keys, UTF-8, LF, and one trailing newline. | all machine receipts | an existing owner contract requires a different canonical form |
| PD-003 | SHA-256 binds source, object, payload, and receipt bytes. | cache and validation | owner standard changes |
| PD-004 | Exact Markdown heading selection and whole-short-file selection are the L0 selector set. | SWU-DCC-002 | real benchmark sources cannot be represented |
| PD-005 | Bytes are always recorded; tokenizer counts are optional and named. | SWU-DCC-005 | none; this is an evidence invariant |
| PD-006 | Full payload is default; delta requires an exact base receipt. | SWU-DCC-006 | none; this is a safety invariant |
| PD-007 | Canonical Context Builder files do not change until L3 evidence. | SWU-DCC-008 | Sigil Development explicitly narrows the route |
| PD-008 | `SWU-DCC-001` is the first candidate, but `selected_swu` remains `none`. | execution admission | explicit lifecycle-owner selection |
