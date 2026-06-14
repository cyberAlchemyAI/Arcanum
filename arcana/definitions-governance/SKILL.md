---
name: definitions-governance
description: "Use when: maintaining canonical definitions, synchronized indexes, explanatory intuition, and downstream drift checks for critical terms."
argument-hint: "[--add <id>] [--update <id>] [--sync] [--audit] [--config <path>]"
tier: arcana
domain: semantic-governance
version: 0.1.0
origin: generalized from recurring canonical definitions maintenance practice
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Sigil: Definitions Governance

<objective>
Keep critical definitions authoritative, interpretable, discoverable, and traceable across downstream artifacts.
</objective>

<logic-type>
Arcana: semantic authority governance with drift detection and remediation routing.
</logic-type>

<project-authority-boundary>
Definitions Governance is the maintainer process, not the canonical definition
store.

When used in any repository, resolve the consuming project's root and write to
that project's configured definitions surface. Do not place project definitions
inside the installed sigil package, copied skill directory, `.codex/skills`
snapshot, `.agents/skills` symlink target, or `arcana/definitions-governance/`
unless the repository has explicitly configured that path as its project-level
definition authority.

Default project-level convention when no authority source exists:

```text
definitions/
  DEFINITIONS.md
  DEFINITIONS-INDEX.md
  DEFINITION-DRIFT-AUDIT.md
```

For this Arcanum repository, the canonical project-level source is
`definitions/DEFINITIONS.md` and the lookup layer is
`definitions/DEFINITIONS-INDEX.md`.
</project-authority-boundary>

<process>
1. Resolve the consuming project's authority model from the project root, not
   from the installed sigil package:
   - canonical definitions source,
   - lookup or index layer,
   - narrative consumers,
   - operational consumers,
   - validation checks.
2. If no canonical definitions source exists, initialize the default
   project-level `definitions/` surface unless the user or repository metadata
   names a different location.
3. Read the canonical definitions source and index before making changes.
4. Add or update critical terms with stable IDs when the repository uses IDs.
5. For formal or mathematical constructs, keep the minimum interpretation package together:
   - formal expression,
   - variable or notation meaning,
   - operational interpretation,
   - plain-language intuition.
6. Keep explanatory intuition colocated with the definition and clearly non-normative.
7. Sync lookup or index artifacts so definitions are discoverable.
8. Audit downstream drift:
   - conflicting wording,
   - stale anchors,
   - undefined critical terms,
   - narrative text that redefines authority,
   - missing references.
9. Emit remediation items with target files and recommended action.
10. Run available structure, link, or schema validation checks.
</process>

<authority-rule>
Only the consuming project's configured canonical definitions source may define
normative semantics. Narrative, summary, protocol, planning, presentation,
runtime, install-surface, or copied skill artifacts may explain or reference
definitions, but should not redefine them.
</authority-rule>

<quality-bar>
A successful execution must:

- resolve and report the consuming project's canonical definitions path,
- avoid writing project definitions into the sigil package or installed skill copy,
- keep critical terms in the canonical source,
- preserve stable IDs when used,
- colocate plain-language intuition with formal definitions,
- prevent intuition from contradicting normative wording,
- keep indexes synchronized,
- identify downstream drift with exact remediation targets,
- validate structure where checks exist.
</quality-bar>

<anti-patterns>
Avoid:

- using the sigil's own folder as the default project definition authority,
- treating copied skill packages as canonical definition stores,
- letting narrative artifacts become hidden definition authorities,
- adding formulas without symbol meaning and plain-language intent,
- creating detached intuition that can drift away from the definition,
- changing stable IDs casually,
- syncing indexes without auditing downstream consumers,
- treating local glossary terms as global canonical definitions without review.
</anti-patterns>

<concept-registry-aggregation>
DomainSpec extension (M2-C1). When the project uses the DomainSpec spec template, this
sigil also aggregates per-feature Concept Registries into a project-level typed registry:

1. Collect each feature SPEC's Concept Registry table (`Concept | ID | Type`, where Type is
   a DS-D1 meta-type per `definitions/DEFINITIONS.md#ds-d1-meta-type-system`).
2. Aggregate into a global registry keyed by ID, carrying the DS-D1 meta-type.
3. Build concept-graph edges from each feature's typed relationships (DS-D2 verbs),
   validated against the DS-D8 edge signature; reject edges whose endpoint meta-types
   violate the signature.
4. Detect duplicates (same ID, different type or feature) and drift (a concept whose
   meta-type changed across features) — flag, never auto-merge.
5. Emit the aggregated registry + edge list + a dup/drift report. Promotion of any new
   global term still follows the authority rules above.

Wedge method only: reads the public DomainSpec spec interface (`M2-CONTRACT`) and the
canonical DS-D1/D2 definitions; it does not import governance-engine logic.
</concept-registry-aggregation>

<output-contract>
Return:

```markdown
## Definitions Governance Summary

- Definitions updated: <ids or none>
- Index synced: yes | no | not applicable
- Drift found: yes | no
- Undefined critical terms: <count>
- Conflicting consumers: <count>
- Concept registry aggregated: <concept count | n/a>
- Registry duplicates/drift: <count | n/a>
- Validation: pass | fail | not run
- Canonical source: <project-relative path>
- Follow-ups: <ordered remediation list>
```
</output-contract>
