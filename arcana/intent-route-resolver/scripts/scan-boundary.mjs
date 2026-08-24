#!/usr/bin/env node
import { readFile, readdir, stat } from "node:fs/promises";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const forbiddenTerms = [
  "cyber" + "alchemy-v2",
  "agent-" + "reasoning-engine",
  "workspace-" + "resonant",
  "domainspec-" + "core"
];
const executableSuffixes = new Set([".mjs", ".js", ".cjs"]);
const hostPrefix = "/" + "home" + "/";
const forbiddenModule = "node:" + "child_process";
const effectCallPattern = new RegExp(
  `\\b(?:${[
    "sp" + "awn",
    "ex" + "ec",
    "exec" + "File",
    "fe" + "tch",
    "write" + "File",
    "append" + "File"
  ].join("|")})\\s*\\(`
);

async function files(directory) {
  const output = [];
  for (const name of (await readdir(directory)).sort()) {
    const absolute = join(directory, name);
    const info = await stat(absolute);
    if (info.isDirectory()) output.push(...await files(absolute));
    else output.push(absolute);
  }
  return output;
}

const violations = [];
for (const absolute of await files(root)) {
  const path = relative(root, absolute).replaceAll("\\", "/");
  const bytes = await readFile(absolute);
  const text = bytes.toString("utf8");
  const lower = text.toLowerCase();
  for (const term of forbiddenTerms) {
    if (lower.includes(term)) violations.push(`${path}: forbidden identifier`);
  }
  if (text.includes(hostPrefix) || text.includes("file" + "://")) violations.push(`${path}: host-specific path`);
  if (!text.endsWith("\n")) violations.push(`${path}: missing final newline`);
  if (text.split("\n").some((line) => /[ \t]+$/.test(line))) violations.push(`${path}: trailing whitespace`);

  const suffix = path.slice(path.lastIndexOf("."));
  if (!executableSuffixes.has(suffix)) continue;
  const semanticSource = path.startsWith("src/") || path === "scripts/invoke-json-port.mjs";
  if (semanticSource && (text.includes(forbiddenModule) || effectCallPattern.test(text))) {
    violations.push(`${path}: ambient effect API`);
  }
  for (const match of text.matchAll(/(?:from\s+|import\s*\()\s*["']([^"']+)["']/g)) {
    const specifier = match[1];
    if (specifier.startsWith("node:")) continue;
    if (!specifier.startsWith("./") && !specifier.startsWith("../")) {
      violations.push(`${path}: external package import`);
      continue;
    }
    const resolved = resolve(dirname(absolute), specifier);
    if (!resolved.startsWith(`${resolve(root)}/`)) violations.push(`${path}: import escapes package root`);
  }
}

if (violations.length > 0) {
  process.stdout.write(`${JSON.stringify({schema: "intent-route.public-boundary-scan@1", status: "fail", violations})}\n`);
  process.exitCode = 1;
} else {
  process.stdout.write(`${JSON.stringify({schema: "intent-route.public-boundary-scan@1", status: "pass", scanned_files: (await files(root)).length, authority_effect: "none"})}\n`);
}
