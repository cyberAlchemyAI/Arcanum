# Arcanum Install Tutorial For Codex

This installs Arcanum into your own repository so Codex can discover Arcanum as repo-local skills.

## Prerequisites

- You have a Git repository where you want to use Arcanum.
- You can run shell commands from that repository root.
- `curl` or `wget` is installed.
- For Codex use, open Codex from the target repository after installing.

## Recommended Install

From the root of your target repository, run:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/Arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --profiles repo-codex,repo-local,github-copilot,observability --sigils all --spells all
```

This installs:

- `.agents/skills/` for Codex skill discovery.
- `tools/arcanum` for deterministic local resolve/validate helpers.
- `.github/` Copilot instructions and skills.
- `.arcanum/observability/` for local run evidence.

## Codex-Only Install

If you only want Codex skills and no repo tooling or GitHub/Copilot files:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/Arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --profile repo-codex --sigils all --spells none
```

## Verify

After install, run:

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
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/Arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --profiles repo-codex,repo-local,github-copilot,observability --sigils all --spells all --force
```

## Troubleshooting

- If `./tools/arcanum --resolve refine` fails, confirm you ran the command from the target repository root.
- If Codex does not show skills, restart Codex from inside the target repository.
- If duplicate `arcanum-*` skill suggestions appear, reinstall without `--prefixed-skill-packages`.
- If you need a smaller install, choose specific sigils:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/Arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --profiles repo-codex,repo-local --sigils refine,task-session,context-builder --spells none
```

