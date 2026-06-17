# ARCANUM-MANUAL — Validation Evidence

> Output of dispatch step **s05 (validate-manual-against-source)** for
> [`arcanum-manual-research-strategy-20260616`](../../.craft/artifacts/20260616-arcanum-manual-research-strategy.dispatch.json).
> Method: each load-bearing claim in [ARCANUM-MANUAL.md](ARCANUM-MANUAL.md) was resolved to a source
> path that was confirmed to exist on disk. This is **validation evidence only** — it proves the
> manual is source-backed; it does not promote the manual or any source to canonical authority.

## Verdict: **pass**

- All 24 capability/spell/sigil link targets referenced by the manual were confirmed to exist
  (directory check, 2026-06-16): `arcana/refine`, `spells/invoke`, `arcana/decision-gate`,
  `arcana/x-ray`, `arcana/task-session`, `arcana/sigil-development`, `arcana/spellcraft`,
  `arcana/experiment-harness`, `arcana/skill-decomposer`, `arcana/skill-transcriptor`,
  `spells/arcanum-bootstrap`, `arcana/sigil-runtime-installer`, `formulae/observability-setup`,
  `arcana/inventory`, `arcana/ontology-vault`, `arcana/scope-interview`, `arcana/robot-talks`,
  `spells/publication-research-pipeline`, `spells/guide-architecture`, `arcana/signal-observer`,
  `arcana/workflow-reflect`, `transmutations/context-builder`, `transmutations/feature-glossary`,
  `.claude/skills/dispatch-spec`.
- All framework source files cited were confirmed to exist (`framework/CYBERALCHEMY-METHOD.md`,
  `framework/QUALITY-BAR.md`, `framework/ANTI-PATTERNS.md`, `framework/ARTIFACT-CONSTITUTION.md`,
  `framework/SIGIL-DEVELOPMENT-WORKFLOW.md`, `framework/observability/README.md`,
  `framework/observability/SIGIL-OBSERVABILITY-HOOK.md`, `framework/runtime/README.md`,
  `disciplines/README.md`, `disciplines/DISCIPLINES.md`, `CLAUDE.md`).

## Claim → source map (load-bearing claims)

| # | Manual claim | Source | Status |
| --- | --- | --- | --- |
| 1 | "Arcanum is a framework for creating reusable agent capabilities through governed synthesis." | `README.md` | verified |
| 2 | Five anchors: objective, output artifact, discovery, tension, route. | `framework/CYBERALCHEMY-METHOD.md`, `README.md` | verified |
| 3 | Method loop Orient→Discover→Shape→Stabilize→Evolve (13 steps). | `framework/CYBERALCHEMY-METHOD.md` | verified |
| 4 | Three building blocks: sigil / spell / discipline, with stated boundaries. | `registry/SIGILS.md`, `registry/SPELLS.md`, `disciplines/README.md` | verified |
| 5 | Counts: 34 arcana, 4 transmutations, 2 formulae sigil packages; 14 spells; ~21 disciplines. | dir listing of `arcana/`, `transmutations/`, `formulae/`, `spells/`; `disciplines/DISCIPLINES.md` | verified (counts from listing) |
| 6 | Three tiers Formulae / Transmutations / Arcana, by kind of reasoning; tier sets quality bar & anti-patterns. | `README.md`, `framework/QUALITY-BAR.md`, `framework/ANTI-PATTERNS.md` | verified |
| 7 | 12-stage sigil lifecycle; promotion is evidence-gated. | `framework/SIGIL-DEVELOPMENT-WORKFLOW.md`, `arcana/sigil-development/SKILL.md` | verified |
| 8 | One JSON signal per run to a central ledger; reflection triggers (manual / 5 / 10 / 3 / 1-severe). | `framework/observability/README.md`, `framework/observability/SIGIL-OBSERVABILITY-HOOK.md`, `framework/SIGIL-DEVELOPMENT-WORKFLOW.md` | verified |
| 9 | Observe→reflect→iterate owned by signal-observer → workflow-reflect → sigil-development. | `arcana/signal-observer/SKILL.md`, `arcana/workflow-reflect/SKILL.md` | verified |
| 10 | Distributed authority; execution evidence does not silently promote canonical knowledge. | `CLAUDE.md`, `arcana/constitution-governance/SKILL.md`, `framework/ARTIFACT-CONSTITUTION.md` | verified |
| 11 | Audience taxonomy → entry points (7 personas). | `development/user-guide/README.md`, `README.md`, `FRIEND-INSTALL-TUTORIAL.md`; registry use-when conditions | verified; 3 personas marked inferred |
| 12 | Worked path (idea → refine → invoke → blocker routing → task-session → residue). | `development/user-guide/ARCANUM-DEVELOPMENT-USAGE-GUIDE.md` | verified |

## Honesty notes / residue

- **Inferred personas.** Reviewer/validator, researcher, and cross-functional collaborator are not a
  single explicit roster in one file; they are inferred from registry "use-when" conditions and the
  User/Translate/Guide thesis. The manual labels each as *(inferred)* / *(partly inferred)*.
- **No live numbers baked in.** A research lane quoted point-in-time runtime counts (e.g. "390
  executions") from `.arcanum/observability/`. These are mutable runtime state, not canonical claims;
  the manual deliberately avoids hard numbers and links to the ledger instead.
- **Tier placements verified.** `context-builder` and `feature-glossary` are under `transmutations/`
  and `observability-setup` under `formulae/` (confirmed by listing), not `arcana/`.
- **Candidate vs canonical.** Items the corpus marked candidate (e.g. metadata/markdown-linking
  constitutions, open observability tensions, the User/Translate/Guide pattern) are presented as
  patterns/directions, not settled canon.

## Boundary check

This validation produced evidence only. No sigil, spell, definition, registry, or other canonical
Arcanum surface was created, mutated, or promoted by the manual or by this validation.
