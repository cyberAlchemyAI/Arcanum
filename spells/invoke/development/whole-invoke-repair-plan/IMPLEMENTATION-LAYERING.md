# Whole Invoke Repair — Implementation Layering

- Target: canonical public Invoke authoring and preacceptance workflow
- Complexity: high
- Execution designation: `blocked-before-execution-candidate`
- Authority effect: `none`

## Layer Boundary Heuristic

Layer value is the decision unlocked, operator-visible outcome, and risk reduced. Layer cost is implementation, verification, and coordination burden. Each layer stops when the next change answers a materially different decision.

| Layer | Decision question | Minimum working unit | Included SWUs | Deferred scope | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 — trustworthy admission | After this layer, we know whether Invoke rejects untrusted status and constructs complete preacceptance fixtures. | Mode-specific artifact-evidence admission plus `joined_driver_digest` regression repair. | SWU-WIR-001–002 | Plan production and downstream execution closure. | Negative status denominator passes; complete preacceptance suite passes without fixture errors. | Promote only when self-asserted/stale/wrong-owner evidence blocks and aggregate preacceptance is green. |
| L1 — canonical execution chain | After this layer, we know whether one source can produce and rehearse a complete Plan candidate through real consumers and one owner-decision family. | Complete source producer, real transformations, unified request/response contracts. | SWU-WIR-003–005 | Remaining mode producers, surface cleanup, release proof. | Atomic source compilation; real consumer closure; one version family round trip. | Promote only when no development adapter or schema-only substitute can satisfy closure. |
| L2 — truthful authoring modes | After this layer, we know whether every advertised authoring mode has an executable producer or a truthful downgraded status. | Define, Design, Handoff, Refresh producer/status slices plus generic frontier and public boundary closure. | SWU-WIR-006–012 | Deferred-mode removal and final laboratory proof. | Mode-specific producer tests, generic frontier matrix, public-content audit. | Promote only when status claims equal executable evidence and generated mirrors are exact. |
| L3 — compatibility closure and proof | After this layer, we know whether obsolete routing is removed safely and the repaired workflow works end to end. | Compatibility-closed `full` removal followed by a fresh generic laboratory workflow. | SWU-WIR-010, SWU-WIR-013 | Publication, release, deployment, and external rollout. | Historical-read compatibility tests; fresh no-effect laboratory receipts across all real boundaries. | Final promotion remains separately owner-controlled. |

## Non-regression Guarantees

- Exact-byte, lifecycle-owner, one-SWU, authority, publication, Git, deployment, and external-effect boundaries remain fail closed.
- Historical receipts remain readable unless an explicit versioned migration says otherwise.
- A passing authoring receipt never implies registry release, acceptance, selection, admission, or runtime readiness.
- Invalid input publishes no partial final bundle.
- Public canonical artifacts contain generic contracts and fixtures only.

## Recommended Next Layer

L0 only, beginning with SWU-WIR-001. Implementation cannot begin from this package until a future canonical Plan producer emits the complete machine execution source, WPRA evidence, and Implementation Readiness preflight over these exact final bytes.
