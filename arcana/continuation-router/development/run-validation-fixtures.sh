#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
package_dir="$(cd "$script_dir/.." && pwd)"
arcanum_root="$(cd "$script_dir/../../.." && pwd)"
export EXPERIMENT_REPO_ROOT="$arcanum_root"
"$arcanum_root/arcana/experiment-harness/scripts/validate-harness.sh" "$package_dir"
python3 "$script_dir/validate-route-fixtures.py"
python3 "$script_dir/validate-work-pack-route-fixtures.py"
