import { readFile, readdir } from "node:fs/promises";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { canonicalJson, sha256Hex, sha256HexText } from "../src/canonical-json.mjs";

const root = dirname(dirname(fileURLToPath(import.meta.url)));

async function files(directory) {
  const output = [];
  for (const name of (await readdir(directory, {withFileTypes: true})).sort((a, b) => a.name.localeCompare(b.name))) {
    const path = join(directory, name.name);
    if (name.isDirectory()) output.push(...await files(path));
    else output.push(path);
  }
  return output;
}

export async function computeClosureDigest() {
  const roots = [join(root, "src"), join(root, "schemas")];
  const included = [];
  for (const directory of roots) for (const path of await files(directory)) {
    if (path.endsWith("/src/version.mjs")) continue;
    const bytes = await readFile(path);
    included.push({path: relative(root, path).replaceAll("\\", "/"), sha256: sha256Hex(bytes), size_bytes: bytes.length});
  }
  const entry = join(root, "scripts/invoke-json-port.mjs");
  const bytes = await readFile(entry);
  included.push({path: "scripts/invoke-json-port.mjs", sha256: sha256Hex(bytes), size_bytes: bytes.length});
  return sha256HexText(canonicalJson(included.sort((a, b) => a.path.localeCompare(b.path))));
}

if (process.argv[1] === fileURLToPath(import.meta.url)) process.stdout.write(`${await computeClosureDigest()}\n`);
