#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
canonical_dir="$(cd "$script_dir/.." && pwd)"
repository_root="$(git -C "$canonical_dir" rev-parse --show-superproject-working-tree)"
if [[ -z "$repository_root" ]]; then
  repository_root="$(git -C "$canonical_dir" rev-parse --show-toplevel)"
fi

validation_status=0
validation_child_count=0

run_validation_child() {
  local child_status=0
  validation_child_count=$((validation_child_count + 1))
  "$@" || child_status=$?
  if (( child_status != 0 )); then
    printf 'TASK_SESSION_VALIDATION_CHILD_FAILED child=%d exit=%d command=%q\n' \
      "$validation_child_count" "$child_status" "$1" >&2
    if (( validation_status == 0 )); then
      validation_status="$child_status"
    fi
  fi
}

if [[ "${1:-}" == "--exit-propagation-fixture" ]]; then
  shift
  for requested_status in "$@"; do
    if [[ ! "$requested_status" =~ ^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$ ]]; then
      printf 'invalid fixture child exit: %s\n' "$requested_status" >&2
      exit 64
    fi
    run_validation_child bash -c 'exit "$1"' _ "$requested_status"
  done
  printf 'TASK_SESSION_VALIDATION_FIXTURE children=%d aggregate_exit=%d\n' \
    "$validation_child_count" "$validation_status"
  exit "$validation_status"
fi

run_validation_child python3 \
  "$script_dir/validate-decision-validation-policy.py" \
  "$repository_root" \
  "$canonical_dir"

run_validation_child python3 \
  "$script_dir/validate-nearest-swu-resolver.py" \
  "$canonical_dir"

run_validation_child python3 "$script_dir/test_fast_execution_entry_guard.py"

run_validation_child python3 "$script_dir/pre-execution-prerequisite-fast-path/validate-fixtures.py"
run_validation_child python3 "$script_dir/pre-execution-prerequisite-fast-path/test_classifier.py"
run_validation_child python3 "$script_dir/pre-execution-prerequisite-fast-path/test_owner_resume.py"

run_validation_child python3 \
  "$script_dir/validate-mutation-admission.py"

run_validation_child python3 "$script_dir/test_plan_once_admission.py"
run_validation_child python3 "$script_dir/test_plan_once_governance.py"
run_validation_child python3 "$script_dir/test_execution_entry_projection.py"
run_validation_child python3 "$script_dir/test_validation_wrapper_exit_propagation.py"

exit "$validation_status"
