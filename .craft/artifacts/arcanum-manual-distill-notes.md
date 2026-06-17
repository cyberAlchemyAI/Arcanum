# Arcanum Manual — Inventory & Distill Notes

> Output of dispatch steps **s02 (inventory)** and **s03 (distill-per-audience)** for
> [`arcanum-manual-research-strategy-20260616`](20260616-arcanum-manual-research-strategy.dispatch.json).
> Produced by four read-only explorer lanes + one pattern/audience lane, joined by parent synthesis.
> Status of every unit below: **source-backed** unless marked `candidate`. All paths are relative to
> the `arcanum/` scope.

## 1. Source-backed knowledge inventory (the corpus)

### Framework & method (lane: framework-method-explorer)
| Unit | Source | Status |
| --- | --- | --- |
| What Arcanum is | `README.md` | canonical |
| CyberAlchemy Method — 5 anchors (objective, output artifact, discovery, tension, route) | `framework/CYBERALCHEMY-METHOD.md` | canonical |
| Method loop — Orient → Discover → Shape → Stabilize → Evolve (13 steps) | `framework/CYBERALCHEMY-METHOD.md` | canonical |
| Governing principles (intent before machinery; discovery feeds synthesis; artifact over vibes; ergonomics is governance; lifecycle ownership; reflection closes the loop) | `framework/CYBERALCHEMY-METHOD.md` | canonical |
| Quality Bar (observable success, tier-specific) | `framework/QUALITY-BAR.md` | canonical |
| Anti-Patterns (tier-specific misuse boundaries) | `framework/ANTI-PATTERNS.md` | canonical |
| Artifact Constitution (4 retention classes) | `framework/ARTIFACT-CONSTITUTION.md` | canonical |
| Artifact metadata / schema / markdown-linking / gitignore constitutions | `framework/ARTIFACT-METADATA-CONSTITUTION.md`, `framework/SCHEMA-CONSTITUTION.md`, `framework/MARKDOWN-LINKING-CONSTITUTION.md`, `framework/GITIGNORE-CONSTITUTION.md` | canonical / candidate |
| Experiment harness standard + validation-experiment protocol | `framework/EXPERIMENT-HARNESS-STANDARD.md`, `framework/VALIDATION-EXPERIMENT-PROTOCOL.md` | canonical |
| Disciplines (cross-capability practices; 21 catalogued) | `disciplines/README.md`, `disciplines/DISCIPLINES.md` | canonical |

### Capability surface (lanes: sigil-explorer, spell-explorer)
| Unit | Source | Status |
| --- | --- | --- |
| Sigil = one reusable capability; tiers Formulae / Transmutations / Arcana | `registry/SIGILS.md`, `arcana/README.md`, `README.md` | canonical |
| Spell = composed multi-sigil workflow (references sigils, owns phases/state/gates) | `registry/SPELLS.md`, `spells/README.md`, `README.md` | canonical |
| 34 sigil packages under `arcana/`, 4 under `transmutations/`, 2 under `formulae/` | `arcana/`, `transmutations/`, `formulae/` (dir listing) | canonical |
| 14 spell packages under `spells/` | `spells/` (dir listing) | canonical |
| Whisper composition lifecycle (intake → substrate distill → SCU tournament → composition plan → draft+review → learning residue) | `spells/whisper/README.md` | canonical |
| Necronomicon knowledge-authority model (classifies source-backed vs candidate; no self-promotion) | `spells/necronomicon/README.md` | canonical |

