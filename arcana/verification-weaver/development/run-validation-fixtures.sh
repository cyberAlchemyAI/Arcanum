#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
POSITIVE_DIR="$SCRIPT_DIR/fixtures/positive"
NEGATIVE_DIR="$SCRIPT_DIR/negative-controls"
LOCAL_RUN_DIR="$SCRIPT_DIR/runs"
VALIDATION_MD="$SCRIPT_DIR/VALIDATION.md"
RESIDUE_LEDGER="$SCRIPT_DIR/residue-ledger.yml"

failures=()
validated=()

fail() {
  failures+=("$1")
}

require_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    fail "missing required file: ${path#$PACKAGE_DIR/}"
  fi
}

require_line() {
  local file="$1"
  local pattern="$2"
  local message="$3"
  if ! grep -Eq "$pattern" "$file"; then
    fail "${file#$PACKAGE_DIR/}: $message"
  fi
}

field_value() {
  local file="$1"
  local field="$2"
  sed -n "s/^[[:space:]]*${field}: //p" "$file" | head -n 1
}

top_field_value() {
  local file="$1"
  local field="$2"
  sed -n "s/^${field}: //p" "$file" | head -n 1
}

join_pattern() {
  printf '%s' "$@"
}

check_no_denylist_literals() {
  local pattern
  local matches
  local patterns=(
    "$(join_pattern 'implementation/' 'domainspec')"
    "$(join_pattern 'validation/' 'poker-team')"
    "$(join_pattern '/' 'home/' 'vrondelli')"
    "$(join_pattern '.arcanum/' 'observability')"
    "$(join_pattern 'example-' 'outputs')"
    "$(join_pattern 'example-' 'runs')"
    "$(join_pattern 'development/' 'runs')"
  )

  for pattern in "${patterns[@]}"; do
    matches="$(grep -RInF --exclude-dir=.git -- "$pattern" "$PACKAGE_DIR" || true)"
    if [[ -n "$matches" ]]; then
      fail "public-boundary denylist matched pattern '${pattern}'"
    fi
  done
}

check_common_receipt() {
  local file="$1"
  local status
  local promotion
  local target_kind
  local oracle_type
  local ref
  local refs=()

  require_line "$file" '^schema_version: "0\.1\.0"$' "schema_version must be 0.1.0"
  require_line "$file" '^receipt_type: VERIFICATION-WEAVE$' "receipt_type must be VERIFICATION-WEAVE"
  require_line "$file" '^fixture_id: .+$' "fixture_id is required"
  require_line "$file" '^fixture_role: (positive|negative-control)$' "fixture_role must be positive or negative-control"
  require_line "$file" '^target:$' "target section is required"
  require_line "$file" '^classification:$' "classification section is required"
  require_line "$file" '^lanes:$' "lanes section is required"
  require_line "$file" '^public_safety:$' "public_safety section is required"

  target_kind="$(field_value "$file" target_kind)"
  case "$target_kind" in
    spec_derivation|frontend_ux|execution_repeatability|architecture_gap|research_evidence|mixed|unsupported) ;;
    *) fail "${file#$PACKAGE_DIR/}: invalid target_kind '${target_kind}'" ;;
  esac

  oracle_type="$(field_value "$file" oracle_type)"
  case "$oracle_type" in
    deterministic_derivation|fixture_runner|proof_checker|browser_evidence|human_review|research_run_data|explicit_gap|null) ;;
    *) fail "${file#$PACKAGE_DIR/}: invalid oracle_type '${oracle_type}'" ;;
  esac

  status="$(top_field_value "$file" status)"
  case "$status" in
    pass|flag|block) ;;
    *) fail "${file#$PACKAGE_DIR/}: invalid top-level status '${status}'" ;;
  esac

  promotion="$(top_field_value "$file" promotion_action)"
  case "$promotion" in
    none|candidate-request) ;;
    *) fail "${file#$PACKAGE_DIR/}: invalid promotion_action '${promotion}'" ;;
  esac

  mapfile -t refs < <(sed -n 's/^[[:space:]]*- owner_capability_ref: //p' "$file")
  if [[ "${#refs[@]}" -eq 0 ]]; then
    fail "${file#$PACKAGE_DIR/}: at least one owner_capability_ref is required"
  fi

  for ref in "${refs[@]}"; do
    case "$ref" in
      arcanum/arcana/test-derivation|\
      arcanum/arcana/ux-evidence-validator|\
      arcanum/arcana/experiment-harness|\
      arcanum/arcana/architecture-pattern-inventory|\
      arcanum/arcana/research-evidence-harness|\
      arcanum/arcana/verification-weaver) ;;
      *) fail "${file#$PACKAGE_DIR/}: invalid owner_capability_ref '${ref}'" ;;
    esac
  done
}

