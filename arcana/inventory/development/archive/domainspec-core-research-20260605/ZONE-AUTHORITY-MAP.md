---
module: inventory-domainspec-core
version: 0.1.0
status: draft
updatedAt: 2026-06-05
docType: research-lane-output
lane: zone-authority-map
dispatch: domainspec-core-tagging-indexing-20260605
---

# Zone Authority Map

## Scope

This map classifies top-level zones in
`/home/vrondelli/projects/domainspec-core` for repository-wide Inventory tagging
and indexing.

Inventory use: route future lookup and ingest work. This map does not authorize
source moves, deletions, lifecycle promotion, ontology promotion, or definition
promotion.

## Repository Frame

Evidence:

- `/home/vrondelli/projects/domainspec-core/README.md`
- `/home/vrondelli/projects/domainspec-core/.gitmodules`
- `/home/vrondelli/projects/domainspec-core/ops/REPOSITORY-ORGANIZATION-PLAN.md`
- `/home/vrondelli/projects/domainspec-core/ops/ASSET-OWNERSHIP-POLICY.md`

The root README describes `domainspec-core` as a unified research hub with a
3-project operating model:

- DomainSpec implementation source of truth,
- research orchestration hub,
- validation harness.

The `.gitmodules` file confirms nested repository boundaries:

| Submodule Path | Remote |
| --- | --- |
| `implementation/domainspec` | `https://github.com/vrondelli/domainspec.git` |
| `validation/poker-team` | `https://github.com/vrondelli/poker-team.git` |
| `arcanum` | `git@github.com:cyberAlchemyAI/Arcanum.git` |

## File Count Snapshot

From a current `rg --files` top-level scan:

| Zone | File Count | Initial Treatment |
| --- | ---: | --- |
| `.git` | 13734 | exclude |
| `projects` | 2749 | source, project-local |
| `arcanum` | 2412 | submodule source, Arcanum owner |
| `implementation` | 1529 | contains implementation submodule and runtime/generated state |
| `domainspec-lean-formalization` | 746 | source, research/formalization |
| `validation` | 565 | contains validation submodule and sandbox |
| `.github` | 352 | root orchestration assets |
| `research` | 286 | root research project source |
| `.arcanum` | 100 | local runtime/generated state |
| `cyberAlchemy` | 56 | candidate concept/ontology/product source |
| `.planning` | 22 | planning state |
| `vscode-workspaces` | 15 | workspace navigation |
| `tools` | 11 | executable checks and sync scripts |
| `.codex` | 9 | local runtime/adapter state |
| `docs` | 7 | root docs surface |
| `sigils-library` | 8 | capability library source/candidate authority |
| `ops` | 3 | repository governance source |
| `.githooks` | 1 | local hook source |
| `.agents`, `.data`, `output` | 0-3 | local/runtime/generated state |

## Authority Classes

| Class | Meaning | Default Inventory Action |
| --- | --- | --- |
| canonical-source | owns durable behavior or policy | index and cite as source |
| submodule-source | owns durable behavior inside nested Git boundary | index by pointer and owner; avoid parent mutation |
| research-source | owns project research evidence | index by project contract and source status |
| project-local-source | owns local project artifacts | index by project, avoid cross-project promotion |
| generated-state | produced by tools or runtime | exclude by default |
| local-runtime-state | machine/session/runtime state | exclude by default |
| navigation-surface | workspace/docs/navigation | index as navigation evidence only |
| candidate-knowledge | concept or ontology candidate | index as candidate; route promotion to owner |

## Zone Map

