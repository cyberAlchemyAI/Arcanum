import { canonicalJson } from "../../src/canonical-json.mjs";
import { resolveIntentRoute } from "../../src/resolve.mjs";
import { CLOSURE_DIGEST, CORE_VERSION, MANIFEST_VERSION } from "../../src/version.mjs";
import { makeCatalog, makeRequest } from "../fixture-factory.mjs";

const cases = [];
for (const kind of ["candidate", "ambiguous", "no-match", "invalid"]) {
  const catalog = makeCatalog();
  const observed = resolveIntentRoute(makeRequest(kind, catalog), catalog).kind;
  cases.push({case_id: `BROWSER-${kind.toUpperCase()}`, expected: kind, observed, status: observed === kind ? "pass" : "fail"});
}
const leftCatalog = makeCatalog(["route.general", "route.image", "route.special"]);
const rightCatalog = makeCatalog(["route.special", "route.general", "route.image"]);
const permutationPass = canonicalJson(resolveIntentRoute(makeRequest("candidate", leftCatalog), leftCatalog)) === canonicalJson(resolveIntentRoute(makeRequest("candidate", rightCatalog), rightCatalog));
cases.push({case_id: "BROWSER-PERMUTATION", expected: true, observed: permutationPass, status: permutationPass ? "pass" : "fail"});
const uncertainCatalog = makeCatalog();
const complete = makeRequest("candidate", uncertainCatalog);
const reduced = structuredClone(complete); delete reduced.intent.discriminators.audience;
const monotone = resolveIntentRoute(complete, uncertainCatalog).kind === "candidate" && resolveIntentRoute(reduced, uncertainCatalog).kind === "ambiguous";
cases.push({case_id: "BROWSER-UNCERTAINTY", expected: true, observed: monotone, status: monotone ? "pass" : "fail"});

const result = {
  schema: "intent-route.browser-page-result@1",
  status: cases.every((item) => item.status === "pass") ? "pass" : "fail",
  core_version: CORE_VERSION,
  manifest_version: MANIFEST_VERSION,
  closure_digest: CLOSURE_DIGEST,
  case_count: cases.length,
  passed: cases.filter((item) => item.status === "pass").length,
  cases,
  authority_effect: "none"
};
window.__intentRouteWitness = result;
document.querySelector("#status").textContent = `${result.status.toUpperCase()} — ${result.passed}/${result.case_count} deterministic cases`;
document.querySelector("#status").dataset.status = result.status;
document.querySelector("#result").textContent = JSON.stringify(result, null, 2);
