# Invoke Handoff: Artifact Metadata Validator

## Identity

- Mode: handoff
- Spell: invoke
- Handoff type: execution-continuation
- Source session: current Codex thread on 2026-05-29
- Target lifecycle owner: Constitution Governance
- Target repository: `/home/vrondelli/projects/domainspec-core/arcanum`
- Context pack: `CONTEXT-PACK.md`
- Handoff index: `handoff-index.json`

## New Session Prompt

```text
Continue Artifact Constitution / Constitution Governance work in `/home/vrondelli/projects/domainspec-core/arcanum`.

Use Task Session for one bounded implementation slice: implement artifact metadata validation so governed files can declare artifact intent/type and validators can select the right constitution rules.

Start from:
- `framework/ARTIFACT-METADATA-CONSTITUTION.md`
- `arcana/constitution-governance/development/ARTIFACT-METADATA-VALIDATION-ADAPTER.md`
- `arcana/constitution-governance/development/handoffs/20260529T161446Z-artifact-metadata-validator/CONTEXT-PACK.md`
- `tools/validate-artifact-constitution.sh`

Goal:
- add `tools/validate-artifact-metadata.py` or equivalent parser,
- parse metadata from Markdown frontmatter, YAML `artifact` block, and JSON `artifact` object,
- require key fields for new governed source artifacts while avoiding legacy noise,
- add self-test fixtures,
- wire the helper into `tools/validate-artifact-constitution.sh` if safe,
- update the adapter/work-pack evidence.

Do not work on x-ray YAML component conversion in this session.
```

## Route Rationale

This is an execution continuation because the rule and adapter plan already exist. The missing work is deterministic implementation and validation evidence.

Recommended next route:

```bash
task-session to arcana/constitution-governance/development/ARTIFACT-METADATA-VALIDATION-ADAPTER.md
```

If the new session wants a formal work-pack slice first, create a small `CG-006A` task under `arcana/constitution-governance/development/WORK-PACK.md` before implementation.

## Context Builder Selection Summary

Selected:

- the user's stated gap: file intent/type should drive validation selection,
- Artifact Metadata Constitution,
- metadata validation adapter plan,
- current artifact constitution validator limitation,
- validation commands and fixture expectations,
- scope exclusions to avoid blending with x-ray implementation.

Excluded:

- full x-ray visual-layered revision history,
- x-ray component library details beyond the motivating validation gap,
- unrelated generated-artifact cleanup,
- Constitution Governance promotion work beyond this validator slice.

## Obligation Coverage Matrix

| Obligation | Coverage | Source |
| --- | --- | --- |
| Prompt for new session | pass | `New Session Prompt` above |
| Source session reference | pass | current Codex thread, 2026-05-29 |
| Handoff type | pass | execution-continuation |
| Context Builder selection | pass | `CONTEXT-PACK.md` |
| Target boundary | pass | Artifact Metadata validator only |
| Next route | pass | Task Session to adapter plan |
| Blockers | pass | none; implementation choices remain local |
| Non-goals | pass | x-ray YAML conversion, promotion, generated cleanup |

## Gaps And Blockers

No blocker gaps for starting the next session.

Non-blocker gaps:

- The exact parser implementation shape is still open: standalone Python helper vs direct shell integration.
- Selector/profile registry validation may be deferred if it is too large for the first slice.
- Legacy migration policy is not implemented; first slice should avoid failing old files.

## Provenance

This handoff was produced by Invoke handoff mode from the current session after the user asked to move Artifact Constitution work into another session.

Relevant artifacts created before this handoff:

- `framework/ARTIFACT-METADATA-CONSTITUTION.md`
- `arcana/constitution-governance/development/ARTIFACT-METADATA-VALIDATION-ADAPTER.md`
- `framework/ARTIFACT-CONSTITUTION.md` update linking the metadata constitution
- `arcana/constitution-governance/development/WORK-PACK.md` update adding CG-006 evidence.
