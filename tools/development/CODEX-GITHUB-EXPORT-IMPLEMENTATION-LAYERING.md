---
module: codex-github-export
version: current
status: draft
updatedAt: 2026-06-01
docType: implementation-layering
---

# Implementation Layering: Codex/GitHub Export

## Purpose

Make Arcanum easy to export into a fresh Codex and GitHub project without relying on legacy `.codex/commands` as the primary discovery surface.

## Source Contract

- Export review findings from 2026-06-01.
- Bootstrap installer: `tools/bootstrap_arcanum.sh`.
- Repository command surface: `tools/arcanum`.
- Codex skill discovery guidance: `README.md`.
- Existing native package completeness work-pack: `tools/development/NATIVE-SKILL-PACKAGE-COMPLETENESS-WORK-PACK.md`.

## Target And Scope

- Target: Codex/GitHub export path.
- Scope: repository install workflow and deterministic resolver.
- Current state: partially implemented.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether a fresh repository can receive repo-scoped Codex skills. | `repo-codex` profile writes `.agents/skills` packages. | Bootstrap profile, generated packages, basic AGENTS guidance. | GitHub archive live download proof. | `/tmp` install contains `.agents/skills/refine/SKILL.md` and `arcanum-refine/SKILL.md`. | Continue if profile output is complete. |
| L1 | After this layer, we know whether repo-local `tools/arcanum` resolves native skills without legacy command files. | Resolver checks `.agents/skills` before/alongside `.codex/commands`. | `--list`, `--resolve`, prompt building metadata compatibility. | Full observability skill-mode parity. | `/tmp` install resolves `refine` without `--legacy-codex-commands`. | Harden if resolver works for alias and canonical packages. |
| L2 | After this layer, we know whether export validation is repeatable. | Smoke commands for profile combinations. | Syntax checks and `/tmp` staged installs for `repo-codex`, `repo-local`, `github-copilot`, `personal-codex`, and `claude`. | CI workflow integration. | Commands listed in work-pack pass. | Package after smoke suite passes. |
| L3 | After this layer, we know whether GitHub install is release-ready. | Remote archive install proof from pushed ref. | `install_arcanum.sh` documentation and remote smoke. | Versioned release/tag automation. | `curl ... install_arcanum.sh` path installs expected surfaces from GitHub. | Publish or tag after remote proof. |

## Non Regression Guardrails

- Do not make `.codex/commands` primary again; it remains an explicit legacy surface.
- Generated native packages keep provenance frontmatter and copied support assets.
- Alias packages remain thin.
- Repo-local tools stay deterministic and do not spawn nested model CLIs by default.

## Recommended Next Layer

- Next layer: L0 + L1.
- Key decision unlocked: fresh project Codex skill export and native resolver proof.
- Major deferred scope: live GitHub archive install proof after committing and pushing.