check_positive_receipt() {
  local file="$1"
  local status
  local private_scan
  local generated_scan

  check_common_receipt "$file"

  status="$(top_field_value "$file" status)"
  if [[ "$status" == "block" ]]; then
    fail "${file#$PACKAGE_DIR/}: positive fixture cannot block"
  fi

  private_scan="$(field_value "$file" private_path_scan)"
  generated_scan="$(field_value "$file" generated_output_scan)"
  if [[ "$private_scan" != "pass" || "$generated_scan" != "pass" ]]; then
    fail "${file#$PACKAGE_DIR/}: positive fixture must pass public_safety scans"
  fi

  require_line "$file" '^(evidence|gaps):' "positive fixture must declare evidence or gaps"
  validated+=("positive:${file#$PACKAGE_DIR/}")
}

check_negative_receipt() {
  local file="$1"
  local control_id
  local status

  check_common_receipt "$file"

  control_id="$(top_field_value "$file" control_id)"
  status="$(top_field_value "$file" status)"

  if [[ -z "$control_id" ]]; then
    fail "${file#$PACKAGE_DIR/}: control_id is required"
    return
  fi

  case "$control_id" in
    NC-MIX-001)
      [[ "$status" == "block" ]] || fail "${file#$PACKAGE_DIR/}: NC-MIX-001 must block"
      require_line "$file" 'target_kind: mixed' "NC-MIX-001 target_kind must be mixed"
      require_line "$file" 'required: true' "NC-MIX-001 must require decomposition"
      require_line "$file" 'reason: mixed_target_requires_split' "NC-MIX-001 must record split gap"
      ;;
    NC-UNSUPPORTED-001)
      [[ "$status" == "block" ]] || fail "${file#$PACKAGE_DIR/}: NC-UNSUPPORTED-001 must block"
      require_line "$file" 'target_kind: unsupported' "NC-UNSUPPORTED-001 target_kind must be unsupported"
      require_line "$file" 'unsupported_reason: no_recognized_verification_oracle' "NC-UNSUPPORTED-001 needs unsupported_reason"
      ;;
    NC-PRIVATE-001)
      [[ "$status" == "block" ]] || fail "${file#$PACKAGE_DIR/}: NC-PRIVATE-001 must block"
      require_line "$file" 'private_path_scan: block' "NC-PRIVATE-001 must block private scan"
      require_line "$file" 'reason: public_boundary_failure' "NC-PRIVATE-001 must record public boundary gap"
      ;;
    NC-GENERATED-001)
      [[ "$status" == "block" ]] || fail "${file#$PACKAGE_DIR/}: NC-GENERATED-001 must block"
      require_line "$file" 'generated_output_scan: block' "NC-GENERATED-001 must block generated scan"
      require_line "$file" 'reason: generated_artifact_authority' "NC-GENERATED-001 must record generated authority gap"
      ;;
    NC-NO-ORACLE-001)
      [[ "$status" == "block" ]] || fail "${file#$PACKAGE_DIR/}: NC-NO-ORACLE-001 must block"
      require_line "$file" 'oracle_type: null' "NC-NO-ORACLE-001 must have null oracle"
      require_line "$file" 'reason: missing_oracle' "NC-NO-ORACLE-001 must record missing oracle"
      ;;
    NC-UX-HUMAN-001)
      [[ "$status" == "flag" ]] || fail "${file#$PACKAGE_DIR/}: NC-UX-HUMAN-001 must flag"
      require_line "$file" 'target_kind: frontend_ux' "NC-UX-HUMAN-001 target_kind must be frontend_ux"
      require_line "$file" 'reason: human_comprehension_risk' "NC-UX-HUMAN-001 must preserve UX residue"
      ;;
    NC-UX-DENSE-001)
      [[ "$status" == "flag" ]] || fail "${file#$PACKAGE_DIR/}: NC-UX-DENSE-001 must flag"
      require_line "$file" 'reason: density_false_positive_note' "NC-UX-DENSE-001 must preserve density note"
      ;;
    NC-E2E-FLAKE-001)
      [[ "$status" == "block" ]] || fail "${file#$PACKAGE_DIR/}: NC-E2E-FLAKE-001 must block"
      require_line "$file" 'reason: flaky_evidence' "NC-E2E-FLAKE-001 must record flaky evidence"
      ;;
    NC-ADAPTER-001)
      [[ "$status" == "block" ]] || fail "${file#$PACKAGE_DIR/}: NC-ADAPTER-001 must block"
      require_line "$file" 'reason: adapter_failure' "NC-ADAPTER-001 must record adapter failure"
      ;;
    NC-RESEARCH-DRYRUN-001)
      [[ "$status" =~ ^(flag|block)$ ]] || fail "${file#$PACKAGE_DIR/}: NC-RESEARCH-DRYRUN-001 must flag or block"
      require_line "$file" 'reason: dry_run_only' "NC-RESEARCH-DRYRUN-001 must preserve dry-run residue"
      require_line "$file" '^attempted_parent_action: promote$' "NC-RESEARCH-DRYRUN-001 must record attempted promotion"
      require_line "$file" '^promotion_action: none$' "NC-RESEARCH-DRYRUN-001 must keep promotion_action none"
      ;;
    NC-ARCH-FOLDER-ONLY-001)
      [[ "$status" == "flag" ]] || fail "${file#$PACKAGE_DIR/}: NC-ARCH-FOLDER-ONLY-001 must flag"
      require_line "$file" 'reason: insufficient_source_evidence' "NC-ARCH-FOLDER-ONLY-001 must record source evidence gap"
      ;;
    NC-RECEIPT-PROMOTE-001)
      [[ "$status" == "block" ]] || fail "${file#$PACKAGE_DIR/}: NC-RECEIPT-PROMOTE-001 must block"
      require_line "$file" '^attempted_parent_action: promote$' "NC-RECEIPT-PROMOTE-001 must record attempted promotion"
      require_line "$file" '^promotion_action: none$' "NC-RECEIPT-PROMOTE-001 must keep promotion_action none"
      require_line "$file" 'reason: parent_promotion_blocked' "NC-RECEIPT-PROMOTE-001 must record parent promotion gap"
      ;;
    *)
      fail "${file#$PACKAGE_DIR/}: unknown negative control '${control_id}'"
      ;;
  esac

  validated+=("negative:${file#$PACKAGE_DIR/}")
}

