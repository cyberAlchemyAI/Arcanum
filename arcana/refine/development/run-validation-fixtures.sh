#!/usr/bin/env bash
set -euo pipefail

root="/home/vrondelli/projects/domainspec-core/arcanum"
artifact="$root/arcana/refine"
validator="$root/arcana/experiment-harness/scripts/validate-harness.sh"
dispatch_validator="$root/formulae/dispatch-spec/scripts/validate-dispatch.py"
dispatch_generator="$root/arcana/refine/scripts/generate-refine-dispatch.py"
xray_output="$artifact/development/example-outputs/sigil-new-low.output.md"

generic_output="$("$validator" "$artifact" 2>&1 || true)"
printf '%s\n' "$generic_output"

generic_validation="$(printf '%s\n' "$generic_output" | sed -n 's/^VALIDATION=//p' | tail -n 1)"
profile_validation="$(printf '%s\n' "$generic_output" | sed -n 's/^PROFILE_VALIDATION=//p' | tail -n 1)"

case "${generic_validation:-pass}" in
	pass | flag | block) ;;
	*) generic_validation="flag" ;;
esac

case "${profile_validation:-pass}" in
	pass | flag | block) ;;
	*) profile_validation="flag" ;;
esac

refine_live_validation="pass"

dispatch_template_output="$("$dispatch_validator" "$artifact/templates/refine-dispatch.json" 2>&1 || true)"
printf '%s\n' "$dispatch_template_output"
dispatch_template_validation="$(printf '%s\n' "$dispatch_template_output" | sed -n 's/^VALIDATION=//p' | tail -n 1)"
case "${dispatch_template_validation:-block}" in
	pass) ;;
	flag)
		printf 'FLAG: refine dispatch template validation returned flag\n'
		refine_live_validation="flag"
		;;
	block | *)
		printf 'BLOCK: refine dispatch template validation failed\n'
		refine_live_validation="block"
		;;
esac

generated_dispatch="$(mktemp)"
generator_output="$("$dispatch_generator" --seed "$artifact/development/fixtures/refine-dispatch-seed.json" --output "$generated_dispatch" --validate 2>&1 || true)"
printf '%s\n' "$generator_output"
if ! jq empty "$generated_dispatch" >/dev/null 2>&1; then
	printf 'BLOCK: generated refine dispatch is not valid JSON\n'
	refine_live_validation="block"
else
	generator_validation="$("$dispatch_validator" "$generated_dispatch" 2>&1 || true)"
	printf '%s\n' "$generator_validation"
	generator_status="$(printf '%s\n' "$generator_validation" | sed -n 's/^VALIDATION=//p' | tail -n 1)"
	case "${generator_status:-block}" in
		pass) ;;
		flag)
			printf 'FLAG: generated refine dispatch validation returned flag\n'
			if [[ "$refine_live_validation" == "pass" ]]; then
				refine_live_validation="flag"
			fi
			;;
		block | *)
			printf 'BLOCK: generated refine dispatch validation failed\n'
			refine_live_validation="block"
			;;
	esac
fi
rm -f "$generated_dispatch"

if ! rg -q -- '"gate_id": "g03-native-capability-receipts"' "$artifact/templates/refine-dispatch.json"; then
	printf 'BLOCK: refine dispatch template is missing native capability receipt gate\n'
	refine_live_validation="block"
fi

if rg -q -- 'tools/arcanum --resolve|tools/arcanum --exec|command-backed|command file|Command file|\\.codex/commands' \
	"$artifact/SKILL.md" \
	"$artifact/README.md" \
	"$artifact/REFINEMENT-LOOP.md" \
	"$artifact/templates/runtime-handoff.md" \
	"$artifact/templates/run-manifest.md" \
	"$artifact/templates/evidence-index.json" \
	"$artifact/templates/usage-telemetry.md" \
	"$artifact/templates/reflection-report.md" \
	"$artifact/templates/refine-dispatch.json"; then
	if ! rg -q -- 'Deprecated command files|explicit legacy compatibility|Legacy model CLI adapters|not active .*success gates' \
		"$artifact/SKILL.md" \
		"$artifact/README.md" \
		"$artifact/REFINEMENT-LOOP.md" \
		"$artifact/templates/runtime-handoff.md" \
		"$artifact/templates/refine-dispatch.json"; then
		printf 'BLOCK: active Refine contract has unclassified command-interface wording\n'
		refine_live_validation="block"
	fi
fi

