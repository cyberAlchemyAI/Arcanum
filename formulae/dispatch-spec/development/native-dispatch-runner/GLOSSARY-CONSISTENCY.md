# Glossary Consistency Check

Status: pass for planning

| Term | Define | Design | Contract | Consistent |
| --- | --- | --- | --- | --- |
| Dispatch Spec | validation-only | validation-only | route validator | yes |
| Native Dispatch Runner | Orchestrate execution mode | coordinator plus native driver | `orchestrate execute` | yes |
| Action | permitted runtime instruction | coordinator output | enumerated action | yes |
| Receipt | bound structured result | reducer input | required fields | yes |
| Gate | dependent-action decision | deterministic reducer output | failure withholding | yes |
| Canary | causal single-entry run | failure and success sequences | two acceptance scenarios | yes |

No term in the package treats a test expectation as an execution result or Markdown as runtime authority.
