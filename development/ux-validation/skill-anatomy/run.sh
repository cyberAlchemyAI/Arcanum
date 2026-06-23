#!/usr/bin/env bash
# Serve arcanum/docs, run the UX validator against desktop + mobile, write evidence bundle.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS="$(cd "$HERE/../../../docs" && pwd)"
PORT="${PORT:-8754}"
RUN="${RUN:-$(date +%Y%m%dT%H%M%SZ)}"
OUT="$(cd "$HERE/../../../" && pwd)/output/playwright/ux-validator/$RUN"
mkdir -p "$OUT"

python3 -m http.server "$PORT" --directory "$DOCS" >/tmp/ux-docsrv.log 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null || true' EXIT
sleep 1

BASE_URL="http://localhost:$PORT" OUT="$OUT" node "$HERE/ux-validate.mjs"
echo "Evidence: $OUT"
