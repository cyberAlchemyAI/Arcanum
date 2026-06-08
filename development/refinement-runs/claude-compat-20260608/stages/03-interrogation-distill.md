# Stage 7-8 Receipt — Interrogation + Distill Repair

- surface: claude-agent (general-purpose) | status: pass
- native_capability: blocked | substituted_with: claude-agent

## Verified (file:line)
- `write_generated_skill_file` (bootstrap_arcanum.sh:883-909) copies allowed-tools verbatim for all runtimes — CONFIRMED.
- Dangling `skills:` real AND worse: `prefixed_skill_packages` defaults false (:72); orchestrate written to dir `orchestrate` (:1013) with `name: arcanum-orchestrate` (:978); `arcanum-orchestrate` alias only when prefixed (:1015). So default claude install has no `arcanum-orchestrate` package; stage-worker (:1142) + CLAUDE.md (:1160) dangle; plus empty-dir `mkdir` (:1131) and name≠dir on orchestrate.
- Nothing in Arcanum consumes codex/copilot `allowed-tools` → changing/dropping them is cosmetic; source edit is unjustified blast radius.

## Distilled decision list
D1 claude-only allowed-tools map (generation); D2 orchestrate identity + dangling fix; D3 reusable validate-claude-skills.sh; D4 bootstrap blocking post-step; D5 doctrine reword; D6 narrow body fix; D7 dogfood make target + commit; D8 CI validate + freshness; D9 optional vocab note.
Rejected: 20-file source vocab edit; codex/copilot DROP/reverse-map; generated frontmatter trim.
