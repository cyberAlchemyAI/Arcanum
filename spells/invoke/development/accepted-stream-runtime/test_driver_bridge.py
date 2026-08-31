#!/usr/bin/env python3
"""Direct positive and negative validation for SWU-RPL-001."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[5]
INVOKE_SCRIPTS = REPO_ROOT / "arcanum/spells/invoke/scripts"
sys.path.insert(0, str(INVOKE_SCRIPTS))

import accepted_stream_driver_bridge as bridge
from accepted_stream_contract import ContractError, child_id, stream_id


def load_driver():
    path = REPO_ROOT / bridge.DRIVER_PATH
    spec = importlib.util.spec_from_file_location("test_bridge_driver", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DriverBridgeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.authority = {
            name: []
            for name in (
                "material",
                "control",
                "terminal",
                "lifecycle",
                "transient",
                "failure",
                "claim",
                "stream",
            )
        }
        self.effect = {"kind": "bounded-write", "external_effect": "none"}
        self.frontier = [
            {"ordinal": ordinal, "swu_id": f"SWU-{ordinal + 1:03d}"}
            for ordinal in range(14)
        ]
        self.stream = stream_id(
            "1" * 64, self.effect, self.authority, self.frontier, "epoch-rpl-001"
        )
        for unit in self.frontier:
            unit["child_id"] = child_id(
                self.stream, unit["ordinal"], unit["swu_id"]
            )
        self.units = [
            {
                "unit_id": unit["swu_id"],
                "ordinal": unit["ordinal"],
                "status": "pass",
                "result_digest": f"{unit['ordinal'] + 1:064x}",
            }
            for unit in self.frontier
        ]
        self.projection = {
            "schema_version": "invoke.accepted-stream-finalized-projection.v1",
            "graph_digest": "1" * 64,
            "accepted_stream_id": self.stream,
            "requested_effect": self.effect,
            "authority": self.authority,
            "epoch": "epoch-rpl-001",
            "frontier_digest": bridge.canonical_digest(self.frontier),
            "acceptance_request_digest": "2" * 64,
            "units": self.units,
        }
        self.baseline = {
            "schema_version": "invoke.accepted-stream-live-baseline.v1",
            "accepted_stream_id": self.stream,
            "epoch": "epoch-rpl-001",
            "frontier_digest": self.projection["frontier_digest"],
            "baseline_digest": "3" * 64,
            "status": "pass",
        }
        self.response = {
            "schema_version": "invoke.owner-acceptance-response.v2",
            "request_id": "RPL-001",
            "request_digest": "2" * 64,
            "accepted_stream_id": self.stream,
            "literal_token": "ACCEPT-RPL-001-" + "2" * 64,
            "decision": "accepted",
        }

    def compile(self, *, no_effect=False, response=...):
        if response is ...:
            response = None if no_effect else self.response
        return bridge.compile_request(
            REPO_ROOT,
            self.projection,
            response,
            self.baseline,
            self.frontier,
            no_effect=no_effect,
        )

    def test_effectful_compile_and_exact_join(self) -> None:
        request = self.compile()
        receipt = load_driver().run(request)
        join = bridge.join_receipt(
            REPO_ROOT, self.projection, self.baseline, request, [receipt]
        )
        schema = json.loads(
            (
                REPO_ROOT
                / "arcanum/spells/invoke/schemas/accepted-stream-driver-join-v1.schema.json"
            ).read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(join)
        self.assertEqual(join["joined_receipt_count"], 1)
        self.assertFalse(join["no_effect"])

    def test_no_effect_rehearsal_is_deterministic_and_grants_no_authority(self) -> None:
        first = self.compile(no_effect=True)
        second = self.compile(no_effect=True)
        self.assertEqual(bridge.canonical_bytes(first), bridge.canonical_bytes(second))
        self.assertTrue(first["no_effect"])
        self.assertEqual(first["stream_id"], self.stream)
        receipt = load_driver().run(first)
        first_join = bridge.join_receipt(
            REPO_ROOT, self.projection, self.baseline, first, [receipt]
        )
        second_join = bridge.join_receipt(
            REPO_ROOT, self.projection, self.baseline, second, [copy.deepcopy(receipt)]
        )
        self.assertEqual(
            bridge.canonical_bytes(first_join), bridge.canonical_bytes(second_join)
        )
        self.assertTrue(first_join["no_effect"])

    def test_remaining_frontier_preserves_stable_ids_and_nonzero_ordinals(self) -> None:
        frontier = [
            {"ordinal": ordinal, "swu_id": f"SWU-GENERIC-FEATURE-{ordinal + 1:03d}"}
            for ordinal in range(1, 5)
        ]
        stream = stream_id("4" * 64, self.effect, self.authority, frontier, "epoch-suffix")
        for item in frontier:
            item["child_id"] = child_id(stream, item["ordinal"], item["swu_id"])
        projection = {
            "schema_version": "invoke.accepted-stream-finalized-projection.v1",
            "graph_digest": "4" * 64,
            "accepted_stream_id": stream,
            "requested_effect": self.effect,
            "authority": self.authority,
            "epoch": "epoch-suffix",
            "frontier_digest": bridge.canonical_digest(frontier),
            "acceptance_request_digest": "5" * 64,
            "units": [
                {"unit_id": item["swu_id"], "ordinal": item["ordinal"], "status": "pass", "result_digest": f"{item['ordinal']:064x}"}
                for item in frontier
            ],
        }
        baseline = {
            "schema_version": "invoke.accepted-stream-live-baseline.v1",
            "accepted_stream_id": stream,
            "epoch": "epoch-suffix",
            "frontier_digest": projection["frontier_digest"],
            "baseline_digest": "6" * 64,
            "status": "pass",
        }
        first = bridge.compile_request(REPO_ROOT, projection, None, baseline, frontier, no_effect=True)
        second = bridge.compile_request(REPO_ROOT, projection, None, baseline, frontier, no_effect=True)
        self.assertEqual(first, second)
        self.assertEqual(first["frontier"], [item["swu_id"] for item in frontier])
        receipt = load_driver().run(first)
        joined = bridge.join_receipt(REPO_ROOT, projection, baseline, first, [receipt])
        self.assertEqual(receipt["ordered_units"], first["frontier"])
        self.assertEqual(joined["joined_receipt_count"], 1)

    def test_effectful_mode_rejects_missing_acceptance(self) -> None:
        with self.assertRaisesRegex(ContractError, "requires an accepted response"):
            self.compile(response=None)

    def test_rehearsal_rejects_acceptance_consumption(self) -> None:
        with self.assertRaisesRegex(ContractError, "must not consume"):
            self.compile(no_effect=True, response=self.response)

    def test_rejects_authority_and_child_identity_drift(self) -> None:
        drift = copy.deepcopy(self.projection)
        drift["authority"]["control"] = ["../escape"]
        with self.assertRaises(ContractError):
            bridge.compile_request(
                REPO_ROOT, drift, self.response, self.baseline, self.frontier, no_effect=False
            )
        stale = copy.deepcopy(self.frontier)
        stale[0]["child_id"] = "f" * 64
        stale_projection = copy.deepcopy(self.projection)
        stale_projection["frontier_digest"] = bridge.canonical_digest(stale)
        stale_baseline = copy.deepcopy(self.baseline)
        stale_baseline["frontier_digest"] = stale_projection["frontier_digest"]
        with self.assertRaisesRegex(ContractError, "stale child identity"):
            bridge.compile_request(
                REPO_ROOT,
                stale_projection,
                self.response,
                stale_baseline,
                stale,
                no_effect=False,
            )

    def test_rejects_live_baseline_and_response_drift(self) -> None:
        baseline = copy.deepcopy(self.baseline)
        baseline["status"] = "block"
        with self.assertRaisesRegex(ContractError, "did not pass"):
            bridge.compile_request(
                REPO_ROOT,
                self.projection,
                self.response,
                baseline,
                self.frontier,
                no_effect=False,
            )
        response = copy.deepcopy(self.response)
        response["accepted_stream_id"] = "f" * 64
        with self.assertRaisesRegex(ContractError, "stream mismatch"):
            self.compile(response=response)

    def test_join_rejects_missing_duplicate_stale_cross_stream_and_fabricated(self) -> None:
        request = self.compile()
        receipt = load_driver().run(request)
        cases = [
            [],
            [receipt, copy.deepcopy(receipt)],
            [{**receipt, "ordered_units": receipt["ordered_units"][:-1]}],
            [{**receipt, "stream_id": "f" * 64}],
            [{**receipt, "event_digests": ["0" * 64] * 14}],
        ]
        for receipts in cases:
            with self.subTest(receipts=len(receipts)):
                with self.assertRaises(ContractError):
                    bridge.join_receipt(
                        REPO_ROOT,
                        self.projection,
                        self.baseline,
                        request,
                        receipts,
                    )

    def test_join_rejects_driver_identity_drift(self) -> None:
        request = self.compile()
        receipt = load_driver().run(request)
        identity = bridge.driver_identity(REPO_ROOT)
        identity["executable_ref"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ContractError, "driver identity"):
            bridge.join_receipt(
                REPO_ROOT,
                self.projection,
                self.baseline,
                request,
                [receipt],
                identity=identity,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
