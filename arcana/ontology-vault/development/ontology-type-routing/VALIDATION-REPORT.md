# Ontology Type Routing Validation

Date: 2026-07-31

Result: pass

## Contract Result

- Catalog entries: 6
- Routing cases: 7
- Clear cases selecting without user prompt: 6
- Ambiguous cases requiring user selection: 1
- Choices in ambiguous case: 3
- Project-local alias cases: 1
- Architecture-property correction regressions: 1
- Canonical definitions or promotion changes: 0

The architecture-property case selects element types, typed properties,
relations, profiles, observation projections, and findings. The bridge case
selects cross-branch realization, traceability, coverage, constraints, gaps,
and drift. They are distinct routes despite both potentially inspecting system
evidence.

## Commands And Results

### Routing, Catalog, And Links

```bash
node arcanum/arcana/ontology-vault/development/ontology-type-routing/validate-routing.mjs
```

Result: pass.

- Six reusable catalog types validated.
- Seven fixture results reproduced.
- Six clear cases did not prompt.
- One ambiguous case produced three catalog-backed choices.
- Project-local alias preservation and non-registration passed.
- Eleven local Markdown targets resolved across six changed canonical files.

The repository root has no `package.json`, so `npm run validate:docs` is not an
available root validation command (`ENOENT`). The dependency-free artifact
validator performs the scoped local-link check instead.

### Selective Generated-Package Sync

```bash
arcanum/tools/sync-generated-skill-package.sh \
  --target . \
  --sigil ontology-vault \
  --profiles repo-codex,claude \
  --apply
```

Result: pass. Only the Ontology Vault Codex and Claude packages were targeted;
the generation run also reported Claude skill validation as pass.

The same command without `--apply` completed its post-sync preview. Exact
comparison then confirmed:

- README parity for canonical, Codex, and Claude copies;
- runtime-profile template parity;
- ontology-type catalog parity;
- SKILL body parity after generated runtime frontmatter is removed.

### Scoped Whitespace

```bash
git -C arcanum diff --check -- arcana/ontology-vault
git diff --check -- .agents/skills/ontology-vault .claude/skills/ontology-vault
```

Result: pass with no output.

### Observability

```bash
jq -e . \
  .arcanum/observability/tmp/ontology-vault-20260731T193158Z-ontology-type-routing-update.json
arcanum/framework/observability/scripts/observe-invocation.sh \
  --envelope \
  .arcanum/observability/tmp/ontology-vault-20260731T193158Z-ontology-type-routing-update.json
```

Result: pass. The observer recorded central-ledger line 459, updated the
Ontology Vault capability views, and retained `manual` / `targeted-update` as
the reflection state.

## Quality And Authority Boundaries

- Usage evidence, observer inference, and applied edits remain separate.
- The six types are routing archetypes with `authority_effect: none`.
- Local aliases cannot extend the reusable catalog.
- Existing branch arguments remain traversal controls.
- No project ontology, canonical definition, promotion state, runtime product,
  or external transport changed.

## Blockers

None for this targeted update.

## Next Lifecycle Step

Observe five post-update meaningful Ontology Vault uses. Reflect earlier if a
clear request prompts, an ambiguous request silently selects, or
architecture-property intent routes to a bridge again.
