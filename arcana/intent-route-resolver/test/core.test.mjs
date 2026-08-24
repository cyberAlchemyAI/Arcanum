import test from "node:test";
import assert from "node:assert/strict";
import { canonicalJson, digestJson, sha256HexText } from "../src/canonical-json.mjs";
import { resolveIntentRoute, verifyDispositionDigest } from "../src/resolve.mjs";
import { makeCatalog, makeRequest } from "./fixture-factory.mjs";

test("P01 core tests", () => {
  assert.equal(sha256HexText("abc"), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
  for (const kind of ["candidate", "ambiguous", "no-match", "invalid"]) {
    const catalog = makeCatalog();
    assert.equal(resolveIntentRoute(makeRequest(kind, catalog), catalog).kind, kind);
  }
});

test("P02 candidate values contain no ambient authority", () => {
  const catalog = makeCatalog();
  const result = resolveIntentRoute(makeRequest("candidate", catalog), catalog);
  assert.equal(result.authority_effect, "none");
  assert.equal(result.candidate_route_id, "route.special");
  assert.equal(result.evaluated_routes.length, 3);
});

test("P03 catalog order is canonical", () => {
  const left = makeCatalog(["route.general", "route.image", "route.special"]);
  const right = makeCatalog(["route.special", "route.general", "route.image"]);
  assert.equal(left.content_digest, right.content_digest);
  assert.equal(canonicalJson(resolveIntentRoute(makeRequest("candidate", left), left)), canonicalJson(resolveIntentRoute(makeRequest("candidate", right), right)));
});

test("P04 zero-authority response integrity", () => {
  const catalog = makeCatalog();
  const result = resolveIntentRoute(makeRequest("candidate", catalog), catalog);
  assert.equal(verifyDispositionDigest(result), true);
  assert.equal(result.authority_effect, "none");
});

test("P05 explicit dominance only", () => {
  const catalog = makeCatalog();
  const result = resolveIntentRoute(makeRequest("candidate", catalog), catalog);
  assert.equal(result.evaluated_routes.find((item) => item.route_id === "route.general").eligibility, "dominated");
});

test("P06 unresolved information stays visible", () => {
  const catalog = makeCatalog();
  const result = resolveIntentRoute(makeRequest("ambiguous", catalog), catalog);
  assert.equal(result.kind, "ambiguous");
  assert.equal(result.clarification.discriminator, "audience");
});

test("P07 canonical digest is stable", () => {
  assert.equal(digestJson({b: 2, a: 1}), digestJson({a: 1, b: 2}));
});

test("P08 evidence removal cannot improve disposition", () => {
  const catalog = makeCatalog();
  const complete = makeRequest("candidate", catalog);
  const reduced = structuredClone(complete); delete reduced.intent.discriminators.audience;
  assert.equal(resolveIntentRoute(complete, catalog).kind, "candidate");
  assert.equal(resolveIntentRoute(reduced, catalog).kind, "ambiguous");
});
