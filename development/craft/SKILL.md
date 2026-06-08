---
name: craft
description: "Use when: starting or operating a local Craft project ledger for recursive development contexts, blockers, enablers, decisions, gaps, definitions, next moves, validation, and recomposition."
argument-hint: "[start|state|describe|blocker|decision|gap|definition|next|validate|recompose|export] [--ledger .craft/ledger.yml]"
tier: development-candidate
domain: craft-method
version: 0.1.0
origin: exposed from development/craft after local interface and interaction validation passed
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Skill: Craft

<status>
Craft is a candidate-local method surface. It is ready for local live tests in
another repository, but it is not promoted as an Arcanum sigil, spell, registry
entry, runtime adapter, command surface, or canonical framework method.
</status>

<objective>
Start and operate a file-backed Craft project ledger that keeps recursive
development state explicit: context, descriptions, blockers, enablers, open
decisions, gaps, definitions, next moves, child contexts, validation evidence,
and recomposition.
</objective>

<logic-type>
Candidate Craft method: recursive ledger governance for schema/data translation,
residue handling, smallest coherent units, validation, and recomposition.
</logic-type>

<source-authority>
When running inside the Arcanum repository, use these source artifacts as the
current interface authority:

- `development/craft/CRAFT-INTERFACE.md`
- `development/craft/CRAFT-INTERACTION-CONTRACT.md`
- `development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml`
- `development/craft/CRAFT-INTERFACE-EXAMPLE.yml`
- `development/craft/CRAFT-INTERACTION-LEDGER-SCHEMA.yml`
- `development/craft/CRAFT-INTERACTION-EXAMPLE.yml`
- `development/craft/CRAFT-LIVE-TEST-RECIPE.md`
- `development/craft/CRAFT-INTERFACE-VALIDATION.md`
- `development/craft/CRAFT-INTERACTION-VALIDATION.md`

When this skill is copied into another project, treat this `SKILL.md` as the
portable operating contract and create project-local Craft state under
`.craft/`.
</source-authority>

<storage-contract>
Target projects use:

```text
.craft/
  ledger.yml
  artifacts/
CRAFT.md
```

`.craft/ledger.yml` is the source of truth. `CRAFT.md` is a human-readable view
or summary only. Evidence, receipts, and supporting artifacts may be stored
under `.craft/artifacts/`.
</storage-contract>

<applicability>
Use Craft when:

- a project needs a durable local ledger before runtime automation exists,
- work contains nested contexts with their own blockers, enablers, decisions,
  gaps, and definitions,
- a blocker needs refinement before resolution,
- a child context must recompose into its parent before closure,
- a local live test needs to record residue without mutating Arcanum surfaces.
</applicability>

<non-use>
Do not use Craft to:

- promote Craft into a canonical sigil, spell, registry entry, or framework
  method,
- edit command surfaces, runtime adapters, registries, sigils, spells, or
  canonical definition sources,
- make `CRAFT.md` the source of truth,
- resolve raw blockers directly,
- treat dispatch validation as execution evidence,
- close child work without recomposition evidence,
- promote candidate definitions without their owner governance route.
</non-use>

<core-methods>
`start_project`

- Inputs: `project_id`, `title`, `purpose`, `description`,
  `source_contracts`, optional `initial_definitions`.
- Writes: root context, description row, candidate definitions, first
  `next_move`.
- Returns: root `context_id` and ledger path.

`state`

- Inputs: optional `context_id`, default root.
- Returns: context stage and gate, latest description, blockers, enablers, open
  decisions, gaps, candidate definitions, children, recomposition status, and
  current `next_move`.
- Invariant: read-only.

`describe`

- Inputs: `context_id`, `description`, optional `evidence`.
- Writes: description row. Preserve description history.

`add_blocker`

- Inputs: `context_id`, `summary`, `blocker_type`, `lane`, `evidence`,
  `closure_condition`.
- Writes: blocker typed item and optional relation.
- Invariant: raw blockers cannot be resolved directly.

`refine_blocker`

- Inputs: `blocker_id`, `blocker_type`, `lane`, `closure_condition`, `owner`.
- Writes: typed item update with `refinement_status: refined`.
- Invariant: refinement supplies closure criteria, not closure evidence by
  itself.

