#!/usr/bin/env bash
set -u

root="${1:-arcana/inventory/development/whole-arcanum}"
repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
failures=0

fail() {
  failures=$((failures + 1))
  printf 'FAIL: %s\n' "$1" >&2
}

pass() {
  printf 'PASS: %s\n' "$1"
}

run() {
  local label="$1"
  shift
  if "$@"; then
    pass "$label"
  else
    fail "$label"
  fi
}

require_file() {
  local path="$1"
  if [[ -f "$path" ]]; then
    pass "exists: $path"
  else
    fail "missing required file: $path"
  fi
}

if ! command -v jq >/dev/null 2>&1; then
  fail "jq is required"
  printf 'RESULT: fail (%s failures)\n' "$failures" >&2
  exit 1
fi

cd "$repo_root" || exit 1

slices=(inventory governance lifecycle arcana composition runtime)

for slice in "${slices[@]}"; do
  slice_dir="$root/cards/$slice"
  require_file "$slice_dir/cards.json"
  require_file "$slice_dir/index.json"
  require_file "$slice_dir/retrieval.json"
  run "slice validates: $slice" bash arcana/inventory/scripts/validate-evidence-card-slice.sh "$slice_dir"
done

require_file "$root/evidence-sets/evidence-sets.json"
require_file "$root/source-manifest.json"
require_file "$root/SOURCE-POLICY.md"

run "all source refs exist and line spans fit" bash -c '
  root="$1"
  jq -r ".cards[].source_refs[] | [.path, (.start_line // 0), (.end_line // 0), .selector_type] | @tsv" "$root"/cards/*/cards.json |
  while IFS=$'\''\t'\'' read -r path start end selector_type; do
    if [[ ! -f "$path" ]]; then
      printf "missing source ref: %s\n" "$path" >&2
      exit 1
    fi
    if [[ "$selector_type" == "line-span" ]]; then
      lines=$(wc -l < "$path")
      if [[ "$start" -lt 1 || "$end" -gt "$lines" || "$start" -gt "$end" ]]; then
        printf "bad line span: %s %s-%s of %s\n" "$path" "$start" "$end" "$lines" >&2
        exit 1
      fi
    fi
  done
' _ "$root"

run "evidence sets reference known cards" bash -c '
  root="$1"
  cards_tmp=$(mktemp)
  refs_tmp=$(mktemp)
  trap "rm -f \"$cards_tmp\" \"$refs_tmp\"" EXIT
  jq -r ".cards[].id" "$root"/cards/*/cards.json | sort -u > "$cards_tmp"
  jq -r ".evidence_sets[] | (.card_refs[].id), (.excluded_card_refs[].id)" "$root/evidence-sets/evidence-sets.json" | sort -u > "$refs_tmp"
  while IFS= read -r id; do
    if ! grep -Fxq "$id" "$cards_tmp"; then
      printf "unknown evidence-set card ref: %s\n" "$id" >&2
      exit 1
    fi
  done < "$refs_tmp"
' _ "$root"

run "pilot evidence-card fixtures validate" bash arcana/inventory/scripts/validate-evidence-card-fixtures.sh arcana/inventory/development/pilot/evidence-card
run "artifact constitution self-test" tools/validate-artifact-constitution.sh --self-test
run "artifact constitution validates current tree" bash tools/validate-artifact-constitution.sh

if [[ "$failures" -eq 0 ]]; then
  printf 'RESULT: pass\n'
  exit 0
fi

printf 'RESULT: fail (%s failures)\n' "$failures" >&2
exit 1

