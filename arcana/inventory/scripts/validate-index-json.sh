#!/usr/bin/env bash
set -u

index_file="${1:-.arcanum/inventory/index.json}"
failures=0

fail() {
  failures=$((failures + 1))
  printf 'FAIL: %s\n' "$1" >&2
}

pass() {
  printf 'PASS: %s\n' "$1"
}

run_jq_check() {
  local label="$1"
  local filter="$2"
  local file="$3"
  if jq -e "$filter" "$file" >/dev/null; then
    pass "$label"
  else
    fail "$label"
  fi
}

if [[ ! -f "$index_file" ]]; then
  printf 'Usage: %s [index-json]\n' "$0" >&2
  fail "missing machine index: $index_file"
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  fail "jq is required"
  exit 1
fi

run_jq_check "json parses: $index_file" "." "$index_file"

run_jq_check "machine index has required top-level fields" '
  .schema_version == "inventory.index.v0.1" and
  (.inventory_root | type == "string" and length > 0) and
  (.generated_at | type == "string" and length > 0) and
  (.human_index | type == "string" and length > 0) and
  (.entries | type == "array") and
  (.indexes | type == "object") and
  (.validation | type == "object")
' "$index_file"

run_jq_check "entries have required fields" '
  .entries | all(.[]; (
    (.id | type == "string" and length > 0) and
    (.path | type == "string" and length > 0) and
    (.kind | IN("page","entry","query","lint","raw-manifest","evidence-card-bundle","evidence-set-bundle")) and
    (.type | type == "string" and length > 0) and
    (.title | type == "string" and length > 0) and
    (.summary | type == "string") and
    (.tags | type == "array") and
    (.sources | type == "array") and
    (.updated | type == "string") and
    (.status | type == "string") and
    (.residue | type == "array")
  ))
' "$index_file"

run_jq_check "entry ids are unique" '
  [.entries[].id] as $ids | ($ids | unique | length) == ($ids | length)
' "$index_file"

run_jq_check "required derived indexes exist" '
  (.indexes.by_id | type == "object") and
  (.indexes.by_type | type == "object") and
  (.indexes.by_tag | type == "object") and
  (.indexes.by_source | type == "object") and
  (.indexes.by_status | type == "object")
' "$index_file"

run_jq_check "by_id references only entry ids" '
  [.entries[].id] as $ids |
  (.indexes.by_id | keys | all(. as $id | $ids | index($id) != null))
' "$index_file"

run_jq_check "projection declarations are secondary to index.json" '
  (.projections // []) | all(.[]; (
    (.path | type == "string" and length > 0) and
    (.format | type == "string" and length > 0) and
    (.source == "index.json") and
    (.purpose | type == "string" and length > 0) and
    (.freshness | type == "string" and length > 0)
  ))
' "$index_file"

run_jq_check "validation boundary is inventory read model only" '
  .validation.parseable == true and
  (.validation.source_coverage | IN("complete","partial","unknown")) and
  .validation.validation_boundary == "inventory-read-model-only"
' "$index_file"

if [[ "$failures" -eq 0 ]]; then
  printf 'RESULT: pass\n'
  exit 0
fi

printf 'RESULT: fail (%s failures)\n' "$failures" >&2
exit 1
