# Craft Architecture Glossary Consistency

## Verdict

pass

The architecture uses the local candidate vocabulary from `CRAFT-GLOSSARY.md` consistently. No term is promoted beyond `development/craft/`, and deferred terms remain outside the architecture acceptance gate.

## Checked Terms

| Term | Glossary Status | Architecture Usage | Status |
| --- | --- | --- | --- |
| Craft | candidate | Candidate method architecture for LLM-centered making. | pass |
| Craft Space | candidate | Local bounded development and source-contract boundary. | pass |
| Schema | candidate | Represented through definition, design, plan, and validation contracts. | pass |
| Data | candidate | Produced artifact, evidence, ledger row, or observed result. | pass |
| Residue | candidate | Validation mismatch that is closed, routed, deferred, or promoted to a new context. | pass |
| Smallest Coherent Unit | candidate | General unit selection boundary before planning and execution. | pass |
| SCU | candidate | Used as the non-execution-specific coherent unit boundary. | pass |
| SWU | candidate | Used as the planning and execution form of SCU. | pass |
| Reflection | candidate | Used as post-validation review and residue analysis. | pass |
| Recomposition | candidate | Required closure relation from a lower unit back to its parent context. | pass |
| Validation | validated-by-mvp | Used as evidence comparison with pass, flag, block, or waiver outcomes. | pass |
| Promotion | candidate | Explicit future decision path, not automatic. | pass |
| Route | candidate | Existing capability path selected by Craft without authority takeover. | pass |
| Handoff | candidate | Selective transfer to another thread, route, or runtime owner. | pass |
| Context | validated-by-mvp | Recursive ledger unit for nested projects and work areas. | pass |
| Artifact | validated-by-mvp | Produced object owned by a context. | pass |
| Work-Pack | validated-by-mvp | Execution artifact owned by a context, not the ledger root. | pass |
| Blocker | validated-by-mvp | Typed condition that can prevent progress. | pass |
| Gate | validated-by-mvp | Pass, flag, or block check before movement. | pass |
| Enabler | validated-by-mvp | Condition that allows another context to progress. | pass |
| Lane | validated-by-mvp | Operational responsibility category, not automatic assignee. | pass |
| Blocker Refiner | validated-by-mvp | Lane responsible for making blockers resolvable. | pass |
| Blocker Refinement Gate | validated-by-mvp | Rule preventing raw blocker resolution without refinement or waiver. | pass |
| Waiver | validated-by-mvp | Explicit evidence-backed exception path. | pass |
| Priority Scoring | deferred | Named as future automation requiring evidence. | pass |
| Generated Index | deferred | Kept out of current acceptance gate. | pass |
| Role Delegation Automation | deferred | Manual until example coverage and authority exist. | pass |
| Runtime Interface | deferred | External side-thread dependency only. | pass |

## Conflicts

None found.

## Gaps

| Gap | Treatment |
| --- | --- |
| Example suite is not yet built. | Non-blocking for design; required by next plan before promotion or automation. |
| Promotion target is undecided. | Expected; architecture defines decision path rather than selecting target. |
| Runtime/interface strategy is incomplete. | Non-blocking side-thread; architecture references it without claiming resolution. |
| Automation terms are named but not executable. | Correct for current layer; evidence-gated in architecture. |

## Gate Result

`pass`: glossary usage is consistent enough for `invoke plan development/craft/CRAFT-ARCHITECTURE.md`.
