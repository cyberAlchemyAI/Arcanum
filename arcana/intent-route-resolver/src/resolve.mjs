import { canonicalizeJson, deepFreeze, digestJson } from "./canonical-json.mjs";
import { admitRouteRequest, RequestAdmissionError } from "./request.mjs";
import { admitRouteCatalog, CatalogAdmissionError } from "./catalog.mjs";
import { DISPOSITION_PROTOCOL } from "./version.mjs";

function scalarEqual(left, right) {
  return typeof left === typeof right && left === right;
}

function evaluateRoute(request, route) {
  const reasons = [];
  const unresolved = new Set();
  if (request.constraints.forbidden_route_ids.includes(route.route_id)) reasons.push("IR_ROUTE_FORBIDDEN");
  for (const capability of request.constraints.required_capabilities) if (!route.capabilities.includes(capability)) reasons.push("IR_CAPABILITY_MISSING");
  for (const [key, excluded] of Object.entries(route.excluded).sort(([a], [b]) => a.localeCompare(b))) {
    const actual = request.intent.discriminators[key];
    if (!actual || actual.posture === "unresolved") unresolved.add(key);
    else if (scalarEqual(actual.value, excluded)) reasons.push("IR_EXCLUDED");
  }
  for (const [key, required] of Object.entries(route.required).sort(([a], [b]) => a.localeCompare(b))) {
    const actual = request.intent.discriminators[key];
    if (!actual || actual.posture === "unresolved") unresolved.add(key);
    else if (!scalarEqual(actual.value, required)) reasons.push("IR_REQUIRED_MISMATCH");
  }
  const eligibility = reasons.length > 0 ? "ineligible" : unresolved.size > 0 ? "unresolved" : "eligible";
  if (eligibility === "eligible") reasons.push("IR_ELIGIBLE");
  if (eligibility === "unresolved") reasons.push("IR_MISSING_DISCRIMINATOR");
  return {route_id: route.route_id, eligibility, reason_codes: [...new Set(reasons)].sort(), unresolved_discriminators: [...unresolved].sort()};
}

function disposition({requestId, catalogId, catalogDigest, kind, reasonCode, traces, candidateRouteId = null, clarification = null}) {
  const value = {
    schema: DISPOSITION_PROTOCOL,
    request_id: requestId,
    catalog_id: catalogId,
    catalog_digest: catalogDigest,
    kind,
    reason_code: reasonCode,
    evaluated_routes: traces,
    candidate_route_id: candidateRouteId,
    clarification,
    authority_effect: "none"
  };
  return deepFreeze(canonicalizeJson({...value, integrity_digest: digestJson(value)}));
}

function invalid(rawRequest, rawCatalog, reasonCode) {
  const digest = /^[0-9a-f]{64}$/.test(rawCatalog?.content_digest ?? "") ? rawCatalog.content_digest : "0".repeat(64);
  return disposition({requestId: typeof rawRequest?.request_id === "string" && rawRequest.request_id ? rawRequest.request_id : "invalid-request", catalogId: typeof rawCatalog?.catalog_id === "string" && rawCatalog.catalog_id ? rawCatalog.catalog_id : "invalid-catalog", catalogDigest: digest, kind: "invalid", reasonCode, traces: []});
}

export function verifyDispositionDigest(value) {
  const copy = canonicalizeJson(value);
  const supplied = copy.integrity_digest;
  delete copy.integrity_digest;
  return supplied === digestJson(copy);
}

export function resolveIntentRoute(rawRequest, rawCatalog) {
  let request; let catalog;
  try { request = admitRouteRequest(rawRequest); } catch (error) {
    if (error instanceof RequestAdmissionError) return invalid(rawRequest, rawCatalog, "IR_INVALID_REQUEST");
    throw error;
  }
  try { catalog = admitRouteCatalog(rawCatalog); } catch (error) {
    if (error instanceof CatalogAdmissionError) return invalid(rawRequest, rawCatalog, "IR_INVALID_CATALOG");
    throw error;
  }
  if (request.catalog_id !== catalog.catalog_id || request.catalog_digest !== catalog.content_digest) return invalid(request, catalog, "IR_INVALID_CATALOG");
  const traces = catalog.routes.map((route) => evaluateRoute(request, route));
  const eligible = new Set(traces.filter((trace) => trace.eligibility === "eligible").map((trace) => trace.route_id));
  const dominated = new Set();
  for (const route of catalog.routes) if (eligible.has(route.route_id)) for (const target of route.dominates) if (eligible.has(target)) dominated.add(target);
  for (const trace of traces) if (dominated.has(trace.route_id)) {
    trace.eligibility = "dominated";
    trace.reason_codes = ["IR_DOMINATED"];
  }
  const unresolved = traces.flatMap((trace) => trace.unresolved_discriminators);
  const nonDominated = traces.filter((trace) => trace.eligibility === "eligible");
  if (unresolved.length > 0 || nonDominated.length > 1) {
    const discriminator = [...new Set(unresolved)].sort()[0] ?? null;
    return disposition({requestId: request.request_id, catalogId: catalog.catalog_id, catalogDigest: catalog.content_digest, kind: "ambiguous", reasonCode: "IR_AMBIGUOUS", traces, clarification: discriminator ? {discriminator, prompt: `Provide a value for discriminator \"${discriminator}\".`} : null});
  }
  if (nonDominated.length === 1) return disposition({requestId: request.request_id, catalogId: catalog.catalog_id, catalogDigest: catalog.content_digest, kind: "candidate", reasonCode: "IR_CANDIDATE", traces, candidateRouteId: nonDominated[0].route_id});
  return disposition({requestId: request.request_id, catalogId: catalog.catalog_id, catalogDigest: catalog.content_digest, kind: "no-match", reasonCode: "IR_NO_MATCH", traces});
}
