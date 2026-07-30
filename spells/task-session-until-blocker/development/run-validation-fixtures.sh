#!/usr/bin/env bash
set -euo pipefail
development_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
spell_dir="$(cd "$development_dir/.." && pwd)"
arcanum_dir="$(cd "$development_dir/../../.." && pwd)"

python3 "$development_dir/validate-chain-fixtures.py"
python3 "$development_dir/validate-chain-v2.py"
"$arcanum_dir/arcana/experiment-harness/scripts/validate-harness.sh" "$spell_dir"
