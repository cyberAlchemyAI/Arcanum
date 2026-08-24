import test from "node:test";
import assert from "node:assert/strict";
import { canonicalJson } from "../src/canonical-json.mjs";
import { resolveIntentRoute } from "../src/resolve.mjs";
import { makeCatalog, makeRequest } from "./fixture-factory.mjs";

test("catalog permutations preserve response bytes", () => {
  const permutations = [
    ["route.general", "route.image", "route.special"],
    ["route.image", "route.special", "route.general"],
    ["route.special", "route.general", "route.image"]
  ];
  const bytes = permutations.map((order) => {
    const catalog = makeCatalog(order);
    return canonicalJson(resolveIntentRoute(makeRequest("candidate", catalog), catalog));
  });
  assert.equal(new Set(bytes).size, 1);
});

test("uncertainty is monotone under evidence removal", () => {
  const catalog = makeCatalog();
  const request = makeRequest("candidate", catalog);
  const candidate = resolveIntentRoute(request, catalog);
  request.intent.discriminators.audience = {posture: "unresolved", value: null};
  const ambiguous = resolveIntentRoute(request, catalog);
  assert.equal(candidate.kind, "candidate");
  assert.equal(ambiguous.kind, "ambiguous");
});