| Zone | Authority Class | Owner Signal | Inventory Notes |
| --- | --- | --- | --- |
| `README.md` | canonical-source | root operating model | Cite for the 3-project model and quick links. |
| `.gitmodules` | canonical-source | Git submodule contract | Cite for nested repo boundaries. |
| `ops/` | canonical-source | repository governance | Use `ASSET-OWNERSHIP-POLICY.md` and `REPOSITORY-ORGANIZATION-PLAN.md` as authority for asset classes and zone policy. |
| `research/` | research-source | root research orchestration | Use `research/registry/PROJECT-INDEX.md` as primary navigation; project internals remain project-owned. |
| `implementation/domainspec/` | submodule-source | DomainSpec implementation source of truth | Do not mutate from parent Inventory. Index source pointers, canonical pack assets, and repo-local inventory surfaces. |
| `validation/poker-team/` | submodule-source | validation harness | Index as validation/case-study evidence; respect Type C overlay ownership. |
| `arcanum/` | submodule-source | Arcanum framework/capabilities | Reuse existing whole-Arcanum Inventory method. Avoid duplicating its evidence cards. |
| `sigils-library/` | candidate-knowledge | claims authoritative Cyber Alchemy sigil library | Authority conflicts with `arcanum/` must route to decision-gate before promotion. |
| `domainspec-lean-formalization/` | research-source | theorem/formalization repository | Index as mathematical/formal source; separate Lean proofs from prose/research. |
| `cyberAlchemy/` | candidate-knowledge | candidate agentic-system and ontology workspace | Index as candidate knowledge. Ontology promotion belongs to Ontology Vault or CyberAlchemy owner artifacts. |
| `docs/` | navigation-surface | root registry/glossary placeholders | Use as root docs surface; current registry/glossary are mostly empty templates. |
| `projects/` | project-local-source | project-specific workspaces | Index by project. GoldenQuill already has memory/context indexes. |
| `.github/` | canonical-source and generated-support | Type B root orchestration assets | Index only durable agents/skills/workflows; do not treat generated manifests as source unless needed. |
| `.planning/` | local planning state | GSD workflow state | Exclude by default; may become evidence for planning-work queries. |
| `.arcanum/` | local-runtime-state | local Arcanum install/runtime state | Exclude by default. Runtime evidence requires explicit durable promotion. |
| `.codex/` | local-runtime-state | local Codex command/adapter state | Exclude by default. |
| `.agents/` | local-runtime-state | repo-scoped agent/skill exposure | Index only when skill-surface installation is the task. |
| `.data/` | local-runtime-state | generated/local data | Exclude by default. |
| `output/` | generated-state | output artifacts | Exclude by default. |
| `tools/` | canonical-source | repo checks and sync scripts | Index as validation/tooling source. |
| `validation/sigil-spell-sandbox/` | project-local-source | sandbox validation area | Index separately from `validation/poker-team`. |
| `vscode-workspaces/` | navigation-surface | operator workspace shortcuts | Index as navigation only. |

## Authority Risks

1. `arcanum/` and `sigils-library/` both present sigil/capability authority
   language. Do not merge these zones without a decision gate.
2. `implementation/domainspec` is a submodule and also contains local runtime
   state such as `.arcanum`, `.codex`, `.data`, and generated inventories. Index
   the source repository separately from runtime artifacts.
3. `research/projects/*/inventory` directories already exist. Parent Inventory
   should point to them and create cross-project lookup handles, not duplicate
   project-local inventories.
4. `cyberAlchemy/ontology` contains candidate ontology material. Inventory may
   capture source evidence, but promotion belongs elsewhere.
5. `.github` contains durable root orchestration assets and generated manifests.
   Treat generated manifests as secondary evidence.

## Residue

- `sigils-library/README.md` claims authoritative registry status, while
  `arcanum/README.md` describes Arcanum as the governed capability framework.
  This needs a decision before either zone becomes canonical for shared sigil
  authority.
- The root README still references external canonical paths
  `/home/vrondelli/projects/poker-team/domainspec` and
  `/home/vrondelli/projects/poker-team`, while the current checkout uses
  submodule paths under `implementation/` and `validation/`. Treat this as a
  path-contract review candidate.
- File-count evidence is a shape signal only. It should not decide priority
  without task value and source authority.
