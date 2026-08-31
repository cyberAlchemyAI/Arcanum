#!/usr/bin/env python3
"""Project a Design source v2 into the deterministic Design artifact v2 read model."""

from __future__ import annotations

import argparse
import copy
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from project_design_artifact import (
    POLICY_PATH,
    PROCESS_PATH,
    PROFILE_PATH,
    digest_without,
    exact_ref,
    load_json,
    project_design_artifact as project_v1,
)


def project_design_artifact(
    source: dict[str, Any],
    source_ref: dict[str, Any],
    process_ref: dict[str, Any],
    profile_ref: dict[str, Any],
    policy_ref: dict[str, Any],
    selection: dict[str, Any],
) -> dict[str, Any]:
    artifact = project_v1(source, source_ref, process_ref, profile_ref, policy_ref, selection)
    artifact["$schema"] = "https://arcanum.dev/schemas/invoke/design-artifact/v2"
    artifact["schema_version"] = "invoke.design-artifact.v2"
    artifact["artifact_id"] = f"{source['source_id']}:candidate:v2"
    artifact["artifact_digest"] = digest_without(artifact, "artifact_digest")
    return artifact


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--schema-dir", type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    source = load_json(args.source)
    selection_path = root / source["upstream_bindings"]["selection_result_ref"]["path"]
    if source.get("source_digest") != digest_without(source, "source_digest"):
        raise SystemExit("source self digest mismatch")
    if exact_ref(selection_path, root) != source["upstream_bindings"]["selection_result_ref"]:
        raise SystemExit("selection result binding mismatch")
    artifact = project_design_artifact(
        source,
        exact_ref(args.source, root),
        exact_ref(root / PROCESS_PATH, root),
        exact_ref(root / PROFILE_PATH, root),
        exact_ref(root / POLICY_PATH, root),
        load_json(selection_path),
    )
    output = Path(os.path.abspath(args.output))
    if output.exists() or output.is_symlink() or not output.is_absolute() or not output.parent.is_dir():
        raise SystemExit("output must be one absent absolute file with an existing parent")
    fd, temporary = tempfile.mkstemp(prefix=f".{output.name}.", dir=output.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(copy.deepcopy(artifact), handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, output)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
