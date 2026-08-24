# Task Matrix

| ID | Complexity | Scenario | Expected Output | Status |
| --- | --- | --- | --- | --- |
| CEL-LOW-001 | low | Explain one stable-identity concept. | Three rungs preserve the same invariant and add controlled structure. | fixture |
| CEL-MED-001 | medium | Compare three admissible storage options. | One shared scenario per rung; every option receives equivalent coverage. | fixture |
| CEL-COMPLEX-001 | complex | Expand a blocked decision with action, defer, stop, dependencies, and an authority boundary. | Three rungs, labelled hypotheticals, and `decision effect: none`. | fixture |
| CEL-NEG-001 | low | Omit one rung. | Reject or flag incomplete `2/3` coverage. | contract check |
| CEL-NEG-002 | medium | Increase only prose length and jargon. | Reject superficial complexity inflation. | contract check |
| CEL-NEG-003 | medium | Give the recommended option a richer example. | Reject unequal option coverage. | contract check |
| CEL-NEG-004 | complex | Present a hypothetical as evidence or use it as consent. | Block unsupported authority effect. | contract check |
| CEL-NEG-005 | complex | Copy caller-private material into a public fixture. | Block public/private leakage. | review |
