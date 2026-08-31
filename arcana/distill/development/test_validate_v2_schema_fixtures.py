from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, RefResolver


ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = ROOT / "arcana/distill/scripts/validate-v2-schema-fixtures.py"
FAMILY_MANIFEST = Path(
    "arcana/distill/development/fixtures/v2/schema/schema-family/cases.json"
)

SPEC = importlib.util.spec_from_file_location("distill_v2_schema_validator", RUNNER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load Distill v2 schema validator")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


EXPECTED_FAMILY = (
    ("common", "arcana/distill/development/fixtures/v2/schema/common/cases.json", 27),
    ("mode_spec", "arcana/distill/development/fixtures/v2/schema/mode-spec/cases.json", 184),
    ("technique_spec", "arcana/distill/development/fixtures/v2/schema/technique-spec/cases.json", 164),
    ("profile", "arcana/distill/development/fixtures/v2/schema/profile/cases.json", 60),
    ("source", "arcana/distill/development/fixtures/v2/schema/source/cases.json", 132),
    ("trace_event", "arcana/distill/development/fixtures/v2/schema/trace-event/cases.json", 144),
    ("result", "arcana/distill/development/fixtures/v2/schema/result/cases.json", 219),
    ("stage_receipt", "arcana/distill/development/fixtures/v2/schema/stage-receipt/cases.json", 204),
)

EXPECTED_IDENTITIES = {
    "common": ("distill-common-v2.schema.json", "https://arcanum.dev/schemas/distill/common/2-0-0", "distill.common.v2"),
    "mode_spec": ("distill-mode-spec-v2.schema.json", "https://arcanum.dev/schemas/distill/mode-spec/2-0-0", "distill.mode_spec.v2"),
    "technique_spec": ("distill-technique-spec-v2.schema.json", "https://arcanum.dev/schemas/distill/technique-spec/2-0-0", "distill.technique_spec.v2"),
    "profile": ("distill-profile-v2.schema.json", "https://arcanum.dev/schemas/distill/profile/2-0-0", "distill.profile.v2"),
    "source": ("distill-source-v2.schema.json", "https://arcanum.dev/schemas/distill/source/2-0-0", "distill.source.v2"),
    "trace_event": ("distill-trace-event-v2.schema.json", "https://arcanum.dev/schemas/distill/trace-event/2-0-0", "distill.trace_event.v2"),
    "result": ("distill-result-v2.schema.json", "https://arcanum.dev/schemas/distill/result/2-0-0", "distill.result.v2"),
    "stage_receipt": ("distill-stage-receipt-v2.schema.json", "https://arcanum.dev/schemas/distill/stage-receipt/2-0-0", "distill.stage_receipt.v2"),
}

EXPECTED_ID_DIGESTS = {
    "common": "640d214fa445a108b0e5ac5cbc35de58f668ec151e8a45b6ee82402e77231320",
    "mode_spec": "68860afaa1f27ce66c394ac7d24cb63ea989b6ed9dfd6c160c49c0f8fa33845d",
    "technique_spec": "25a63f398d7828cc9c1ecdd46173f4acdd13fe3a536e9f59a40b4a0036c55b20",
    "profile": "179a2a5be1a7d9909adfcb7a3c49e1c0bb1ba1c9f650a90d1ffd1d84b904d09d",
    "source": "32ac9f40e0b63dff5e3f2ef713605975edfc64b847644e7d3242359b657bf773",
    "trace_event": "e70eba85c7a26a9a33e5913af913f493ce3f12ba931ba4e8c3f6db82a3001315",
    "result": "174f3fc98582c1a09b13414cdde12e39c955a7e9a1944f9ad1fa9b5d43904e66",
    "stage_receipt": "cf5397ee849f590836cd7daaea4b3a96ff660c628bdc278d454da636fd9e0774",
}

EXPECTED_PROBES = {
    "mode_spec": {
        "required": (67, "793979258133c095adaf0153c6712916b5c145350ee0289ba017811de71f6fcf"),
        "wrong_type": (56, "764fd160ad595c92479e28ae91b6fc95da8498836886e26c59827b80e1bba755"),
        "invalid_enum": (34, "02dc508ec1cac5424b6a530de8f4a54836a2f58cc9bfbf4c1376da771355a5f2"),
    },
    "technique_spec": {
        "required": (44, "e05979cf0a5863e10e39f28e8add493153a733cbc8e91f20da1244b33b9d36fc"),
        "wrong_type": (48, "f6214278616526ea19b1ce1b5964b1b15063b6681d69022fa78367940721a52c"),
        "invalid_enum": (29, "03c3dd78d18c9d91dca31402d6a7bc25283a15aa58bcffebf2df35a63ecb1eb2"),
    },
    "profile": {
        "required": (16, "753de1490554c6b05e3255830429676e71f36b9f364a7ad2e05512acd02f1113"),
        "wrong_type": (16, "bb4af2a4469e1b38a0d9cc8f362be5b833a7366e8ddd7ab0eb28a884b0f9b125"),
        "invalid_enum": (17, "83b70e21a989496c352284e3b77ad86eaa5f1cea2a87d2da5def5afd6c560600"),
    },
    "source": {
        "required": (43, "a5b7f71cead86a805a41e41d1edc1ec27ae1334969a87569fa39c4789996e8d0"),
        "wrong_type": (52, "449af04da6313f71a66f3fc3ed27ef8beed515aa11e21b33df68071e42fafd3c"),
        "invalid_enum": (4, "873736d17d5435016285dfe2ee909a522e4ecd0e301f3e2df0d4b981c32742d6"),
    },
    "trace_event": {
        "required": (43, "430b02e9f11bdbde83e564638cf8b35481fb714c0fe470958d23b514e497f410"),
        "wrong_type": (33, "ea521f064b58a47fc2e9ffa9c03e042c38a99980fe6adde2f35c7ca2da23014f"),
        "invalid_enum": (13, "a58be3bcd408a3f38bf448d0c07c32d6e69aa981eb003b394479988452650b19"),
    },
    "result": {
        "required": (74, "a6b8c610d1407e34c084b4519f10906bde9a79c2ced0b7e4d02df257dfeec9a3"),
        "wrong_type": (72, "c2a87e82f186248f52f9143e3c373e7c2fe9d9c3635e60fbcaa835c28afafe98"),
        "invalid_enum": (14, "8a6db892221d3ea3f60bb79a36c8f714fde61913db4875176ce65ec9f928e40a"),
    },
    "stage_receipt": {
        "required": (83, "7ad72886cfadbad8f673d901b78749c4a343706f4c0a59b6d2d9e08393c39e95"),
        "wrong_type": (79, "6abcc7a748ba1030628a1ec5ea56c424911003838e923a55e05f0b6feba5b5c8"),
        "invalid_enum": (20, "e3c00ea578bb47f195b60fcd7b236b632276cac3244bb2bbae2f7eee3cf28eb4"),
    },
}

EXPECTED_COMMON_REFS = {
    "mode_spec": (11, "c7c7b8002b2ca0a7f605847e88e55291a01839e9d418ec62d4200904f0073748"),
    "technique_spec": (17, "166e90fa35aeb8cb0722cad061f5d154a15b85e94d5808eafc9e7a813a606b36"),
    "profile": (5, "b71778308f619d572c80cfbb5b3b02e7766e438bb95e5a3e7530b5e0c0028bc9"),
    "source": (24, "d2ebe31d1a4aa48409211e70d216481235d5c47ff512e5f42c321c1870aad5cb"),
    "trace_event": (39, "6b4e7821db9d82090a0132562b967bcfdcf4f559baf6358fb89ee8320ca744f4"),
    "result": (44, "e9bac05d41a0843e115fc5acc9cc16313dc1a848872c903ee584240ab4e46db1"),
    "stage_receipt": (13, "e31ac29f967c057d25a64f92119c7f3b6e0f690754a78a062616cfe88b607d48"),
}

EXPECTED_POLICY_SPECS = {
    "common": (26, "ad5e1fee0303a29daec5c24f6909bd54189ab16e7609dbb072c7d010b09e8b99"),
    "mode_spec": (14, "e0e6de36f046bd7f335ab6d9034f3050b323b82d0daa509eb328fcd8bf8b2c8d"),
    "technique_spec": (24, "633d4cf6b61b60ee0eeb4d02c8bd360877d19c16a0183a3ded076e1ebddaa624"),
    "profile": (4, "6d3ac979eabe50df7277381d463d9e0ea5e5f82c3f9bd1037ea19688548f3f3b"),
    "source": (7, "41f297692054b5d7b5ce2896e1e33ee07e8817ee8bc5c01eb4cb867296b99112"),
    "trace_event": (14, "63760fc08fb4bac14eef0b519ba641dd4fc5224e67ac352b02fcdd520e6323bb"),
    "result": (13, "3d9cebeeec421e3ecef5ec0d4b3ccb4f4d679500aa4857d7d1e6b25cb9d40e0a"),
    "stage_receipt": (7, "24081156a64e010afdec5cdaa73fd02d45f65de07416740874acbb2987d3dcf3"),
}

OBJECTION_CATEGORIES = (
    "lost_recomposition",
    "missing_input_or_output",
    "wrong_abstraction_level",
    "unconfirmed_evolution_profile",
    "excessive_cognitive_load",
    "external_variety_not_handled",
    "internal_complexity_greater_than_needed",
    "stakeholder_boundary_ambiguity",
    "concept_claim_treated_as_knowledge",
    "validation_burden",
    "hidden_glue",
    "premature_complexity",
    "brittle_minimalism",
)


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class DistillV2W1RGrammarClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.store = validator._schema_store(ROOT)
        cls.schemas = {
            artifact: validator.read_json(
                ROOT / "arcana/distill/schemas" / identity[0]
            )
            for artifact, identity in EXPECTED_IDENTITIES.items()
        }
        cls.family = validator.run_all(ROOT, FAMILY_MANIFEST)
        cls.technique_fixture = validator.read_json(
            ROOT
            / "arcana/distill/development/fixtures/v2/schema/technique-spec/valid-abstraction-level-guard.json"
        )
        cls.mode_fixture = validator.read_json(
            ROOT / "arcana/distill/development/fixtures/v2/schema/mode-spec/valid-mode-spec.json"
        )
        cls.trace_fixture = validator.read_json(
            ROOT / "arcana/distill/development/fixtures/v2/schema/trace-event/valid-trace-event.json"
        )
        cls.result_fixture = validator.read_json(
            ROOT / "arcana/distill/development/fixtures/v2/schema/result/valid-result.json"
        )

    def errors(self, artifact: str, instance: object) -> list[object]:
        schema = self.schemas[artifact]
        resolver = RefResolver.from_schema(schema, store=self.store)
        return list(Draft202012Validator(schema, resolver=resolver).iter_errors(instance))

    def assert_valid(self, artifact: str, instance: object) -> None:
        self.assertEqual(self.errors(artifact, instance), [])
        self.assertIsNone(validator._instance_policy_blocker(artifact, instance))

    def test_family_denominator_and_every_case_id_are_frozen(self) -> None:
        manifest = validator.read_json(ROOT / FAMILY_MANIFEST)
        observed = tuple(
            (item["artifact"], item["manifest_path"], item["expected_case_count"])
            for item in manifest["members"]
        )
        self.assertEqual(observed, EXPECTED_FAMILY)
        self.assertEqual(manifest["expected_member_count"], 8)
        self.assertEqual(manifest["expected_case_count"], 1134)
        self.assertEqual(
            (self.family["status"], self.family["passed"], self.family["total"]),
            ("pass", 1134, 1134),
        )
        for artifact, path, count in EXPECTED_FAMILY:
            leaf = validator.run_all(ROOT, Path(path))
            ids = sorted(item["id"] for item in leaf["results"])
            self.assertEqual((len(ids), digest(ids)), (count, EXPECTED_ID_DIGESTS[artifact]))

    def test_probe_surfaces_are_independently_non_shrinkable(self) -> None:
        for artifact, expected in EXPECTED_PROBES.items():
            path = next(Path(path) for name, path, _ in EXPECTED_FAMILY if name == artifact)
            manifest = validator.read_json(ROOT / path)
            positive = validator.read_json((ROOT / path).parent / manifest["positive_fixture"])
            surfaces = validator._probe_surfaces(positive, self.schemas[artifact], self.store)
            for name, (count, expected_digest) in expected.items():
                with self.subTest(artifact=artifact, surface=name):
                    self.assertEqual((len(surfaces[name]), digest(surfaces[name])), (count, expected_digest))

    def test_reference_edges_and_policy_mutation_specs_are_independently_pinned(self) -> None:
        for artifact, (count, expected_digest) in EXPECTED_COMMON_REFS.items():
            entries = validator._common_ref_entries(self.schemas[artifact])
            self.assertEqual((len(entries), digest(entries)), (count, expected_digest))
        for artifact, path, _ in EXPECTED_FAMILY:
            manifest = validator.read_json(ROOT / path)
            specs = [
                {key: value for key, value in item.items() if key != "expected_blocker"}
                for item in validator._manifest_policy_mutations(manifest)
            ]
            self.assertEqual(
                (len(specs), digest(specs)),
                EXPECTED_POLICY_SPECS[artifact],
            )

    def test_all_schema_identities_meta_validate_and_reject_cue_semantics(self) -> None:
        for artifact, (_, schema_id, version) in EXPECTED_IDENTITIES.items():
            schema = self.schemas[artifact]
            Draft202012Validator.check_schema(schema)
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertEqual(schema["$id"], schema_id)
            observed_version = schema["schema_version"] if artifact == "common" else schema["properties"]["schema_version"]["const"]
            self.assertEqual(observed_version, version)
            encoded = json.dumps(schema, sort_keys=True)
            self.assertNotIn("$dynamicRef", encoded)
            self.assertNotIn("$recursiveRef", encoded)

    def test_state_field_reference_is_closed_and_used_on_all_three_edges(self) -> None:
        common = self.schemas["common"]
        pattern = common["$defs"]["state_field_reference"]["pattern"]
        self.assertEqual(
            pattern,
            "^[a-z][a-z0-9]*(?:_[a-z0-9]+)*(?:\\.[a-z][a-z0-9]*(?:_[a-z0-9]+)*)+(?![\\s\\S])",
        )
        self.assertEqual(
            self.schemas["technique_spec"]["properties"]["allowed_inputs"]["items"]["$ref"],
            f"{validator.COMMON_ID}#/$defs/state_field_reference",
        )
        self.assertEqual(
            self.schemas["technique_spec"]["$defs"]["activation_predicate"]["properties"]["input"]["$ref"],
            f"{validator.COMMON_ID}#/$defs/state_field_reference",
        )
        self.assertEqual(
            self.schemas["technique_spec"]["$defs"]["activation_predicate"]["properties"]["predicate_id"]["$ref"],
            f"{validator.COMMON_ID}#/$defs/canonical_identifier",
        )
        self.assertEqual(
            self.schemas["trace_event"]["$defs"]["technique_payload"]["properties"]["inspected_state"]["items"]["$ref"],
            f"{validator.COMMON_ID}#/$defs/state_field_reference",
        )
        self.assertTrue(all(value == value.lower() for value in self.technique_fixture["allowed_inputs"]))

    def test_activation_is_flat_and_supports_always_any_and_all(self) -> None:
        canonical_predicate = self.technique_fixture["activation"]["predicates"][0]
        self.assertEqual(self.technique_fixture["activation"]["operator"], "all")
        self.assertEqual(canonical_predicate["predicate_id"], "target_context_present")
        always_candidate = copy.deepcopy(self.technique_fixture)
        always_candidate["activation"] = {"operator": "always"}
        self.assert_valid("technique_spec", always_candidate)
        for operator in ("any", "all"):
            candidate = copy.deepcopy(self.technique_fixture)
            candidate["activation"] = {
                "operator": operator,
                "predicates": [
                    {
                        "predicate_id": "target_context_present",
                        "input": "run_frame.target_context",
                        "comparison": "exists",
                    }
                ],
            }
            self.assert_valid("technique_spec", candidate)
        missing_id = copy.deepcopy(candidate)
        del missing_id["activation"]["predicates"][0]["predicate_id"]
        self.assertTrue(self.errors("technique_spec", missing_id))
        invalid_id = copy.deepcopy(candidate)
        invalid_id["activation"]["predicates"][0]["predicate_id"] = "target-context-present"
        self.assertTrue(self.errors("technique_spec", invalid_id))
        duplicate_id = copy.deepcopy(candidate)
        duplicate_id["activation"]["predicates"].append(
            {
                "predicate_id": "target_context_present",
                "input": "candidate_unit.name",
                "comparison": "exists",
            }
        )
        self.assertEqual(
            validator._instance_policy_blocker("technique_spec", duplicate_id),
            "E_ACTIVATION_PREDICATE_ID_DUPLICATE",
        )
        nested = copy.deepcopy(candidate)
        nested["activation"]["predicates"][0]["predicates"] = []
        self.assertTrue(self.errors("technique_spec", nested))
        self.assertEqual(
            validator._instance_policy_blocker("technique_spec", nested),
            "E_ACTIVATION_NOT_FLAT",
        )

    def test_all_five_bounded_emitted_descriptor_kinds_are_representable(self) -> None:
        variants = (
            {"value_kind": "scalar", "scalar_type": "string"},
            {"value_kind": "enum", "values": ["a", "b"]},
            {
                "value_kind": "list",
                "minimum_items": 0,
                "maximum_items": 2,
                "unique_items": True,
                "items": {"value_kind": "scalar", "scalar_type": "string"},
            },
            {
                "value_kind": "record",
                "fields": {"name": {"value_kind": "scalar", "scalar_type": "string"}},
                "required_fields": ["name"],
                "additional_fields": False,
            },
            {
                "value_kind": "union",
                "discriminator": "kind",
                "variants": [
                    {"tag": "text", "descriptor": {"value_kind": "scalar", "scalar_type": "string"}},
                    {"tag": "truth", "descriptor": {"value_kind": "scalar", "scalar_type": "boolean"}},
                ],
            },
        )
        for descriptor in variants:
            with self.subTest(kind=descriptor["value_kind"]):
                candidate = copy.deepcopy(self.technique_fixture)
                candidate["emitted_field_constraints"]["unit_or_layer_id"] = descriptor
                self.assert_valid("technique_spec", candidate)
        bounded = copy.deepcopy(self.technique_fixture)
        bounded["emitted_field_constraints"]["unit_or_layer_id"] = {
            "value_kind": "list",
            "minimum_items": 0,
            "maximum_items": 33,
            "unique_items": True,
            "items": {"value_kind": "scalar", "scalar_type": "string"},
        }
        self.assertTrue(self.errors("technique_spec", bounded))
        self.assertEqual(validator._descriptor_policy_blocker(
            bounded["emitted_field_constraints"]["unit_or_layer_id"]
        ), "E_DESCRIPTOR_BOUNDS")

    def test_failure_responses_use_closed_ordered_actions_and_route_targets(self) -> None:
        schema = self.schemas["technique_spec"]
        actions = schema["$defs"]["failure_action"]["oneOf"]
        non_route = set(actions[0]["properties"]["action"]["enum"])
        self.assertEqual(
            non_route,
            {
                "revise_candidate", "reject_candidate", "merge_candidates",
                "add_guardrail", "defer_complexity", "ask_human_gate",
                "preserve_alternatives",
            },
        )
        self.assertEqual(actions[1]["properties"]["action"]["const"], "route")
        self.assertIn("route_target", actions[1]["required"])
        self.assertEqual(
            [item["decision"] for item in self.technique_fixture["failure_responses"]],
            ["pass", "flag", "block"],
        )
        routed = copy.deepcopy(self.technique_fixture)
        routed["failure_responses"][2]["responses"] = [
            {"action": "route", "route_target": "decision_gate"}
        ]
        routed["failure_responses"][2]["readiness_effect"] = "route"
        self.assert_valid("technique_spec", routed)

    def test_mode_program_policy_pitch_and_human_gate_are_closed(self) -> None:
        program = self.mode_fixture["role_program"]
        self.assertEqual(
            [(item["step"], item["actor"], item["action"]) for item in program],
            [(1, "proposer", "propose"), (2, "balancer", "balance"), (3, "core_engine", "reconcile")],
        )
        ids = [item["technique_id"] for item in self.mode_fixture["technique_policy"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(
            {item["disposition"] for item in self.mode_fixture["technique_policy"]},
            {"required", "available", "not_applicable"},
        )
        self.assertTrue(self.mode_fixture["skipped_reason_required"])
        self.assertEqual(self.mode_fixture["pitch_off_policy"], {"status": "prohibited"})

        validate_mode = copy.deepcopy(self.mode_fixture)
        validate_mode["role_program"] = [
            {
                "step": 1, "actor": "balancer", "action": "balance",
                "participation": "required",
                "execution_paths": ["true_subagent", "role_simulation"],
                "preserve_role_trace": True,
            },
            {
                "step": 2, "actor": "proposer", "action": "repair",
                "participation": "conditional",
                "execution_paths": ["true_subagent", "role_simulation"],
                "preserve_role_trace": True,
            },
            {
                "step": 3, "actor": "core_engine", "action": "reconcile",
                "participation": "required", "preserve_role_trace": True,
            },
        ]
        self.assert_valid("mode_spec", validate_mode)

        dimensions = [
            "context_fit", "closure", "recomposition", "evolution_fit",
            "cognitive_load", "validation_cost", "risk_of_brittle_minimalism",
            "risk_of_premature_generality",
        ]
        for status in ("required", "conditional"):
            candidate = copy.deepcopy(self.mode_fixture)
            candidate["pitch_off_policy"] = {
                "status": status,
                "technique_id": "set_based_tournament",
                "comparison_dimensions": dimensions,
                "preserve_options_when_no_winner": True,
            }
            if status == "conditional":
                candidate["pitch_off_policy"]["condition"] = "multiple_viable_tracks"
            self.assert_valid("mode_spec", candidate)

        periodic = copy.deepcopy(self.mode_fixture)
        periodic["human_gates"][0]["trigger"] = "periodic"
        periodic["human_gates"][0]["round_interval"] = 2
        self.assert_valid("mode_spec", periodic)
        del periodic["human_gates"][0]["round_interval"]
        self.assertTrue(self.errors("mode_spec", periodic))

    def test_profile_and_trace_share_exact_thirteen_objection_categories(self) -> None:
        profile_categories = tuple(
            self.schemas["profile"]["properties"]["objection_categories"]["items"]["enum"]
        )
        trace_categories = tuple(
            self.schemas["trace_event"]["$defs"]["objection_payload"]["properties"]["category"]["enum"]
        )
        self.assertEqual(profile_categories, OBJECTION_CATEGORIES)
        self.assertEqual(trace_categories, OBJECTION_CATEGORIES)
        profile = validator.read_json(
            ROOT / "arcana/distill/development/fixtures/v2/schema/profile/valid-profile.json"
        )
        self.assertEqual(tuple(profile["objection_categories"]), OBJECTION_CATEGORIES)
        rejected = copy.deepcopy(profile)
        rejected["objection_categories"][0] = "boundary"
        self.assertTrue(self.errors("profile", rejected))

    def test_source_keeps_groups_required_but_allows_empty_input_collections(self) -> None:
        source_schema = self.schemas["source"]
        self.assertEqual(
            set(source_schema["required"]),
            {"schema_version", "identity", "intent", "policy", "discovery", "constraints", "artifacts", "lineage"},
        )
        self.assertNotIn("minItems", source_schema["properties"]["artifacts"])
        self.assertNotIn(
            "minItems",
            source_schema["$defs"]["policy"]["properties"]["requested_technique_refs"],
        )
        source = validator.read_json(
            ROOT / "arcana/distill/development/fixtures/v2/schema/source/valid-source.json"
        )
        self.assertEqual(source["artifacts"], [])
        self.assertEqual(source["policy"]["requested_technique_refs"], [])
        self.assert_valid("source", source)
        missing = copy.deepcopy(source)
        del missing["artifacts"]
        self.assertTrue(self.errors("source", missing))

    def test_trace_is_typed_for_activation_skip_route_and_emitted_values(self) -> None:
        payload = self.trace_fixture["payload"]
        self.assertEqual(payload["activation_status"], "activated")
        predicate_ids = [
            item["predicate_id"]
            for item in self.technique_fixture["activation"]["predicates"]
        ]
        self.assertEqual(payload["matched_predicate_ids"], predicate_ids)
        self.assertTrue(payload["activation_reason"])
        self.assertTrue(all(
            item["value"]["value_kind"] in {"scalar", "enum", "list", "record", "union"}
            for item in payload["emitted_output"]
        ))

        skipped = copy.deepcopy(self.trace_fixture)
        skipped_payload = skipped["payload"]
        skipped_payload["activation_status"] = "skipped"
        skipped_payload["emitted_output"] = []
        skipped_payload["decision"] = "skipped_with_reason"
        skipped_payload["readiness_effect"] = "unchanged"
        skipped_payload["skip_reason"] = "The available predicate did not match."
        self.assert_valid("trace_event", skipped)

        routed = copy.deepcopy(self.trace_fixture)
        routed["payload"]["decision"] = "route"
        routed["payload"]["readiness_effect"] = "route"
        routed["payload"]["route_target"] = "decision_gate"
        self.assert_valid("trace_event", routed)

    def test_result_trace_outcome_requires_exact_event_link_and_activation_state(self) -> None:
        outcome = self.result_fixture["technique_pack_trace"][0]
        self.assertEqual(outcome["event_id"], self.trace_fixture["event_id"])
        self.assertEqual(outcome["activation_status"], "activated")
        required = set(self.schemas["result"]["$defs"]["technique_outcome"]["required"])
        self.assertIn("event_id", required)
        self.assertIn("activation_status", required)

        skipped = copy.deepcopy(self.result_fixture)
        item = skipped["technique_pack_trace"][0]
        item["activation_status"] = "skipped"
        item["decision"] = "skipped_with_reason"
        item["readiness_effect"] = "unchanged"
        item["skip_reason"] = "Predicate did not match."
        self.assert_valid("result", skipped)

        routed = copy.deepcopy(self.result_fixture)
        item = routed["technique_pack_trace"][0]
        item["decision"] = "route"
        item["readiness_effect"] = "route"
        item["route_target"] = "robot_talks"
        self.assert_valid("result", routed)

    def test_stage_receipt_bytes_and_inventory_laws_remain_unchanged(self) -> None:
        path = ROOT / "arcana/distill/schemas/distill-stage-receipt-v2.schema.json"
        self.assertEqual(
            hashlib.sha256(path.read_bytes()).hexdigest(),
            "52cfb8df67c39b28a823ff5b0955664fba96e574d42d8416e02a39303321be98",
        )
        inventory = self.schemas["stage_receipt"]["properties"]["artifact_inventory"]
        self.assertEqual((inventory["minItems"], inventory["maxItems"]), (4, 4))
        roles = {
            rule["contains"]["properties"]["role"]["const"]
            for rule in inventory["allOf"]
        }
        self.assertEqual(roles, {"source", "trace", "result", "markdown"})

    def test_manifest_expectations_are_not_an_oracle_and_cannot_shrink(self) -> None:
        path = ROOT / "arcana/distill/development/fixtures/v2/schema/mode-spec/cases.json"
        manifest = validator.read_json(path)
        positive = validator.read_json(path.parent / manifest["positive_fixture"])
        mutation = next(
            item
            for item in validator._manifest_policy_mutations(manifest)
            if item["id"] == "mode-role-program-order"
        )
        changed = validator._apply_mutation(positive, mutation)
        observed = validator._generic_observed(
            "mode_spec", changed, self.schemas["mode_spec"], self.store
        )
        self.assertEqual(observed, "E_ROLE_PROGRAM_ORDER")
        self.assertNotEqual(observed, "E_UNKNOWN_PROPERTY")

        shrunk = copy.deepcopy(manifest)
        shrunk["groups"][-1]["mutations"].pop()
        blockers = validator._manifest_contract_blockers(shrunk, "mode_spec")
        self.assertIn("E_FIXTURE_ID_SET_MISMATCH", blockers)
        self.assertIn("E_MUTATION_SPEC_MISMATCH", blockers)

    def test_cli_surface_is_unchanged_and_legacy_manifest_dispatch_is_removed(self) -> None:
        destinations = {action.dest for action in validator.parser()._actions}
        self.assertEqual(destinations, {"help", "root", "manifest", "output_format"})
        source = RUNNER_PATH.read_text(encoding="utf-8")
        run_all_source = source[source.index("def run_all("):source.index("def parser(")]
        self.assertNotIn("distill.technique_spec_fixture_manifest.v2", run_all_source)


if __name__ == "__main__":
    unittest.main()
