#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
canonical_dir="$(cd "$script_dir/.." && pwd)"
repository_root="$(git -C "$canonical_dir" rev-parse --show-superproject-working-tree)"
if [[ -z "$repository_root" ]]; then
  repository_root="$(git -C "$canonical_dir" rev-parse --show-toplevel)"
fi

python3 \
  "$script_dir/validate-decision-validation-policy.py" \
  "$repository_root" \
  "$canonical_dir"

python3 \
  "$script_dir/validate-nearest-swu-resolver.py" \
  "$canonical_dir"

python3 \
  "$script_dir/validate-mutation-admission.py"
