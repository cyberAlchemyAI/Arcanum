# Design Selection Fixture Source Trace

The corpus is synthetic and project-agnostic. It freezes selection boundaries,
not examples copied from a consuming repository.

| Source principle | Fixture coverage |
| --- | --- |
| closed, inspectable architecture scope | every case resolves all declared field classes; omission cases fail closed |
| concern-to-view and evidence binding | every passing case names exact concerns, dispositions, outputs, and evidence state |
| quality-attribute scenarios are risk-triggered | bounded controls select only extensions justified by their traits |
| human semantic consequence governs UX depth | natural-person plus changed semantic-surface positives select `ux-plan`; style and backend controls do not |
| authored contracts are not executed evidence | Design results expose only `authored-complete` or `design-validator-pass` |
| deterministic admission needs independent replay | stale, self-issued, unbound, and changed-pass cases block with exact diagnostics |

Public background references:

- ISO/IEC/IEEE 42010 architecture-description conceptual model:
  <https://www.iso-architecture.org/ieee-1471/cm/>
- SEI quality-attribute scenarios:
  <https://www.sei.cmu.edu/library/reasoning-about-software-quality-attributes/>
- WCAG 2.2:
  <https://www.w3.org/TR/WCAG22/>

The source trace supplies design rationale only. The fixture denominator,
schemas, extractor, validator, and runner remain independent artifacts with
separate receipts.
