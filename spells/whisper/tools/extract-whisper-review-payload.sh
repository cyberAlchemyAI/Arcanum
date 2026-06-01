#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  extract-whisper-review-payload.sh <url> <output-json>

Opens a Whisper review HTML page with playwright-cli and extracts
window.WhisperReview.getAgentPayload() into a JSON file.

Serve local files over localhost when possible:
  python3 -m http.server 8765
USAGE
}

if [[ "$#" -ne 2 ]]; then
	usage >&2
	exit 2
fi

url="$1"
output="$2"
codex_home="${CODEX_HOME:-$HOME/.codex}"
pwcli="${PWCLI:-$codex_home/skills/playwright/scripts/playwright_cli.sh}"

if [[ ! -x "$pwcli" ]]; then
	printf 'ERROR: playwright wrapper not found: %s\n' "$pwcli" >&2
	exit 1
fi

"$pwcli" open "$url" >/dev/null
raw_payload="$(mktemp)"
"$pwcli" eval '() => JSON.stringify(window.WhisperReview.getAgentPayload(), null, 2)' > "$raw_payload"
"$pwcli" close >/dev/null || true

python3 - "$raw_payload" "$output" <<'PY'
import json
import sys
from pathlib import Path

raw = Path(sys.argv[1]).read_text(encoding="utf-8")
output = Path(sys.argv[2])

if "### Result" in raw:
    result = raw.split("### Result", 1)[1].split("### Ran Playwright code", 1)[0].strip()
else:
    result = raw.strip()

payload_text = json.loads(result) if result.startswith('"') else result
payload = json.loads(payload_text)
output.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
PY
rm -f "$raw_payload"
jq empty "$output"
printf 'WROTE %s\n' "$output"
