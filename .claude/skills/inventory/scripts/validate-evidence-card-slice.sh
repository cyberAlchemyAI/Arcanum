#!/usr/bin/env bash
set -u

slice_dir="${1:-}"
failures=0

fail() {
  failures=$((failures + 1))
  printf 'FAIL: %s\n' "$1" >&2
}

pass() {
  printf 'PASS: %s\n' "$1"
}

require_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    fail "missing required file: $path"
    return 1
  fi
  return 0
}

run_jq_check() {
  local label="$1"
  local filter="$2"
  local file="$3"
  shift 3
  if jq -e "$filter" "$file" "$@" >/dev/null; then
    pass "$label"
  else
    fail "$label"
  fi
}

if [[ -z "$slice_dir" ]]; then
  printf 'Usage: %s <slice-dir>\n' "$0" >&2
  exit 2
fi

if ! command -v jq >/dev/null 2>&1; then
  fail "jq is required"
  exit 1
fi

cards_file="$slice_dir/cards.json"
index_file="$slice_dir/index.json"
retrieval_file="$slice_dir/retrieval.json"
evidence_sets_file="$slice_dir/evidence-sets.json"

require_file "$cards_file" || true

for file in "$slice_dir"/*.json; do
  if [[ -f "$file" ]]; then
    run_jq_check "json parses: $file" "." "$file"
  fi
done

if [[ -f "$cards_file" ]]; then
  run_jq_check "cards collection has cards array" '.cards | type == "array" and length > 0' "$cards_file"
  run_jq_check "cards have unique ids" '
    [.cards[].id] as $ids | ($ids | unique | length) == ($ids | length)
  ' "$cards_file"
  run_jq_check "cards have required fields" '
    .cards | all(.[]; (
      has("id") and has("schema_version") and has("profile") and has("card_type") and
      has("title") and has("summary") and has("source_refs") and has("authority_level") and
      has("tags") and has("selection_reason") and has("captured") and
      has("promotion_status") and has("promotion_owner") and has("updated_at")
    ))
  ' "$cards_file"
  run_jq_check "controlled vocabularies are valid" '
    def in_list($xs): . as $v | $xs | index($v) != null;
    .cards | all(.[]; (
      (.schema_version == "inventory.evidence-card.v0.2") and
      (.profile | in_list(["full","minimal"])) and
      (.card_type | in_list(["source-summary","concept","method","claim","question","context","relation-candidate","contradiction-candidate","operational-lesson"])) and
      (.authority_level | in_list(["raw-source","session-evidence","discovery-baseline","inventory-knowledge","ontology-candidate","downstream-governed-ref"])) and
      (.promotion_status | in_list(["captured","candidate","proposed","promoted","rejected","superseded","blocked"])) and
      (.promotion_owner | in_list(["none","inventory","ontology-vault","definitions-governance","context-builder","invoke","repository-harness","other"]))
    ))
  ' "$cards_file"
  run_jq_check "source refs are non-empty" '
    .cards | all(.[]; (.source_refs | type == "array" and length > 0))
  ' "$cards_file"
  run_jq_check "selector shape is valid" '
    def valid_selector:
      (.path | type == "string" and length > 0) and
      (.selector | type == "string" and length > 0) and
      (.selector_type | IN("file","heading","line-span","anchor","query","fragment")) and
      ((.selector_type != "line-span") or ((.start_line | type == "number") and (.end_line | type == "number") and (.start_line <= .end_line)));
    .cards | all(.[]; all(.source_refs[]; valid_selector))
  ' "$cards_file"
  run_jq_check "full cards include handoff targets and trace" '
    .cards | all(.[]; (.profile != "full") or ((.handoff_targets | type == "array") and (.trace | type == "array" and length > 0)))
  ' "$cards_file"
  run_jq_check "terminal promotion statuses have owners" '
    .cards | all(.[]; ((.promotion_status | IN("promoted","rejected","superseded","blocked")) | not) or (.promotion_owner != "none"))
  ' "$cards_file"
  run_jq_check "relation candidates include non-authority notice and evidence" '
    .cards | all(.[]; (.card_type != "relation-candidate") or (
      (.claim_shape.non_authority_notice | type == "string" and length > 0) and
      (.claim_shape.evidence_refs | type == "array" and length > 0) and
      (.claim_shape.target_resolution | IN("resolved","unresolved","proposed"))
    ))
  ' "$cards_file"
fi

if [[ -f "$index_file" && -f "$cards_file" ]]; then
  run_jq_check "index references only slice card ids" '
    . as $index |
    input as $cards |
    ($cards.cards | map(.id)) as $ids |
    ([($index.cards_by_id | keys[])] | all(. as $id | $ids | index($id) != null))
  ' "$index_file" "$cards_file"
fi

if [[ -f "$retrieval_file" && -f "$cards_file" ]]; then
  run_jq_check "retrieval has selected cards and excluded matches" '
    (.selected_cards | type == "array" and length > 0) and
    (.excluded_matches | type == "array") and
    (.trace_notes | type == "array")
  ' "$retrieval_file"
  run_jq_check "retrieval references only slice card ids" '
    . as $retrieval |
    input as $cards |
    ($cards.cards | map(.id)) as $ids |
    ([($retrieval.selected_cards[].id), ($retrieval.excluded_matches[].id)] | all(. as $id | $ids | index($id) != null))
  ' "$retrieval_file" "$cards_file"
fi

if [[ -f "$evidence_sets_file" && -f "$cards_file" ]]; then
  run_jq_check "evidence sets collection has sets array" '
    .schema_version == "inventory.evidence-set.collection.v0.1" and
    (.evidence_sets | type == "array" and length > 0)
  ' "$evidence_sets_file"
  run_jq_check "evidence sets reference only slice card ids" '
    . as $sets |
    input as $cards |
    ($cards.cards | map(.id)) as $ids |
    ([($sets.evidence_sets[].card_refs[].id), ($sets.evidence_sets[].excluded_card_refs[].id)] | all(. as $id | $ids | index($id) != null))
  ' "$evidence_sets_file" "$cards_file"
fi

if [[ "$failures" -eq 0 ]]; then
  printf 'RESULT: pass\n'
  exit 0
fi

printf 'RESULT: fail (%s failures)\n' "$failures" >&2
exit 1
