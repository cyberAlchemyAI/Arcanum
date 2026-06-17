---
name: craft
description: "Use when: starting or operating a link-indexed local Craft project ledger for recursive development contexts, blockers, enablers, decisions, gaps, definitions, next moves, pending-by-node status, validation, and recomposition."
argument-hint: "[start|state|status|describe|blocker|decision|gap|definition|next|validate|recompose|export] [all|--ledger .craft/ledger.yml]"
tier: arcana
domain: craft-method
version: 0.2.1
origin: promoted from development/craft after local interface validation and two project-ledger examples
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Sigil: Craft

<status>
Craft is a first canonical Arcana sigil for project-local recursive ledgers. It
is intentionally small: it governs file-backed Craft state, human views,
linking, indexing, blocker/decision/gap visibility, and recomposition evidence.
It does not yet provide an automated command runner or full ledger renderer.
</status>

<objective>
Start and operate a file-backed Craft project ledger that keeps recursive
development state explicit: context, descriptions, blockers, enablers, open
decisions, gaps, definitions, next moves, child contexts, validation evidence,
and recomposition.
</objective>

<logic-type>
Craft method: recursive ledger governance for schema/data translation, residue
handling, smallest coherent units, validation, and recomposition.
</logic-type>

<source-authority>
When running inside the Arcanum repository, use these source artifacts as the
current canonical interface authority:

- `arcana/craft/SKILL.md`
- `arcana/craft/README.md`
- `arcana/craft/ARCHITECTURE.md`
- `arcana/craft/templates/ledger.schema.yml`
- `arcana/craft/templates/schemas/ledger-core.schema.yml`
- `arcana/craft/templates/schemas/index.schema.yml`
- `arcana/craft/examples/product-launch-ledger.yml`
- `arcana/craft/examples/product-launch-CRAFT.md`
- `arcana/craft/examples/platform-governance-ledger.yml`
- `arcana/craft/examples/platform-governance-CRAFT.md`

The older `development/craft/` package remains historical promotion evidence and
working material, not the runtime contract for `$craft`.

When this skill is copied into another project, treat this `SKILL.md` as the
portable operating contract and create project-local Craft state under
`.craft/`.
</source-authority>

<storage-contract>
Target projects use:

```text
.craft/
  ledger.yml
  index.json          # optional generated machine index
  artifacts/
CRAFT.md
```

`.craft/ledger.yml` is the source of truth. `CRAFT.md` is a human-readable view
or summary only. `.craft/index.json`, when present, is a rebuildable machine
index derived from the ledger; do not make it more authoritative than
`.craft/ledger.yml`. Evidence, receipts, and supporting artifacts may be stored
under `.craft/artifacts/`.
</storage-contract>

<linking-and-indexing-contract>
Craft ledgers must be navigable by both humans and machines.

Machine ledger requirements:

- every row keeps a stable ID and enough description to be useful outside its
  original conversation;
- every row that names another row uses a valid ID reference or an explicit
  `links` entry;
- each row family may include `links`, a list of `{label, target, kind}`;
- paths are relative to the Craft scope unless marked `[repo-root]` or absolute;
- ledgers should include an `indexes` section with at least `by_id`,
  `open_decisions`, `blocking_decisions`, `active_blockers`, `active_gaps`,
  `next_moves`, and `artifacts_by_path`;
- generated indexes may duplicate lookup data, but they must point back to row
  IDs rather than redefining row content.

Human view requirements:

- `CRAFT.md` renders row IDs as anchors or Markdown links when the target is a
  file, section, or row in the same view;
- decisions include a question, description or impact, status, blocking state,
  selected option when known, rationale when known, and evidence links;
- blocker, gap, decision, recomposition, route, and artifact sections link to
  each other instead of listing isolated IDs;
- the view includes a compact index or "quick links" section for current
  next moves, blocking decisions, active blockers, active gaps, and artifacts.
</linking-and-indexing-contract>

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

- mutate Craft's own canonical sigil, registry entry, generated runtime
  surfaces, or framework status outside an explicit sigil-development,
  task-session, or maintainer-approved repository task,
- edit command surfaces, runtime adapters, registries, sigils, spells, or
  canonical definition sources,
- make `CRAFT.md` the source of truth,
- resolve raw blockers directly,
- treat dispatch validation as execution evidence,
- close child work without recomposition evidence,
- promote candidate definitions without their owner governance route.
</non-use>

