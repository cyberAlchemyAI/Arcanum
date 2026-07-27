# Template Selection

## Result

- Define: `spells/invoke/templates/sigil/sigil.md`
- Design: `spells/invoke/templates/architecture/architecture.md`
- Plan companions:
  - `spells/invoke/templates/implementation-layering.md`
  - `spells/invoke/templates/work-pack.md`
  - `spells/invoke/templates/domainspec-spec/execution-pack.md`
- Selection status: eligible current public templates
- Tie: none

## Eligibility

| Template | Evidence | Decision |
| --- | --- | --- |
| Sigil handoff | The target is an existing reusable Transmutation sigil and lifecycle mutation belongs to Sigil Development. | selected for Define handoff |
| Architecture | The proposed compiler has interfaces, generated state, writers, failure rules, and a validation boundary. | selected for Design |
| Implementation Layering | Plan mode requires a global L0-L3 decision model. | selected for Plan |
| Work Pack | Plan mode requires the executable planning source of truth. | selected for Plan |
| Execution Pack | The plan is medium complexity and needs layer-mapped waves. | selected for Plan |
| Generic template | It would erase the target sigil lifecycle boundary. | rejected |
| Retired implementation-plan template | New Plan work is owned by `WORK-PACK.md`. | rejected |

## Inventory Boundary

Consumer-local Inventory lookup was performed machine-index-first. No private
Inventory path, entry prose, or consumer binding is admitted into this public
package. Template eligibility is established from the current public Invoke
templates and target type.

## Discovery Waiver

- Discovery artifact found: no
- Waiver reason: the direct user request follows a same-thread manual
  maintenance reflection that already fixed the target, failure hypothesis,
  public/private boundary, and desired Define/Design/Plan outputs. Repeating
  broad discovery would add context without resolving a blocker.
- Waiver scope: Invoke authoring only
- Not authorized: sigil contract mutation, implementation, runtime deployment,
  registry release, or promotion
