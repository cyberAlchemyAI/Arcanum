# Glossary

| Term | Plain-language meaning | Contract meaning |
| --- | --- | --- |
| Execution entry | The moment a selected task or SWU is checked before expensive execution preparation. | The bounded phase between selector resolution and Context Builder. |
| Owner prerequisite | Work another capability must complete before Task Session can continue. | A typed `PreExecutionOwnerPrerequisite` bound to one task/SWU and one owner route. |
| Fast block | An immediate, useful stop rather than a full failed execution audit. | A receipt emitted before Context Builder with exact missing route or evidence and zero mutation. |
| Plan-once | Audit stable plan semantics once and admit material only for the selected unit later. | The existing `selected-unit-at-task-session` readiness profile. |
| Satisfaction predicate | The exact rule that says a prerequisite is complete. | A receipt-type, status, identity, scope, digest, and validation condition. |
| Exact authorization | Permission for one precisely bounded route and effect. | Evidence bound to route, task, SWU, targets, validation, and attempt. |
| Owner hop | One call through Continuation Router to the capability that owns the prerequisite. | A single selected route with joined terminal owner receipt. |
| Resume point | Where Task Session continues after the owner hop. | `task-session:context-build` for the same bounded attempt. |
| Prerequisite fingerprint | Stable identity for the prerequisite state. | Digest material used for idempotency and cycle rejection. |
| Structural effort bound | A deterministic limit on work performed before routing. | Allowed input categories and forbidden phases, independent of machine speed. |
| Semantic plan drift | A change to the selected unit's execution meaning. | A plan-once manifest mismatch that requires re-audit or Invoke repair. |
| Material drift | A mismatch in the selected unit's staged bytes or live baselines. | A Task Session admission failure owned by the material producer or target owner. |
