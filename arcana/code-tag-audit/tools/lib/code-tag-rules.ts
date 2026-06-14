import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join, relative, resolve } from "node:path";

import type { CanonicalEdgeRule, ConceptCatalogEntry } from "./code-tag-types";

type TableRow = {
  cells: string[];
  line: number;
};

type MarkdownTable = {
  headers: string[];
  rows: TableRow[];
};

export function normalizeTypeName(input: string): string {
  return input
    .trim()
    .toLowerCase()
    .replace(/\[[^\]]*\]/g, "")
    .replace(/[^a-z0-9]+/g, "");
}

export function parseTaxonomyTypes(taxonomyPath: string): Map<string, string> {
  if (!existsSync(taxonomyPath)) {
    return new Map();
  }

  const raw = readFileSync(taxonomyPath, "utf-8");
  const lines = raw.split(/\r?\n/);
  const types = new Map<string, string>();

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed.startsWith("|")) {
      continue;
    }

    const cells = parseTableRow(trimmed);
    if (cells.length < 2) {
      continue;
    }

    const candidate = cleanCell(cells[1] || "");
    const normalizedCandidate = normalizeTypeName(candidate);
    if (!candidate || !normalizedCandidate) {
      continue;
    }

    if (
      normalizedCandidate === "metaconcept" ||
      normalizedCandidate === "purpose" ||
      normalizedCandidate === "backendcounterpart" ||
      normalizedCandidate === "category"
    ) {
      continue;
    }

    if (!types.has(normalizedCandidate)) {
      types.set(normalizedCandidate, candidate);
    }
  }

  return types;
}

export function parseRelationshipRules(
  relationshipsPath: string,
): Map<string, CanonicalEdgeRule> {
  if (!existsSync(relationshipsPath)) {
    return new Map();
  }

  const raw = readFileSync(relationshipsPath, "utf-8");
  const lines = raw.split(/\r?\n/);
  const rules = new Map<string, CanonicalEdgeRule>();

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed.startsWith("| `")) {
      continue;
    }

    const cells = parseTableRow(trimmed);
    if (cells.length < 2) {
      continue;
    }

    const edge = cleanCell(cells[0] || "").replace(/`/g, "");
    const relation = cleanCell(cells[1] || "");
    if (!edge || !relation.includes("→")) {
      continue;
    }

    const [fromRaw, toRaw] = relation.split("→").map((v) => v.trim());
    if (!fromRaw || !toRaw) {
      continue;
    }

    const fromTypes = parseTypeSide(fromRaw);
    const toTypes = parseTypeSide(toRaw);

    if (fromTypes.size === 0 || toTypes.size === 0) {
      continue;
    }

    rules.set(edge, {
      edge,
      fromRaw,
      toRaw,
      fromTypes,
      toTypes,
    });
  }

  return rules;
}

export function loadConceptCatalog(
  featuresRoot: string,
): Map<string, ConceptCatalogEntry> {
  const catalog = new Map<string, ConceptCatalogEntry>();

  if (!existsSync(featuresRoot)) {
    return catalog;
  }

  const specs = walk(featuresRoot).filter((path) => path.endsWith("/SPEC.md"));
  const sectionCandidates = ["Concept Registry", "Concepts", "Domain Concepts"];

  for (const specPath of specs) {
    const raw = readFileSync(specPath, "utf-8");
    const lines = raw.split(/\r?\n/);

    for (const section of sectionCandidates) {
      const table = parseTableForSection(lines, section);
      if (!table) {
        continue;
      }

      const headerMap = toHeaderMap(table.headers);
      const idIndex = headerMap.get("id");
      const typeIndex = headerMap.get("type");
      if (idIndex === undefined || typeIndex === undefined) {
        continue;
      }

      for (const row of table.rows) {
        const id = cleanCell(row.cells[idIndex] || "");
        const type = cleanCell(row.cells[typeIndex] || "");
        if (!id || !type) {
          continue;
        }

        if (isPlaceholder(id) || isPlaceholder(type)) {
          continue;
        }

        if (!catalog.has(id)) {
          catalog.set(id, {
            id,
            type,
            specPath: toRelative(specPath),
            line: row.line,
          });
        }
      }
    }
  }

  return catalog;
}

export function toRelative(absPath: string): string {
  return relative(process.cwd(), absPath).replace(/\\/g, "/");
}

function parseTypeSide(side: string): Set<string> {
  const cleaned = side
    .replace(/@[A-Za-z0-9_.-]+/g, "")
    .replace(/\[[^\]]*\]/g, "")
    .trim();

  const tokens = cleaned
    .split("/")
    .map((token) => token.trim())
    .filter(Boolean)
    .map((token) => normalizeTypeName(token))
    .filter(Boolean);

  return new Set(tokens);
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
      rows.push({
        cells,
        line: rowIndex + 1,
      });
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
