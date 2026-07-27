# TASK-DRE-04: Generated Runtime Profiles

## SWU-DRE-007

- Primary behavior: regenerate Codex and Claude Distill profiles from the
  accepted canonical source.
- Split analysis: all generated profiles are one canonical projection decision;
  editing or accepting them independently creates drift.
- Dependencies: DRE-006.
- Write scope:
  - `.agents/skills/distill/`
  - `.claude/skills/distill/`
  - generated-parity fixture only when projection coverage must be extended
- Done: isolated bootstrap includes the new scripts/contracts and exact
  comparisons pass.
- Validation: bootstrap `--sigils distill --profiles repo-codex,claude`,
  executable-bit check, generated parity, scoped diff check.
- Execution owner: local fallback through bootstrap owner.
- Handoff: only a passing result may admit TASK-DRE-VERIFY.
