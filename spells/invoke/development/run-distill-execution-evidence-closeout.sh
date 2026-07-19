#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../../../../" && pwd)"

echo "== existing Invoke fixture suite =="
"$script_dir/run-validation-fixtures.sh"

echo "== DEE focused suites =="
for runner in \
  run-distill-evidence-schema-fixtures.sh \
  run-distill-runtime-event-fixtures.sh \
  run-distill-semantic-fixtures.sh \
  run-distill-provenance-fixtures.sh \
  run-distill-mode-capability-fixtures.sh \
  run-distill-active-mode-evidence-fixtures.sh \
  run-distill-positive-evidence-fixture.sh \
  run-distill-missing-evidence-fixture.sh \
  run-distill-fabricated-evidence-fixture.sh \
  run-distill-generated-parity-fixture.sh \
  run-distill-workbench-replay-fixture.sh \
  run-distill-workbench-route-fixture.sh; do
  echo "-- $runner"
  "$script_dir/$runner"
done

echo "== artifact and boundary checks =="
python3 - "$repo_root" <<'PY'
import json
import pathlib
import sys

repo_root = pathlib.Path(sys.argv[1])
evidence_dir = repo_root / "arcanum/spells/invoke/development/fixtures/distill-evidence"
work_pack = repo_root / "arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md"
observability = repo_root / ".arcanum/observability/by-sigil/invoke.jsonl"
failures = []

for path in sorted(evidence_dir.iterdir()):
    if path.suffix == ".json":
        json.loads(path.read_text(encoding="utf-8"))
    elif path.suffix == ".jsonl":
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                json.loads(line)

rows = [line for line in work_pack.read_text(encoding="utf-8").splitlines() if line.startswith("| SWU-DEE-")]
ids = [row.split("|")[1].strip() for row in rows]
expected = [f"SWU-DEE-{index:03d}" for index in range(1, 14)]
if ids != expected or len(set(ids)) != 13:
    failures.append(f"SWU manifest mismatch: {ids}")

observability_rows = [json.loads(line) for line in observability.read_text(encoding="utf-8").splitlines() if line.strip()]
if not any(row.get("run_id") == "invoke-20260717T-dee013-closeout" for row in observability_rows):
    failures.append("DEE-013 observability append missing")

if failures:
    print("FAIL integrated artifact checks")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("PASS all DEE fixture JSON/JSONL artifacts parse")
print("PASS Work Pack contains thirteen unique ordered SWUs")
print("PASS DEE-013 closeout observability append is present")
PY

private_marker_pattern="${ARCANUM_PRIVATE_MARKER_PATTERN:-}"
if [[ -n "$private_marker_pattern" ]] && rg -n "$private_marker_pattern" "$repo_root/arcanum/spells/invoke/development/distill-execution-evidence"; then
  echo "FAIL public boundary scan found caller-supplied private markers" >&2
  exit 1
fi
if rg -n '/(home|Users)/[^/]+/' "$repo_root/arcanum/spells/invoke/development/distill-execution-evidence"; then
  echo "FAIL public boundary scan found an absolute local user path" >&2
  exit 1
fi
echo "PASS public boundary scan"

(cd "$repo_root/arcanum" && git diff --check -- spells/invoke tools/bootstrap_arcanum.sh)
(cd "$repo_root" && git diff --check -- .agents/skills/invoke .claude/skills/invoke projects/ide-extension .arcanum/observability/by-sigil/invoke.jsonl)
echo "PASS scoped git diff --check"
echo "SUMMARY: PASS integrated Distill execution-evidence closeout"
