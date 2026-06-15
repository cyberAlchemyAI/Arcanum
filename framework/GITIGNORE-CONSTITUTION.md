# Gitignore Constitution

Status: candidate
Date: 2026-06-15
Owner: Constitution Governance

## Purpose

`.gitignore` content should keep generated artifacts, local runtime state, caches, and secrets out of version control, while keeping canonical source, schemas, templates, and documentation tracked. Ignore rules should be narrow, evidence-backed, and safe to review.

This constitution hardens the [gitignore discipline](../disciplines/cards/gitignore.md) into reviewable rules.

## Scope

Applies to:

- new and changed `.gitignore` files in Arcanum and its consuming repositories,
- ignore rules added by Arcanum sigils, spells, templates, or tools,
- decisions about whether an artifact class belongs in the tracked tree.

Does not apply to:

- the content of tracked files,
- per-repository build tooling or language-specific tool defaults that ship their own ignore lists,
- submodule commit and push ordering, which the runtime-boundary and submodule rules own,
- secret management beyond keeping secret material untracked.

## Rules

| Rule ID | Rule | Validation Mode | Validator | Status |
| --- | --- | --- | --- | --- |
| `gitignore.generated` | Generated artifacts, build output, and run bundles must be ignored, not tracked. | review | none yet | candidate |
| `gitignore.local-state` | Local runtime state, session artifacts, caches, and editor or worktree scratch must be ignored. | review | none yet | candidate |
| `gitignore.secrets` | Secret material (keys, tokens, credentials, `.env` files) must never be tracked, and ignore patterns must cover the common secret file names. | review | none yet | candidate |
| `gitignore.source-tracked` | Ignore rules must not over-broadly exclude canonical source, schemas, templates, or documentation. | review | none yet | candidate |
| `gitignore.already-tracked` | Adding an ignore rule does not untrack a file that is already tracked; untracking requires an explicit `git rm --cached` decision recorded in the change. | review | none yet | candidate |
| `gitignore.narrow-scope` | An ignore rule should be as narrow as the artifact class it targets; prefer a scoped path over a broad glob. | review | none yet | candidate |

## Examples

Preferred:

- ignoring `development/runner-bundles/` (generated run tarballs),
- ignoring `.arcanum/observability/**/*.jsonl` and reflection state (local telemetry),
- ignoring `.claude/worktrees/` and session scratch directories,
- ignoring `__pycache__/`, `*.py[cod]`, and `.venv/`.

Not preferred:

- ignoring a whole `docs/` or `src/` tree to silence one generated file,
- adding an ignore rule for a file that is already tracked and expecting it to disappear,
- committing secrets and relying on later history rewrites,
- a broad `*` or `*.json` rule that also hides canonical schema or source.

## Validation

No deterministic validator exists yet. Until one does, changes to `.gitignore` are reviewed against these rules.

Next hardening move: add an ignore-policy check under `tools/` that flags already-tracked files matched by new ignore rules and over-broad globs that cover source paths, then raise the affected rules from `review` to `deterministic`.

## Promotion Boundary

This constitution is `candidate`. Promote it to canonical only after the ignore-policy validator exists and the [gitignore discipline](../disciplines/cards/gitignore.md) names its validation surface and mutation boundary.
</content>
