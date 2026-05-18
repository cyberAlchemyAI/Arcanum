#!/usr/bin/env bash
set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  printf '{}\n'
  exit 0
fi

input="$(cat)"
repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
observability_dir="$repo_root/.arcanum/observability"
observer="$repo_root/framework/observability/scripts/observe-invocation.sh"
reflector="$repo_root/framework/observability/scripts/reflect-invocation-signals.sh"
strict_mode="${OBSERVED_INVOCATION_STRICT:-0}"
turn_id="$(printf '%s\n' "$input" | jq -r '.turn_id // "unknown-turn"')"
safe_turn="${turn_id//[^A-Za-z0-9._-]/-}"
run_id="arcanum-hook-$safe_turn"
run_dir="$observability_dir/runs/arcanum-hooks/$run_id"
pending="$run_dir/pending-envelope.json"
closed="$run_dir/envelope.json"

if [[ ! -f "$pending" ]]; then
  printf '{}\n'
  exit 0
fi

timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
last_message="$(printf '%s\n' "$input" | jq -r '.last_assistant_message // ""')"
tool_event_count=0
tool_failure_count=0
if [[ -f "$run_dir/tool-events.jsonl" ]]; then
  tool_event_count="$(wc -l < "$run_dir/tool-events.jsonl" | tr -d ' ')"
  tool_failure_count="$(jq -s '[.[]? | select((.tool_response.exit_code? // 0) != 0 or (.tool_response.error? != null) or (.tool_response.is_error? == true))] | length' "$run_dir/tool-events.jsonl" 2>/dev/null || printf '0')"
fi
existing_status="$(jq -r '.execution.status // "partial"' "$pending")"
closeout_status="$existing_status"
if [[ "$tool_failure_count" != "0" ]]; then
  closeout_status="failed"
elif [[ "$existing_status" == "partial" && -n "$last_message" ]]; then
  closeout_status="completed"
fi
quality_status="partial"
case "$closeout_status" in
  completed) quality_status="pass" ;;
  failed) quality_status="fail" ;;
  blocked|interrupted|partial) quality_status="partial" ;;
esac

tmp="$(mktemp)"
jq \
  --arg timestamp "$timestamp" \
  --arg last_message "$last_message" \
  --arg closeout_status "$closeout_status" \
  --arg quality_status "$quality_status" \
  --argjson tool_event_count "$tool_event_count" \
  --argjson tool_failure_count "$tool_failure_count" \
  '.timestamp = $timestamp
  | .execution.status = $closeout_status
  | .execution.validation += ["codex Stop hook closed observer envelope"]
  | .execution.notes = ((.execution.notes // "") + "; tool_events=" + ($tool_event_count|tostring) + "; tool_failures=" + ($tool_failure_count|tostring))
  | .observer.quality_bar_status = $quality_status
  | .observer.recommendation = "none"
  | .observer.closeout_excerpt = ($last_message | if length > 800 then .[0:800] else . end)' \
  "$pending" > "$tmp" && mv "$tmp" "$closed"

if [[ ! -x "$observer" ]]; then
  if [[ "$strict_mode" == "1" ]]; then
    jq -n --arg reason "Arcanum observer unavailable at framework/observability/scripts/observe-invocation.sh" '{
      decision: "block",
      reason: $reason
    }'
  else
    jq -n --arg reason "Arcanum observer unavailable at framework/observability/scripts/observe-invocation.sh" '{
      hookSpecificOutput: {
        hookEventName: "Stop",
        additionalContext: ("Arcanum observer closeout skipped.\nOBSERVATION=skipped\nREASON=" + $reason)
      }
    }'
  fi
  exit 0
fi

observe_output="$("$observer" --envelope "$closed" --observability-dir "$observability_dir" 2>&1 || true)"
printf '%s\n' "$observe_output" > "$run_dir/observer-output.txt"

if printf '%s\n' "$observe_output" | grep -q '^OBSERVATION=\(recorded\|skipped\)'; then
  reflection_mode="${OBSERVED_REFLECT:-auto}"
  recommendation="$(printf '%s\n' "$observe_output" | sed -n 's/^RECOMMENDATION=//p' | tail -n 1)"
  capability_id="$(jq -r '.capability.id // .sigil // empty' "$closed")"
  capability_kind="$(jq -r '.capability.kind // "sigil"' "$closed")"
  reflection_output="REFLECTION=skipped
REASON=no-recommendation
REPORT=n/a"
  case "$reflection_mode" in
    off)
      reflection_output="REFLECTION=skipped
REASON=reflection-disabled
REPORT=n/a"
      ;;
    auto)
      if [[ "$recommendation" == "reflect-now" && -x "$reflector" ]]; then
        reflection_output="$("$reflector" --capability "$capability_id" --kind "$capability_kind" --observability-dir "$observability_dir" 2>&1 || true)"
      fi
      ;;
    always)
      if [[ -x "$reflector" ]]; then
        reflection_output="$("$reflector" --capability "$capability_id" --kind "$capability_kind" --observability-dir "$observability_dir" 2>&1 || true)"
      else
        reflection_output="REFLECTION=failed
REASON=reflector-unavailable
REPORT=n/a"
      fi
      ;;
    *)
      reflection_output="REFLECTION=failed
REASON=invalid OBSERVED_REFLECT: $reflection_mode
REPORT=n/a"
      ;;
  esac
  printf '%s\n' "$reflection_output" > "$run_dir/reflection-output.txt"
  rm -f "$pending"
  jq -n --arg context "$observe_output" --arg reflection "$reflection_output" '{
    hookSpecificOutput: {
      hookEventName: "Stop",
      additionalContext: ("Arcanum observer closeout completed.\n" + $context + "\n" + $reflection)
    }
  }'
  exit 0
fi

if [[ "$strict_mode" == "1" ]]; then
  jq -n --arg reason "Arcanum observer closeout did not complete. Inspect .arcanum/observability/runs/arcanum-hooks and finish telemetry before final closeout." '{
    decision: "block",
    reason: $reason
  }'
else
  jq -n --arg context "$observe_output" '{
    hookSpecificOutput: {
      hookEventName: "Stop",
      additionalContext: ("Arcanum observer closeout failed in standard mode; primary result preserved.\n" + $context)
    }
  }'
fi
