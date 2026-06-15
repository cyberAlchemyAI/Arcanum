#!/usr/bin/env tsx

import { existsSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, relative, resolve } from "node:path";

import {
  loadConceptCatalog,
  normalizeTypeName,
  toRelative,
} from "./lib/code-tag-rules";
import type {
  ExtractedTag,
  ExtractionOutput,
  Mode,
} from "./lib/code-tag-types";

type DriftRow = {
  from: string;
  edge: string;
  to: string;
  source: string;
};

type TypeMismatchRow = {
  conceptId: string;
  codeType: string;
  docType: string;
  source: string;
};

type TableRow = {
  cells: string[];
  line: number;
};

type MarkdownTable = {
  headers: string[];
  rows: TableRow[];
};

const args = process.argv.slice(2);
const mode = (getArg("--mode") || "strict") as Mode;
const inputPath = resolve(
  process.cwd(),
  getArg("--input") || "code-tags.json",
);
const featuresRoot = resolve(
  process.cwd(),
  getArg("--features-root") || "docs/features",
);
const reportPath = resolve(
  process.cwd(),
  getArg("--report") || "governance/tags/CODE-TAG-DRIFT-REPORT.md",
);

if (!existsSync(inputPath)) {
  console.error(
    `compare-code-tag-drift: input not found: ${toRelative(inputPath)}`,
  );
  process.exit(1);
}

const extraction = readExtraction(inputPath);
const tags = extraction.tags;

const docsTriples = parseDocTriples(featuresRoot);
const docSet = new Set(
  docsTriples.map((row) => tripleKey(row.from, row.edge, row.to)),
);

const codeTriples = tags.flatMap((tag) =>
  tag.edges
    .filter((edge) => edge.edge && edge.to)
    .map((edge) => ({
      from: tag.concept.id,
      edge: edge.edge,
      to: edge.to,
      source: `${tag.file}:${tag.line}`,
    })),
);

const codeSet = new Set(
  codeTriples.map((row) => tripleKey(row.from, row.edge, row.to)),
);

const docsOnly = docsTriples.filter(
  (row) => !codeSet.has(tripleKey(row.from, row.edge, row.to)),
);

const codeOnly = codeTriples.filter(
  (row) => !docSet.has(tripleKey(row.from, row.edge, row.to)),
);

const directionMismatch = codeOnly.filter((row) =>
  docSet.has(tripleKey(row.to, row.edge, row.from)),
);

const conceptCatalog = loadConceptCatalog(featuresRoot);
const typeMismatch: TypeMismatchRow[] = [];

for (const tag of tags) {
  const id = (tag.concept.id || "").trim();
  const type = (tag.concept.type || "").trim();
  if (!id || !type) {
    continue;
  }

  const doc = conceptCatalog.get(id);
  if (!doc) {
    continue;
  }

  if (normalizeTypeName(type) !== normalizeTypeName(doc.type)) {
    typeMismatch.push({
      conceptId: id,
      codeType: type,
      docType: doc.type,
      source: `${tag.file}:${tag.line}`,
    });
  }
}

const report = buildReport({
  mode,
  input: toRelative(inputPath),
  featuresRoot: toRelative(featuresRoot),
  docsTripleCount: docsTriples.length,
  codeTripleCount: codeTriples.length,
  docsOnly,
  codeOnly,
  directionMismatch,
  typeMismatch,
});

writeFileSync(reportPath, report, "utf-8");

console.log(
  `compare-code-tag-drift: docsTriples=${docsTriples.length} codeTriples=${codeTriples.length} docsOnly=${docsOnly.length} codeOnly=${codeOnly.length} directionMismatch=${directionMismatch.length} typeMismatch=${typeMismatch.length} report=${toRelative(reportPath)}`,
);

const blocking =
  docsOnly.length > 0 ||
  codeOnly.length > 0 ||
  directionMismatch.length > 0 ||
  typeMismatch.length > 0;

if (mode === "strict" && blocking) {
  process.exit(1);
}

process.exit(0);

