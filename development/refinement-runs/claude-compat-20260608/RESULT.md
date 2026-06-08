# Refine Result — Claude Compatibility for All Sigils & Spells (Non-Executed Plan)

- run_id: claude-compat-20260608
- target: `arcanum/` Claude skill surface + the installer that generates it
- status: pass (plan ready; not executed)
- preset: full
- research: research-if-gap-appears (no external research needed — defect is local)
- subagent_strategy: recommended → used (Context Builder, 2× Design tournament, Interrogation) as Claude `Agent` subagents; native Arcanum capability skills not installed, so receipts recorded as `native_capability=blocked, substituted_with=claude-agent`

## Problem (verified)

The installer **already** generates a Claude surface (`write_claude_surface` →
`.claude/skills/`), so this is a correctness/parity fix, not greenfield. The one
runtime-fatal defect: `write_generated_skill_file`
([bootstrap_arcanum.sh:883-909](../../../tools/bootstrap_arcanum.sh#L883-L909))
copies source frontmatter verbatim, so 21 sigils ship `allowed-tools` containing
`Task` / `AskQuestions` — names that don't exist in Claude (`Agent`,
`AskUserQuestion`). Claude treats `allowed-tools` as an allowlist, so those skills
**silently lose** delegation and clarifying-question capability.

Secondary defects found: dangling `skills: arcanum-orchestrate` reference + an
empty `arcanum-orchestrate/` dir + orchestrate `name`≠dir; no Claude-package
validation; doctrine conflict in `sigil-runtime-installer/SKILL.md`; repo not
dogfooded.

## Decision (synthesized from the A/B tournament)

**Fix at the generator, claude-only, plus a reusable validator gate.** Reject
editing the 20 source files into one runtime's vocabulary (nothing consumes the
codex/copilot tokens, so a source land-grab only perturbs two working surfaces to
fix one). Keep one canonical source; transform per-runtime at generation.

## Implementation plan (MVP)

### Phase 1 — Make every Claude skill valid (must)

**Step 1 [D1] — claude-only `allowed-tools` map at generation.**
In `write_generated_skill_file` ([bootstrap_arcanum.sh:866-927](../../../tools/bootstrap_arcanum.sh#L866-L927)),
when `runtime == claude`, rewrite the `allowed-tools` line: `Task→Agent`,
`AskQuestions→AskUserQuestion`. Sources use inline CSV (`allowed-tools: Read, …, Task`),
so the transform must parse CSV, map tokens, dedup, preserve order. Codex/copilot =
identity passthrough (no source edits). Files with no `allowed-tools` line
(`robot-talks`) and synthesized spell frontmatter are unaffected (no line to match).

**Step 2 [D2] — fix the orchestrate package identity + dangling reference.**
Pick one canonical id (`arcanum-orchestrate`) and use it consistently:
- package dir ([:1013](../../../tools/bootstrap_arcanum.sh#L1013)) and `name:` ([:978](../../../tools/bootstrap_arcanum.sh#L978)) must match,
- stage-worker `skills:` ([:1142](../../../tools/bootstrap_arcanum.sh#L1142)) and `CLAUDE.md` ([:1160](../../../tools/bootstrap_arcanum.sh#L1160)) must reference the same id,
- remove the stray empty-dir `mkdir -p .claude/skills/arcanum-orchestrate` ([:1131](../../../tools/bootstrap_arcanum.sh#L1131)).

**Step 3 [D3] — reusable validator** `arcanum/tools/validate-claude-skills.sh <skills-root>`.
Fails (exit 1, reports all offenders) on: (a) `Task`/`AskQuestions` (or any token
outside the real Claude tool set) in `allowed-tools`; (b) `name` ≠ package dir;
(c) missing/empty `description`; (d) `skills:` entry not resolving to a sibling
package; (e) a skill dir with no `SKILL.md`. `--warn-only` for local use.

**Step 4 [D4] — bootstrap calls Step 3 as a blocking post-step** after
`write_claude_surface` (skip on `--dry-run`). Non-zero aborts the install with a
clear "fix sources / regenerate, do not edit generated packages" message. Closes
the "hide failures behind a success message" anti-pattern.

**Step 5 [D5] — resolve the doctrine conflict.** Reword the anti-pattern in
[sigil-runtime-installer/SKILL.md:118-126](../../../arcana/sigil-runtime-installer/SKILL.md#L118-L126)
to scope "avoid installing Claude…" to the *legacy command* installer, and
document that `tools/bootstrap_arcanum.sh --profile claude` owns + validates the
Claude surface.

### Phase 2 — Quality + durability (should)

**Step 6 [D6] — narrow operative-body fix at source.** Neutralize only genuinely
operative references ("use the Task tool", live `$slash`/`.codex/` execution
instructions). Do NOT touch domain nouns like the "Task Session" heading.

**Step 7 [D7] — dogfood this repo.** Add a `make claude-skills` target running
`arcanum/tools/bootstrap_arcanum.sh --target . --profile claude --sigils all --spells all --force`,
run it, and commit the generated `.claude/skills/` so arcanum's own sigils appear
as Claude skills here (this is what surfaced the original question).

**Step 8 [D8] — CI.** Job that generates to a temp dir and runs the validator;
after Step 7, add a freshness check (regenerate, diff against committed
`.claude/skills/`, fail on drift). Mirror `.github/workflows/drift-check.yml`.

### Optional

**Step 9 [D9]** — record the `Task→Agent` / `AskQuestions→AskUserQuestion` claude
map in an existing framework doc. Skip a dedicated vocabulary file.

### Explicitly rejected
Editing the ~20 source SKILL.md files into Claude vocabulary; DROP/reverse-map
machinery for codex/copilot; trimming tier/domain/version/origin from generated
frontmatter (Claude ignores them).

## Verification surface (for execution)
- `bash arcanum/tools/bootstrap_arcanum.sh --target /tmp/x --profile claude --sigils all --spells all --force` then `validate-claude-skills.sh /tmp/x/.claude/skills` → pass.
- Grep generated claude skills: no `Task`/`AskQuestions` in any `allowed-tools`.
- After Step 7: `/reload-skills` in this repo surfaces arcanum sigils.

## Recommended next routes
- **Sigil Development / Task Session** to execute Phase 1 (Steps 1-5) as one bounded change.
- Phase 2 as a follow-up task.
