# TASK-NDR-003 — Canonical Source and Generated Surfaces

Owner: Task Session

Objective: eliminate the hardcoded Orchestrate skill body and make installed surfaces reproducible from canonical runtime source.

## SWU-NDR-006 — Generate Orchestrate from canonical source

- Behavior: change bootstrap generation so Orchestrate packages are copied/rendered from `runtime/orchestrate/` instead of a hardcoded skill heredoc.
- Split analysis: canonical generation is independently testable in a temporary install root; current repo surface refresh is excluded.
- Dependencies: `SWU-NDR-005` pass receipt.
- Source anchors: `tools/bootstrap_arcanum.sh` `write_orchestrate_skill_file`; `runtime/orchestrate/SKILL.md`; `ARCHITECTURE.json` generation rule.
- Related context: `DESIGN.md` deployment and generation view.
- Write scope: `tools/bootstrap_arcanum.sh`, `runtime/orchestrate/`, bootstrap generation tests and fixtures.
- Done criteria: hardcoded canonical skill content is removed; temporary Codex and repository-local installations contain the canonical contract, scripts, schemas, and host driver material selected for them.
- Acceptance evidence: temporary install manifests, byte/semantic comparison, bootstrap test receipt.
- Validation: bootstrap into isolated temporary roots and compare canonical/generated required files.
- Handoff: pass unlocks `SWU-NDR-007`.

## SWU-NDR-007 — Refresh and drift-check installed surfaces

- Behavior: regenerate the supported installed Orchestrate surfaces and prove they match canonical source according to the generation manifest.
- Split analysis: this changes generated consumers only after generation itself passes; it does not add runtime behavior.
- Dependencies: `SWU-NDR-006` pass receipt.
- Source anchors: bootstrap generation manifest; installed `.agents/skills/orchestrate/` and `.claude/skills/orchestrate/` packages.
- Related context: `work-pack/shared/cross-task-gaps.md` cross-host parity limitation.
- Write scope: generated `.agents/skills/orchestrate/`, generated `.claude/skills/orchestrate/`, generation receipts; preserve local deviations unless the Task Session explicitly adjudicates them.
- Done criteria: supported generated surfaces contain the execute mode; drift check passes; host packages that lack native proof are marked unsupported/blocking rather than equivalent.
- Acceptance evidence: before/after generated manifests, drift check, host capability matrix.
- Validation: isolated regeneration plus repo-local drift validation; no live dispatch required.
- Handoff: pass satisfies the generation dependency for `TASK-NDR-005`.