write_reports() {
  local result="$1"
  local timestamp="$2"
  local report="$LOCAL_RUN_DIR/${timestamp}-validation.md"
  local failure
  local item

  mkdir -p "$LOCAL_RUN_DIR"

  {
    echo "# Verification Weaver Validation"
    echo
    echo "- Result: ${result}"
    echo "- Timestamp UTC: ${timestamp}"
    echo "- Positive fixtures: $(find "$POSITIVE_DIR" -type f -name '*.receipt.yml' | wc -l | tr -d ' ')"
    echo "- Negative controls: $(find "$NEGATIVE_DIR" -type f -name '*.receipt.yml' | wc -l | tr -d ' ')"
    echo "- Parent receipt: VERIFICATION-WEAVE"
    echo "- Promotion action allowed: none, candidate-request"
    echo
    echo "## Validated Items"
    for item in "${validated[@]}"; do
      echo "- ${item}"
    done
    echo
    echo "## Failures"
    if [[ "${#failures[@]}" -eq 0 ]]; then
      echo "- none"
    else
      for failure in "${failures[@]}"; do
        echo "- ${failure}"
      done
    fi
    echo
    echo "## Residue"
    echo "- Candidate package is not registered."
    echo "- Owner lanes remain authoritative for their own evidence."
    echo "- Follow-up route: sigil-development review, then experiment-harness calibration."
  } > "$VALIDATION_MD"

  cp "$VALIDATION_MD" "$report"

  {
    echo 'schema_version: "0.1.0"'
    echo "receipt_type: VERIFICATION-WEAVE-RESIDUE"
    echo "validation_result: ${result}"
    echo "hard_residue:"
    if [[ "${#failures[@]}" -eq 0 ]]; then
      echo "  - none"
    else
      for failure in "${failures[@]}"; do
        echo "  - ${failure}"
      done
    fi
    echo "soft_residue:"
    echo "  - candidate_package_not_registered"
    echo "  - owner_lanes_remain_authoritative"
    echo "next_route:"
    echo "  - arcanum/arcana/sigil-development"
    echo "  - arcanum/arcana/experiment-harness"
  } > "$RESIDUE_LEDGER"
}

main() {
  local file
  local timestamp
  local positive_count
  local negative_count

  require_file "$PACKAGE_DIR/README.md"
  require_file "$PACKAGE_DIR/SKILL.md"
  require_file "$SCRIPT_DIR/OUTPUT-CONTRACT.md"
  require_file "$SCRIPT_DIR/QUALITY-BAR.md"
  require_file "$SCRIPT_DIR/ANTI-PATTERNS.md"
  require_file "$SCRIPT_DIR/VALIDATION-EXPERIMENT.md"

  positive_count="$(find "$POSITIVE_DIR" -type f -name '*.receipt.yml' | wc -l | tr -d ' ')"
  negative_count="$(find "$NEGATIVE_DIR" -type f -name '*.receipt.yml' | wc -l | tr -d ' ')"

  [[ "$positive_count" == "6" ]] || fail "expected 6 positive fixtures, found ${positive_count}"
  [[ "$negative_count" == "12" ]] || fail "expected 12 negative controls, found ${negative_count}"

  while IFS= read -r file; do
    check_positive_receipt "$file"
  done < <(find "$POSITIVE_DIR" -type f -name '*.receipt.yml' | sort)

  while IFS= read -r file; do
    check_negative_receipt "$file"
  done < <(find "$NEGATIVE_DIR" -type f -name '*.receipt.yml' | sort)

  check_no_denylist_literals

  timestamp="${VW_VALIDATION_TIMESTAMP:-$(date -u +%Y%m%dT%H%M%SZ)}"
  if [[ "${#failures[@]}" -eq 0 ]]; then
    write_reports "pass" "$timestamp"
    echo "verification-weaver validation passed"
    echo "validated ${positive_count} positive fixtures and ${negative_count} negative controls"
    echo "summary: ${VALIDATION_MD#$PACKAGE_DIR/}"
    exit 0
  fi

  write_reports "fail" "$timestamp"
  printf 'verification-weaver validation failed with %d issue(s)\n' "${#failures[@]}" >&2
  printf ' - %s\n' "${failures[@]}" >&2
  exit 1
}

main "$@"
