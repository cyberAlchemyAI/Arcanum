#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
package_dir="$(cd "$script_dir/.." && pwd)"
arcanum_root="$(cd "$script_dir/../../.." && pwd)"
"$arcanum_root/arcana/experiment-harness/scripts/loop-harness.sh" "$package_dir" "$@"
