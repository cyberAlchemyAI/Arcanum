#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${CODEX_BIN:-}" && -x "${CODEX_BIN:-}" ]]; then
	printf '%s\n' "$CODEX_BIN"
	exit 0
fi

if command -v codex >/dev/null 2>&1; then
	command -v codex
	exit 0
fi

for candidate in \
	"$HOME/.vscode-server/extensions/openai.chatgpt-"*/bin/linux-x86_64/codex \
	"$HOME/.vscode/extensions/openai.chatgpt-"*/bin/linux-x86_64/codex \
	"$HOME/.local/bin/codex" \
	"$HOME/bin/codex"; do
	if [[ -x "$candidate" ]]; then
		printf '%s\n' "$candidate"
		exit 0
	fi
done

exit 1