<workspace-resolution>
Craft spaces are per-scope, and a repository can hold several at once (for example a
parent space plus one `.craft/` per project under `projects/<name>/`). On every `start`
or `state`, resolve the workspace before acting; never silently default to the first or
root ledger.

1. Discover: glob for existing `.craft/ledger.yml` files across the repository and its
   project folders, and note scopes that plausibly need a ledger but do not have one.
2. Disambiguate: match the user's target scope to a discovered space. If more than one
   space could own the work, list the candidates and let the user pick rather than
   guessing or opening only the first.
3. Bind: operate inside the chosen space's `.craft/`. An existing scoped ledger is the
   authority for that scope — its blockers and open decisions are already controlled by
   it, so route reads through `state` and changes through `decide` / `refine` / `next`
   instead of recreating them in another ledger.
4. Create only on miss: start a new ledger only when no discovered space owns the scope
   and the user wants to begin one.

When another sigil (for example decision-gate) resolves an item that already lives in a
scope's ledger, record the outcome back into the owning ledger via `decide` rather than
leaving it in a separate artifact.
</workspace-resolution>

<core-methods>
`start_project`

- Precondition: resolve the workspace first (see <workspace-resolution>); only start a
  new root when no existing scope already owns the work.
- Inputs: `project_id`, `title`, `purpose`, `description`,
  `source_contracts`, optional `initial_definitions`.
- Writes: root context, description row, candidate definitions, first
  `next_move`.
- Returns: root `context_id` and ledger path.

`state`

- Precondition: resolve the workspace first (see <workspace-resolution>); default to the
  scope that owns the work, not the first ledger found.
- Inputs: optional `context_id`, default root.
- Returns: context stage and gate, latest description, blockers, enablers, open
  decisions, gaps, candidate definitions, children, recomposition status, and
  current `next_move`.
- For repository-wide requests such as `return all status`, `all status`, `state all`,
  `status of each node`, or `what is pending`, return every discovered Craft space and
  include a `Pending by node` section. Do not collapse node state to aggregate counts.
- Invariant: read-only.

`describe`

- Inputs: `context_id`, `description`, optional `evidence`.
- Writes: description row. Preserve description history.

`add_blocker`

- Inputs: `context_id`, `summary`, `blocker_type`, `lane`, `evidence`,
  `closure_condition`, optional `secondary_lanes`, `default_role`,
  `allowed_roles`, `delegation_route`, `requires_human`, `role_confidence`,
  `owner_ref`, and `role_notes`.
- Writes: blocker typed item and optional relation.
- Invariant: raw blockers cannot be resolved directly.
- Invariant: lane names the responsibility type; role fields suggest local
  handlers but do not assign authority without owner, decision, policy, route,
  or receipt evidence.

`refine_blocker`

- Inputs: `blocker_id`, `blocker_type`, `lane`, `closure_condition`, `owner`,
  optional `secondary_lanes`, `default_role`, `allowed_roles`,
  `delegation_route`, `requires_human`, `role_confidence`, `owner_ref`, and
  `role_notes`.
- Writes: typed item update with `refinement_status: refined`.
- Invariant: refinement supplies closure criteria, not closure evidence by
  itself.
- Invariant: if `requires_human` is true, closure needs decision, policy, or
  human evidence; route-shape validation alone is not enough.

`add_enabler`

- Inputs: `context_id`, `summary`, `enabler_type`, `lane`, `evidence`.
- Writes: enabler typed item and optional `enables` relation.

`next`

- Inputs: `context_id`, `next_move`, `route`, `evidence`.
- Writes: one current context next move.

`open_decision`

- Inputs: `scope_id`, `question`, `options`, optional `default_option`,
  `decision_type`, `blocking`, optional `description`, `impact`, and `links`.
- Writes: active decision row.
- Invariant: blocking decisions stop dependent execution until closed, waived,
  or deferred.

`decide`

- Inputs: `decision_id`, `selected_option`, `rationale`, `evidence`.
- Writes: closed decision, retained question/description/impact, evidence links,
  and optional relation or condition updates.

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
- Invariant: export never replaces `.craft/ledger.yml` authority, and exported
  row IDs remain navigable.
</core-methods>

