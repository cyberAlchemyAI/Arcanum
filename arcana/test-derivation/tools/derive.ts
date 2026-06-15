#!/usr/bin/env tsx
/**
 * Test Derivation engine — L0 (built fresh in arcanum per decision B3).
 * No LLM, no network: deterministic by construction.
 *
 * L0 scope: the state-transition rule. Each transition-table row in a DomainSpec
 * `states.md` yields one existence-test obligation, content-addressed for reproducibility.
 * Round-trip oracle: engine-derived set must be a superset of a committed set.
 *
 * Usage:
 *   tsx derive.ts --states <states.md> [--out <TEST-SPEC.md>] [--check <committed TEST-SPEC.md>]
 */
import { readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";

type Obligation = { key: string; rule: string; from: string; event: string; to: string; anchor: string };

function arg(name: string): string | undefined {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : undefined;
}

// Parse a markdown transition table with From | Event | To columns (order-insensitive by header).
function parseTransitions(md: string, anchor: string): Obligation[] {
  const lines = md.split(/\r?\n/);
  const out: Obligation[] = [];
  let header: string[] | null = null;
  for (const line of lines) {
    if (!line.trim().startsWith("|")) { header = null; continue; }
    const cells = line.split("|").map((c) => c.trim()).filter((c, i, a) => !(i === 0 && c === "") && !(i === a.length - 1 && c === ""));
    if (cells.every((c) => /^:?-+:?$/.test(c))) continue; // separator row
    if (!header) { header = cells.map((c) => c.toLowerCase()); continue; }
    const idx = (n: string) => header!.findIndex((h) => h.includes(n));
    const fi = idx("from"), ei = idx("event"), ti = idx("to");
    if (fi < 0 || ei < 0 || ti < 0) { continue; }
    const from = cells[fi], event = cells[ei], to = cells[ti];
    if (!from || !event || !to) continue;
    const params = `${from}|${event}|${to}`;
    const key = createHash("sha1").update(`${anchor}|state-transition-existence|${params}`).digest("hex").slice(0, 12);
    out.push({ key, rule: "state-transition-existence", from, event, to, anchor });
  }
  // deterministic order: by key
  return out.sort((a, b) => a.key.localeCompare(b.key));
}

function renderSpec(obs: Obligation[]): string {
  const rows = obs.map((o) => `| \`${o.key}\` | ${o.rule} | ${o.from} --${o.event}--> ${o.to} | should transition \`${o.from}\` to \`${o.to}\` on \`${o.event}\` |`).join("\n");
  return `# TEST-SPEC (derived)\n\n> Deterministically derived by test-derivation L0. Do not hand-edit; re-derive.\n\n| Obligation | Rule | Transition | Assertion |\n| --- | --- | --- | --- |\n${rows}\n`;
}

function keysOf(spec: string): Set<string> {
  const s = new Set<string>();
  for (const m of spec.matchAll(/\|\s*`([0-9a-f]{12})`\s*\|/g)) s.add(m[1]);
  return s;
}

const statesPath = arg("--states");
if (!statesPath) { console.error("--states required"); process.exit(2); }
const anchor = `${statesPath}#transition-table`;
const obs = parseTransitions(readFileSync(statesPath, "utf8"), anchor);
const spec = renderSpec(obs);

const outPath = arg("--out");
if (outPath) writeFileSync(outPath, spec);

const checkPath = arg("--check");
if (checkPath) {
  const committed = keysOf(readFileSync(checkPath, "utf8"));
  const derived = keysOf(spec);
  const missing = [...committed].filter((k) => !derived.has(k));
  const verdict = missing.length === 0 ? "PASS" : "FAIL";
  console.log(`round-trip: derived=${derived.size} committed=${committed.size} missing=${missing.length} verdict=${verdict}`);
  process.exit(verdict === "PASS" ? 0 : 1);
}

console.log(`test-derivation L0: obligations=${obs.length}${outPath ? ` out=${outPath}` : ""}`);
