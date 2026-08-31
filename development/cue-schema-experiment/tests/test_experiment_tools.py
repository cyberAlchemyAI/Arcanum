#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = load_module("cue_experiment_runner", PACKAGE / "scripts/run-cue-schema-experiment.py")
VERIFIER = load_module("cue_experiment_verifier", PACKAGE / "scripts/verify-cue-schema-experiment.py")


class CueExperimentToolsTest(unittest.TestCase):
    def test_exact_regime_topology(self) -> None:
        self.assertEqual(("R0", "R1", "R2", "R3", "R4", "R5", "R6"), RUNNER.REGIME_IDS)
        self.assertEqual(RUNNER.REGIME_IDS, VERIFIER.REGIME_IDS)

    def test_configuration_pins_all_five_cohorts_and_census(self) -> None:
        config = json.loads((PACKAGE / "experiment.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {"invoke", "orchestrate", "work_pack_readiness", "infra_spec", "distill"},
            set(config["cohorts"]),
        )
        self.assertEqual(37, config["cohorts"]["invoke"]["expected_count"])
        self.assertEqual(225, config["census"]["expected_count"])
        self.assertEqual("v22.12.0", config["runtime_tools"]["node"]["version"])
        self.assertEqual("Python 3.12.3", config["runtime_tools"]["python"]["version"])
        self.assertEqual(23, len(config["cases"]))
        self.assertEqual(23, len({case["case_id"] for case in config["cases"]}))
        self.assertEqual("none", config["claim_ceiling"].split("authority_effect:")[-1] if "authority_effect:" in config["claim_ceiling"] else "none")

    def test_stressor_denominator_is_exact_and_unique(self) -> None:
        manifest = json.loads((PACKAGE / "fixtures/distill-stressor/cases.json").read_text(encoding="utf-8"))
        self.assertEqual(10, manifest["expected_case_count"])
        self.assertEqual(10, len(manifest["cases"]))
        self.assertEqual(10, len({item["case_id"] for item in manifest["cases"]}))
        self.assertEqual(2, sum(item["expected_valid"] for item in manifest["cases"]))

    def test_run_case_denominator_is_independently_pinned(self) -> None:
        self.assertEqual(523, sum(VERIFIER.EXPECTED_CASE_KIND_COUNTS.values()))
        self.assertEqual(23, VERIFIER.EXPECTED_CASE_KIND_COUNTS["persisted"])

    def test_infra_yaml_is_migration_evidence_not_a_new_schema_surface(self) -> None:
        config = json.loads((PACKAGE / "experiment.json").read_text(encoding="utf-8"))
        self.assertEqual(
            "arcanum/formulae/infra-spec/infra-spec.schema.yml",
            config["infra_yaml_path"],
        )

    def test_report_integrity_digest_excludes_only_integrity_field(self) -> None:
        document = {"schema_version": "test", "report_digest": "normalized", "value": 1}
        document["report_integrity_digest"] = VERIFIER.sha256_bytes(
            VERIFIER.canonical_bytes(document)
        )
        VERIFIER.verify_integrity(document)
        document["value"] = 2
        with self.assertRaisesRegex(ValueError, "report integrity digest"):
            VERIFIER.verify_integrity(document)

    def test_command_output_tamper_is_rejected(self) -> None:
        command = {
            "command_id": "R0-0001",
            "network_isolation": "bubblewrap_unshare_net",
            "expected_exit": 0,
            "exit_status": 0,
            "expected_result": True,
            "stdout_base64": "",
            "stdout_size_bytes": 0,
            "stdout_sha256": VERIFIER.sha256_bytes(b""),
            "stderr_base64": "",
            "stderr_size_bytes": 0,
            "stderr_sha256": VERIFIER.sha256_bytes(b""),
        }
        VERIFIER.verify_command(command)
        command["stdout_size_bytes"] = 1
        with self.assertRaisesRegex(ValueError, "stdout size"):
            VERIFIER.verify_command(command)

    def test_classification_rejects_semantic_mismatch(self) -> None:
        report = {
            "commands": [],
            "regimes": {
                "R0": {"blockers": []},
                "R1": {"semantic_mismatches": [{"case_id": "x"}]},
                "R2": {"cohorts": {"invoke": {"status": "pass"}}, "census": {"status": "pass"}},
                "R3": {"status": "pass", "semantic_mismatches": []},
                "R4": {"cohorts": {"invoke": {"status": "pass"}}},
                "R5": {"cohorts": {"invoke": {"status": "pass"}}},
                "R6": {"status": "pass", "median_reduction_percent": 100},
            },
        }
        self.assertEqual("reject_cue", RUNNER.classify(report))
        self.assertEqual("reject_cue", VERIFIER.classify(report))

    def test_generation_evidence_tolerates_strict_import_failures(self) -> None:
        generated = {"path": "/tmp/generated.json", "sha256": "a" * 64, "size_bytes": 1}
        results = {
            "import-failed.schema.json": {
                "status": "not_evaluable",
                "blockers": ["strict_import_failed"],
            },
            "generated.schema.json": {
                "status": "pass",
                "generated_ref": generated,
            },
        }
        self.assertEqual([generated], RUNNER.collect_generated_refs(results))

    def test_native_commands_use_physical_not_logical_prototype_path(self) -> None:
        reference = {
            "path": "arcanum/example.schema.cue",
            "physical_path": "/tmp/run/native-cue/arcanum/example.schema.cue",
        }
        self.assertEqual(reference["physical_path"], RUNNER.physical_ref_path(reference))

    def test_archived_native_fallback_is_package_relative(self) -> None:
        report = PACKAGE / "reports/run-01.json"
        reference = {
            "path": "arcanum/example.schema.cue",
            "physical_path": "/definitely/absent/native.cue",
        }
        self.assertEqual(
            PACKAGE / "prototypes/native/arcanum/example.schema.cue",
            VERIFIER.resolve_report_artifact(report, reference, "native"),
        )

    def test_reproducibility_digest_ignores_run_local_identity(self) -> None:
        base = {
            "run_id": "run-a",
            "membership": {"census": {"count": 1, "membership_digest": "m"}},
            "inputs": {"before_tree_digest": "i"},
            "regimes": {
                regime: {"status": "pass"} for regime in RUNNER.REGIME_IDS
            },
            "classification": "retain_json_schema",
            "native_prototype_tree": {"digest": "n"},
            "generated_tree": {"digest": "g"},
        }
        base["regimes"]["R0"]["cases"] = [
            {
                "case_id": "case-1",
                "r0_observed_valid": True,
                "r1_observed_valid": True,
                "r3_observed_valid": True,
            }
        ]
        second = json.loads(json.dumps(base))
        second["run_id"] = "run-b"
        self.assertEqual(
            RUNNER.reproducibility_projection(base),
            RUNNER.reproducibility_projection(second),
        )

    def test_physical_ref_verification_ignores_nonidentity_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "cue"
            path.write_bytes(b"binary")
            expected = VERIFIER.file_ref(path)
            expected["release_archive_sha256"] = "a" * 64
            VERIFIER.verify_ref(path, expected)

    def test_native_bundler_preserves_external_and_internal_constraints(self) -> None:
        by_path = {
            "schemas/common.json": {
                "$id": "https://example.test/common.json",
                "$defs": {"identifier": {"type": "string", "pattern": "^[a-z]+$"}},
            },
            "schemas/root.json": {
                "$id": "https://example.test/root.json",
                "type": "object",
                "properties": {
                    "id": {"$ref": "common.json#/$defs/identifier"},
                },
            },
        }
        by_id = {document["$id"]: document for document in by_path.values()}
        bundled = RUNNER.bundle_schema_references(
            by_path["schemas/root.json"], "schemas/root.json", by_path, by_id
        )
        self.assertEqual(
            {"type": "string", "pattern": "^[a-z]+$"},
            bundled["properties"]["id"],
        )


if __name__ == "__main__":
    unittest.main()
