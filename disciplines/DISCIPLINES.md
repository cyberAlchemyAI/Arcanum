# Discipline Catalog

Status: candidate
Owner: Arcanum framework

This catalog formalizes recurring Arcanum practices that are useful beyond one capability. The catalog is evidence-backed but not yet a promotion surface for sigils or spells.

## Discipline Model

A discipline is a reusable operating practice with:

- a named purpose,
- a boundary that says what it does not own,
- evidence that it already appears in Arcanum,
- an owner or likely steward,
- a maturity status,
- a next hardening move.

## Catalog

| ID | Discipline | Status | Steward | Evidence | Next hardening move |
| --- | --- | --- | --- | --- | --- |
| `craft` | Craft discipline | candidate | Craft development package | [Craft README](../development/craft/README.md) | Keep as candidate until repeated local use and receipt-backed validation support promotion. |
| `planning` | Planning discipline | active-pattern | Invoke, implementation-layering, task-session | [Lifecycle Work](../README.md#lifecycle-work) | Add clearer plan artifact criteria across invoke plan, work-packs, SWUs, and execution packs; now absorbs the implementation-readiness rule (merged 2026-06-21). |
| `schema` | Schema discipline | canonical | Constitution Governance | [Schema Constitution](../framework/SCHEMA-CONSTITUTION.md) | Keep validator-backed and migrate legacy non-YML schemas through scoped tasks. |
| `artifact-constitution` | Artifact constitution discipline | canonical | Constitution Governance | [Artifact Constitution](../framework/ARTIFACT-CONSTITUTION.md) | Add `disciplines/**` to source artifact examples and metadata validation scope. |
| `quality-bar` | Quality-bar discipline | canonical | Framework | [Quality Bar](../framework/QUALITY-BAR.md) | Add a deterministic card-quality validator; canonical rests on the Quality Bar constitution, not a validator (curation 2026-06-21). |
| `validation-experiment` | Validation experiment discipline | canonical | Experiment Harness | [Experiment Harness Standard](../framework/EXPERIMENT-HARNESS-STANDARD.md) | Reuse fixture and report expectations for disciplines that become executable. |
| `observability` | Observability discipline | implemented | Signal Observer and observability setup | [Observability layer](../README.md#observability-layer) | Define when discipline changes should emit reflection or maintenance signals. |
| `dispatch` | Dispatch discipline | active-pattern | Dispatch Spec | [Dispatch Spec](../formulae/dispatch-spec/README.md) | Use dispatch route artifacts for multi-phase discipline formalization. |
| `context-selection` | Context-selection discipline | active-pattern | Context Builder | [Context Builder](../transmutations/context-builder/README.md) | Define selection criteria for discipline evidence packs and hidden-practice scans. |
| `evidence-inventory` | Evidence and inventory discipline | active-pattern | Inventory | [Inventory](../arcana/inventory/README.md) | Keep evidence handoffs non-authoritative until downstream owners promote them. |
| `definition-governance` | Definition governance discipline | active-pattern | Definitions Governance | [Definitions Governance](../arcana/definitions-governance/README.md) | Decide which discipline terms need canonical definitions versus local explanations. |
| `ontology` | Ontology discipline | candidate | Ontology Vault | [Ontology Vault](../arcana/ontology-vault/README.md) | Prove independent cross-capability recurrence or keep candidate-grade; thin one-per-sigil pointer (curation 2026-06-21). |
| `decision-gating` | Decision discipline | active-pattern | Decision Gate | [Decision Gate](../arcana/decision-gate/README.md) | Route blocker-level alternatives through explicit gates before mutation. |
| `residuality` | Residuality discipline | candidate | Residuality Spec | [Residuality Spec](../arcana/residuality-spec/README.md) | Prove independent cross-capability recurrence or keep candidate-grade; thin one-per-sigil pointer (curation 2026-06-21). |
| `distillation` | Distillation discipline | candidate | Distill | [Distill](../arcana/distill/README.md) | Prove independent cross-capability recurrence or keep candidate-grade; thin one-per-sigil pointer (curation 2026-06-21). |
| `interview` | Interview discipline | active-pattern | Structured Interview Kits | [Structured Interview Kits](../arcana/structured-interview-kits/README.md) | Use one-question cadence when a discipline cannot be responsibly inferred from repo evidence. |
| `research-evidence` | Research evidence discipline | active-pattern | Research Evidence Harness and research tower | [Research Evidence Harness](../arcana/research-evidence-harness/README.md) | Separate proof, hypothesis, conflict, and publication evidence for research-facing disciplines. |
| `implementation-readiness` | Implementation readiness discipline | deprecated | Implementation Layering and implementation-readiness spell | [Implementation Layering](../transmutations/implementation-layering/README.md) | Merged into `planning` (2026-06-21); retained for provenance. |
| `runtime-boundary` | Runtime boundary discipline | active-pattern | Runtime framework and observed invocation loop | [Runtime framework](../framework/runtime/README.md) | Keep canonical source, generated install surfaces, and local runtime state separate. |
| `ux-evidence` | UX evidence discipline | candidate | UX Evidence Validator | [UX Evidence Validator](../arcana/ux-evidence-validator/README.md) | Use browser evidence and accessibility checks when interface work becomes durable. |
| `gitignore` | Gitignore discipline | candidate | Constitution Governance | [Gitignore constitution](../framework/GITIGNORE-CONSTITUTION.md) | Give the gitignore constitution a validation surface (ignore-policy check) before promoting beyond candidate. |
| `receipt-id-legend` | Receipt id legend discipline | candidate | Constitution Governance | [Receipt id legend constitution](../framework/RECEIPT-ID-LEGEND-CONSTITUTION.md) | Validator `tools/validate-receipt-legend.py` now enforces gloss-on-cite (2026-06-21); extend to define-on-mint + bulk-legend, then canonical. |

## Status Meanings

| Status | Meaning |
| --- | --- |
| `candidate` | Useful practice exists, but authority and validation are still being proven. |
| `active-pattern` | Practice is already used by promoted or active capabilities, but its discipline-level contract is not fully canonical. |
| `implemented` | Practice has working repository support, but may still need discipline-level rules. |
| `canonical` | Practice has accepted framework authority and validator or constitution support. |

## Growth Rule

Promote a discipline only when the next route names its owner, evidence, validation surface, and mutation boundary. Discipline evidence can recommend a route, but it cannot directly promote registry, ontology, glossary, sigil, or spell knowledge.
