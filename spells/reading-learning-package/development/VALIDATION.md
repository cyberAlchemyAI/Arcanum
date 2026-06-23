# Reading Learning Package Validation

Date: 2026-06-22

## Checks Run

| Check | Command | Result |
| --- | --- | --- |
| Dispatch route validation | `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py arcanum/spells/reading-learning-package/development/reading-learning-package.dispatch.json` | pass |
| Dispatch JSON parse | `python3 -m json.tool arcanum/spells/reading-learning-package/development/reading-learning-package.dispatch.json` | pass |
| Runtime compile | `python3 -m py_compile arcanum/spells/reading-learning-package/runtime/reading_learning_package.py arcanum/spells/reading-learning-package/validation/run-fixtures.py` | pass |
| Fixture suite | `python3 arcanum/spells/reading-learning-package/validation/run-fixtures.py` | pass |
| Markdown links | `find arcanum/spells/reading-learning-package -name '*.md' -print0 \| xargs -0 -n1 bash tools/check_markdown_links.sh` | pass |
| Registry markdown links | `bash tools/check_markdown_links.sh arcanum/registry/SPELLS.md` | pass |
| Temp bootstrap resolution | `bash arcanum/tools/bootstrap_arcanum.sh --target <tmp> --sigils "" --spells reading-learning-package --profile repo-codex,claude --force` | pass |
| Generated mirror links | `bash tools/check_markdown_links.sh .agents/skills/reading-learning-package/SKILL.md && bash tools/check_markdown_links.sh .claude/skills/reading-learning-package/SKILL.md` | pass |
| Public boundary scan | private path and private repository literal scan over spell, registry, and generated mirrors | pass, no matches |
| Diff whitespace | `git -C arcanum diff --check -- spells/reading-learning-package registry && git diff --check -- .agents/skills/reading-learning-package .claude/skills/reading-learning-package` | pass |

## Validation Notes

- The dispatch route validates as `VALIDATION=pass`.
- The fixture suite validates `deep_voice_reading`, `quick_video`, and
  `medium_explanation`, plus a missing-source block case.
- Per-package validation reports may return `flag` when no deterministic PDF
  renderer exists. This is expected when HTML fallback is emitted and the
  renderer gap is explicit.
- The Spellcraft contract now explicitly names aliases, required and optional
  sigils, prerequisites, shared state, handoff artifacts, gates, failure policy,
  local customization, observability, experiment harness evidence, and output
  contract.
- The registry lists `Reading Learning Package` with no aliases and a source
  boundary that preserves `research-tower` evidence authority and Whisper
  composition authority.
- Temporary bootstrap generation proves the repo Codex and Claude skill surfaces
  resolve to `canonical_source: spells/reading-learning-package/README.md`.

## Remaining Lifecycle Evidence

| Evidence | Owner | Status |
| --- | --- | --- |
| Spell contract | `spellcraft` | pass; registry promotion recorded |
| Preset fixtures for deep, quick, and medium presets | `experiment-harness` | pass |
| PDF renderer detection and fallback | `task-session` | flag accepted; optional renderer integration remains future work |
| End-to-end package fixture | `spellcraft` / `experiment-harness` | pass |
| Promotion receipt | `spellcraft` | pass; see `PROMOTION-RECEIPT.md` |
