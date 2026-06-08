# Stage 6 Receipt — Invoke Design (A/B Tournament)

- surface: claude-agent (Plan ×2, parallel) | status: pass
- native_capability: blocked | substituted_with: claude-agent

## Approach A — generation-time transform, zero source edits
Per-runtime allowed-tools map claude-only inside write_generated_skill_file; leave bodies; keep frontmatter; validate_claude_surface inside bootstrap; remove stage-worker `skills:`; reword doctrine; Makefile dogfood.

## Approach B — canonical source vocabulary + hard gate
Edit ~20 source files to Claude vocab (canonical=Claude names); per-runtime map table (codex/copilot drop or map); reusable validate-claude-skills.sh + CI + freshness drift diff; trim generated frontmatter; narrow source body neutralization; framework/RUNTIME-TOOL-VOCABULARY.md; fix dangling skills:; continuous dogfood.

## Tournament outcome (resolved in stage 7)
Winner: A's generator-only locus + B's reusable validator/CI/dogfood + B's dangling-skills bug catch. Rejected B's source-vocab edit and codex/copilot DROP/reverse-map machinery (nothing consumes those tokens).
