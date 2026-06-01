# Arcanum Install Tutorial For Codex And Claude Code

This installs Arcanum into your own repository so Codex and Claude Code can discover Arcanum as repo-local skills.

## Prerequisites

- You have a Git repository where you want to use Arcanum.
- You can run shell commands from that repository root.
- `curl` or `wget` is installed.
- For Codex use, open Codex from the target repository after installing.
- For Claude Code use, open Claude Code from the target repository after installing.

## Recommended Install

From the root of your target repository, run this if you want Codex, Claude Code, GitHub/Copilot, local helper tools, and observability:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/Arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --profiles repo-codex,claude,repo-local,github-copilot,observability --sigils all --spells all
```

This installs:

- `.agents/skills/` for Codex skill discovery.
- `.claude/skills/` for Claude Code skill discovery.
- `.claude/agents/arcanum-stage-worker.md` for bounded Claude sidecar work.
- `CLAUDE.md` with Claude Code project instructions.
- `tools/arcanum` for deterministic local resolve/validate helpers.
- `.github/` Copilot instructions and skills.
- `.arcanum/observability/` for local run evidence.

## Codex-Only Install

If you only want Codex skills and no repo tooling or GitHub/Copilot files:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/Arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --profile repo-codex --sigils all --spells none
```

## Claude-Code-Only Install

If you only want Claude Code skills plus the local helper tool:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/Arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --profiles claude,repo-local --sigils all --spells all
```

This creates:

```text
.claude/skills/refine/SKILL.md
.claude/skills/task-session/SKILL.md
.claude/agents/arcanum-stage-worker.md
CLAUDE.md
tools/arcanum
```

## Verify

After a Codex or combined install, run:

```bash
./tools/arcanum --resolve refine
```

Expected result:

```text
COMMAND=refine
COMMAND_FILE=.agents/skills/refine/SKILL.md
```

You can also check that the repo has:

```text
.agents/skills/refine/SKILL.md
.agents/skills/task-session/SKILL.md
tools/arcanum
```

After a Claude Code or combined install, check:

```bash
test -f .claude/skills/refine/SKILL.md
test -f .claude/skills/task-session/SKILL.md
test -f .claude/agents/arcanum-stage-worker.md
test -f CLAUDE.md
```

## Use In Codex

Open Codex in the installed repository and invoke a skill by name, for example:

```text
[$refine](.agents/skills/refine/SKILL.md) help me shape this feature idea
```

Or:

```text
[$task-session](.agents/skills/task-session/SKILL.md) run the next ready task
```

Codex should show short skill names such as `refine`, `invoke`, `context-builder`, and `task-session`. It should not show duplicate `arcanum-refine` style packages unless you intentionally install compatibility packages.

## Use In Claude Code

Open Claude Code in the installed repository. Claude Code should read `CLAUDE.md` and the `.claude/skills/` packages.

Ask for Arcanum work by naming the capability, for example:

```text
Use the refine skill to shape this feature idea.
```

Or:

```text
Use task-session to run the next ready task from the work-pack.
```

Claude Code should use short skill names such as `refine`, `invoke`, `context-builder`, and `task-session`. The generated `.claude/agents/arcanum-stage-worker.md` is available for bounded sidecar stages when delegation is helpful.

## Optional Compatibility Flags

Legacy slash-command files are not installed by default. If you intentionally need old `.codex/commands` compatibility:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/Arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --profile repo-local --legacy-codex-commands --sigils all --spells all
```

If you need old `arcanum-*` skill package names:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/Arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --profile repo-codex --prefixed-skill-packages --sigils all --spells none
```

## Updating

Re-run the recommended install command with `--force` if you want to refresh generated surfaces:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/Arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --profiles repo-codex,claude,repo-local,github-copilot,observability --sigils all --spells all --force
```

## Troubleshooting

- If `./tools/arcanum --resolve refine` fails, confirm you ran the command from the target repository root.
- If Codex does not show skills, restart Codex from inside the target repository.
- If Claude Code does not use the skills, restart Claude Code from inside the target repository and confirm `CLAUDE.md` plus `.claude/skills/` exist.
- If duplicate `arcanum-*` skill suggestions appear, reinstall without `--prefixed-skill-packages`.
- If you need a smaller install, choose specific sigils:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/Arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --profiles repo-codex,claude,repo-local --sigils refine,task-session,context-builder --spells none
```
