# Refine Seed Proposal — Claude Compatibility for All Sigils & Spells

- run_id: claude-compat-20260608
- target: `arcanum/` Claude skill surface (all sigils + spells) and the installer path that generates it
- preset: full
- research_mode: research-if-gap-appears
- subagent_strategy: recommended (Claude `Agent` subagents as stage workers; native Arcanum capability skills not installed → receipts recorded as `native_capability=blocked, substituted_with=claude-agent`)

## Target / Source Context

The installer (`arcanum/tools/bootstrap_arcanum.sh`) already exposes a `claude` profile that
generates `.claude/skills/<name>/SKILL.md` packages via `write_claude_surface` →
`write_runtime_skill_packages` → `write_generated_skill_file`. Compatibility is therefore a
**correctness/parity** problem, not greenfield. Source frontmatter (including `allowed-tools`)
is copied verbatim, so Codex-flavored tool names (`Task`, `AskQuestions`) leak into generated
Claude skills, mis-scoping them. There is no Claude-package validation, a doctrine conflict in
`sigil-runtime-installer/SKILL.md`, and the source repo is not dogfooded.

## Write Scope (for the eventual EXECUTION, not this run)

- `arcanum/tools/bootstrap_arcanum.sh` (generation + validation)
- `arcanum/tools/` new validation script for Claude packages
- `arcanum/arcana/sigil-runtime-installer/SKILL.md` (doctrine reconciliation)
- Possibly the 32 source `SKILL.md` `allowed-tools` lines (decided by the design tournament)
- Dogfood entrypoint (make target / wrapper) + generated `.claude/` surface in this repo

## Done Criteria

1. Every generated `.claude/skills/*/SKILL.md` has `allowed-tools` ⊆ real Claude tools.
2. A validation step blocks installs that would emit an invalid Claude package.
3. Doctrine conflict resolved; Claude-surface ownership documented.
4. This repo dogfoods: arcanum sigils discoverable as Claude skills here.
5. Spells covered with the same guarantees as sigils.

## Validation Surface

`bash` install dry-run + new Claude-package validator; `/reload-skills` discovery in this repo.

## Research Decision

`research-if-gap-appears` — the answer is local (installer + SKILL.md sources). External research
only if a named gap about Claude skill-frontmatter rules appears.
