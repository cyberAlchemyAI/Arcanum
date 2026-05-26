# Dispatch Spec Glossary Consistency

Status: design-stage consistency check.

## Result

Glossary consistency: `pass`

## Checked Terms

| Term | Define Source | Design Usage | Result |
| --- | --- | --- | --- |
| Dispatch document | `GLOSSARY.md` | Central schema object in `DESIGN.md` | pass |
| Capability reference | `GLOSSARY.md` | Step field and dependency interface | pass |
| Frame | Weaver-linked local term | Handoff and dependency interface | pass |
| Handle | Weaver-linked local term | Artifact reference and handoff | pass |
| Pattern | `GLOSSARY.md` | Step shape and decision flow | pass |
| Promotion guardrail | `GLOSSARY.md` | Gate model and risks | pass |
| Trace event | Weaver-linked local term | Observability grouping | pass |
| SRU/SWU | Craft-owned vocabulary | Referenced as method vocabulary only | pass |

## Notes

- No term is promoted to canonical repository glossary authority.
- Weaver terms are explicitly marked as linked concepts, not imported ownership.
- Spellcraft, Invoke, Necronomicon, Task Session, and Experiment Harness ownership boundaries are preserved.

