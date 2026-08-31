#!/usr/bin/env python3
"""Executable W2 tests for the closure-bound Invoke Define v3 compiler."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable
from unittest import mock

from jsonschema import Draft202012Validator, RefResolver

DEVELOPMENT_DIR = Path(__file__).resolve().parent
if str(DEVELOPMENT_DIR) not in sys.path:
    sys.path.insert(0, str(DEVELOPMENT_DIR))

from define_v3_test_fixture import (  # noqa: E402
    COMPILER,
    DefineV3RepositoryFixture,
    canonical_bytes,
    write_json,
)


COMPILER_SPEC = importlib.util.spec_from_file_location("compile_define_source_v3", COMPILER)
assert COMPILER_SPEC is not None and COMPILER_SPEC.loader is not None
COMPILER_MODULE = importlib.util.module_from_spec(COMPILER_SPEC)
COMPILER_SPEC.loader.exec_module(COMPILER_MODULE)


class CompileDefineSourceV3Test(unittest.TestCase):
    def fixture(self, mode: str = "mixed") -> tuple[tempfile.TemporaryDirectory[str], DefineV3RepositoryFixture]:
        temporary = tempfile.TemporaryDirectory()
        return temporary, DefineV3RepositoryFixture(Path(temporary.name), mode)

    def assert_blocked(
        self,
        fixture: DefineV3RepositoryFixture,
        message: str | None = None,
    ) -> None:
        result = fixture.compile()
        self.assertEqual(2, result.returncode, result.stdout)
        self.assertFalse(fixture.output_dir.exists())
        if message is not None:
            self.assertIn(message, result.stderr)

    def direct_compile(
        self,
        fixture: DefineV3RepositoryFixture,
        late_validator: Callable[[Path], None] | None = None,
    ) -> dict[str, Any]:
        return COMPILER_MODULE.compile_source(
            source_path=fixture.source_path,
            output_dir=fixture.output_dir,
            repo_root=fixture.root,
            schema_dir=fixture.schema_dir,
            discovery_roots=["public"],
            public_roots=["public"],
            late_validator=late_validator,
        )

    def receipt(self, fixture: DefineV3RepositoryFixture) -> dict[str, Any]:
        return json.loads(
            (fixture.output_dir / "INVOKE-DEFINE-STAGE-RECEIPT.json").read_text(encoding="utf-8")
        )

    def test_publication_dispatches_to_linux_backend(self) -> None:
        with (
            mock.patch.object(COMPILER_MODULE.sys, "platform", "linux"),
            mock.patch.object(COMPILER_MODULE, "publish_linux_no_replace") as publisher,
        ):
            COMPILER_MODULE.publish_no_replace(Path("stage"), Path("output"))
        publisher.assert_called_once_with(Path("stage"), Path("output"))

    def test_publication_dispatches_to_macos_backend(self) -> None:
        with (
            mock.patch.object(COMPILER_MODULE.sys, "platform", "darwin"),
            mock.patch.object(COMPILER_MODULE, "publish_macos_no_replace") as publisher,
        ):
            COMPILER_MODULE.publish_no_replace(Path("stage"), Path("output"))
        publisher.assert_called_once_with(Path("stage"), Path("output"))

    def test_publication_dispatches_to_windows_backend(self) -> None:
        with (
            mock.patch.object(COMPILER_MODULE.sys, "platform", "win32"),
            mock.patch.object(COMPILER_MODULE, "publish_windows_no_replace") as publisher,
        ):
            COMPILER_MODULE.publish_no_replace(Path("stage"), Path("output"))
        publisher.assert_called_once_with(Path("stage"), Path("output"))

    def test_publication_fails_closed_on_unknown_platform(self) -> None:
        with mock.patch.object(COMPILER_MODULE.sys, "platform", "unknown"):
            with self.assertRaisesRegex(ValueError, "unavailable on unknown"):
                COMPILER_MODULE.publish_no_replace(Path("stage"), Path("output"))

    def test_linux_backend_requests_no_replace_rename(self) -> None:
        renameat2 = mock.Mock(return_value=0)
        libc = mock.Mock(renameat2=renameat2)
        with mock.patch.object(COMPILER_MODULE.ctypes, "CDLL", return_value=libc):
            COMPILER_MODULE.publish_linux_no_replace(Path("stage"), Path("output"))
        self.assertEqual(-100, renameat2.call_args.args[0])
        self.assertEqual(-100, renameat2.call_args.args[2])
        self.assertEqual(1, renameat2.call_args.args[4])

    def test_macos_backend_requests_exclusive_rename(self) -> None:
        renamex_np = mock.Mock(return_value=0)
        libc = mock.Mock(renamex_np=renamex_np)
        with mock.patch.object(COMPILER_MODULE.ctypes, "CDLL", return_value=libc):
            COMPILER_MODULE.publish_macos_no_replace(Path("stage"), Path("output"))
        self.assertEqual(0x00000004, renamex_np.call_args.args[2])

    def test_mixed_bundle_is_exact_complete_and_schema_valid(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        result = fixture.compile()
        self.assertEqual(0, result.returncode, result.stderr)
        names = sorted(path.name for path in fixture.output_dir.iterdir())
        self.assertEqual(13, len(names))
        self.assertEqual(
            sorted([*fixture.source["output_contracts"].values()]),
            names,
        )
        receipt = self.receipt(fixture)
        self.assertEqual("mixed", receipt["semantic_outcome"])
        self.assertEqual(12, len(receipt["outputs"]))
        self.assertEqual([], receipt["structural_schema_refs"])
        self.assertEqual("none", receipt["authority_effect"])
        schemas = {
            name: json.loads((fixture.schema_dir / name).read_text(encoding="utf-8"))
            for name in (
                "define-result-v3.schema.json",
                "define-source-v3.schema.json",
                "define-profile-v3.schema.json",
                "definitions.schema.json",
                "definitions-v2.schema.json",
            )
        }
        result_schema = schemas["define-result-v3.schema.json"]
        store = {schema["$id"]: schema for schema in schemas.values()}
        Draft202012Validator(result_schema, resolver=RefResolver.from_schema(result_schema, store=store)).validate(receipt)

    def test_reference_only_bundle_contains_references_without_canonical_normative_copy(self) -> None:
        temporary, fixture = self.fixture("reference-only")
        self.addCleanup(temporary.cleanup)
        result = fixture.compile()
        self.assertEqual(0, result.returncode, result.stderr)
        receipt = self.receipt(fixture)
        artifact = json.loads((fixture.output_dir / "DEFINITIONS.json").read_text(encoding="utf-8"))
        views = (
            (fixture.output_dir / "DEFINITIONS.md").read_text(encoding="utf-8")
            + (fixture.output_dir / "GLOSSARY.md").read_text(encoding="utf-8")
        )
        self.assertEqual("reference-only", receipt["semantic_outcome"])
        self.assertEqual([], artifact["definitions"])
        self.assertEqual(1, len(artifact["authority_bindings"]))
        self.assertIn("public/definitions/DEFINITIONS.md", views)
        self.assertIn("normative prose is not copied", views.lower())
        self.assertNotIn("A contract is the promise around bounded work.", views)

    def test_candidate_only_bundle_is_supported(self) -> None:
        temporary, fixture = self.fixture("candidate-only")
        self.addCleanup(temporary.cleanup)
        result = fixture.compile()
        self.assertEqual(0, result.returncode, result.stderr)
        receipt = self.receipt(fixture)
        artifact = json.loads((fixture.output_dir / "DEFINITIONS.json").read_text(encoding="utf-8"))
        self.assertEqual("candidate-definitions", receipt["semantic_outcome"])
        self.assertEqual(1, len(artifact["definitions"]))
        self.assertEqual([], artifact["authority_bindings"])

    def test_same_source_compiles_deterministically(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        first = fixture.root / "first"
        second = fixture.root / "second"
        one = fixture.compile(first)
        two = fixture.compile(second)
        self.assertEqual(0, one.returncode, one.stderr)
        self.assertEqual(0, two.returncode, two.stderr)
        self.assertEqual(
            {path.name: path.read_bytes() for path in first.iterdir()},
            {path.name: path.read_bytes() for path in second.iterdir()},
        )

    def test_semantic_context_and_closure_are_copied_byte_for_byte_first(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        result = fixture.compile()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            fixture.context_path.read_bytes(),
            (fixture.output_dir / "DEFINE-SEMANTIC-CONTEXT.json").read_bytes(),
        )
        self.assertEqual(
            fixture.closure_path.read_bytes(),
            (fixture.output_dir / "DEFINE-SEMANTIC-CLOSURE-RECEIPT.json").read_bytes(),
        )
        receipt = self.receipt(fixture)
        self.assertEqual(
            ["semantic-context", "semantic-closure-receipt"],
            [item["kind"] for item in receipt["outputs"][:2]],
        )

    def test_private_context_and_private_candidate_projection_compile(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)

        def make_private(value: Any) -> None:
            if isinstance(value, dict):
                if "visibility" in value:
                    value["visibility"] = "private"
                for child in value.values():
                    make_private(child)
            elif isinstance(value, list):
                for child in value:
                    make_private(child)

        make_private(fixture.context)
        fixture.write_context()
        fixture.closure_path.unlink()
        closure = fixture.run("public/DEFINE-SEMANTIC-CLOSURE-RECEIPT.json")
        self.assertEqual(0, closure.returncode, closure.stderr)
        fixture.closure = json.loads(fixture.closure_path.read_text(encoding="utf-8"))
        fixture.source = fixture._source("mixed")
        fixture.write_source()
        result = fixture.compile()
        self.assertEqual(0, result.returncode, result.stderr)
        artifact = json.loads((fixture.output_dir / "DEFINITIONS.json").read_text(encoding="utf-8"))
        self.assertEqual("private", artifact["visibility"])

    def test_public_registry_rejects_private_candidate_evidence(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.source["definition_registry"]["definitions"][0]["source_refs"][0]["visibility"] = "private"
        fixture.write_source()
        self.assert_blocked(fixture, "source schema invalid")

    def test_layering_contract_mismatch_blocks_without_output(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.source["output_contracts"]["layering"] = "IMPLEMENTATION-LAYERING.md"
        fixture.write_source()
        self.assert_blocked(fixture, "layering output contract")

    def test_required_identity_denominator_passes_with_exact_pass_result(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        request = fixture.root / "public/identity-request.json"
        result_path = fixture.root / "public/identity-result.json"
        write_json(request, {"request_id": "fixture:identity"})
        write_json(result_path, {"verdict": "pass"})
        fixture.source["identity_denominator"] = {
            "classification": "required",
            "request_ref": fixture.exact_ref(request),
            "result_ref": fixture.exact_ref(result_path),
        }
        fixture.write_source()
        result = fixture.compile()
        self.assertEqual(0, result.returncode, result.stderr)

    def test_required_identity_denominator_blocks_non_pass_result(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        request = fixture.root / "public/identity-request.json"
        result_path = fixture.root / "public/identity-result.json"
        write_json(request, {"request_id": "fixture:identity"})
        write_json(result_path, {"verdict": "block"})
        fixture.source["identity_denominator"] = {
            "classification": "required",
            "request_ref": fixture.exact_ref(request),
            "result_ref": fixture.exact_ref(result_path),
        }
        fixture.write_source()
        self.assert_blocked(fixture, "identity denominator result is not pass")

    def test_registry_added_after_closure_blocks_replay(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        write_json(
            fixture.root / "public/late/DEFINITIONS.json",
            {"definitions": [{"id": "LATE-D1", "term": "late term", "aliases": []}]},
        )
        self.assert_blocked(fixture, "does not equal current in-memory replay")

    def test_consumer_added_after_closure_blocks_replay(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        late = fixture.root / "public/late-consumer.md"
        late.write_text("# Late Consumer\n\nUses semantic closure.\n", encoding="utf-8")
        self.assert_blocked(fixture, "does not equal current in-memory replay")

    def test_stale_context_binding_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.context_path.write_bytes(fixture.context_path.read_bytes() + b" ")
        self.assert_blocked(fixture, "semantic context exact reference is stale")

    def test_stale_closure_binding_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.closure_path.write_bytes(fixture.closure_path.read_bytes() + b" ")
        self.assert_blocked(fixture, "semantic closure receipt exact reference is stale")

    def test_tampered_closure_digest_blocks_even_when_source_binding_is_refreshed(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        closure = json.loads(fixture.closure_path.read_text(encoding="utf-8"))
        closure["claim_scope"] = "configured-roots-complete"
        closure["receipt_digest"] = "0" * 64
        write_json(fixture.closure_path, closure)
        fixture.source["upstream_bindings"]["semantic_closure_receipt_ref"] = fixture.exact_ref(fixture.closure_path)
        fixture.write_source()
        self.assert_blocked(fixture, "receipt digest is invalid")

    def test_tampered_bound_context_schema_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.context_schema.write_bytes(fixture.context_schema.read_bytes() + b" ")
        self.assert_blocked(fixture, "context schema exact reference is stale")

    def test_tampered_validator_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        validator = fixture.root / fixture.closure["validator"]["path"]
        validator.write_bytes(validator.read_bytes() + b"# drift\n")
        self.assert_blocked(fixture, "closure validator exact reference is stale")

    def test_duplicate_key_source_is_rejected_strictly(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        source = fixture.source_path.read_text(encoding="utf-8")
        fixture.source_path.write_text(source.replace('{"$schema":', '{"source_id":"duplicate","$schema":', 1), encoding="utf-8")
        self.assert_blocked(fixture, "duplicate JSON key")

    def test_application_order_mismatch_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        apps = fixture.source["semantic_applications"]
        apps[0], apps[1] = apps[1], apps[0]
        fixture.write_source()
        self.assert_blocked(fixture, "do not exactly cover probes")

    def test_application_rationale_mismatch_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.source["semantic_applications"][0]["rationale"] = "A different locally invented rationale."
        fixture.write_source()
        self.assert_blocked(fixture, "rationale differs from closure")

    def test_authority_binding_mismatch_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.source["definition_registry"]["authority_bindings"][0]["term"] = "altered contract"
        fixture.write_source()
        self.assert_blocked(fixture, "differs from the canonical match")

    def test_candidate_definition_term_mismatch_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.source["definition_registry"]["definitions"][0]["term"] = "altered closure"
        fixture.write_source()
        self.assert_blocked(fixture, "term or aliases differ from probe")

    def test_registry_scope_mismatch_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.source["definition_registry"]["authority_scope"] = {
            "kind": "artifact",
            "ref": "different-artifact",
        }
        fixture.write_source()
        self.assert_blocked(fixture, "registry scope")

    def test_probe_scope_must_equal_semantic_target_scope(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.context["concept_probes"][1]["intended_scope"] = {
            "kind": "artifact",
            "ref": "other-artifact",
        }
        fixture.write_context()
        fixture.closure_path.unlink()
        closure = fixture.run("public/DEFINE-SEMANTIC-CLOSURE-RECEIPT.json")
        self.assertEqual(0, closure.returncode, closure.stderr)
        fixture.closure = json.loads(fixture.closure_path.read_text(encoding="utf-8"))
        fixture.source = fixture._source("mixed")
        fixture.write_source()
        self.assert_blocked(fixture, "probe intended scope differs")

    def test_registry_visibility_mismatch_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.source["definition_registry"]["visibility"] = "private"
        for definition in fixture.source["definition_registry"]["definitions"]:
            for ref in definition["source_refs"]:
                ref["visibility"] = "private"
        for binding in fixture.source["definition_registry"]["authority_bindings"]:
            binding["authority_ref"]["visibility"] = "private"
        fixture.write_source()
        self.assert_blocked(fixture, "registry visibility")

    def test_candidate_selector_or_evidence_mismatch_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.source["definition_registry"]["definitions"][0]["source_refs"][0]["selector"] = "Purpose"
        fixture.write_source()
        self.assert_blocked(fixture, "source references differ from probe")

    def test_normalized_candidate_label_collision_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.source["definition_registry"]["definitions"][1]["aliases"] = ["semantic\u00a0closure"]
        # Keep the probe projection equal so the independent collision check is reached.
        fixture.context["concept_probes"][2]["aliases"] = ["semantic\u00a0closure"]
        fixture.write_context()
        fixture.closure_path.unlink()
        closure = fixture.run("public/DEFINE-SEMANTIC-CLOSURE-RECEIPT.json")
        self.assertEqual(1, closure.returncode)
        self.assertFalse(fixture.output_dir.exists())

    def test_unknown_candidate_relation_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.source["definition_registry"]["definitions"][0]["relations"] = [
            {"id": "FIX-UNKNOWN", "type": "depends-on"}
        ]
        fixture.write_source()
        self.assert_blocked(fixture, "unknown candidate")

    def test_missing_machine_checkable_structural_schema_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.source["definition_registry"]["definitions"][0]["structural_schema"] = {
            "handle": "FIX-SCHEMA",
            "status": "machine-checkable",
            "ref": "public/missing.schema.json",
        }
        fixture.write_source()
        self.assert_blocked(fixture, "structural schema is invalid")

    def test_stage_receipt_exact_binds_machine_checkable_structural_schema(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        structural = fixture.root / "public/FIX-D1.schema.json"
        write_json(
            structural,
            {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"},
        )
        fixture.source["definition_registry"]["definitions"][0]["structural_schema"] = {
            "handle": "FIX-D1-SCHEMA",
            "status": "machine-checkable",
            "ref": "public/FIX-D1.schema.json",
        }
        fixture.write_source()
        result = fixture.compile()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            [{"definition_id": "FIX-D1", **fixture.exact_ref(structural)}],
            self.receipt(fixture)["structural_schema_refs"],
        )

    def test_structural_schema_change_during_compile_blocks_publication(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        structural = fixture.root / "public/FIX-D1.schema.json"
        write_json(
            structural,
            {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"},
        )
        fixture.source["definition_registry"]["definitions"][0]["structural_schema"] = {
            "handle": "FIX-D1-SCHEMA",
            "status": "machine-checkable",
            "ref": "public/FIX-D1.schema.json",
        }
        fixture.write_source()

        def mutate_schema(_stage: Path) -> None:
            write_json(
                structural,
                {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "array"},
            )

        with self.assertRaisesRegex(ValueError, "structural schema changed during compilation"):
            self.direct_compile(fixture, mutate_schema)
        self.assertFalse(fixture.output_dir.exists())

    def test_specialization_must_narrow_scope(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        binding = fixture.source["definition_registry"]["authority_bindings"][1]
        binding["authority_scope"] = copy.deepcopy(fixture.context["target"]["authority_scope"])
        # Make the exact closure match agree so the narrowing check is isolated.
        fixture.closure["probe_results"][2]["matches"][0]["authority_scope"] = copy.deepcopy(binding["authority_scope"])
        fixture.closure["receipt_digest"] = hashlib.sha256(
            canonical_bytes({key: value for key, value in fixture.closure.items() if key != "receipt_digest"})
        ).hexdigest()
        write_json(fixture.closure_path, fixture.closure)
        fixture.source["upstream_bindings"]["semantic_closure_receipt_ref"] = fixture.exact_ref(fixture.closure_path)
        fixture.write_source()
        # Replay correctly rejects the forged closure before specialization compilation.
        self.assert_blocked(fixture, "does not equal current in-memory replay")

    def test_late_view_drift_removes_only_compiler_staging(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)

        def drift(stage: Path) -> None:
            (stage / "DEFINITIONS.md").write_text("# drift\n", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "late output drift"):
            self.direct_compile(fixture, drift)
        self.assertFalse(fixture.output_dir.exists())
        self.assertEqual([], list(fixture.root.glob(".define-v3-output.*")))

    def test_late_validator_failure_leaves_output_absent(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)

        def fail(_stage: Path) -> None:
            raise RuntimeError("late validator failed")

        with self.assertRaisesRegex(RuntimeError, "late validator failed"):
            self.direct_compile(fixture, fail)
        self.assertFalse(fixture.output_dir.exists())

    def test_source_change_during_late_validation_blocks_publication(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)

        def change_source(_stage: Path) -> None:
            fixture.source_path.write_bytes(fixture.source_path.read_bytes() + b" ")

        with self.assertRaisesRegex(ValueError, "source changed during compilation"):
            self.direct_compile(fixture, change_source)
        self.assertFalse(fixture.output_dir.exists())

    def test_existing_output_is_preserved(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.output_dir.mkdir()
        owner = fixture.output_dir / "OWNER.txt"
        owner.write_bytes(b"owner bytes\n")
        result = fixture.compile()
        self.assertEqual(2, result.returncode)
        self.assertEqual(b"owner bytes\n", owner.read_bytes())

    def test_competing_output_created_at_publication_is_preserved(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)

        def compete(_stage: Path) -> None:
            fixture.output_dir.mkdir()
            (fixture.output_dir / "OWNER.txt").write_bytes(b"competitor\n")

        with self.assertRaisesRegex(ValueError, "appeared during publication"):
            self.direct_compile(fixture, compete)
        self.assertEqual(b"competitor\n", (fixture.output_dir / "OWNER.txt").read_bytes())

    def test_path_escape_in_source_reference_blocks(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        fixture.source["upstream_bindings"]["semantic_context_ref"]["path"] = "../outside.json"
        fixture.write_source()
        self.assert_blocked(fixture, "source schema invalid")

    def test_result_schema_failure_leaves_no_bundle(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        result_schema_path = fixture.schema_dir / "define-result-v3.schema.json"
        result_schema = json.loads(result_schema_path.read_text(encoding="utf-8"))
        result_schema["properties"]["result"]["const"] = "block"
        write_json(result_schema_path, result_schema)
        self.assert_blocked(fixture, "Define stage receipt schema invalid")

    def test_receipt_schema_bindings_and_output_refs_are_exact(self) -> None:
        temporary, fixture = self.fixture()
        self.addCleanup(temporary.cleanup)
        result = fixture.compile()
        self.assertEqual(0, result.returncode, result.stderr)
        receipt = self.receipt(fixture)
        expected_schema_paths = {
            "source_schema_ref": "define-source-v3.schema.json",
            "profile_schema_ref": "define-profile-v3.schema.json",
            "definitions_v1_schema_ref": "definitions.schema.json",
            "definitions_v2_schema_ref": "definitions-v2.schema.json",
            "result_schema_ref": "define-result-v3.schema.json",
        }
        for key, filename in expected_schema_paths.items():
            path = fixture.schema_dir / filename
            data = path.read_bytes()
            self.assertEqual(
                {
                    "path": path.relative_to(fixture.root).as_posix(),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "size": len(data),
                },
                receipt["schema_bindings"][key],
            )
        for output in receipt["outputs"]:
            data = (fixture.output_dir / output["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), output["sha256"])
            self.assertEqual(len(data), output["size"])
        digest_material = {key: value for key, value in receipt.items() if key != "receipt_digest"}
        expected_digest = hashlib.sha256(canonical_bytes(digest_material).rstrip(b"\n")).hexdigest()
        self.assertEqual(expected_digest, receipt["receipt_digest"])


if __name__ == "__main__":
    unittest.main()
