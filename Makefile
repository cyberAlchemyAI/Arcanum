# Arcanum developer convenience targets.

TARGET ?= .

.PHONY: claude-skills validate-claude-skills

# Generate the Claude Code skill surface for TARGET (default: this repo) and
# validate it. This is the single documented "dogfood / regenerate" command.
claude-skills:
	bash tools/bootstrap_arcanum.sh --target "$(TARGET)" --profile claude --sigils all --spells all --force

# Validate an already-generated Claude skill surface without regenerating.
validate-claude-skills:
	bash tools/validate-claude-skills.sh "$(TARGET)/.claude/skills"
