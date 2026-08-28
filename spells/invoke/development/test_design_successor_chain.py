#!/usr/bin/env python3
"""Real Define v3 through Design v3 successor-chain canary tests."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


DEVELOPMENT = Path(__file__).resolve().parent
INVOKE = DEVELOPMENT.parent
if str(DEVELOPMENT) not in sys.path:
    sys.path.insert(0, str(DEVELOPMENT))
if str(INVOKE / "scripts") not in sys.path:
    sys.path.insert(0, str(INVOKE / "scripts"))


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DEFINE_TESTS = load_module(
    "successor_define_admission",
    DEVELOPMENT / "test_validate_define_bundle_admission.py",
)
W2_TESTS = load_module(
    "successor_w2_fixture",
    DEVELOPMENT / "test_compile_design_candidate.py",
)
W3_TESTS = load_module(
    "successor_w3_fixture",
    DEVELOPMENT / "test_compile_design_source_v2.py",
)
W1_V2 = load_module(
    "successor_w1_v2",
    INVOKE / "scripts/compile_design_input_bundle_v2.py",
)
W2_V2 = load_module(
    "successor_w2_v2",
    INVOKE / "scripts/compile_design_candidate_v2.py",
)
W3_V3 = load_module(
    "successor_w3_v3",
    INVOKE / "scripts/compile_design_source_v3.py",
)
ADMISSION_V2 = load_module(
    "successor_admission_v2",
    INVOKE / "scripts/validate_design_bundle_admission_v2.py",
)


def exact(path: Path, root: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
    }


def digest_without(document: dict[str, Any], field: str) -> str:
    projection = {key: value for key, value in document.items() if key != field}
    return hashlib.sha256(
        json.dumps(
            projection,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def replace_string(value: Any, before: str, after: str) -> Any:
    if isinstance(value, dict):
        return {key: replace_string(child, before, after) for key, child in value.items()}
    if isinstance(value, list):
        return [replace_string(child, before, after) for child in value]
    if isinstance(value, str):
        return value.replace(before, after)
    return value


def remove_pointer(document: dict[str, Any], pointer: str) -> None:
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]
    current: Any = document
    for part in parts[:-1]:
        current = current[part]
    current.pop(parts[-1])


def strip_exact_refs(value: Any, pointer: str = "") -> list[dict[str, str]]:
    bindings: list[dict[str, str]] = []
    if isinstance(value, dict):
        if "path" in value and "sha256" in value and "size" in value:
            bindings.append({"pointer": pointer, "path": value["path"]})
            value.pop("sha256")
            value.pop("size")
        for key, child in list(value.items()):
            escaped = key.replace("~", "~0").replace("/", "~1")
            bindings.extend(strip_exact_refs(child, f"{pointer}/{escaped}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            bindings.extend(strip_exact_refs(child, f"{pointer}/{index}"))
    return bindings


class DesignSuccessorChainTests(unittest.TestCase):
    def setUp(self) -> None:
        self.candidate = W2_TESTS.DesignCandidateTests(methodName="runTest")
        self.candidate.setUp()
        self.addCleanup(self.candidate.tearDown)
        self.repo = self.candidate.repo
        self.schemas = self.candidate.schemas

        define = DEFINE_TESTS.AdmissionFixture(self.repo, "mixed")
        define.context["target"]["id"] = self.candidate.fixture.target_id
        define.configure_mode("mixed")
        compiled = define.compile()
        self.assertEqual(0, compiled.returncode, compiled.stderr)
        admitted, define_admission_path = define.admit()
        self.assertEqual(0, admitted.returncode, admitted.stderr)
        self.define = define
        self.define_admission_path = define_admission_path

        self._compile_w1_v2()
        self._compile_w2_v2()
        self._prepare_w3_v2()

    def _compile_w1_v2(self) -> None:
        fixture = self.candidate.fixture
        old_relative = "define-output/DEFINITIONS.json"
        new_relative = "define-v3-output/DEFINITIONS.json"
        closure = replace_string(copy.deepcopy(fixture.closure), old_relative, new_relative)
        boundary = fixture.make_boundary(
            "define-v3-output", "define-artifact", "DEFINITIONS.json"
        )
        fixture.write_approval(fixture.approval_path, boundary)
        closure["$schema"] = "https://arcanum.dev/schemas/invoke/design-input-closure/v2"
        closure["schema_version"] = "invoke.design-input-closure.v2"
        closure["discovery_boundary"] = boundary
        stage_path = self.define.output_dir / "INVOKE-DEFINE-STAGE-RECEIPT.json"
        definitions_path = self.define.output_dir / "DEFINITIONS.json"
        closure["activation"] = {
            "kind": "normal",
            "define_stage_receipt_ref": {
                **exact(stage_path, self.repo),
                "visibility": "public",
                "expected_schema_id": "https://arcanum.dev/schemas/invoke/define-result/v3",
                "expected_schema_version": "invoke.define-stage-receipt.v3",
            },
            "define_admission_receipt_ref": {
                **exact(self.define_admission_path, self.repo),
                "visibility": "public",
                "expected_schema_id": "https://arcanum.dev/schemas/invoke/define-bundle-admission-receipt/v1",
                "expected_schema_version": "invoke.define-bundle-admission-receipt.v1",
            },
            "approval_ref": fixture.file_ref(
                fixture.approval_path,
                "public",
                "https://arcanum.dev/schemas/invoke/design-input-boundary-approval/v1",
                "invoke.design-input-boundary-approval.v1",
            ),
        }
        input_item = closure["input_catalog"][0]
        input_item["selector"] = f"file:{new_relative}"
        input_item["source_ref"] = {
            **exact(definitions_path, self.repo),
            "visibility": "public",
            "expected_schema_id": "https://arcanum.dev/schemas/invoke/definitions/v2",
            "expected_schema_version": "definitions/v2",
        }
        fixture.closure = closure
        fixture.write_closure(closure)
        output = self.repo / "w1-v2"
        attempt = self.repo / "w1-v2.attempt.json"
        receipt = W1_V2.compile_bundle(
            fixture.closure_path,
            self.repo,
            output,
            attempt,
            self.schemas,
        )
        self.assertEqual("pass", receipt["result"], receipt.get("blockers"))
        self.assertFalse(attempt.exists())
        self.candidate.w1_dir = output
        self.candidate.w1_receipt = receipt

    def _compile_w2_v2(self) -> None:
        source = self.candidate.make_source()
        source["$schema"] = "https://arcanum.dev/schemas/invoke/design-source/v2"
        source["schema_version"] = "invoke.design-source.v2"
        # Model the real JSON request boundary so repeated equal refs are distinct
        # values rather than Python object aliases from fixture construction.
        authored = json.loads(json.dumps(source))
        for pointer in (
            "/$schema",
            "/schema_version",
            "/source_id",
            "/activation_kind",
            "/profile_binding/profile_id",
            "/template_selection/selected_profile_id",
            "/transport_policy/append_existing_only",
            "/transport_policy/upstream_mutation",
            "/transport_policy/targets",
            "/next_route",
            "/authority_effect",
            "/source_digest",
        ):
            remove_pointer(authored, pointer)
        request = {
            "$schema": "https://arcanum.dev/schemas/invoke/design-source-v2-authoring-request/v1",
            "schema_version": "invoke.cli-authoring-request.v1",
            "mode": "design",
            "stage": "source",
            "document": authored,
            "evidence_paths": strip_exact_refs(authored),
        }
        request_path = self.repo / "design-source-v2-request.json"
        request_path.write_text(
            json.dumps(request, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        self.candidate.source_path = self.repo / "DESIGN-SOURCE-v2.json"
        authored_result = subprocess.run(
            [
                str(INVOKE.parents[2] / "tools/arcanum"),
                "invoke",
                "design",
                "author",
                "source",
                "--request",
                str(request_path),
                "--repo-root",
                str(self.repo),
                "--output",
                str(self.candidate.source_path),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            0,
            authored_result.returncode,
            authored_result.stdout + authored_result.stderr,
        )
        self.candidate.source = json.loads(
            self.candidate.source_path.read_text(encoding="utf-8")
        )
        output = self.repo / "w2-v2"
        attempt = self.repo / "w2-v2.attempt.json"
        result = W2_V2.compile_candidate(
            self.candidate.source_path,
            self.repo,
            output,
            attempt,
            self.schemas,
        )
        if result != 0:
            diagnostics = (
                json.loads(attempt.read_text(encoding="utf-8")).get("blockers", [])
                if attempt.is_file()
                else []
            )
            self.fail(f"W2 v2 failed with exit {result}: {diagnostics}")
        self.assertFalse(attempt.exists())
        self.w2_dir = output

    def _prepare_w3_v2(self) -> None:
        fixture = W3_TESTS.DesignBundleV2Tests(methodName="runTest")
        fixture.fixture = self.candidate
        fixture.repo = self.repo
        fixture.schemas = self.schemas
        fixture.w2_dir = self.w2_dir
        fixture.artifact_path = self.w2_dir / "DESIGN.json"
        fixture.candidate_receipt_path = (
            self.w2_dir / "DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json"
        )
        fixture.distill_dir = self.repo / "distill-v2"
        fixture.distill_dir.mkdir()
        fixture.closure_path = self.repo / "DESIGN-BUNDLE-CLOSURE-v2.json"
        closure = fixture.make_closure()
        closure["$schema"] = "https://arcanum.dev/schemas/invoke/design-bundle-closure/v2"
        closure["schema_version"] = "invoke.design-bundle-closure.v2"
        closure["closure_digest"] = digest_without(closure, "closure_digest")
        fixture.closure = closure
        fixture.write_json(fixture.closure_path, closure)
        self.w3_fixture = fixture

    def compile_w3(self, name: str) -> tuple[dict[str, Any], Path]:
        output = self.repo / name
        attempt = self.repo / f"{name}.attempt.json"
        result = W3_V3.compile_bundle(
            self.w3_fixture.closure_path,
            self.repo,
            output,
            attempt,
            self.schemas,
        )
        if result != 0:
            diagnostics = (
                json.loads(attempt.read_text(encoding="utf-8")).get("blockers", [])
                if attempt.is_file()
                else []
            )
            self.fail(f"W3 v3 failed with exit {result}: {diagnostics}")
        self.assertFalse(attempt.exists())
        receipt = json.loads(
            (output / "INVOKE-DESIGN-STAGE-RECEIPT.json").read_text(encoding="utf-8")
        )
        return receipt, output

    def validate_w1_variant(
        self, name: str, closure: dict[str, Any]
    ) -> dict[str, Any]:
        closure["closure_digest"] = digest_without(closure, "closure_digest")
        path = self.repo / f"DESIGN-INPUT-CLOSURE-{name}.json"
        path.write_text(
            json.dumps(closure, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return W1_V2.validate_input_closure(
            closure,
            path,
            self.repo,
            self.schemas,
        )

    def assert_activation_block(
        self, name: str, closure: dict[str, Any]
    ) -> dict[str, Any]:
        receipt = self.validate_w1_variant(name, closure)
        self.assertEqual("block", receipt["verdict"])
        self.assertIn(
            "ACTIVATION_RECEIPT_INVALID",
            {item["code"] for item in receipt["blockers"]},
        )
        check = next(
            item
            for item in receipt["checks"]
            if item["check_id"] == "define-predecessor-admission"
        )
        self.assertEqual("block", check["status"])
        return receipt

    def test_w1_rejects_missing_stale_forged_mismatched_historical_and_stage_only_define_predecessors(
        self,
    ) -> None:
        base = self.candidate.fixture.closure

        missing = copy.deepcopy(base)
        missing_ref = missing["activation"]["define_admission_receipt_ref"]
        missing_ref.update(
            {
                "path": "missing-define-admission.json",
                "sha256": "0" * 64,
                "size": 1,
            }
        )
        missing_receipt = self.assert_activation_block("missing", missing)
        self.assertIsNone(
            missing_receipt["bindings"]["define_admission_receipt_ref"]
        )

        stale = copy.deepcopy(base)
        stale["activation"]["define_admission_receipt_ref"]["sha256"] = "1" * 64
        stale_receipt = self.assert_activation_block("stale", stale)
        self.assertIsNone(stale_receipt["bindings"]["define_admission_receipt_ref"])

        admission = json.loads(
            self.define_admission_path.read_text(encoding="utf-8")
        )
        forged = copy.deepcopy(admission)
        forged["validator"]["identity"] = "invoke.forged-define-admission"
        forged["receipt_digest"] = digest_without(forged, "receipt_digest")
        forged_path = self.repo / "forged-define-admission.json"
        forged_path.write_text(
            json.dumps(forged, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        forged_closure = copy.deepcopy(base)
        forged_closure["activation"]["define_admission_receipt_ref"].update(
            exact(forged_path, self.repo)
        )
        self.assert_activation_block("forged", forged_closure)

        mismatched = copy.deepcopy(admission)
        mismatched["stage_receipt_ref"]["size"] += 1
        mismatched["receipt_digest"] = digest_without(
            mismatched, "receipt_digest"
        )
        mismatched_path = self.repo / "mismatched-define-admission.json"
        mismatched_path.write_text(
            json.dumps(mismatched, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
        mismatched_closure = copy.deepcopy(base)
        mismatched_closure["activation"]["define_admission_receipt_ref"].update(
            exact(mismatched_path, self.repo)
        )
        self.assert_activation_block("mismatched", mismatched_closure)

        current_stage_path = self.define.output_dir / "INVOKE-DEFINE-STAGE-RECEIPT.json"
        historical = json.loads(current_stage_path.read_text(encoding="utf-8"))
        historical["$schema"] = (
            "https://arcanum.dev/schemas/invoke/define-result/v2"
        )
        historical["schema_version"] = "invoke.define-stage-receipt.v2"
        historical_path = self.repo / "historical-define-stage.json"
        historical_path.write_text(
            json.dumps(historical, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
        historical_closure = copy.deepcopy(base)
        historical_closure["activation"]["define_stage_receipt_ref"].update(
            exact(historical_path, self.repo)
        )
        historical_closure["activation"]["define_stage_receipt_ref"].update(
            {
                "expected_schema_id": historical["$schema"],
                "expected_schema_version": historical["schema_version"],
            }
        )
        self.assert_activation_block("historical", historical_closure)

        stage_only = copy.deepcopy(base)
        del stage_only["activation"]["define_admission_receipt_ref"]
        stage_only["closure_digest"] = digest_without(
            stage_only, "closure_digest"
        )
        stage_only_path = self.repo / "DESIGN-INPUT-CLOSURE-stage-only.json"
        stage_only_path.write_text(
            json.dumps(stage_only, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "schema invalid"):
            W1_V2.validate_input_closure(
                stage_only,
                stage_only_path,
                self.repo,
                self.schemas,
            )

    def test_define_v3_to_design_v3_is_deterministic_and_admitted(self) -> None:
        first_receipt, first = self.compile_w3("w3-v3-first")
        second_receipt, second = self.compile_w3("w3-v3-second")
        self.assertEqual(first_receipt, second_receipt)
        self.assertEqual(
            {path.name: path.read_bytes() for path in first.iterdir()},
            {path.name: path.read_bytes() for path in second.iterdir()},
        )
        self.assertEqual("invoke.design-stage-receipt.v3", first_receipt["schema_version"])
        self.assertEqual(15, len(list(first.iterdir())))

        admission_path = self.repo / "design-admission-v2.json"
        admission_exit = ADMISSION_V2.validate_bundle(
            first,
            self.repo,
            admission_path,
            self.schemas,
        )
        self.assertEqual(0, admission_exit)
        admission = json.loads(admission_path.read_text(encoding="utf-8"))
        self.assertEqual("pass", admission["result"], admission.get("blockers"))
        self.assertEqual("invoke.design-bundle-admission-receipt.v2", admission["schema_version"])
        self.assertEqual(15, len(admission["output_inventory"]))

        second_admission_path = self.repo / "design-admission-v2-second.json"
        self.assertEqual(
            0,
            ADMISSION_V2.validate_bundle(
                second,
                self.repo,
                second_admission_path,
                self.schemas,
            ),
        )
        second_admission = json.loads(second_admission_path.read_text(encoding="utf-8"))
        self.assertEqual("pass", second_admission["result"])

        cli_output = self.repo / "cli-w3-v3"
        cli_result = subprocess.run(
            [
                str(INVOKE.parents[2] / "tools/arcanum"),
                "invoke",
                "design",
                "produce",
                "final-bundle",
                "--closure",
                str(self.w3_fixture.closure_path),
                "--repo-root",
                str(self.repo),
                "--output",
                str(cli_output),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, cli_result.returncode, cli_result.stdout + cli_result.stderr)
        command_receipt = json.loads(cli_result.stdout)
        self.assertEqual("pass", command_receipt["status"])
        self.assertEqual(
            {path.name: path.read_bytes() for path in first.iterdir()},
            {path.name: path.read_bytes() for path in cli_output.iterdir()},
        )

        cli_admission_path = self.repo / "cli-design-admission-v2.json"
        cli_admission = subprocess.run(
            [
                str(INVOKE.parents[2] / "tools/arcanum"),
                "invoke",
                "design",
                "admit",
                "admission",
                "--bundle",
                str(cli_output),
                "--repo-root",
                str(self.repo),
                "--output",
                str(cli_admission_path),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            0,
            cli_admission.returncode,
            cli_admission.stdout + cli_admission.stderr,
        )
        self.assertEqual("pass", json.loads(cli_admission.stdout)["status"])
        cli_admission_document = json.loads(
            cli_admission_path.read_text(encoding="utf-8")
        )
        self.assertEqual("pass", cli_admission_document["result"])

        cli_stage = json.loads(
            (cli_output / "INVOKE-DESIGN-STAGE-RECEIPT.json").read_text(
                encoding="utf-8"
            )
        )
        status_request = {
            "schema_version": "invoke.capability-status.request.v1",
            "mode": "design",
            "artifact_receipt": {
                "receipt_id": "artifact:design-cli-canary",
                "axis": "artifact_authored",
                "mode": "design",
                "status": "pass",
                "evidence": [
                    "INVOKE-DESIGN-STAGE-RECEIPT.json",
                    "cli-design-admission-v2.json",
                ],
                "producer_receipt": cli_stage,
                "producer_admission_receipt": cli_admission_document,
            },
            "registry_receipt": None,
            "material_package_receipt": None,
            "runtime_receipt": None,
        }
        status_request_path = self.repo / "design-status-request.json"
        status_request_path.write_text(
            json.dumps(status_request, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        status_path = self.repo / "design-status.json"
        status_result = subprocess.run(
            [
                str(INVOKE.parents[2] / "tools/arcanum"),
                "invoke",
                "design",
                "status",
                "--request",
                str(status_request_path),
                "--repo-root",
                str(self.repo),
                "--output",
                str(status_path),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, status_result.returncode, status_result.stdout + status_result.stderr)
        self.assertEqual(
            "pass",
            json.loads(status_path.read_text(encoding="utf-8"))["artifact_authored"][
                "status"
            ],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
