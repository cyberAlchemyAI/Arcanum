# WORK-PACK: Craft Feature Readiness Indexes

## Purpose

Implement an additive Craft readiness-index contract so ledgers that already point to Invoke work-packs can expose what is executable, what approval applies, and what mutation or publication remains blocked.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | flag | Planning is complete; mutation requires selected SWU and maintainer approval. |
| complexity | medium | Multiple canonical surfaces, examples, generated copies, and validation gates. |
| outputMode | split | Uses task and wave files under `work-pack/`. |
| designRef | [INVOKE-DESIGN.md](INVOKE-DESIGN.md) | Source design artifact. |
| implementationPlanRef | [INVOKE-PLAN.md](INVOKE-PLAN.md) | Source plan artifact. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0-L3 layer decisions. |
| activeLayerWindow | L0 | Start with schema/index contract. |
| currentExecutionTarget | `SWU-CFR-001` | First proposed executable unit. |
| executionMode | maintainer-approved-local-mutation | Do not publish without submodule-first checks. |
| blockedMutationScope | generated-surfaces, publication | Blocked until source edits pass L0/L1 validation. |
| blockedPublicationScope | commit, push, parent-gitlink | Blocked until generated surfaces and bump-check pass. |

## Objective Summary

- Add readiness lookup handles without invalidating existing Craft ledgers.
- Make repository-wide Craft status easier to consume when next moves point at work-packs.
- Preserve Craft as ledger authority and route memory, not execution owner.
- Keep public Craft development artifacts free of private workspace details.

## Task Status Board

| Task ID | Goal | Layer | Waves | Gate Status | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-CFR-001](work-pack/tasks/TASK-CFR-001.md) | Add schema and index contract. | L0 | W0 | ready | planned |
| [TASK-CFR-002](work-pack/tasks/TASK-CFR-002.md) | Update Craft skill and README. | L1 | W1 | blocked-on-TASK-CFR-001 | planned |
| [TASK-CFR-003](work-pack/tasks/TASK-CFR-003.md) | Add public-safe example or fixture coverage. | L2 | W2 | blocked-on-TASK-CFR-002 | planned |
| [TASK-CFR-004](work-pack/tasks/TASK-CFR-004.md) | Add validation and status/export review checks. | L2/L3 | W2 | blocked-on-TASK-CFR-003 | planned |
| [TASK-CFR-005](work-pack/tasks/TASK-CFR-005.md) | Regenerate generated surfaces and prepare publication gates. | L3 | W3 | blocked-on-TASK-CFR-004 | planned |

## SWU Manifest

| SWU | Parent Task | Goal | Dependencies | Write Scope | Acceptance Evidence | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| `SWU-CFR-001` | [TASK-CFR-001](work-pack/tasks/TASK-CFR-001.md) | Add optional readiness index schema contract. | none | `arcana/craft/templates/ledger.schema.yml` | Schema contains optional `execution_readiness` index contract and no required-field breakage. | `python3 - <<'PY' ... yaml.safe_load(...)` or equivalent YAML parse. |
| `SWU-CFR-002` | [TASK-CFR-001](work-pack/tasks/TASK-CFR-001.md) | Confirm existing examples remain compatible. | `SWU-CFR-001` | example parse only, or minimal example touch if needed | Existing examples parse and omit readiness indexes without error. | YAML parse examples. |
| `SWU-CFR-003` | [TASK-CFR-002](work-pack/tasks/TASK-CFR-002.md) | Update Craft `SKILL.md` guidance. | `SWU-CFR-001` | `arcana/craft/SKILL.md` | Linking/indexing and all-status contracts mention readiness handles and preserve non-execution boundary. | `rg -n "execution_readiness|approval_record|blocked_mutation_scope|product_worktree" arcana/craft/SKILL.md` |
| `SWU-CFR-004` | [TASK-CFR-002](work-pack/tasks/TASK-CFR-002.md) | Update Craft `README.md`. | `SWU-CFR-003` | `arcana/craft/README.md` | README explains readiness indexing as optional lookup data. | `rg -n "execution readiness|approval|work-pack|SWU" arcana/craft/README.md` |
| `SWU-CFR-005` | [TASK-CFR-003](work-pack/tasks/TASK-CFR-003.md) | Add public-safe readiness example or fixture. | `SWU-CFR-004` | `arcana/craft/examples/` | New synthetic fixture shows ready and blocked scopes without private workspace details, or owner approval explicitly permits editing named examples. | YAML parse plus strict public-boundary scan. |
| `SWU-CFR-006` | [TASK-CFR-004](work-pack/tasks/TASK-CFR-004.md) | Add validation and status/export review checklist. | `SWU-CFR-005` | `arcana/craft/development/refinement-runs/20260614T200439Z-craft-feature-readiness-indexes/` or validation docs | Checklist names parse, grep, diff, and public-boundary checks. | Run listed checks. |
| `SWU-CFR-007` | [TASK-CFR-005](work-pack/tasks/TASK-CFR-005.md) | Regenerate generated runtime surfaces. | `SWU-CFR-006` | generated runtime packages only | Generated `craft` copies include new canonical wording. | Bootstrap/generation command plus grep. |
| `SWU-CFR-008` | [TASK-CFR-005](work-pack/tasks/TASK-CFR-005.md) | Run submodule-safe publication checks. | `SWU-CFR-007` | no content edits unless fixing validation residue | `git diff --check` passes; `make bump-check` passes before parent publication. | `git diff --check`; `make bump-check` |

## Execution Rules

- Select one SWU before execution.
- Do not mutate generated surfaces before canonical source changes pass.
- Do not commit or push from this work-pack unless the user explicitly requests publication.
- If publishing, commit and push `arcanum` first, then update the parent gitlink after `make bump-check`.

## Validation Strategy

1. Parse JSON artifacts in this packet.
2. Parse YAML schema and examples after each schema/example SWU.
3. Run targeted grep checks for readiness fields.
4. Run a public-boundary scan before any public submodule commit.
   - Minimum denylist: `/home/`, `../`, `projects/`, `implementation/`, private product names, private source names, person/team names, and any local product path.
5. Run `git diff --check`.
6. Run `make bump-check` before parent gitlink movement.

## Next Move

Start with `SWU-CFR-001` only after maintainer approval for canonical Craft source mutation.
