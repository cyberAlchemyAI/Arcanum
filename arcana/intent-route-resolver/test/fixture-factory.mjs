import { sealCatalog } from "../src/catalog.mjs";
import {
  CAPABILITY_TOKEN, CLOSURE_DIGEST, CORE_VERSION, MANIFEST_VERSION,
  REQUEST_PROTOCOL, RUNTIME_PORT_REQUEST_PROTOCOL
} from "../src/version.mjs";

const SOURCE_DIGEST = "1".repeat(64);
const EVIDENCE_DIGEST = "2".repeat(64);

export function makeCatalog(order = ["route.general", "route.image", "route.special"]) {
  const definitions = {
    "route.general": {route_id: "route.general", label: "General text route", required: {medium: "text"}, excluded: {}, capabilities: ["compose"], dominates: []},
    "route.image": {route_id: "route.image", label: "Image route", required: {medium: "image"}, excluded: {}, capabilities: ["render"], dominates: []},
    "route.special": {route_id: "route.special", label: "Expert text route", required: {audience: "expert", medium: "text"}, excluded: {}, capabilities: ["compose"], dominates: ["route.general"]}
  };
  return sealCatalog({
    schema: "intent-route.catalog@1",
    catalog_id: "synthetic-routes-v1",
    content_digest: "0".repeat(64),
    derived_from: {owner: "synthetic-fixture-owner", revision: "1", content_digest: SOURCE_DIGEST},
    routes: order.map((id) => definitions[id])
  });
}

export function makeRequest(kind = "candidate", catalog = makeCatalog()) {
  const discriminators = {
    candidate: {medium: {posture: "declared", value: "text"}, audience: {posture: "declared", value: "expert"}},
    ambiguous: {medium: {posture: "declared", value: "text"}, audience: {posture: "unresolved", value: null}},
    "no-match": {medium: {posture: "declared", value: "audio"}, audience: {posture: "declared", value: "general"}},
    invalid: {medium: {posture: "declared", value: "text"}}
  }[kind];
  return {
    schema: REQUEST_PROTOCOL,
    request_id: `fixture-${kind}`,
    intent: {text: kind === "invalid" ? "" : `Resolve ${kind} fixture`, discriminators},
    support_evidence_refs: [{artifact_ref: "fixture://support/1", content_digest: EVIDENCE_DIGEST}],
    constraints: {required_capabilities: [], forbidden_route_ids: []},
    catalog_id: catalog.catalog_id,
    catalog_digest: catalog.content_digest,
    supersedes_request_id: null
  };
}

export function makeEnvelope(kind = "candidate", catalog = makeCatalog()) {
  return {
    schema: RUNTIME_PORT_REQUEST_PROTOCOL,
    request: makeRequest(kind, catalog),
    catalog,
    expected_core_version: CORE_VERSION,
    expected_manifest_version: MANIFEST_VERSION,
    expected_closure_digest: CLOSURE_DIGEST,
    capability_token: CAPABILITY_TOKEN
  };
}
