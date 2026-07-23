#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATES_DIR="$SCRIPT_DIR/fixtures/runtime-states"

fail() {
  printf 'SCENARIO_VALIDATION=block\n'
  printf 'REASON=%s\n' "$1"
  exit 1
}

match_index="$STATES_DIR/relevant-match/.arcanum/inventory/index.json"
no_match_index="$STATES_DIR/no-match/.arcanum/inventory/index.json"
fallback_root="$STATES_DIR/index-fallback/.arcanum/inventory"
absent_root="$STATES_DIR/no-inventory/.arcanum/inventory"
insufficient="$STATES_DIR/insufficient-signal/invocation.json"
rejected="$STATES_DIR/rejected-approval/invocation.json"

jq -e . "$match_index" >/dev/null || fail "relevant-match index is not parseable"
jq -e '.entries | map(select((.id + " " + .title + " " + .summary) | test("example-sigil|output drift"; "i"))) | length == 1' "$match_index" >/dev/null || fail "relevant-match lookup did not select exactly one entry"

jq -e . "$no_match_index" >/dev/null || fail "no-match index is not parseable"
jq -e '.entries | map(select((.id + " " + .title + " " + .summary) | test("example-sigil|output drift"; "i"))) | length == 0' "$no_match_index" >/dev/null || fail "no-match lookup returned an asserted match"

test ! -e "$fallback_root/index.json" || fail "fallback fixture unexpectedly contains index.json"
test -f "$fallback_root/index.md" || fail "fallback fixture lacks index.md"

test ! -d "$absent_root" || fail "no-inventory fixture unexpectedly contains an Inventory package"

jq -e '.manual_trigger == false and .signal_count == 0 and .expected_result == "insufficient_signal" and .mutation_allowed == false' "$insufficient" >/dev/null || fail "insufficient-signal fixture does not stop before mutation"
jq -e '.approval == "rejected" and .expected_result == "block-before-mutation" and .mutation_allowed == false' "$rejected" >/dev/null || fail "rejected-approval fixture does not block mutation"

printf 'SCENARIO_VALIDATION=pass\n'
printf 'SCENARIOS=6\n'
printf 'RELEVANT_MATCH=pass\n'
printf 'NO_MATCH=pass\n'
printf 'INDEX_FALLBACK=pass\n'
printf 'INVENTORY_UNAVAILABLE=pass\n'
printf 'INSUFFICIENT_SIGNAL=pass\n'
printf 'REJECTED_APPROVAL=pass\n'