### Lifecycle, observability & governance (lane: observability-lifecycle-explorer)
| Unit | Source | Status |
| --- | --- | --- |
| 12-stage sigil development lifecycle (candidate → … → promotion → observe → maintain) | `framework/SIGIL-DEVELOPMENT-WORKFLOW.md`, `arcana/sigil-development/SKILL.md` | canonical |
| Observability model — one JSONL signal per run, central ledger, reflection thresholds | `framework/observability/README.md`, `framework/observability/SIGIL-OBSERVABILITY-HOOK.md`, `.arcanum/observability/` | canonical |
| Reflection triggers (manual / 5 executions / 10 outputs / 3 gaps / 1 severe gap) | `framework/SIGIL-DEVELOPMENT-WORKFLOW.md`, `framework/observability/README.md` | canonical |
| Observe→reflect→iterate loop (signal-observer → workflow-reflect → sigil-development) | `arcana/signal-observer/SKILL.md`, `arcana/workflow-reflect/SKILL.md` | canonical |
| Runtime model (orchestrator → handoff → native skill/subagent or adapter) | `framework/runtime/README.md` | canonical |
| Distributed authority & promotion boundaries | `CLAUDE.md`, `arcana/constitution-governance/SKILL.md` | canonical |
| Open architectural tensions (native-skill observation, ledger normalization, setup defaults) | `framework/observability/ARCHITECTURE-OVERVIEW.md` | candidate |

### Pattern base (lane: user-guide-pattern)
| Unit | Source | Status |
| --- | --- | --- |
| Existing user-guide pattern: multi-surface, role-separated, evidence-forward, sequencing-by-tension | `development/user-guide/README.md`, `development/user-guide/ARCANUM-DEVELOPMENT-USAGE-GUIDE.md` | canonical |
| User / Translate / Guide three-part separation thesis | `development/user-guide/README.md` | candidate pattern |

## 2. Distilled concept units, grouped by reader leverage

Three leverage groups, matching the manual's spine:

- **What Arcanum is** → thesis, the problem it solves, the three building blocks (sigil / spell / discipline), the capability tiers.
- **What its processes are** → the CyberAlchemy method loop, the capability lifecycle, the observe→reflect→iterate loop, governance & promotion boundaries.
- **How each user leverages it** → the audience taxonomy below mapped to entry points.

## 3. Audience taxonomy (resolves GAP-AUDIENCE-TAXONOMY-001)

| Persona | Wants | Primary entry points | Sourced? |
| --- | --- | --- | --- |
| Newcomer / learner | Understand what Arcanum is and where to start | `README.md` Start-Here, this manual, user-guide HTML, `FRIEND-INSTALL-TUTORIAL.md` | direct |
| Capability consumer / invoker | Shape ideas into defined/planned/validated work | `refine`, `invoke`, `decision-gate`, `x-ray`, `task-session` | direct |
| Capability author | Turn an idea into a promoted, observable capability | `sigil-development`, `spellcraft`, `experiment-harness`, `skill-decomposer`, `skill-transcriptor` | direct |
| Repository maintainer / installer | Install & operate Arcanum in a repo | `arcanum-bootstrap`, `sigil-runtime-installer`, `observability-setup`, `FRIEND-INSTALL-TUTORIAL.md` | direct |
| Reviewer / validator | Gate output against contract & evidence | `QUALITY-BAR.md`, `ANTI-PATTERNS.md`, `experiment-harness`, `VALIDATION-EXPERIMENT-PROTOCOL.md`, `signal-observer` | inferred from registry use-when |
| Researcher / evidence hunter | Organize discovery, evidence, claims | `dispatch-spec`, `inventory`, `ontology-vault`, `scope-interview`, `robot-talks`, `publication-research-pipeline` | partly inferred |
| Cross-functional collaborator | Shared understanding across roles | `guide-architecture`, User/Translate/Guide pattern, `decision-gate` | inferred (candidate pattern) |

Personas marked *inferred* are grounded in registry "use-when" conditions and the user-guide thesis rather than a single explicit roster; the manual marks them as such.

## 4. Residue / honesty notes for validation (s05)
- Several capability tier placements were verified against directory listings (e.g. `context-builder`, `feature-glossary` live under `transmutations/`; `observability-setup` under `formulae/`).
- Live observability counts quoted by a lane (e.g. "390 executions") are point-in-time runtime state under `.arcanum/observability/`, not canonical claims; the manual avoids hard numbers and points to the ledger instead.
- Inferred personas (reviewer, researcher, cross-functional) are labelled inferred in the manual.