function readExtraction(pathToInput: string): ExtractionOutput {
  const raw = readFileSync(pathToInput, "utf-8");
  const parsed = JSON.parse(raw) as Partial<ExtractionOutput> | ExtractedTag[];

  if (Array.isArray(parsed)) {
    return {
      meta: {
        generatedAt: new Date().toISOString(),
        mode: "warn",
        include: [],
        root: process.cwd(),
      },
      tags: parsed,
      issues: [],
      stats: {
        scannedFiles: 0,
        taggedSymbols: parsed.length,
        issues: 0,
      },
    };
  }

  return {
    meta: parsed.meta || {
      generatedAt: new Date().toISOString(),
      mode: "warn",
      include: [],
      root: process.cwd(),
    },
    tags: parsed.tags || [],
    issues: parsed.issues || [],
    stats: parsed.stats || {
      scannedFiles: 0,
      taggedSymbols: (parsed.tags || []).length,
      issues: (parsed.issues || []).length,
    },
  };
}

function parseDocTriples(featuresRootPath: string): DriftRow[] {
  if (!existsSync(featuresRootPath)) {
    return [];
  }

  const specs = walk(featuresRootPath).filter((path) =>
    path.endsWith("/SPEC.md"),
  );
  const rows: DriftRow[] = [];

  for (const specPath of specs) {
    const raw = readFileSync(specPath, "utf-8");
    const lines = raw.split(/\r?\n/);
    const table = parseTableForSection(lines, "Feature Concept Graph");
    if (!table) {
      continue;
    }

    const headerMap = toHeaderMap(table.headers);
    const fromIndex = headerMap.get("from");
    const edgeIndex = headerMap.get("edge");
    const toIndex = headerMap.get("to");

    if (
      fromIndex === undefined ||
      edgeIndex === undefined ||
      toIndex === undefined
    ) {
      continue;
    }

    for (const row of table.rows) {
      const from = cleanCell(row.cells[fromIndex] || "");
      const edge = cleanCell(row.cells[edgeIndex] || "");
      const to = cleanCell(row.cells[toIndex] || "");

      if (!from || !edge || !to) {
        continue;
      }

      if (isPlaceholder(from) || isPlaceholder(edge) || isPlaceholder(to)) {
        continue;
      }

      rows.push({
        from,
        edge,
        to,
        source: `${toRelative(specPath)}:${row.line}`,
      });
    }
  }

  return rows;
}

function buildReport(input: {
  mode: Mode;
  input: string;
  featuresRoot: string;
  docsTripleCount: number;
  codeTripleCount: number;
  docsOnly: DriftRow[];
  codeOnly: DriftRow[];
  directionMismatch: DriftRow[];
  typeMismatch: TypeMismatchRow[];
}): string {
  const lines: string[] = [];

  lines.push("# CODE-TAG-DRIFT-REPORT");
  lines.push("");
  lines.push(`- Mode: ${input.mode}`);
  lines.push(`- Input: ${input.input}`);
  lines.push(`- Features root: ${input.featuresRoot}`);
  lines.push("");

  lines.push("## Summary");
  lines.push("");
  lines.push(`- Doc triples: ${input.docsTripleCount}`);
  lines.push(`- Code triples: ${input.codeTripleCount}`);
  lines.push(`- Docs only: ${input.docsOnly.length}`);
  lines.push(`- Code only: ${input.codeOnly.length}`);
  lines.push(`- Direction mismatch: ${input.directionMismatch.length}`);
  lines.push(`- Type mismatch: ${input.typeMismatch.length}`);
  lines.push("");

  lines.push("## Docs Only (missing in code tags)");
  lines.push("");
  lines.push("| From | Edge | To | Source |");
  lines.push("| ---- | ---- | -- | ------ |");
  for (const row of input.docsOnly.slice(0, 200)) {
    lines.push(`| ${row.from} | ${row.edge} | ${row.to} | ${row.source} |`);
  }
  lines.push("");

  lines.push("## Code Only (missing in docs)");
  lines.push("");
  lines.push("| From | Edge | To | Source |");
  lines.push("| ---- | ---- | -- | ------ |");
  for (const row of input.codeOnly.slice(0, 200)) {
    lines.push(`| ${row.from} | ${row.edge} | ${row.to} | ${row.source} |`);
  }
  lines.push("");

  lines.push("## Direction Mismatch");
  lines.push("");
  lines.push("| From | Edge | To | Source |");
  lines.push("| ---- | ---- | -- | ------ |");
  for (const row of input.directionMismatch.slice(0, 200)) {
    lines.push(`| ${row.from} | ${row.edge} | ${row.to} | ${row.source} |`);
  }
  lines.push("");

  lines.push("## Type Mismatch");
  lines.push("");
  lines.push("| Concept ID | Code Type | Doc Type | Source |");
  lines.push("| ---------- | --------- | -------- | ------ |");
  for (const row of input.typeMismatch.slice(0, 200)) {
    lines.push(
      `| ${row.conceptId} | ${row.codeType} | ${row.docType} | ${row.source} |`,
    );
  }
  lines.push("");

  return lines.join("\n") + "\n";
}

