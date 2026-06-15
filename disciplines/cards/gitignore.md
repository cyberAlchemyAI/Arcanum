# Gitignore Discipline

Status: candidate
Steward: Constitution Governance

## Purpose

Govern what belongs in `.gitignore` across Arcanum and its consuming repositories. Keep generated artifacts, local runtime state, caches, secrets, and build output out of version control, while keeping canonical source, schemas, templates, and documentation tracked.

## Boundary

This discipline names the practice of deciding what is ignored versus tracked. It does not own:

- the tracked files themselves or their content,
- per-repository build tooling or language-specific tool defaults,
- submodule discipline (commit and push ordering across submodules),
- secret management beyond keeping secret material untracked.

Enforcement of the rules routes through [constitution-governance](../../arcana/constitution-governance/) and the repository owner; mutation of the catalog and this card routes through [discipline-governance](../../arcana/discipline-governance/).

## Evidence

- `../../framework/GITIGNORE-CONSTITUTION.md` - the enforceable constitution that hardens this practice into reviewable rules.
- `../../framework/runtime/README.md` - the runtime-boundary discipline already separates canonical source, generated install surfaces, and local runtime state, which is the same separation `.gitignore` must protect.
- `../DISCIPLINES.md` - the `runtime-boundary` and `artifact-constitution` rows show that "keep generated and local state out of the tracked tree" is a recurring, cross-capability concern.

## Quality Bar

A useful gitignore discipline entry must:

- name a recurring practice (separating tracked source from generated or local state) rather than a one-off ignore edit,
- cite concrete repository evidence,
- identify Constitution Governance as steward,
- separate the ignore decision from the file content and build tooling it touches,
- name the next hardening move (the gitignore constitution and a future ignore-policy validator).

## Promotion Guardrail

Discipline evidence can recommend a route, but it cannot directly promote registry, ontology, glossary, sigil, or spell knowledge. Advancing this discipline beyond `candidate` requires the constitution's rules to gain a validation surface and a named mutation boundary.
</content>
