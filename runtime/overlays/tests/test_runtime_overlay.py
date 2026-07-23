#!/usr/bin/env python3
"""Causal fixture battery for the generic runtime-overlay validator."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = PACKAGE / "scripts" / "validate_runtime_overlay.py"
SCHEMA_PATH = PACKAGE / "runtime-overlay-manifest.schema.json"
SPEC = importlib.util.spec_from_file_location("runtime_overlay_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class RuntimeOverlayFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.canonical = root / "public/demo/README.md"
        self.generator = root / "tools/generate.sh"
        self.payload_root = root / ".local/overlays/demo/presets"
        self.preset_dir = self.payload_root / "alpha"
        self.payload = self.preset_dir / "payload.md"
        self.fragment = root / ".local/overlays/demo/fragments/alpha.md"
        self.manifest_path = root / ".local/overlays/demo/manifest.json"
        self.base = (
            "# Demo\n\n"
            "## Controls\n\n"
            "KEEP_GATE\n\nKEEP_STATUS\n\nKEEP_AUTHORITY\n\n"
            "## Catalog\n\nANCHOR\n"
        )
        self.fragment_text = "DECLARED_ALPHA"
        write(self.canonical, self.base)
        write(self.generator, 'GENERATOR_VERSION = "1.0.0"\n')
        write(self.payload, "alpha payload\n")
        write(self.fragment, self.fragment_text + "\n")
        self.manifest = self._manifest()
        self.write_manifest()
        self.write_generated()

    def _manifest(self) -> dict:
        return {
            "schema_version": "arcanum.runtime-overlay-manifest.v1",
            "target": "demo",
            "canonical": {
                "source": "public/demo/README.md",
                "sha256": digest(self.canonical),
                "package_root": "public/demo",
            },
            "generator": {
                "path": "tools/generate.sh",
                "version": "1.0.0",
                "version_marker": 'GENERATOR_VERSION = "1.0.0"',
                "overlay_protocol": "arcanum.runtime-overlay-manifest.v1",
            },
            "payload_root": ".local/overlays/demo/presets",
            "runtime_targets": [
                {
                    "id": runtime,
                    "package_root": f"runtime/{runtime}/demo",
                    "skill_path": f"runtime/{runtime}/demo/SKILL.md",
                    "metadata": {
                        "surface_kind": "generated-native-runtime-package",
                        "runtime": runtime,
                    },
                }
                for runtime in ("one", "two")
            ],
            "allowed_metadata": [
                "surface_kind",
                "runtime",
                "name",
                "description",
            ],
            "fragments": [
                {
                    "id": "alpha-fragment",
                    "preset_ids": ["alpha"],
                    "source": ".local/overlays/demo/fragments/alpha.md",
                    "sha256": digest(self.fragment),
                    "mode": "insert_after_exact",
                    "anchor": "ANCHOR",
                }
            ],
            "presets": [
                {
                    "id": "alpha",
                    "source_dir": ".local/overlays/demo/presets/alpha",
                    "copied_files": [
                        {
                            "source": ".local/overlays/demo/presets/alpha/payload.md",
                            "destination": "presets/alpha/payload.md",
                            "sha256": digest(self.payload),
                        }
                    ],
                }
            ],
            "protected_controls": [
                {"id": "keep-gate", "class": "gate", "text": "KEEP_GATE"},
                {"id": "keep-status", "class": "status", "text": "KEEP_STATUS"},
                {
                    "id": "keep-authority",
                    "class": "authority",
                    "text": "KEEP_AUTHORITY",
                },
            ],
            "validation_command": (
                "python3 arcanum/runtime/overlays/scripts/"
                "validate_runtime_overlay.py --manifest "
                ".local/overlays/demo/manifest.json --target demo"
            ),
        }

    def write_manifest(self) -> None:
        write(self.manifest_path, json.dumps(self.manifest, indent=2) + "\n")

    def composed(self) -> str:
        return self.base.replace("ANCHOR", "ANCHOR\n" + self.fragment_text, 1)

    def write_generated(self) -> None:
        for target in self.manifest["runtime_targets"]:
            metadata = target["metadata"]
            frontmatter = ["---"]
            frontmatter.extend(f"{key}: {value}" for key, value in metadata.items())
            frontmatter.extend(["name: demo", "description: demo fixture", "---", ""])
            write(
                self.root / target["skill_path"],
                "\n".join(frontmatter) + self.composed(),
            )
            destination = (
                self.root
                / target["package_root"]
                / "presets/alpha/payload.md"
            )
            write(destination, self.payload.read_text("utf-8"))

    def validate(self, *, generated: bool = False) -> dict:
        self.write_manifest()
        return VALIDATOR.validate_manifest(
            self.manifest_path,
            self.root,
            "demo",
            check_generated=generated,
        )


class RuntimeOverlayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="runtime-overlay-")
        self.fixture = RuntimeOverlayFixture(Path(self.temp.name))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def assert_fails_with(self, report: dict, phrase: str) -> None:
        self.assertEqual(report["status"], "fail", report)
        self.assertTrue(
            any(phrase in error for error in report["errors"]),
            f"{phrase!r} not found in {report['errors']}",
        )

    def test_manifest_schema_accepts_fixture(self) -> None:
        import jsonschema

        schema = json.loads(SCHEMA_PATH.read_text("utf-8"))
        jsonschema.Draft202012Validator(schema).validate(self.fixture.manifest)

    def test_declared_additive_preset_and_metadata_pass(self) -> None:
        self.fixture.manifest["allowed_metadata"].append("runtime_note")
        for target in self.fixture.manifest["runtime_targets"]:
            target["metadata"]["runtime_note"] = "declared"
        report = self.fixture.validate()
        self.assertEqual(report["status"], "pass", report)

    def test_stale_base_digest_fails(self) -> None:
        write(self.fixture.canonical, self.fixture.base + "\nchanged\n")
        self.assert_fails_with(self.fixture.validate(), "base digest mismatch")

    def test_missing_protected_control_fails_even_with_new_digest(self) -> None:
        self.fixture.base = self.fixture.base.replace("KEEP_GATE", "")
        write(self.fixture.canonical, self.fixture.base)
        self.fixture.manifest["canonical"]["sha256"] = digest(self.fixture.canonical)
        self.assert_fails_with(self.fixture.validate(), "missing protected gate")

    def test_undeclared_preset_directory_fails(self) -> None:
        write(self.fixture.payload_root / "shadow/payload.md", "shadow\n")
        self.assert_fails_with(
            self.fixture.validate(), "undeclared preset directories: shadow"
        )

    def test_payload_digest_mismatch_fails(self) -> None:
        write(self.fixture.payload, "mutated payload\n")
        self.assert_fails_with(self.fixture.validate(), "payload digest mismatch")

    def test_fragment_digest_mismatch_fails(self) -> None:
        write(self.fixture.fragment, "mutated fragment\n")
        self.assert_fails_with(self.fixture.validate(), "fragment digest mismatch")

    def test_non_additive_mode_fails(self) -> None:
        self.fixture.manifest["fragments"][0]["mode"] = "replace"
        self.assert_fails_with(self.fixture.validate(), "only insert_after_exact")

    def test_unsafe_destination_fails(self) -> None:
        self.fixture.manifest["presets"][0]["copied_files"][0][
            "destination"
        ] = "../SKILL.md"
        self.assert_fails_with(self.fixture.validate(), "unsafe package destination")

    def test_fragment_may_not_reference_undeclared_preset(self) -> None:
        self.fixture.manifest["fragments"][0]["preset_ids"] = ["missing"]
        self.assert_fails_with(self.fixture.validate(), "undeclared preset id missing")

    def test_generated_composition_passes(self) -> None:
        report = self.fixture.validate(generated=True)
        self.assertEqual(report["status"], "pass", report)

    def test_generated_protected_control_removal_fails(self) -> None:
        target = self.fixture.manifest["runtime_targets"][0]
        path = self.fixture.root / target["skill_path"]
        write(path, path.read_text("utf-8").replace("KEEP_AUTHORITY", ""))
        self.assert_fails_with(
            self.fixture.validate(generated=True), "missing protected authority"
        )

    def test_generated_undeclared_semantics_fail(self) -> None:
        target = self.fixture.manifest["runtime_targets"][0]
        path = self.fixture.root / target["skill_path"]
        write(path, path.read_text("utf-8") + "\nUNDECLARED_RULE\n")
        self.assert_fails_with(
            self.fixture.validate(generated=True),
            "generated semantic body differs",
        )

    def test_generated_undeclared_metadata_fails(self) -> None:
        target = self.fixture.manifest["runtime_targets"][0]
        path = self.fixture.root / target["skill_path"]
        write(
            path,
            path.read_text("utf-8").replace(
                "runtime: one\n", "runtime: one\nshadow_authority: true\n"
            ),
        )
        self.assert_fails_with(
            self.fixture.validate(generated=True),
            "undeclared generated metadata",
        )

    def test_generated_missing_payload_fails(self) -> None:
        target = self.fixture.manifest["runtime_targets"][0]
        destination = (
            self.fixture.root
            / target["package_root"]
            / "presets/alpha/payload.md"
        )
        destination.unlink()
        self.assert_fails_with(
            self.fixture.validate(generated=True), "missing copied payload"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
