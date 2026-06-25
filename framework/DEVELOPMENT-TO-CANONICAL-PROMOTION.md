# Development To Canonical Promotion

Status: active
Owner: artifact-constitution, definitions-governance

This process governs how content moves from development artifacts into
canonical artifacts. It applies whenever a run, refinement, invoke package,
task-session result, architecture draft, glossary, validation report, or other
candidate evidence should change a source artifact.

Canonical vocabulary:

- `DEF-ARC-DEVELOPMENT-ARTIFACT`
- `DEF-ARC-CANONICAL-ARTIFACT`
- `DEF-ARC-PROMOTION-PATCH`
- `DEF-ARC-STAGED-DELTA`
- `DEF-ARC-APPROVAL-TOKEN`

## Rule

Development artifacts are evidence and proposal surfaces. Canonical artifacts
are authority surfaces. Content may cross that boundary only as a promotion
patch that names the target owner, source evidence, selected durable claim,
transformation rationale, validation surface, and approval state.

## Process

1. Classify the source artifact.
   Confirm whether the input is source, durable evidence, generated output, or
   local runtime state under [Artifact Constitution](ARTIFACT-CONSTITUTION.md).
   Treat raw `development/`, runtime, and run-package material as
   non-authoritative unless it has already been explicitly promoted to durable
   evidence.

2. Resolve the target canonical artifact.
   Identify the exact source file or package that owns the target scope. For
   definitions, use `definitions/DEFINITIONS.md`. For framework rules, use the
   relevant `framework/` constitution or standard. For capability behavior, use
   the owning `SKILL.md`, README, templates, validation files, or registry row.
   For architecture, resolve whether the target is an architecture inventory
   package, a package-local architecture document, or a framework architecture
   standard.

3. Select the smallest durable claim.
   Extract only the content that should become source authority. Leave local
   run details, rejected alternatives, private context, speculative notes, and
   unvalidated follow-ups in the development artifact.

4. Frame a promotion patch.
   The patch must record or make reviewable:
   source development artifact paths, target canonical path, owning capability
   or steward, selected claim or structure, omitted candidate material,
   validation expectation, index or generated-surface updates, and approval
   status.

5. Normalize into the target voice.
   Do not bulk-copy development prose when the canonical artifact has a tighter
   contract. Rewrite the selected content into the target artifact's format,
   authority level, terminology, and maintenance voice.

6. Run the owner gate.
   Use the owner for the target artifact type:
   `definitions-governance` for Arcanum-wide terms, `constitution-governance`
   for rule artifacts, `architecture-pattern-inventory` for architecture
   inventory packages, `sigil-development` for sigils, `spellcraft` for spells,
   and `decision-gate` for consequential scope or authority choices.

7. Validate the canonical target.
   Run available link, schema, artifact constitution, experiment harness, or
   artifact-specific checks. Architecture patches should verify source
   contracts, views, dependency or interface rules, decisions, risks,
   downstream notes, and gate result.

8. Sync lookup and generated surfaces.
   Update indexes, registries, generated runtime copies, downloadable packages,
   or drift audits only when the target artifact contract requires them. A
   canonical source update is incomplete when its lookup layer still points at
   the old authority.

9. Record the result.
   Preserve the source evidence path and validation result in adjacent
   documentation, a drift audit, a validation report, a promotion receipt, or
   the pull request body. Record deferred or rejected candidate material so it
   does not silently become authority later.

## Architecture Example

When an architecture development artifact proposes content for a canonical
architecture artifact:

1. Treat the development architecture file as candidate evidence.
2. Resolve the target: for example `architecture/ARCHITECTURE.md`,
   `arcana/<capability>/ARCHITECTURE.md`, an architecture inventory package, or
   another explicitly owned architecture source.
3. Extract the durable architecture claim, such as a dependency rule, layer
   model, source-contract view, interface rule, risk, or decision.
4. Rewrite that claim into the target architecture artifact's canonical format.
5. Cite the development artifact as evidence, not as authority.
6. Run architecture-specific validation and any repository link or schema
   checks.
7. Update related indexes, concept cards, dependency rules, or downstream notes
   required by the architecture package.
8. Leave unselected draft material in the development artifact with deferred or
   rejected status.

## Anti-Patterns

- Copying a whole development package into source because it passed one local
  run.
- Treating validation output as authority instead of evidence.
- Updating canonical architecture prose without updating companion indexes,
  concept cards, or dependency rules.
- Promoting private or workspace-specific content into public Arcanum source.
- Letting a downstream summary redefine a term that belongs in
  `definitions/DEFINITIONS.md`.
- Committing raw run folders when the durable result is a distilled source
  patch.

## Validation

For this process document, run:

```bash
tools/check_markdown_links.sh framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md
tools/validate-artifact-constitution.sh
```