if [[ -f "$xray_output" ]]; then
	if [[ ! -s "$xray_output" ]]; then
		printf 'BLOCK: sigil-new-low output exists but is empty\n'
		refine_live_validation="block"
	else
		has_runtime_handoff="0"
		has_dispatch_route="0"
		has_final_refinement_evidence="0"
		has_explicit_preflight_status="0"
		has_loop_authority="0"
		has_loop_evidence_section="0"
		has_all_loop_stage_names="0"
		has_stage_evidence_marker="0"
		has_native_receipt_evidence="0"
		manifest_rel=""
		index_rel=""
		runtime_rel=""
		dispatch_rel=""

		rg -q -- 'Runtime handoff|RUNTIME-HANDOFF.md' "$xray_output" && has_runtime_handoff="1" || true
		rg -q -- 'Dispatch route|REFINE-DISPATCH.json|dispatch-spec' "$xray_output" && has_dispatch_route="1" || true
		rg -q -- 'Final synthesis|final synthesis|Final refinement|final refinement|## Final Synthesis' "$xray_output" && has_final_refinement_evidence="1" || true
		rg -q -- 'Status: (flag|block)|preflight-only|proposal-only|not promotion evidence' "$xray_output" && has_explicit_preflight_status="1" || true
		rg -q -- 'arcana/refine/REFINEMENT-LOOP.md|REFINEMENT-LOOP.md' "$xray_output" && has_loop_authority="1" || true
		rg -q -- 'Refinement Loop Evidence|Executed refinement loop stages|Loop Stage Evidence' "$xray_output" && has_loop_evidence_section="1" || true
		if rg -q -- 'Context Builder evidence baseline' "$xray_output" \
			&& rg -q -- 'Invoke Define' "$xray_output" \
			&& rg -q -- 'Interrogation refine-review' "$xray_output" \
			&& rg -q -- 'Research decision' "$xray_output" \
			&& rg -q -- 'Distill' "$xray_output" \
			&& rg -q -- 'Invoke Redefine / Design' "$xray_output" \
			&& rg -q -- 'Interrogation refine-design-review' "$xray_output" \
			&& rg -q -- 'Distill Repair' "$xray_output" \
			&& rg -q -- 'Invoke Plan' "$xray_output" \
			&& rg -q -- 'Final Interrogation and Synthesis' "$xray_output"; then
			has_all_loop_stage_names="1"
		fi
		rg -q -- 'artifact path|Artifact path|observation envelope|observation summary|invocation summary|verdict|blocked reason|Result: (PASS|FLAG|BLOCK)|Status: (pass|flag|block)' "$xray_output" && has_stage_evidence_marker="1" || true
		rg -q -- 'native receipt|Native receipt|receipt artifact|Receipt artifact|capability handle|capability_ref|approved subagent|blocked reason' "$xray_output" && has_native_receipt_evidence="1" || true

		if [[ "$has_runtime_handoff" == "0" || "$has_dispatch_route" == "0" || "$has_final_refinement_evidence" == "0" || "$has_loop_authority" == "0" || "$has_loop_evidence_section" == "0" || "$has_all_loop_stage_names" == "0" || "$has_stage_evidence_marker" == "0" || "$has_native_receipt_evidence" == "0" ]]; then
			printf 'FLAG: sigil-new-low output does not prove the canonical refine loop with dispatch route, runtime handoff, and native receipt evidence\n'
			refine_live_validation="flag"
		fi

		if [[ "$has_explicit_preflight_status" == "0" && "$has_final_refinement_evidence" == "0" ]]; then
			printf 'FLAG: sigil-new-low output lacks final evidence or explicit flag/block status\n'
			refine_live_validation="flag"
		fi

		manifest_rel="$(sed -n 's/^- Run manifest: `\([^`]*\)`.*/\1/p' "$xray_output" | tail -n 1)"
		index_rel="$(sed -n 's/^- Evidence index: `\([^`]*\)`.*/\1/p' "$xray_output" | tail -n 1)"
		dispatch_rel="$(sed -n 's/^- Dispatch route: `\([^`]*\)`.*/\1/p' "$xray_output" | tail -n 1)"
		runtime_rel="$(sed -n 's/^- Runtime handoff: `\([^`]*\)`.*/\1/p' "$xray_output" | tail -n 1)"

		if [[ -z "$manifest_rel" || -z "$index_rel" || -z "$dispatch_rel" || -z "$runtime_rel" ]]; then
			printf 'FLAG: sigil-new-low output does not reference run manifest, evidence index, dispatch route, and runtime handoff\n'
			refine_live_validation="flag"
		else
			manifest_abs="$root/$manifest_rel"
			index_abs="$root/$index_rel"
			dispatch_abs="$root/$dispatch_rel"
			runtime_abs="$root/$runtime_rel"
			if [[ ! -f "$manifest_abs" ]]; then
				printf 'BLOCK: referenced run manifest does not exist: %s\n' "$manifest_rel"
				refine_live_validation="block"
			fi
			if [[ ! -f "$runtime_abs" ]]; then
				printf 'BLOCK: referenced runtime handoff does not exist: %s\n' "$runtime_rel"
				refine_live_validation="block"
			fi
			if [[ ! -f "$dispatch_abs" ]]; then
				printf 'BLOCK: referenced dispatch route does not exist: %s\n' "$dispatch_rel"
				refine_live_validation="block"
			elif ! jq empty "$dispatch_abs" >/dev/null 2>&1; then
				printf 'BLOCK: referenced dispatch route is not valid JSON: %s\n' "$dispatch_rel"
				refine_live_validation="block"
			else
				dispatch_output="$("$dispatch_validator" "$dispatch_abs" 2>&1 || true)"
				printf '%s\n' "$dispatch_output"
				dispatch_validation="$(printf '%s\n' "$dispatch_output" | sed -n 's/^VALIDATION=//p' | tail -n 1)"
				case "${dispatch_validation:-block}" in
					pass) ;;
					flag)
						printf 'FLAG: referenced dispatch route validation returned flag: %s\n' "$dispatch_rel"
						if [[ "$refine_live_validation" == "pass" ]]; then
							refine_live_validation="flag"
						fi
						;;
					block | *)
						printf 'BLOCK: referenced dispatch route validation failed: %s\n' "$dispatch_rel"
						refine_live_validation="block"
						;;
				esac
			fi
			if [[ ! -f "$index_abs" ]]; then
				printf 'BLOCK: referenced evidence index does not exist: %s\n' "$index_rel"
				refine_live_validation="block"
			elif ! jq empty "$index_abs" >/dev/null 2>&1; then
				printf 'BLOCK: referenced evidence index is not valid JSON: %s\n' "$index_rel"
				refine_live_validation="block"
			fi
			if [[ -f "${manifest_abs:-}" ]]; then
				if ! rg -q -- 'arcana/refine/REFINEMENT-LOOP.md|REFINEMENT-LOOP.md' "$manifest_abs"; then
					printf 'FLAG: referenced run manifest does not cite arcana/refine/REFINEMENT-LOOP.md: %s\n' "$manifest_rel"
					if [[ "$refine_live_validation" == "pass" ]]; then
						refine_live_validation="flag"
					fi
				fi
			fi
			if [[ -f "${index_abs:-}" ]] && jq empty "$index_abs" >/dev/null 2>&1; then
				required_stages=(
					"Context Builder evidence baseline"
					"Invoke Define"
					"Interrogation refine-review"
					"Research decision"
					"Distill"
					"Invoke Redefine / Design"
					"Interrogation refine-design-review"
					"Distill Repair"
					"Invoke Plan"
					"Final Interrogation and Synthesis"
				)
				for required_stage in "${required_stages[@]}"; do
					if ! jq -e --arg stage "$required_stage" '.stages[]? | select(.stage == $stage)' "$index_abs" >/dev/null; then
						printf 'FLAG: evidence index is missing required stage: %s\n' "$required_stage"
						if [[ "$refine_live_validation" == "pass" ]]; then
							refine_live_validation="flag"
						fi
					fi
				done
				while IFS= read -r stage_json; do
					stage="$(jq -r '.stage // ""' <<<"$stage_json")"
					status="$(jq -r '.status // ""' <<<"$stage_json")"
					artifact_path="$(jq -r '.artifact_path // ""' <<<"$stage_json")"
					blocked_reason="$(jq -r '.blocked_reason // ""' <<<"$stage_json")"
					capability_ref="$(jq -r '.capability_ref // ""' <<<"$stage_json")"
					receipt_kind="$(jq -r '.receipt_kind // ""' <<<"$stage_json")"
					receipt_artifact="$(jq -r '.receipt_artifact // ""' <<<"$stage_json")"
					if [[ -z "$artifact_path" && -z "$blocked_reason" ]]; then
						printf 'FLAG: evidence index stage has neither artifact path nor blocked reason: %s\n' "$stage"
						if [[ "$refine_live_validation" == "pass" ]]; then
							refine_live_validation="flag"
						fi
					fi
					if [[ -z "$capability_ref" || -z "$receipt_kind" ]]; then
						printf 'FLAG: evidence index stage is missing native capability receipt evidence: %s\n' "$stage"
						if [[ "$refine_live_validation" == "pass" ]]; then
							refine_live_validation="flag"
						fi
					fi
					if [[ "$status" == "pass" && ( ( -z "$artifact_path" || ! -f "$root/$artifact_path" ) && ( -z "$receipt_artifact" || ! -f "$root/$receipt_artifact" ) ) ]]; then
						printf 'BLOCK: evidence index stage is pass but artifact/receipt is missing: %s -> %s / %s\n' "$stage" "$artifact_path" "$receipt_artifact"
						refine_live_validation="block"
					fi
				done < <(jq -c '.stages[]?' "$index_abs")
			fi
		fi
	fi
fi

printf 'REFINE_LIVE_VALIDATION=%s\n' "$refine_live_validation"

final_validation="$generic_validation"
if [[ "$generic_validation" == "block" || "$profile_validation" == "block" || "$refine_live_validation" == "block" ]]; then
	final_validation="block"
elif [[ "$generic_validation" == "flag" || "$profile_validation" == "flag" || "$refine_live_validation" == "flag" ]]; then
	final_validation="flag"
fi

printf 'VALIDATION=%s\n' "$final_validation"
printf 'PROFILE_VALIDATION=%s\n' "$profile_validation"

if [[ "$final_validation" == "block" ]]; then
	exit 1
fi
