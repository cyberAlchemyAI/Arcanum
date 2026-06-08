#!/usr/bin/env bash
set -u

fixture_dir="${1:-arcana/inventory/development/pilot/evidence-card}"

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

if ! command -v jq >/dev/null 2>&1; then
  fail "jq is required"
  exit 1
fi

cards_file="$fixture_dir/pilot-cards.json"
craft_cards_file="$fixture_dir/craft-stressor-cards.json"
index_file="$fixture_dir/pilot-index.json"
retrieval_file="$fixture_dir/pilot-retrieval.json"
evidence_sets_file="$fixture_dir/evidence-sets.json"
ontology_handoff_file="$fixture_dir/pilot-handoff-ontology.json"
definitions_handoff_file="$fixture_dir/pilot-handoff-definitions.json"
invalid_examples_file="$fixture_dir/invalid-examples.json"

for file in "$cards_file" "$index_file" "$retrieval_file" "$evidence_sets_file" "$ontology_handoff_file" "$definitions_handoff_file"; do
  require_file "$file" || true
done

for file in "$fixture_dir"/*.json; do
  if [[ -f "$file" ]]; then
    run_jq_check "json parses: $file" "." "$file"
  fi
done

if [[ -f "$cards_file" ]]; then
  run_jq_check "cards fixture has cards array" '.cards | type == "array" and length > 0' "$cards_file"
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
      (.profile | in_list(["full","minimal"])) and
      (.card_type | in_list(["source-summary","concept","method","claim","question","context","relation-candidate","contradiction-candidate","operational-lesson"])) and
      (.authority_level | in_list(["raw-source","session-evidence","discovery-baseline","inventory-knowledge","ontology-candidate","downstream-governed-ref"])) and
      (.promotion_status | in_list(["captured","candidate","proposed","promoted","rejected","superseded","blocked"])) and
      (.promotion_owner | in_list(["none","inventory","ontology-vault","definitions-governance","context-builder","invoke","repository-harness","other"]))
    ))
  ' "$cards_file"
  run_jq_check "source_refs are non-empty" '
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
  run_jq_check "minimal cards remain traceable and reasoned" '
    .cards | all(.[]; (.profile != "minimal") or ((.source_refs | length > 0) and (.selection_reason | length > 0) and has("captured") and has("promotion_status") and has("promotion_owner")))
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
  run_jq_check "index references only pilot card ids" '
    . as $index |
    input as $cards |
    ($cards.cards | map(.id)) as $ids |
    ([($index.cards_by_id | keys[])] | all(. as $id | $ids | index($id) != null))
  ' "$index_file" "$cards_file"
fi

if [[ -f "$retrieval_file" && -f "$cards_file" ]]; then
  run_jq_check "retrieval has selected cards and excluded matches" '
    (.selected_cards | type == "array" and length > 0) and
    (.excluded_matches | type == "array" and length > 0) and
    (.trace_notes | type == "array")
  ' "$retrieval_file"
  run_jq_check "retrieval references only pilot card ids" '
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
  run_jq_check "evidence sets have required fields" '
    .evidence_sets | all(.[]; (
      has("schema_version") and has("set_id") and has("purpose") and
      has("card_refs") and has("excluded_card_refs") and has("index_terms") and
      has("handoff_target") and has("synthesis_note") and has("residue") and
      has("status") and has("promotion_owner") and has("updated_at")
    ))
  ' "$evidence_sets_file"
  run_jq_check "evidence set controlled vocabularies are valid" '
    def in_list($xs): . as $v | $xs | index($v) != null;
    .evidence_sets | all(.[]; (
      (.schema_version == "inventory.evidence-set.v0.1") and
      (.status | in_list(["candidate","promote-pending","rejected","superseded"])) and
      (.promotion_owner | in_list(["inventory","ontology-vault","definitions-governance","context-builder","invoke","repository-harness","other"])) and
      (.handoff_target | in_list(["context-builder","ontology-vault","definitions-governance","invoke","repository-harness","other"]))
    ))
  ' "$evidence_sets_file"
  run_jq_check "evidence set ids are unique" '
    [.evidence_sets[].set_id] as $ids | ($ids | unique | length) == ($ids | length)
  ' "$evidence_sets_file"
  run_jq_check "evidence sets include reasons and index terms" '
    .evidence_sets | all(.[]; (
      (.purpose | type == "string" and length > 0) and
      (.card_refs | type == "array" and length > 0) and
      all(.card_refs[]; (.id | type == "string" and length > 0) and (.inclusion_reason | type == "string" and length > 0)) and
      (.excluded_card_refs | type == "array") and
      all(.excluded_card_refs[]; (.id | type == "string" and length > 0) and (.reason | type == "string" and length > 0)) and
      (.index_terms | type == "array" and length > 0) and
      all(.index_terms[]; type == "string" and length > 0) and
      (.synthesis_note | type == "string" and length > 0 and length < 280) and
      (.residue | type == "string" and length > 0 and length < 280)
    ))
  ' "$evidence_sets_file"
fi

if [[ -f "$evidence_sets_file" && -f "$cards_file" && -f "$craft_cards_file" ]]; then
  run_jq_check "evidence sets reference only known card ids" '
    . as $sets |
    input as $pilot |
    input as $craft |
    (($pilot.cards + $craft.cards) | map(.id)) as $ids |
    ([($sets.evidence_sets[].card_refs[].id), ($sets.evidence_sets[].excluded_card_refs[].id)] | all(. as $id | $ids | index($id) != null))
  ' "$evidence_sets_file" "$cards_file" "$craft_cards_file"
fi

for file in "$ontology_handoff_file" "$definitions_handoff_file"; do
  if [[ -f "$file" ]]; then
    run_jq_check "handoff has source refs and non-authority notice: $file" '
      (.source_refs | type == "array" and length > 0) and
      (.non_authority_notice | type == "string" and test("not|does not|candidate|proposes"; "i"))
    ' "$file"
  fi
done

if [[ -f "$invalid_examples_file" ]]; then
  run_jq_check "invalid examples cover required classes" '
    (.examples | type == "array") and
    (["selector","enum","owner-status","relation-notice","minimal-profile"] - [.examples[].class] | length == 0)
  ' "$invalid_examples_file"
fi

if [[ "$failures" -eq 0 ]]; then
  printf 'RESULT: pass\n'
  exit 0
fi

printf 'RESULT: fail (%s failures)\n' "$failures" >&2
exit 1
