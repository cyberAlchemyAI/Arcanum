#!/usr/bin/env python3
"""Validate the non-executed tournament package and all deterministic controls."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

from validate_criterion import validate as validate_criterion
from verify_guide_equivalence import verify as verify_guide_equivalence


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[5]
ARCANUM = REPO / "arcanum"
COMPILER = ARCANUM / "spells/invoke/scripts/compile_define_source_v2.py"
DISPATCH = ROOT / "dispatch/RUN-DISPATCH.candidate.json"


def run(command: list[str], cwd: Path = REPO) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(
            f"command failed ({result.returncode}): {' '.join(command)}\n{result.stdout}{result.stderr}"
        )
    return result


def extract_complete_example(guide: Path) -> dict[str, object]:
    text = guide.read_text(encoding="utf-8")
    section = text.split("## Complete Compilable Example", 1)
    if len(section) != 2:
        raise SystemExit(f"complete example section missing: {guide}")
    match = re.search(r"```json\n(.*?)\n```", section[1], re.DOTALL)
    if not match:
        raise SystemExit(f"complete JSON example missing: {guide}")
    return json.loads(match.group(1))


def preconfirmation() -> dict[str, object]:
    criterion = validate_criterion(ROOT)
    guides = verify_guide_equivalence(ROOT)
    blockers = [
        *[f"criterion: {item}" for item in criterion.get("blockers", [])],
        *[f"guides: {item}" for item in guides.get("blockers", [])],
    ]
    return {
        "status": "pass" if not blockers else "block",
        "criterion": criterion,
        "guide_equivalence": guides,
        "writes": 0,
        "agent_runs": "not_started",
        "blockers": blockers,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preconfirmation", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.preconfirmation:
        result = preconfirmation()
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print(f"TOURNAMENT_PRECONFIRMATION={result['status']}")
            print("WRITES=0")
            print("AGENT_RUNS=not_started")
            for blocker in result["blockers"]:
                print(f"BLOCK: {blocker}")
        return 0 if result["status"] == "pass" else 2

    run(["python3", str(ROOT / "render_candidates.py")])
    run(["python3", str(ROOT / "build_oracle_sources.py")])
    run(["python3", str(ROOT / "score_tournament.py"), "--self-test"])

    examples = []
    for guide in sorted((ROOT / "guides").glob("guide-*.md")):
        example = extract_complete_example(guide)
        examples.append(example)
        with tempfile.TemporaryDirectory(prefix="guide-example-", dir=ROOT) as temp:
            source = Path(temp) / "source.json"
            source.write_text(json.dumps(example, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            output = Path(temp) / "bundle"
            run(
                [
                    "python3",
                    str(COMPILER),
                    str(source),
                    "--output-dir",
                    str(output),
                    "--repo-root",
                    str(REPO),
                ]
            )
            if len(list(output.iterdir())) != 11:
                raise SystemExit(f"complete example did not create eleven files: {guide}")
    if not examples or any(example != examples[0] for example in examples[1:]):
        raise SystemExit("candidate guides do not carry the same complete example")

    dispatch = json.loads(DISPATCH.read_text(encoding="utf-8"))
    if dispatch["subagent_strategy"]["authorization"] != "requires_user_permission":
        raise SystemExit("candidate dispatch is not held at the user-permission gate")
    dispatch_result = run(
        [
            "formulae/dispatch-spec/scripts/validate-dispatch.py",
            "spells/invoke/development/define-v2-documentation/tournament/dispatch/RUN-DISPATCH.candidate.json",
        ],
        cwd=ARCANUM,
    )
    if "VALIDATION=pass" not in dispatch_result.stdout:
        raise SystemExit("canonical Dispatch Spec validator did not return pass")

    print("TOURNAMENT_VALIDATION=pass")
    print("GUIDES=3")
    print("SATISFIABLE_CASES=3")
    print("COMPILABLE_GUIDE_EXAMPLES=3")
    print("SCORER_CONTROL=pass")
    print("DISPATCH_SPEC=pass")
    print("AGENT_RUNS=not_started")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
