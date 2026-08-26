#!/usr/bin/env python3
"""Validate the sigil dependency manifest and show deterministic closure."""

from __future__ import annotations

import argparse
import tempfile
from collections import defaultdict, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "registry" / "SIGIL-DEPENDENCIES.tsv"
TIERS = ("formulae", "transmutations", "arcana")


def read_manifest(path: Path) -> tuple[dict[str, list[str]], list[str], int]:
    graph: dict[str, list[str]] = defaultdict(list)
    errors: list[str] = []
    edges = 0
    if not path.is_file():
        return graph, [f"manifest does not exist: {path}"], edges

    seen: set[tuple[str, str]] = set()
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) != 2 or not all(part.strip() for part in parts):
            errors.append(f"line {line_number}: expected exactly two non-empty tab-separated IDs")
            continue
        owner, dependency = (part.strip() for part in parts)
        edge = (owner, dependency)
        if edge in seen:
            errors.append(f"line {line_number}: duplicate dependency edge {owner} -> {dependency}")
            continue
        if owner == dependency:
            errors.append(f"line {line_number}: direct self-dependency is forbidden for {owner}")
            continue
        seen.add(edge)
        graph[owner].append(dependency)
        edges += 1
    return graph, errors, edges


def available_sigils(root: Path) -> set[str]:
    return {
        directory.name
        for tier in TIERS
        for directory in (root / tier).iterdir()
        if directory.is_dir() and (directory / "SKILL.md").is_file()
    }


def validate_graph(graph: dict[str, list[str]], root: Path) -> list[str]:
    available = available_sigils(root)
    errors: list[str] = []
    for owner, dependencies in graph.items():
        if owner not in available:
            errors.append(f"unknown sigil in dependency manifest: {owner}")
        for dependency in dependencies:
            if dependency not in available:
                errors.append(f"unknown dependency for {owner}: {dependency}")
    return errors


def dependency_closure(graph: dict[str, list[str]], requested: list[str]) -> list[str]:
    queue = deque(requested)
    result: list[str] = []
    seen: set[str] = set()
    while queue:
        sigil = queue.popleft()
        if sigil in seen:
            continue
        seen.add(sigil)
        result.append(sigil)
        queue.extend(graph.get(sigil, []))
    return result


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        manifest = root / "dependencies.tsv"
        manifest.write_text("a\tb\nb\ta\na\tc\n", encoding="utf-8")
        graph, errors, edges = read_manifest(manifest)
        if errors or edges != 3 or dependency_closure(graph, ["a"]) != ["a", "b", "c"]:
            print(f"self-test failed: graph={dict(graph)} errors={errors} edges={edges}")
            return 1
        manifest.write_text("a b\n", encoding="utf-8")
        _, errors, _ = read_manifest(manifest)
        if len(errors) != 1:
            print(f"self-test failed: malformed row errors={errors}")
            return 1
    print("sigil dependency validator self-test: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--selection", help="Comma-separated sigil IDs whose closure should be printed.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    graph, errors, edges = read_manifest(args.manifest)
    errors.extend(validate_graph(graph, ROOT))
    requested = [item.strip() for item in (args.selection or "").split(",") if item.strip()]
    available = available_sigils(ROOT)
    errors.extend(f"unknown requested sigil: {item}" for item in requested if item not in available)

    print("Sigil dependency validation")
    print(f"edges: {edges}")
    if requested:
        print("closure: " + ",".join(dependency_closure(graph, requested)))
    if errors:
        print("failures:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("result: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