function parseTableForSection(
  lines: string[],
  sectionName: string,
): MarkdownTable | null {
  const sectionRanges = findSectionRanges(lines);
  const section = sectionRanges.find(
    (entry) =>
      normalizeSectionName(entry.name) === normalizeSectionName(sectionName),
  );

  if (!section) {
    return null;
  }

  let start = section.start;
  while (start < section.end && !(lines[start] || "").trim().startsWith("|")) {
    start += 1;
  }

  if (start >= section.end) {
    return null;
  }

  const headerLine = lines[start] || "";
  const separatorLine = lines[start + 1] || "";
  if (!separatorLine.trim().startsWith("|")) {
    return null;
  }

  const headers = parseTableRow(headerLine);
  const separatorCells = parseTableRow(separatorLine);
  if (
    headers.length === 0 ||
    separatorCells.length === 0 ||
    !separatorCells.every(
      (cell) => /^:?-{3,}:?$/.test(cell) || cell.length === 0,
    )
  ) {
    return null;
  }

  const rows: TableRow[] = [];
  let rowIndex = start + 2;
  while (rowIndex < section.end) {
    const line = lines[rowIndex] || "";
    if (!line.trim().startsWith("|")) {
      break;
    }

    const cells = parseTableRow(line);
    if (!cells.every((cell) => /^:?-{3,}:?$/.test(cell) || cell.length === 0)) {
      rows.push({ cells, line: rowIndex + 1 });
    }

    rowIndex += 1;
  }

  return { headers, rows };
}

function findSectionRanges(
  lines: string[],
): Array<{ name: string; start: number; end: number }> {
  const headings: Array<{ name: string; line: number }> = [];

  for (let i = 0; i < lines.length; i += 1) {
    const line = (lines[i] || "").trim();
    const match = /^##+\s+(.+)$/.exec(line);
    if (!match?.[1]) {
      continue;
    }

    headings.push({
      name: match[1].trim(),
      line: i,
    });
  }

  const sections: Array<{ name: string; start: number; end: number }> = [];
  for (let i = 0; i < headings.length; i += 1) {
    const current = headings[i];
    if (!current) {
      continue;
    }

    const next = headings[i + 1];
    sections.push({
      name: current.name,
      start: current.line + 1,
      end: next ? next.line : lines.length,
    });
  }

  return sections;
}

function parseTableRow(line: string): string[] {
  const trimmed = line.trim();
  if (!trimmed.startsWith("|")) {
    return [];
  }

  const withoutEdges = trimmed.replace(/^\|/, "").replace(/\|$/, "");
  return withoutEdges.split("|").map((cell) => cell.trim());
}

function toHeaderMap(headers: string[]): Map<string, number> {
  const map = new Map<string, number>();
  headers.forEach((header, index) => {
    map.set(cleanCell(header).toLowerCase(), index);
  });
  return map;
}

function cleanCell(value: string): string {
  return value
    .replace(/\*\*/g, "")
    .replace(/`/g, "")
    .replace(/\[([^\]]+)\]\([^\)]+\)/g, "$1")
    .trim();
}

function normalizeSectionName(name: string): string {
  return name.trim().toLowerCase().replace(/\s+/g, " ");
}

function isPlaceholder(value: string): boolean {
  return value.includes("{") && value.includes("}");
}

function tripleKey(from: string, edge: string, to: string): string {
  return `${from}|${edge}|${to}`;
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
