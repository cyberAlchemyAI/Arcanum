#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../../../../" && pwd)"

python3 - "$repo_root" <<'PY'
import pathlib
import subprocess
import sys
import tempfile

repo_root = pathlib.Path(sys.argv[1])
bootstrap = repo_root / "arcanum/tools/bootstrap_arcanum.sh"
canonical = repo_root / "arcanum/spells/invoke"
mirrors = [
    repo_root / ".agents/skills/invoke",
    repo_root / ".claude/skills/invoke",
]
projection_files = [
    "README.md",
    "define.md",
    "design.md",
    "full.md",
    "handoff.md",
    "mode-capabilities.json",
    "refresh.md",
    "validate.md",
    "schemas/distill-execution-receipt.schema.json",
    "schemas/distill-run-request.schema.json",
    "schemas/distill-runtime-event.schema.json",
    "schemas/distill-validation-result.schema.json",
]

with tempfile.TemporaryDirectory(prefix="invoke-parity-") as temporary_directory:
    stage = pathlib.Path(temporary_directory)
    subprocess.run(
        [
            str(bootstrap),
            "--target",
            str(stage),
            "--sigils",
            "",
            "--spells",
            "invoke",
            "--profiles",
            "repo-codex,claude",
            "--no-necronomicon",
            "--force",
        ],
        cwd=repo_root,
        check=True,
        stdout=subprocess.DEVNULL,
    )

    failures = []
    for mirror in mirrors:
        staged_mirror = stage / mirror.relative_to(repo_root)
        for relative_path in projection_files:
            expected = staged_mirror / relative_path
            actual = mirror / relative_path
            if not actual.is_file() or actual.read_bytes() != expected.read_bytes():
                failures.append(f"{mirror.relative_to(repo_root)}/{relative_path}")

    overlays = {
        ".agents/skills/invoke/SKILL.md": ["Evidence Capability Contract", "narrowest reversible trust-building step"],
        ".agents/skills/invoke/plan.md": ["Evidence Capability Contract", "SWU atomicity"],
        ".agents/skills/invoke/templates/work-pack.md": ["swuAtomicityStatus", "firstUnitNarrownessStatus"],
    }
    for relative_path, markers in overlays.items():
        content = (repo_root / relative_path).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in content:
                failures.append(f"overlay marker missing: {relative_path}: {marker}")

if failures:
    print("FAIL generated Invoke parity")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("PASS bootstrap projection regenerated in an isolated target")
print("PASS repo-local Codex and Claude Invoke mirrors match canonical support files")
print("PASS user-owned atomicity overlays retain the DEE evidence contract")
print(f"SUMMARY: PASS ({len(projection_files) * len(mirrors) + 3} checks satisfied expectations)")
print("AUTHORITY: generated parity is derived from bootstrap output; overlays remain explicitly bounded")
PY