`add_enabler`

- Inputs: `context_id`, `summary`, `enabler_type`, `lane`, `evidence`.
- Writes: enabler typed item and optional `enables` relation.

`next`

- Inputs: `context_id`, `next_move`, `route`, `evidence`.
- Writes: one current context next move.

`open_decision`

- Inputs: `scope_id`, `question`, `options`, optional `default_option`,
  `decision_type`, `blocking`.
- Writes: active decision row.
- Invariant: blocking decisions stop dependent execution until closed, waived,
  or deferred.

`decide`

- Inputs: `decision_id`, `selected_option`, `rationale`, `evidence`.
- Writes: closed decision and optional relation or condition updates.

`add_gap`

- Inputs: `context_id`, `summary`, `severity`, `treatment`, `owner_route`,
  `evidence`.
- Writes: active gap row.

`add_definition`

- Inputs: `context_id`, `term`, `meaning`, `status`, `evidence`.
- Writes: candidate local definition row.
- Invariant: local definitions do not become canonical definitions.

`open_child_context`

- Inputs: `parent_context_id`, `purpose`, `trigger`, `expected_artifact`,
  `recomposition_target`.
- Writes: child context with parent and recomposition target.

`link`

- Inputs: `source_id`, `target_id`, `relation_type`, `evidence`.
- Writes: typed relation row.

`validate`

- Inputs: ledger path and optional context id.
- Returns: `pass`, `flag`, or `block`, with evidence and residue.

`recompose`

- Inputs: `child_context_id`, `parent_context_id`, `evidence`,
  `parent_fit_summary`, `next_parent_move`.
- Writes: recomposition record and parent next move update.

`export_ledger`

- Inputs: ledger path and target Markdown path.
- Writes: human-readable `CRAFT.md` view.
- Invariant: export never replaces `.craft/ledger.yml` authority.
</core-methods>

<interaction-boundary>
Craft may prepare handoffs, receive receipts, apply receipt evidence, and open
residue. The called capability owns its native artifact contract, validation,
and verdict. Craft records route memory and local ledger state; it does not
rewrite native results.
</interaction-boundary>

<process>
1. Resolve target project root and ledger path, defaulting to `.craft/ledger.yml`.
2. If no ledger exists and the user wants to start, create `.craft/`,
   `.craft/artifacts/`, `.craft/ledger.yml`, and `CRAFT.md`.
3. Keep ledger changes small and explicit; preserve existing rows unless the
   user asks for a correction.
4. Record descriptions, blockers, enablers, decisions, gaps, definitions, and
   next moves as structured ledger state.
5. Use child contexts for recursive work that has its own purpose, artifacts,
   blockers, or recomposition target.
6. Validate before claiming pass, closure, or recomposition.
7. Export or update `CRAFT.md` only as a view of `.craft/ledger.yml`.
8. Record residue and next move after each meaningful Craft operation.
</process>

<live-test-recipe>
For the first live test in another repository:

1. Start one root Craft project.
2. Record a working description.
3. Add one candidate definition.
4. Add one raw blocker.
5. Open a child context to refine that blocker.
6. Refine the blocker.
7. Open and close one decision.
8. Add one gap.
9. Set the parent next move.
10. Recompose the child context into the parent.
11. Validate the ledger.
12. Export or update `CRAFT.md`.
</live-test-recipe>

<quality-bar>
A successful Craft run must:

- keep `.craft/ledger.yml` as source of truth,
- keep `CRAFT.md` as a view,
- preserve local candidate definition status,
- prevent raw blocker direct resolution,
- require decision rationale and evidence,
- require recomposition evidence before child context closure,
- distinguish route-shape evidence from execution evidence,
- record residue and next move,
- avoid mutating Arcanum canonical surfaces.
</quality-bar>

<output-contract>
Return:

```markdown
## Craft Result

- Target project: <path>
- Ledger: <path>
- Operation: <start|state|update|validate|recompose|export>
- Result: pass | flag | block
- Contexts touched: <ids or none>
- Evidence: <paths or notes>
- Residue: <remaining gaps/blockers/decisions or none>
- Next move: <next action>
- Boundary check: <what was not mutated>
```
</output-contract>
