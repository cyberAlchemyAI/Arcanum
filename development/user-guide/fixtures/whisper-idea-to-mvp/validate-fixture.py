#!/usr/bin/env python3
"""Validate the Whisper idea-to-MVP guide fixture.

The checks are intentionally small and local. They verify that the fixture
preserves the three-core grammar, selected/rejected candidates, hard gates,
part responsibilities, and a negative probe that fails when a core is removed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} must contain a mapping")
    return data


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_substrate(data: dict) -> None:
    for key in ["idea_resonance", "idea_relevance", "idea_trajectory"]:
        require(key in data, f"idea-substrate.yml missing {key}")
    require("hard_gates" in data and data["hard_gates"], "idea-substrate.yml missing hard_gates")


def validate_candidates(data: dict) -> None:
    objectives = [item["id"] for item in data.get("scoring", {}).get("objectives", [])]
    for required in ["idea_resonance", "idea_relevance", "idea_trajectory"]:
        require(required in objectives, f"candidate-routes.yml missing objective {required}")

    candidates = data.get("candidates", [])
    require(candidates, "candidate-routes.yml missing candidates")
    selected = [item for item in candidates if item.get("status") == "selected"]
    rejected = [item for item in candidates if item.get("status") == "rejected"]
    require(len(selected) == 1, "candidate-routes.yml must have exactly one selected candidate")
    require(rejected, "candidate-routes.yml must preserve at least one rejected candidate")

    for item in candidates:
        scores = item.get("objective_scores", {})
        for required in ["idea_resonance", "idea_relevance", "idea_trajectory"]:
            require(required in scores, f"candidate {item.get('id')} missing score {required}")
        gates = item.get("hard_gate_results", {})
        require(gates, f"candidate {item.get('id')} missing hard_gate_results")

    for item in rejected:
        require("reason_rejected" in item, f"rejected candidate {item.get('id')} missing reason_rejected")
        require("preserved_as" in item, f"rejected candidate {item.get('id')} missing preserved_as")


def validate_parts(data: dict) -> None:
    parts = data.get("parts", [])
    require(parts, "composition-parts.yml missing parts")
    for part in parts:
        part_id = part.get("id")
        for key in ["responsibility", "must_do", "must_not_do", "validation"]:
            require(part.get(key), f"part {part_id} missing {key}")


def validate_toy_probe(data: dict) -> None:
    for key in ["idea_resonance", "idea_relevance", "idea_trajectory"]:
        require(key in data, f"toy-nonwriting-probe.yml missing {key}")
    candidates = data.get("candidates", [])
    require(any(item.get("status") == "selected" for item in candidates), "toy probe missing selected candidate")
    require(any(item.get("status") == "rejected" for item in candidates), "toy probe missing rejected candidate")
    probe = data.get("negative_probe", {})
    require(probe.get("remove_core") == "idea_trajectory", "toy probe must remove idea_trajectory")
    require(probe.get("expected_result") == "fail", "toy probe expected_result must be fail")


def run_negative_probe() -> None:
    data = load_yaml(ROOT / "toy-nonwriting-probe.yml")
    data.pop("idea_trajectory", None)
    try:
        validate_toy_probe(data)
    except ValueError as exc:
        print(f"NEGATIVE_PROBE=pass ({exc})")
        return
    raise ValueError("negative probe failed: missing idea_trajectory was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true", help="Run the missing-core negative probe.")
    args = parser.parse_args()

    try:
      validate_substrate(load_yaml(ROOT / "idea-substrate.yml"))
      validate_candidates(load_yaml(ROOT / "candidate-routes.yml"))
      validate_parts(load_yaml(ROOT / "composition-parts.yml"))
      validate_toy_probe(load_yaml(ROOT / "toy-nonwriting-probe.yml"))
      if args.negative:
          run_negative_probe()
    except Exception as exc:
        print(f"VALIDATION=block ({exc})", file=sys.stderr)
        return 1

    print("VALIDATION=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
