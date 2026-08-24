import { canonicalizeJson, deepFreeze, digestJson } from "./canonical-json.mjs";
import { CATALOG_PROTOCOL } from "./version.mjs";

export class CatalogAdmissionError extends Error {
  constructor(message) {
    super(message);
    this.name = "CatalogAdmissionError";
    this.reasonCode = "IR_INVALID_CATALOG";
  }
}

function fail(message) {
  throw new CatalogAdmissionError(message);
}

function normalize(raw, { verifyDigest }) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("catalog must be an object");
  if (Object.keys(raw).sort().join(",") !== "catalog_id,content_digest,derived_from,routes,schema") fail("catalog shape is closed");
  if (raw.schema !== CATALOG_PROTOCOL) fail("unsupported catalog protocol");
  if (typeof raw.catalog_id !== "string" || raw.catalog_id.length === 0) fail("catalog_id must be nonempty");
  if (!/^[0-9a-f]{64}$/.test(raw.content_digest ?? "")) fail("catalog content_digest must be lowercase SHA-256");
  if (!raw.derived_from || typeof raw.derived_from !== "object" || Array.isArray(raw.derived_from) || Object.keys(raw.derived_from).sort().join(",") !== "content_digest,owner,revision") fail("derived_from shape is closed");
  for (const key of ["owner", "revision"]) if (typeof raw.derived_from[key] !== "string" || raw.derived_from[key].length === 0) fail(`derived_from.${key} must be nonempty`);
  if (!/^[0-9a-f]{64}$/.test(raw.derived_from.content_digest ?? "")) fail("derived_from digest must be lowercase SHA-256");
  if (!Array.isArray(raw.routes) || raw.routes.length === 0) fail("catalog routes must be nonempty");
  const routeIds = new Set();
  const routes = raw.routes.map((route) => {
    if (!route || typeof route !== "object" || Array.isArray(route) || Object.keys(route).sort().join(",") !== "capabilities,dominates,excluded,label,required,route_id") fail("route shape is closed");
    if (typeof route.route_id !== "string" || route.route_id.length === 0 || routeIds.has(route.route_id)) fail("route_id must be nonempty and unique");
    routeIds.add(route.route_id);
    if (typeof route.label !== "string" || route.label.length === 0) fail("route label must be nonempty");
    for (const key of ["required", "excluded"]) if (!route[key] || typeof route[key] !== "object" || Array.isArray(route[key])) fail(`${key} predicates must be an object`);
    for (const key of ["capabilities", "dominates"]) if (!Array.isArray(route[key]) || route[key].some((item) => typeof item !== "string" || item.length === 0) || new Set(route[key]).size !== route[key].length) fail(`${key} must be a unique string array`);
    return {...route, required: canonicalizeJson(route.required), excluded: canonicalizeJson(route.excluded), capabilities: [...route.capabilities].sort(), dominates: [...route.dominates].sort()};
  }).sort((left, right) => left.route_id.localeCompare(right.route_id));
  for (const route of routes) for (const target of route.dominates) if (!routeIds.has(target) || target === route.route_id) fail("dominance target must name another route");
  const byId = new Map(routes.map((route) => [route.route_id, route]));
  const visiting = new Set(); const visited = new Set();
  function visit(id) {
    if (visiting.has(id)) fail("dominance graph must be acyclic");
    if (visited.has(id)) return;
    visiting.add(id);
    for (const target of byId.get(id).dominates) visit(target);
    visiting.delete(id); visited.add(id);
  }
  for (const id of routeIds) visit(id);
  const normalized = canonicalizeJson({...raw, routes});
  if (verifyDigest && computeCatalogDigest(normalized) !== normalized.content_digest) fail("catalog content digest mismatch");
  return normalized;
}

export function computeCatalogDigest(catalog) {
  const payload = canonicalizeJson(catalog);
  delete payload.content_digest;
  return digestJson(payload);
}

export function sealCatalog(catalog) {
  const provisional = normalize({...catalog, content_digest: "0".repeat(64)}, {verifyDigest: false});
  provisional.content_digest = computeCatalogDigest(provisional);
  return deepFreeze(canonicalizeJson(provisional));
}

export function admitRouteCatalog(catalog) {
  return deepFreeze(normalize(catalog, {verifyDigest: true}));
}
