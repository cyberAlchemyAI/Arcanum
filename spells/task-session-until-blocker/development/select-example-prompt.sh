#!/usr/bin/env bash
set -euo pipefail
development_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
spell_dir="$(cd "$development_dir/.." && pwd)"
arcanum_dir="$(cd "$development_dir/../../.." && pwd)"
"$arcanum_dir/arcana/experiment-harness/scripts/select-prompt.sh" "$spell_dir" "$@"