<all-status-contract>
When the operator asks for all status, status by node, or pending work, treat the
request as read-only repository-wide `state`.

Discovery and validation:

1. Discover every `.craft/ledger.yml` in the repository before reporting.
2. Parse each ledger as source of truth; use `CRAFT.md` only as a human view.
3. Verify enough structure to trust the status: required `indexes` keys, `by_id`
   pointers, and `artifacts_by_path` existence.
4. Report structural validation separately from readiness. A structurally valid node
   can still be `flag` or `block` because work remains pending.

Pending means any of:

- active gaps, active blockers, or open decisions;
- blocking decisions, gate `block`, or artifact status `block`;
- route, research, runtime, receipt, or handoff artifacts with `not_run`, `flag`,
  `blocked`, `requires_user_permission`, `deferred`, or approval/confirmation wording;
- recomposition entries with residue or non-pass status;
- next moves that ask for approval, confirmation, external research, refinement,
  runtime execution, or downstream route selection.

For each node, show the pending work itself, not only counts:

- ledger path and root context id/title;
- readiness status: `pass`, `flag`, or `block`;
- active blockers by ID and summary, or `none`;
- blocking decisions by ID, question, and next needed action, or `none`;
- other open decisions by ID and question, or `none`;
- active gaps by ID, severity, treatment/owner if present, and summary, or `none`;
- pending artifacts/routes by artifact ID, type, status, path, and why still pending,
  especially runtime handoffs, research approvals, dispatches, receipts, and
  refine/invoke handoffs;
- recomposition residue, if present;
- current `next_move` verbatim.

Aggregate counts are useful, but they must not replace the per-node pending list. If a
node has no pending items, explicitly write `Pending: none`.
</all-status-contract>

<interaction-boundary>
Craft may prepare handoffs, receive receipts, apply receipt evidence, and open
residue. The called capability owns its native artifact contract, validation,
and verdict. Craft records route memory and local ledger state; it does not
rewrite native results.
</interaction-boundary>

<process>
1. Resolve the target workspace before touching any ledger (see
   <workspace-resolution>): discover every Craft space in the repository, decide which
   one the work belongs to, and bind to that scope instead of defaulting to the first
   or root ledger.
2. If a Craft ledger already exists for that scope, treat it as authoritative — its
   contexts, blockers, enablers, open decisions, and gaps already govern the work.
   Operate inside it (state / decide / refine / recompose) rather than starting a new
   root.
3. Only if no ledger covers the scope and the user wants to start, create `.craft/`,
   `.craft/artifacts/`, `.craft/ledger.yml`, and `CRAFT.md` in that scope.
4. Keep ledger changes small and explicit; preserve existing rows unless the
   user asks for a correction.
5. Record descriptions, blockers, enablers, decisions, gaps, definitions, and
   next moves as structured ledger state.
6. Add or refresh ledger indexes after each meaningful mutation so current
   blockers, decisions, gaps, next moves, and artifact links are easy to find.
7. Use child contexts for recursive work that has its own purpose, artifacts,
   blockers, or recomposition target.
8. Validate before claiming pass, closure, or recomposition.
9. Export or update `CRAFT.md` only as a linked view of `.craft/ledger.yml`.
10. Record residue and next move after each meaningful Craft operation.
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

- resolve the owning workspace before acting and treat an existing scoped ledger as authoritative,
- keep `.craft/ledger.yml` as source of truth,
- keep `CRAFT.md` as a linked human view,
- preserve a machine-readable index or ledger `indexes` section,
- for all-status requests, show pending work in each node with IDs and summaries rather
  than only aggregate counts,
- preserve local candidate definition status,
- prevent raw blocker direct resolution,
- require decision question, description or impact, rationale, evidence, and
  links when a decision references ledger rows or artifacts,
- require recomposition evidence before child context closure,
- distinguish route-shape evidence from execution evidence,
- record residue and next move,
- avoid mutating Arcanum canonical surfaces unless the user's task explicitly
  targets Craft maintenance or promotion.
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
- Pending by node:
  - <node title/path>: <blockers, blocking decisions, open decisions, gaps,
    pending artifacts/routes, recomposition residue, next_move>
- Residue: <remaining gaps/blockers/decisions or none>
- Next move: <next action>
- Boundary check: <what was not mutated>
```
</output-contract>
