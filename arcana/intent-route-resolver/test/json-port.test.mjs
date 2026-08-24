import test from "node:test";
import assert from "node:assert/strict";
import { resolveJson, resolveJsonValue } from "../src/json-port.mjs";
import { makeCatalog, makeEnvelope } from "./fixture-factory.mjs";

function parsed(result) {
  assert.equal(result.stderr, "");
  assert.equal(result.stdout.split("\n").filter(Boolean).length, 1);
  return JSON.parse(result.stdout);
}

const cases = [
  ["J01", "candidate", 0, "intent-route.runtime-port@1", "IR_CANDIDATE"],
  ["J02", "ambiguous", 0, "intent-route.runtime-port@1", "IR_AMBIGUOUS"],
  ["J03", "no-match", 0, "intent-route.runtime-port@1", "IR_NO_MATCH"],
  ["J04", "invalid", 0, "intent-route.runtime-port@1", "IR_INVALID_REQUEST"]
];

for (const [id, kind, exit, schema, reason] of cases) test(`${id} ${kind}`, () => {
  const envelope = makeEnvelope(kind);
  const first = resolveJsonValue(envelope);
  const second = resolveJsonValue(envelope);
  assert.equal(first.exit_code, exit);
  assert.equal(first.stdout, second.stdout);
  const value = parsed(first);
  assert.equal(value.schema, schema);
  assert.equal(value.disposition.kind, kind);
  assert.equal(value.disposition.reason_code, reason);
  assert.equal(value.authority_effect, "none");
});

test("J05 malformed JSON", () => {
  const result = resolveJson("{");
  assert.equal(result.exit_code, 2);
  assert.equal(parsed(result).reason_code, "IR_TRANSPORT_MALFORMED_JSON");
});

test("J06 malformed catalog", () => {
  const envelope = makeEnvelope("candidate");
  envelope.catalog = structuredClone(envelope.catalog);
  envelope.catalog.routes[0].dominates = ["missing-route"];
  const value = parsed(resolveJsonValue(envelope));
  assert.equal(value.disposition.kind, "invalid");
  assert.equal(value.disposition.reason_code, "IR_INVALID_CATALOG");
});

test("J07 capability denied", () => {
  const envelope = makeEnvelope(); delete envelope.capability_token;
  const result = resolveJsonValue(envelope);
  assert.equal(result.exit_code, 3); assert.equal(parsed(result).reason_code, "IR_CAPABILITY_DENIED");
});

test("J08 request version", () => {
  const envelope = makeEnvelope(); envelope.request.schema = "intent-route.request@2";
  const result = resolveJsonValue(envelope);
  assert.equal(result.exit_code, 4); assert.equal(parsed(result).reason_code, "IR_REQUEST_VERSION_UNSUPPORTED");
});

test("J09 port version", () => {
  const envelope = makeEnvelope(); envelope.schema = "intent-route.runtime-port.request@2";
  const result = resolveJsonValue(envelope);
  assert.equal(result.exit_code, 4); assert.equal(parsed(result).reason_code, "IR_PORT_VERSION_UNSUPPORTED");
});

test("J10 core version", () => {
  const envelope = makeEnvelope(); envelope.expected_core_version = "9.9.9";
  const result = resolveJsonValue(envelope);
  assert.equal(result.exit_code, 4); assert.equal(parsed(result).reason_code, "IR_CORE_VERSION_MISMATCH");
});

test("J11 manifest version", () => {
  const envelope = makeEnvelope(); envelope.expected_manifest_version = "9.9.9";
  const result = resolveJsonValue(envelope);
  assert.equal(result.exit_code, 4); assert.equal(parsed(result).reason_code, "IR_MANIFEST_VERSION_MISMATCH");
});

test("J12 catalog digest", () => {
  const envelope = makeEnvelope(); envelope.request.catalog_digest = "f".repeat(64);
  const result = resolveJsonValue(envelope);
  assert.equal(result.exit_code, 5); assert.equal(parsed(result).reason_code, "IR_CATALOG_DIGEST_MISMATCH");
});

test("J13 closure digest", () => {
  const envelope = makeEnvelope(); envelope.expected_closure_digest = "f".repeat(64);
  const result = resolveJsonValue(envelope);
  assert.equal(result.exit_code, 5); assert.equal(parsed(result).reason_code, "IR_CONTENT_DIGEST_MISMATCH");
});
