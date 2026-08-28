#!/usr/bin/env python3
"""Focused tests for the stateless deterministic Invoke CLI and root router."""

from __future__ import annotations

import copy
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[4]
INVOKE = REPO / "arcanum/spells/invoke"
CLI = INVOKE / "scripts/invoke_cli.py"
ROOT_TOOL = REPO / "tools/arcanum"
RUNS = INVOKE / "development/runs"


def run(command: list[str], expected: int) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=REPO, text=True, capture_output=True, check=False)
    assert completed.returncode == expected, (
        command,
        completed.returncode,
        completed.stdout,
        completed.stderr,
    )
    result = json.loads(completed.stdout)
    assert result["authority_effect"] == "none"
    return result


def remove_pointer(document: dict[str, Any], pointer: str) -> None:
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]
    current: Any = document
    for part in parts[:-1]:
        current = current[part]
    current.pop(parts[-1])


def escape_pointer(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def strip_exact_refs(value: Any, pointer: str = "") -> list[dict[str, str]]:
    bindings: list[dict[str, str]] = []
    if isinstance(value, dict):
        if "path" in value and "sha256" in value and "size" in value:
            bindings.append({"pointer": pointer, "path": value["path"]})
            value.pop("sha256")
            value.pop("size")
        for key, child in list(value.items()):
            bindings.extend(strip_exact_refs(child, f"{pointer}/{escape_pointer(key)}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            bindings.extend(strip_exact_refs(child, f"{pointer}/{index}"))
    return bindings


def authoring_request(
    source_path: Path,
    *,
    schema_uri: str,
    mode: str,
    stage: str,
    fixed_pointers: list[str],
) -> dict[str, Any]:
    document = json.loads(source_path.read_text(encoding="utf-8"))
    for pointer in fixed_pointers:
        remove_pointer(document, pointer)
    evidence_paths = strip_exact_refs(document)
    return {
        "$schema": schema_uri,
        "schema_version": "invoke.cli-authoring-request.v1",
        "mode": mode,
        "stage": stage,
        "document": document,
        "evidence_paths": evidence_paths,
    }


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_catalog_and_root_routing() -> None:
    direct = run(["python3", str(CLI), "modes"], 0)
    rooted = run([str(ROOT_TOOL), "invoke", "modes"], 0)
    slash = run([str(ROOT_TOOL), "/invoke", "modes"], 0)
    assert direct == rooted == slash
    assert direct["data"]["define"]["status"] == "active"
    assert direct["data"]["design"]["status"] == "active"
    assert direct["data"]["plan"]["status"] == "unsupported"

    described = run([str(ROOT_TOOL), "invoke", "define", "describe", "source"], 0)
    assert described["data"]["output_schema"] == "define-source-v3.schema.json"

    unsupported = run([str(ROOT_TOOL), "invoke", "plan", "describe"], 0)
    assert unsupported["data"]["status"] == "unsupported"

    retired = run([str(ROOT_TOOL), "--exec", "invoke", "modes"], 2)
    assert retired["diagnostics"][0]["code"] == "LEGACY_INVOKE_ADAPTER_RETIRED"
    retired_after_alias = run([str(ROOT_TOOL), "invoke", "--print-prompt"], 2)
    assert retired_after_alias["diagnostics"][0]["code"] == "LEGACY_INVOKE_ADAPTER_RETIRED"

    resolved = subprocess.run(
        [str(ROOT_TOOL), "--resolve", "invoke"],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    assert resolved.returncode == 0
    assert "EXECUTION=deterministic-cli" in resolved.stdout
    assert "ENTRYPOINT=arcanum/spells/invoke/scripts/invoke_cli.py" in resolved.stdout

    other = subprocess.run(
        [str(ROOT_TOOL), "--resolve", "refine"],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    assert other.returncode == 0
    assert "EXECUTION=deterministic-cli" not in other.stdout


def test_define_authoring_and_fail_closed_inputs() -> None:
    with tempfile.TemporaryDirectory(dir=RUNS) as temporary:
        root = Path(temporary)
        context_request = authoring_request(
            INVOKE / "examples/define-v3/DEFINE-SEMANTIC-CONTEXT.json",
            schema_uri="https://arcanum.dev/schemas/invoke/define-semantic-context-authoring-request/v1",
            mode="define",
            stage="semantic-context",
            fixed_pointers=["/$schema", "/schema_version", "/context_id", "/authority_effect"],
        )
        request_path = root / "context-request.json"
        write_json(request_path, context_request)

        checked = run(
            [
                "python3",
                str(CLI),
                "define",
                "check",
                "semantic-context",
                "--request",
                str(request_path),
                "--repo-root",
                str(REPO),
            ],
            0,
        )
        assert checked["status"] == "pass"

        output_a = root / "context-a.json"
        output_b = root / "context-b.json"
        for output in (output_a, output_b):
            authored = run(
                [
                    "python3",
                    str(CLI),
                    "define",
                    "author",
                    "semantic-context",
                    "--request",
                    str(request_path),
                    "--repo-root",
                    str(REPO),
                    "--output",
                    str(output),
                ],
                0,
            )
            assert authored["outputs"][0]["path"].endswith(output.name)
        assert output_a.read_bytes() == output_b.read_bytes()

        exists = run(
            [
                "python3",
                str(CLI),
                "define",
                "author",
                "semantic-context",
                "--request",
                str(request_path),
                "--repo-root",
                str(REPO),
                "--output",
                str(output_a),
            ],
            2,
        )
        assert exists["diagnostics"][0]["code"] == "OUTPUT_EXISTS"

        protected_request = copy.deepcopy(context_request)
        protected_request["document"]["authority_effect"] = "none"
        protected_path = root / "protected.json"
        write_json(protected_path, protected_request)
        protected = run(
            [
                "python3",
                str(CLI),
                "define",
                "check",
                "semantic-context",
                "--request",
                str(protected_path),
                "--repo-root",
                str(REPO),
            ],
            1,
        )
        assert any(item["code"] == "PROTECTED_FIELD_AUTHORED" for item in protected["diagnostics"])

        duplicate_path = root / "duplicate.json"
        duplicate_path.write_text('{"a":1,"a":2}\n', encoding="utf-8")
        duplicate = run(
            [
                "python3",
                str(CLI),
                "define",
                "check",
                "semantic-context",
                "--request",
                str(duplicate_path),
                "--repo-root",
                str(REPO),
            ],
            2,
        )
        assert duplicate["diagnostics"][0]["code"] == "STRICT_JSON_INVALID"

        nonfinite_path = root / "nonfinite.json"
        nonfinite_path.write_text('{"value":NaN}\n', encoding="utf-8")
        nonfinite = run(
            [
                "python3",
                str(CLI),
                "define",
                "check",
                "semantic-context",
                "--request",
                str(nonfinite_path),
                "--repo-root",
                str(REPO),
            ],
            2,
        )
        assert nonfinite["diagnostics"][0]["code"] == "STRICT_JSON_INVALID"


def test_define_source_authoring() -> None:
    with tempfile.TemporaryDirectory(dir=RUNS) as temporary:
        root = Path(temporary)
        request = authoring_request(
            INVOKE / "examples/define-v3/DEFINE-SOURCE.json",
            schema_uri="https://arcanum.dev/schemas/invoke/define-source-v3-authoring-request/v1",
            mode="define",
            stage="source",
            fixed_pointers=[
                "/$schema",
                "/schema_version",
                "/source_id",
                "/profile_id",
                "/template_selection/profile_id",
                "/template_selection/selected",
                "/template_selection/tie",
                "/authority_effect",
            ],
        )
        request_path = root / "source-request.json"
        output = root / "DEFINE-SOURCE.json"
        write_json(request_path, request)
        result = run(
            [
                "python3",
                str(CLI),
                "define",
                "author",
                "source",
                "--request",
                str(request_path),
                "--repo-root",
                str(REPO),
                "--output",
                str(output),
            ],
            0,
        )
        assert result["status"] == "pass"
        authored = json.loads(output.read_text(encoding="utf-8"))
        assert authored["schema_version"] == "invoke.define-source.v3"
        assert authored["profile_id"] == "invoke.generic-definitions-baseline.v3"
        assert authored["authority_effect"] == "none"
        assert authored["source_id"].startswith("define-source:")


def test_define_produce_admit_and_status() -> None:
    with tempfile.TemporaryDirectory(dir=RUNS) as temporary:
        root = Path(temporary)
        bundles = [root / "bundle-one", root / "bundle-two"]
        for bundle in bundles:
            result = run(
                [
                    "python3",
                    str(CLI),
                    "define",
                    "produce",
                    "bundle",
                    "--source",
                    str(INVOKE / "examples/define-v3/DEFINE-SOURCE.json"),
                    "--repo-root",
                    str(REPO),
                    "--output",
                    str(bundle),
                    "--discovery-root",
                    "arcanum/spells/invoke/examples/define-v3",
                    "--public-root",
                    "arcanum",
                ],
                0,
            )
            assert result["status"] == "pass"
            assert len(list(bundle.iterdir())) == 13
        assert {
            path.name: path.read_bytes() for path in bundles[0].iterdir()
        } == {
            path.name: path.read_bytes() for path in bundles[1].iterdir()
        }

        admission_path = root / "admission.json"
        admitted = run(
            [
                "python3",
                str(CLI),
                "define",
                "admit",
                "admission",
                "--bundle",
                str(bundles[0]),
                "--repo-root",
                str(REPO),
                "--output",
                str(admission_path),
            ],
            0,
        )
        assert admitted["status"] == "pass"
        admission = json.loads(admission_path.read_text(encoding="utf-8"))
        assert admission["result"] == "pass"
        assert admission["drift_analysis"]["summary"]["overall"] == "current"

        stage_path = bundles[0] / "INVOKE-DEFINE-STAGE-RECEIPT.json"
        stage_receipt = json.loads(stage_path.read_text(encoding="utf-8"))
        status_request = {
            "schema_version": "invoke.capability-status.request.v1",
            "mode": "define",
            "artifact_receipt": {
                "receipt_id": "artifact:define-cli-canary",
                "axis": "artifact_authored",
                "mode": "define",
                "status": "pass",
                "evidence": [str(stage_path), str(admission_path)],
                "producer_receipt": stage_receipt,
                "producer_admission_receipt": admission,
            },
            "registry_receipt": None,
            "material_package_receipt": None,
            "runtime_receipt": None,
        }
        request_path = root / "status-request.json"
        status_path = root / "status.json"
        write_json(request_path, status_request)
        resolved = run(
            [
                "python3",
                str(CLI),
                "define",
                "status",
                "--request",
                str(request_path),
                "--repo-root",
                str(REPO),
                "--output",
                str(status_path),
            ],
            0,
        )
        assert resolved["status"] == "pass"
        status = json.loads(status_path.read_text(encoding="utf-8"))
        assert status["artifact_authored"]["status"] == "pass"
        assert status["registry_released"]["status"] is False
        assert status["mutation_runtime_ready"]["status"] is False


def test_path_confinement_and_symlink_escape() -> None:
    with tempfile.TemporaryDirectory(dir=RUNS) as temporary, tempfile.TemporaryDirectory(
        prefix="invoke-cli-outside-"
    ) as outside_temporary:
        root = Path(temporary)
        outside_root = Path(outside_temporary)
        outside = outside_root / "request.json"
        outside.write_text("{}\n", encoding="utf-8")
        link = root / "request-link.json"
        link.symlink_to(outside)
        result = run(
            [
                "python3",
                str(CLI),
                "define",
                "check",
                "semantic-context",
                "--request",
                str(link),
                "--repo-root",
                str(REPO),
            ],
            2,
        )
        assert result["diagnostics"][0]["code"] == "PATH_ESCAPE"

        request = authoring_request(
            INVOKE / "examples/define-v3/DEFINE-SEMANTIC-CONTEXT.json",
            schema_uri="https://arcanum.dev/schemas/invoke/define-semantic-context-authoring-request/v1",
            mode="define",
            stage="semantic-context",
            fixed_pointers=["/$schema", "/schema_version", "/context_id", "/authority_effect"],
        )
        request_path = root / "valid-request.json"
        write_json(request_path, request)
        escaped_output = run(
            [
                "python3",
                str(CLI),
                "define",
                "author",
                "semantic-context",
                "--request",
                str(request_path),
                "--repo-root",
                str(REPO),
                "--output",
                str(outside_root / "output.json"),
            ],
            2,
        )
        assert escaped_output["diagnostics"][0]["code"] == "OUTPUT_PATH_ESCAPE"
        assert not (outside_root / "output.json").exists()


def test_design_boundary_authoring_derives_directory_evidence() -> None:
    with tempfile.TemporaryDirectory(dir=RUNS) as temporary:
        root = Path(temporary)
        source = INVOKE / "examples/design-input-v1/DESIGN-INPUT-BOUNDARY-APPROVAL.json"
        document = json.loads(source.read_text(encoding="utf-8"))
        for pointer in (
            "/$schema",
            "/schema_version",
            "/approval_id",
            "/boundary_digest",
            "/authority_effect",
            "/approval_digest",
        ):
            remove_pointer(document, pointer)
        document["roots"][0].pop("sha256")
        document["roots"][0].pop("size")
        request = {
            "$schema": "https://arcanum.dev/schemas/invoke/design-input-boundary-authoring-request/v1",
            "schema_version": "invoke.cli-authoring-request.v1",
            "mode": "design",
            "stage": "boundary",
            "document": document,
            "evidence_paths": [
                {
                    "pointer": "/roots/0",
                    "path": document["roots"][0]["path"],
                    "kind": "directory",
                }
            ],
        }
        request_path = root / "boundary-request.json"
        output = root / "DESIGN-INPUT-BOUNDARY-APPROVAL.json"
        write_json(request_path, request)
        result = run(
            [
                "python3",
                str(CLI),
                "design",
                "author",
                "boundary",
                "--request",
                str(request_path),
                "--repo-root",
                str(REPO),
                "--output",
                str(output),
            ],
            0,
        )
        assert result["status"] == "pass"
        approval = json.loads(output.read_text(encoding="utf-8"))
        assert approval["schema_version"] == "invoke.design-input-boundary-approval.v1"
        assert approval["approval_id"].startswith("design-boundary:")
        assert len(approval["roots"][0]["sha256"]) == 64
        assert approval["roots"][0]["size"] > 0
        assert len(approval["boundary_digest"]) == 64
        assert len(approval["approval_digest"]) == 64


def main() -> int:
    tests = [
        test_catalog_and_root_routing,
        test_define_authoring_and_fail_closed_inputs,
        test_define_source_authoring,
        test_define_produce_admit_and_status,
        test_path_confinement_and_symlink_escape,
        test_design_boundary_authoring_derives_directory_evidence,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)}/{len(tests)} Invoke CLI tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
