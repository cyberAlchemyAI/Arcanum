# Code Tag Audit — deterministic tools

Reference implementation for the [code-tag-audit](../SKILL.md) sigil (M2-C2). Deterministic TypeScript, no LLM. Run with `tsx` (e.g. `pnpm dlx tsx <tool>.ts`).

| Tool | Purpose | Key flags |
| --- | --- | --- |
| `extract-code-tags.ts` | Scan source for `domainspec:` docstring tags → JSON inventory | `--include <dir>` `--output <json>` `--mode strict\|warn` |
| `validate-code-tags.ts` | Validate inventory against schema + taxonomy/relationships | `--input <json>` `--taxonomy <md>` `--relationships <md>` `--features-root <dir>` `--waivers <yaml>` |
| `check-code-tag-composability.ts` | Check tags compose without conflict | `--input <json>` |
| `compare-code-tag-drift.ts` | Compare code tags vs feature docs → drift report | `--input <json>` `--report <md>` |

Language adapters (js/ts/py) under `lib/code-tag-adapters/`. All paths are flag-configurable; defaults are generic (`code-tags.json`, etc.). For Arcanum, point `--taxonomy`/`--relationships` at `definitions/TAXONOMY.md` / `definitions/RELATIONSHIPS.md`.

Verified: extract/validate/composability run green in Arcanum against `definitions/`. Ported from the DomainSpec deterministic toolchain; DS-specific default paths genericized; moat-leak clean.
