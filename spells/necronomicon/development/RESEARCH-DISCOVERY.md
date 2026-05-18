# Research Discovery: Necronomicon Meaning And Operation

## Research Question

What is Necronomicon in Arcanum, how does it work, and where is the boundary between `ontology-harness` and `necronomicon`?

## Scope Boundaries

- Included: repository README, spell registry, ontology-harness contract, necronomicon contract, current local harness state, development wave/layering docs, runtime adapters.
- Excluded: external web research. The ambiguity is repository-local and should be resolved from the current Arcanum contracts first.
- Evidence boundary: repository-only.

## Source Ledger

| Source ID | Source | Status | Notes |
| --- | --- | --- | --- |
| S-001 | `README.md` | selected | Defines Necronomicon as the persistent repository harness and separates ontology governance into `ontology-harness`. |
| S-002 | `registry/SPELLS.md` | selected | Lists `Ontology Harness` and `Necronomicon` as separate spells. |
| S-003 | `spells/ontology-harness/README.md` | selected | Canonical ontology harness contract. |
| S-004 | `spells/necronomicon/README.md` | selected | Canonical session harness contract. |
| S-005 | `.arcanum/necronomicon/README.md` | selected | Defines generated project-local state folder. |
| S-006 | `.arcanum/necronomicon/capabilities.json` | selected | Shows local selected capabilities and harness aliases. |
| S-007 | `.arcanum/runtimes/codex/commands/arcanum-ontology-harness.md` | selected | Friendly alias adapter for `ontology-harness`. |
| S-008 | `.arcanum/runtimes/codex/commands/arcanum-necronomicon.md` | selected | Friendly alias adapter for `necronomicon`. |
| S-009 | `spells/necronomicon/development/WAVE-PLAN.md` | selected | Product UX north star and implementation constraints. |
| S-010 | `spells/necronomicon/development/IMPLEMENTATION-LAYERING.md` | selected | Progressive layer model and first-pass runtime boundary. |

## Evidence Table

| Evidence ID | Source ID | Claim | Support Level | Notes |
| --- | --- | --- | --- | --- |
| E-001 | S-001 | Necronomicon is the persistent repository harness, not the ontology-harness alias. | supports | README now reserves Necronomicon for the repository harness. |
| E-002 | S-001 | Ontology governance routes through `ontology-harness`, `arcanum-ontology-harness`, or `arcanum-spell-ontology-harness`. | supports | README distinguishes ontology governance from the harness command. |
| E-003 | S-002 | `Ontology Harness` and `Necronomicon` are separate registered spells. | supports | Registry gives different purpose rows and different files. |
| E-004 | S-003 | `ontology-harness` maps vault-like knowledge into ontology governance and delegates long-running operations to `necronomicon`. | supports | Ontology contract explicitly points long-running repository work at session spell. |
| E-005 | S-004 | `necronomicon` creates, resumes, routes, checkpoints, researches, updates, maintains, and closes sessions. | supports | Mode list and execution phases are session-oriented. |
| E-006 | S-005 | `.arcanum/necronomicon/` stores local harness state and must not store copied Arcanum definitions. | supports | Generated README says exactly this. |
| E-007 | S-006 | The local harness records `arcanum-necronomicon` for `necronomicon` and `arcanum-ontology-harness` for `ontology-harness`. | supports | `harness_commands` contains separate entries. |
| E-008 | S-007, S-008 | Runtime aliases now preserve the distinction without overloading `arcanum-necronomicon`. | supports | The ontology alias moved to `arcanum-ontology-harness`. |
| E-009 | S-009 | The target UX is a project harness shell, not only ontology mapping. | supports | North Star includes inventory, ontology, sessions, routing, research, invoke, and maintenance. |
| E-010 | S-010 | First-pass implementation is adapter-mediated state, not a full local CLI runtime. | supports | Layering doc makes this a core constraint. |

## Contradictions

| Conflict ID | Evidence IDs | Summary | Resolution |
| --- | --- | --- | --- |
| C-001 | E-001, E-008 | The same word previously named both the ontology alias and the broader session harness surface. | resolved | Breaking rename reserves `Necronomicon` for the persistent repository harness and gives ontology governance the explicit `ontology-harness` surface. |
| C-002 | E-005, E-010 | The session spell describes many modes, but the first-pass implementation is not a complete CLI engine. | resolved | Document adapter-mediated execution as the current operating model and leave CLI automation as a later layer. |
| C-003 | E-005, E-006 | Durable state can look like a local source of truth. | resolved | State is session memory and routing evidence only; canonical definitions stay in Arcanum source and runtime adapters. |

## Claim Status

| Claim | Status | Confidence | Reason |
| --- | --- | --- | --- |
| Necronomicon is the persistent repository harness. | supported | high | Confirmed by README, registry, Necronomicon contract, and runtime adapter. |
| Necronomicon is a persistent operating shell around selected repository capabilities. | supported | high | Confirmed by registry, session contract, wave plan, and local harness state. |
| `.arcanum/necronomicon/` is memory/state, not a definition registry. | supported | high | Confirmed by multiple guardrails. |
| The user confusion came from overloaded naming and missing near-top explanation. | supported | medium | Inferred from source shape and user report; resolved by the breaking rename. |
| A full executable local session CLI already exists. | unsupported | high | Current docs describe adapter-mediated first pass. |

## Synthesis

Necronomicon should be understood as the persistent repository operating shell: it remembers setup, selected capabilities, routes, gaps, checkpoints, research, and maintenance signals, then delegates real work to the owning sigils and spells. Ontology governance is still available through `ontology-harness`, `arcanum-ontology-harness`, and `arcanum-spell-ontology-harness`.

The clearest documentation move is to state that ownership before the existing capability tables. Readers should see the mental model first, then the implementation details.

## Unresolved Gaps

| Gap ID | Gap | Impact | Next Step |
| --- | --- | --- | --- |
| G-001 | The `research` capability is described as selectable, but the current manifest does not show a selected `research` sigil. | Medium | Decide whether research is a future sigil, a mode implemented by session, or an invoke-local research template until a sigil exists. |
| G-002 | Runtime aliases expose both friendly and spell-prefixed Necronomicon adapters. | Medium | Decide whether both aliases are intentional compatibility surfaces or whether docs should recommend only spell-prefixed and friendly command forms. |
| G-003 | Setup decisions and gaps files are named in the contract but not present in the current local harness folder. | Medium | Let the next implementation layer generate baseline state files or document that the current install is partial. |

## Decision Options

| Option | Evidence Basis | Trade-Off |
| --- | --- | --- |
| Reserve `Necronomicon` for the persistent harness. | E-001 through E-009 | Breaking but clearest; requires registry, runtime, and docs rename. |
| Keep Necronomicon as an ontology alias too. | historical evidence | Avoids older doc churn but keeps the ambiguity. |
| Rename the harness away from Necronomicon. | historical conflict | Reduces ambiguity but breaks the intended product metaphor. |

## Gate Result

- Status: pass
- Reason: The breaking rename gives Necronomicon one primary meaning: the persistent repository harness. Remaining work is implementation hardening, not concept naming.
