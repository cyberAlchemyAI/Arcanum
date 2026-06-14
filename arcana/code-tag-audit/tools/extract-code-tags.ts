#!/usr/bin/env tsx

import { existsSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, relative, resolve } from "node:path";

import { extractJsTags } from "./lib/code-tag-adapters/js";
import { extractPyTags } from "./lib/code-tag-adapters/py";
import { extractTsTags } from "./lib/code-tag-adapters/ts";
import type {
  ExtractionOutput,
  Mode,
  SourceLanguage,
  TagIssue,
} from "./lib/code-tag-types";

const args = process.argv.slice(2);
const mode = (getArg("--mode") || "warn") as Mode;
const outputPath = resolve(
  process.cwd(),
  getArg("--output") || "code-tags.json",
);
const includeArg = getArg("--include");
const jsonOnly = hasFlag("--json");

const include = (
  includeArg
    ? includeArg.split(",").map((value) => value.trim())
    : ["backend/src", "apps/web/src"]
).filter(Boolean);

const includeAbs = include
  .map((path) => resolve(process.cwd(), path))
  .filter((path) => existsSync(path));

const files = includeAbs
  .flatMap((dir) => walk(dir))
  .filter((filePath) => isSupportedExtension(filePath));

const tags: ExtractionOutput["tags"] = [];
const issues: TagIssue[] = [];

for (const filePath of files) {
  const raw = readFileSync(filePath, "utf-8");
  const relativePath = toRelative(filePath);
  const ext = extensionOf(filePath);

  const result = extractByLanguage(raw, relativePath, ext);
  tags.push(...result.tags);
  issues.push(...result.issues);
}

tags.sort((left, right) => {
  if (left.file !== right.file) {
    return left.file.localeCompare(right.file);
  }
  if (left.symbol !== right.symbol) {
    return left.symbol.localeCompare(right.symbol);
  }
  return left.line - right.line;
});

const payload: ExtractionOutput = {
  meta: {
    generatedAt: new Date().toISOString(),
    mode,
    include,
    root: process.cwd(),
  },
  tags,
  issues,
  stats: {
    scannedFiles: files.length,
    taggedSymbols: tags.length,
    issues: issues.length,
  },
};

writeFileSync(outputPath, JSON.stringify(payload, null, 2) + "\n", "utf-8");

if (jsonOnly) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  console.log(
    `extract-code-tags: files=${files.length} taggedSymbols=${tags.length} issues=${issues.length} output=${toRelative(outputPath)}`,
  );

  for (const issue of issues) {
    console.log(
      `[code-tag-extract:${mode}] ${issue.file}:${issue.line} | severity=${issue.severity} | code=${issue.code} | ${issue.message}`,
    );
  }
}

const blocking = issues.some((issue) => issue.severity === "CRITICAL");
if (mode === "strict" && blocking) {
  process.exit(1);
}

process.exit(0);

function extractByLanguage(
  raw: string,
  file: string,
  language: SourceLanguage,
): { tags: ExtractionOutput["tags"]; issues: TagIssue[] } {
  if (language === "ts" || language === "tsx") {
    return extractTsTags(raw, file, language);
  }

  if (language === "js" || language === "jsx") {
    return extractJsTags(raw, file, language);
  }

  if (language === "py") {
    return extractPyTags(raw, file);
  }

  return { tags: [], issues: [] };
}

function extensionOf(filePath: string): SourceLanguage {
  if (filePath.endsWith(".tsx")) return "tsx";
  if (filePath.endsWith(".ts")) return "ts";
  if (filePath.endsWith(".jsx")) return "jsx";
  if (filePath.endsWith(".js")) return "js";
  return "py";
}

function isSupportedExtension(filePath: string): boolean {
  return (
    filePath.endsWith(".ts") ||
    filePath.endsWith(".tsx") ||
    filePath.endsWith(".js") ||
    filePath.endsWith(".jsx") ||
    filePath.endsWith(".py")
  );
}

function walk(root: string): string[] {
  const out: string[] = [];
  for (const entry of readdirSync(root, { withFileTypes: true })) {
    const fullPath = join(root, entry.name);
    if (entry.isDirectory()) {
      out.push(...walk(fullPath));
    } else if (entry.isFile()) {
      out.push(fullPath);
    }
  }
  return out;
}

function getArg(name: string): string | undefined {
  const index = args.indexOf(name);
  if (index < 0) {
    return undefined;
  }
  return args[index + 1];
}

function hasFlag(name: string): boolean {
  return args.includes(name);
}

function toRelative(absPath: string): string {
  return relative(process.cwd(), absPath).replace(/\\/g, "/");
}
