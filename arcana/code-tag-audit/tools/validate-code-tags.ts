#!/usr/bin/env tsx

import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

import {
  loadConceptCatalog,
  normalizeTypeName,
  parseRelationshipRules,
  parseTaxonomyTypes,
  toRelative,
} from "./lib/code-tag-rules";
import type {
  ExtractedTag,
  ExtractionOutput,
  Mode,
  TagIssue,
  Waiver,
} from "./lib/code-tag-types";

const args = process.argv.slice(2);
const mode = (getArg("--mode") || "strict") as Mode;
const inputPath = resolve(
  process.cwd(),
  getArg("--input") || "code-tags.json",
);
const outputPath = getArg("--output")
  ? resolve(process.cwd(), getArg("--output") || "")
  : null;
const jsonOnly = hasFlag("--json");
const requireEvidence = hasFlag("--require-evidence");

const relationshipsPath = resolve(
  process.cwd(),
  getArg("--relationships") || "RELATIONSHIPS.md",
);
const taxonomyPath = resolve(
  process.cwd(),
  getArg("--taxonomy") || "TAXONOMY.md",
);
const featuresRoot = resolve(
  process.cwd(),
  getArg("--features-root") || "docs/features",
);
const waiverPath = resolve(
  process.cwd(),
  getArg("--waivers") || "governance/tags/code-tag-waivers.yaml",
);

if (!existsSync(inputPath)) {
  fail([
    issue(
      "CT-VAL-000",
      "CRITICAL",
      `Input not found: ${toRelative(inputPath)}`,
      toRelative(inputPath),
      1,
    ),
  ]);
}

const extraction = readExtraction(inputPath);
const tags = extraction.tags;

const taxonomyTypes = parseTaxonomyTypes(taxonomyPath);
const edgeRules = parseRelationshipRules(relationshipsPath);
const conceptCatalog = loadConceptCatalog(featuresRoot);

if (taxonomyTypes.size === 0) {
  fail([
    issue(
      "CT-VAL-001",
      "CRITICAL",
      `Failed to load taxonomy types from ${toRelative(taxonomyPath)}`,
      toRelative(taxonomyPath),
      1,
    ),
  ]);
}

if (edgeRules.size === 0) {
  fail([
    issue(
      "CT-VAL-002",
      "CRITICAL",
      `Failed to load relationship rules from ${toRelative(relationshipsPath)}`,
      toRelative(relationshipsPath),
      1,
    ),
  ]);
}

const validationIssues: TagIssue[] = [];

const symbolConcept = new Map<string, string>();
const triples = new Set<string>();

for (const tag of tags) {
  validateTag(
    tag,
    {
      requireEvidence,
      taxonomyTypes,
      edgeRules,
      conceptCatalog,
      symbolConcept,
      triples,
    },
    validationIssues,
  );
}

const waiverResult = loadWaivers(waiverPath);
validationIssues.push(...waiverResult.issues);
applyWaivers(validationIssues, waiverResult.waivers);

validationIssues.sort(compareIssues);

const nonWaivedIssues = validationIssues.filter((entry) => !entry.waived);
const blockingIssues = nonWaivedIssues.filter(
  (entry) => entry.severity === "CRITICAL" || entry.severity === "HIGH",
);

const payload = {
  ok: blockingIssues.length === 0,
  mode,
  input: toRelative(inputPath),
  relationships: toRelative(relationshipsPath),
  taxonomy: toRelative(taxonomyPath),
  featuresRoot: toRelative(featuresRoot),
  tags: tags.length,
  issues: validationIssues.length,
  nonWaivedIssues: nonWaivedIssues.length,
  blockingIssues: blockingIssues.length,
  waivedIssues: validationIssues.filter((entry) => entry.waived).length,
  requireEvidence,
  report: validationIssues,
};

if (outputPath) {
  writeFileSync(outputPath, JSON.stringify(payload, null, 2) + "\n", "utf-8");
}

if (jsonOnly) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  console.log(
    `validate-code-tags: tags=${payload.tags} issues=${payload.issues} nonWaived=${payload.nonWaivedIssues} blocking=${payload.blockingIssues} waived=${payload.waivedIssues}`,
  );

  for (const entry of validationIssues) {
    const waived = entry.waived ? ` | waived=${entry.waiverId || "yes"}` : "";
    const remediation = ` | remediation=CODE-TAG-REMEDIATION.md (code=${entry.code})`;
    console.log(
      `[code-tag:${mode}] ${entry.file}:${entry.line} | severity=${entry.severity} | code=${entry.code} | ${entry.message}${remediation}${waived}`,
    );
  }
}

if (mode === "strict" && blockingIssues.length > 0) {
  process.exit(1);
}

process.exit(0);

function validateTag(
  tag: ExtractedTag,
  context: {
    requireEvidence: boolean;
    taxonomyTypes: Map<string, string>;
    edgeRules: ReturnType<typeof parseRelationshipRules>;
    conceptCatalog: ReturnType<typeof loadConceptCatalog>;
    symbolConcept: Map<string, string>;
    triples: Set<string>;
  },
  out: TagIssue[],
): void {
  const conceptId = (tag.concept.id || "").trim();
  const conceptType = (tag.concept.type || "").trim();
  const concern = (tag.concept.concern || "").trim();
  const specRefPath = (tag.concept.spec_ref?.path || "").trim();
  const specRefLine = tag.concept.spec_ref?.line;

  const symbolKey = `${tag.file}::${tag.symbol}`;

  if (!conceptId) {
    out.push(
      issue(
        "CT-001",
        "CRITICAL",
        "Missing concept.id",
        tag.file,
        tag.line,
        tag,
      ),
    );
  }

  if (!conceptType) {
    out.push(
      issue(
        "CT-002",
        "CRITICAL",
        "Missing concept.type",
        tag.file,
        tag.line,
        tag,
      ),
    );
  }

  if (concern && concern !== "biz" && concern !== "sys") {
    out.push(
      issue(
        "CT-012",
        "MEDIUM",
        `Invalid concept.concern '${concern}' (expected biz or sys)`,
        tag.file,
        tag.line,
        tag,
      ),
    );
  }

  const normalizedSourceType = normalizeTypeName(conceptType);
  if (conceptType && !context.taxonomyTypes.has(normalizedSourceType)) {
    out.push(
      issue(
        "CT-010",
        "CRITICAL",
        `concept.type '${conceptType}' is not present in TAXONOMY.md`,
        tag.file,
        tag.line,
        tag,
      ),
    );
  }

  const sourceConcept = conceptId
    ? context.conceptCatalog.get(conceptId)
    : undefined;

  if (conceptId && !sourceConcept) {
    out.push(
      issue(
        "CT-013",
        "HIGH",
        `Source concept '${conceptId}' is not defined in docs/features/*/SPEC.md`,
        tag.file,
        tag.line,
        tag,
      ),
    );
  }

  if (tag.concept.spec_ref) {
    if (!specRefPath) {
      out.push(
        issue(
          "CT-016",
          "CRITICAL",
          "spec_ref.path is required when concept.spec_ref is declared",
          tag.file,
          tag.line,
          tag,
        ),
      );
    } else if (!specRefPath.endsWith("/SPEC.md") && specRefPath !== "SPEC.md") {
      out.push(
        issue(
          "CT-016",
          "MEDIUM",
          `Invalid spec_ref.path '${specRefPath}' (expected path ending with /SPEC.md)`,
          tag.file,
          tag.line,
          tag,
        ),
      );
    }

    if (
      specRefLine !== undefined &&
      (!Number.isInteger(specRefLine) || specRefLine < 1)
    ) {
      out.push(
        issue(
          "CT-019",
          "MEDIUM",
          `Invalid spec_ref.line '${String(specRefLine)}' (expected positive integer)`,
          tag.file,
          tag.line,
          tag,
        ),
      );
    }

    if (sourceConcept && specRefPath) {
      const expectedPath = normalizeSpecPath(sourceConcept.specPath);
      const providedPath = normalizeSpecPath(specRefPath);

      if (providedPath !== expectedPath) {
        out.push(
          issue(
            "CT-017",
            "HIGH",
            `spec_ref.path '${specRefPath}' does not match canonical source '${sourceConcept.specPath}' for concept '${conceptId}'`,
            tag.file,
            tag.line,
            tag,
          ),
        );
      }

      if (
        Number.isInteger(specRefLine) &&
        specRefLine !== undefined &&
        specRefLine !== sourceConcept.line
      ) {
        out.push(
          issue(
            "CT-018",
            "MEDIUM",
            `spec_ref.line '${specRefLine}' does not match canonical line '${sourceConcept.line}' for concept '${conceptId}'`,
            tag.file,
            tag.line,
            tag,
          ),
        );
      }
    }
  }

  const existingConcept = context.symbolConcept.get(symbolKey);
  if (existingConcept && conceptId && existingConcept !== conceptId) {
    out.push(
      issue(
        "CT-008",
        "HIGH",
        `Conflicting concept IDs for symbol '${tag.symbol}' (${existingConcept} vs ${conceptId})`,
        tag.file,
        tag.line,
        tag,
      ),
    );
  } else if (!existingConcept && conceptId) {
    context.symbolConcept.set(symbolKey, conceptId);
  }

  for (const edge of tag.edges) {
    const edgeLabel = (edge.edge || "").trim();
    const targetId = (edge.to || "").trim();

    if (!edgeLabel) {
      out.push(
        issue(
          "CT-014",
          "CRITICAL",
          "Edge entry is missing 'edge' value",
          tag.file,
          tag.line,
          tag,
        ),
      );
      continue;
    }

    if (!targetId) {
      out.push(
        issue(
          "CT-015",
          "CRITICAL",
          `Edge '${edgeLabel}' is missing 'to' endpoint`,
          tag.file,
          tag.line,
          tag,
        ),
      );
      continue;
    }

    const rule = context.edgeRules.get(edgeLabel);
    if (!rule) {
      out.push(
        issue(
          "CT-003",
          "CRITICAL",
          `Unknown edge label '${edgeLabel}'`,
          tag.file,
          tag.line,
          tag,
        ),
      );
      continue;
    }

    if (conceptType && !rule.fromTypes.has(normalizedSourceType)) {
      out.push(
        issue(
          "CT-004",
          "CRITICAL",
          `Invalid source type '${conceptType}' for edge '${edgeLabel}' (expected ${rule.fromRaw})`,
          tag.file,
          tag.line,
          tag,
        ),
      );
    }

    const targetConcept = context.conceptCatalog.get(targetId);
    if (!targetConcept) {
      out.push(
        issue(
          "CT-005",
          "HIGH",
          `Unknown target concept '${targetId}'`,
          tag.file,
          tag.line,
          tag,
          targetId,
        ),
      );
    } else {
      const normalizedTargetType = normalizeTypeName(targetConcept.type);
      if (!rule.toTypes.has(normalizedTargetType)) {
        out.push(
          issue(
            "CT-006",
            "CRITICAL",
            `Invalid target type '${targetConcept.type}' for edge '${edgeLabel}' (expected ${rule.toRaw})`,
            tag.file,
            tag.line,
            tag,
            targetId,
          ),
        );
      }
    }

    if (context.requireEvidence && !edge.evidence?.trim()) {
      out.push(
        issue(
          "CT-009",
          "MEDIUM",
          `Missing evidence for edge '${edgeLabel}' (require-evidence enabled)`,
          tag.file,
          tag.line,
          tag,
          targetId,
        ),
      );
    }

    if (conceptId && edgeLabel && targetId) {
      const tripleKey = `${tag.file}|${conceptId}|${edgeLabel}|${targetId}`;
      if (context.triples.has(tripleKey)) {
        out.push(
          issue(
            "CT-007",
            "HIGH",
            `Duplicate triple in same artifact: ${conceptId} --${edgeLabel}--> ${targetId}`,
            tag.file,
            tag.line,
            tag,
            targetId,
          ),
        );
      } else {
        context.triples.add(tripleKey);
      }
    }
  }
}

function readExtraction(input: string): ExtractionOutput {
  const raw = readFileSync(input, "utf-8");
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

function loadWaivers(pathToWaivers: string): {
  waivers: Waiver[];
  issues: TagIssue[];
} {
  if (!existsSync(pathToWaivers)) {
    return { waivers: [], issues: [] };
  }

  const raw = readFileSync(pathToWaivers, "utf-8");
  const lines = raw.split(/\r?\n/);

  const parsed: Array<Partial<Waiver>> = [];
  let inWaivers = false;
  let current: Partial<Waiver> | null = null;

  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i] || "";
    const trimmed = line.trim();

    if (!trimmed || trimmed.startsWith("#")) {
      continue;
    }

    if (!inWaivers) {
      if (trimmed === "waivers:") {
        inWaivers = true;
      }
      continue;
    }

    if (trimmed.startsWith("- ")) {
      if (current) {
        parsed.push(current);
      }
      current = {};
      const inline = trimmed.slice(2).trim();
      if (inline) {
        assignKeyValue(inline, current);
      }
      continue;
    }

    if (!current) {
      continue;
    }

    assignKeyValue(trimmed, current);
  }

  if (current) {
    parsed.push(current);
  }

  const issues: TagIssue[] = [];
  const waivers: Waiver[] = [];
  const now = Date.now();

  for (const item of parsed) {
    const id = (item.id || "").trim();
    const code = (item.code || "").trim();
    const owner = (item.owner || "").trim();
    const reason = (item.reason || "").trim();
    const expiresAt = (item.expiresAt || "").trim();

    if (!id || !code || !owner || !reason || !expiresAt) {
      issues.push(
        issue(
          "CT-WAIVER-001",
          "CRITICAL",
          `Invalid waiver entry (required: id, code, owner, reason, expiresAt)`,
          toRelative(pathToWaivers),
          1,
        ),
      );
      continue;
    }

    const expiration = Date.parse(expiresAt);
    if (!Number.isFinite(expiration)) {
      issues.push(
        issue(
          "CT-WAIVER-002",
          "CRITICAL",
          `Waiver '${id}' has invalid expiresAt '${expiresAt}'`,
          toRelative(pathToWaivers),
          1,
        ),
      );
      continue;
    }

    if (expiration < now) {
      issues.push(
        issue(
          "CT-WAIVER-003",
          "HIGH",
          `Waiver '${id}' is expired (${expiresAt})`,
          toRelative(pathToWaivers),
          1,
        ),
      );
      continue;
    }

    waivers.push({
      id,
      code,
      owner,
      reason,
      expiresAt,
      approvedBy: (item.approvedBy || "").trim() || undefined,
      file: (item.file || "").trim() || undefined,
      conceptId: (item.conceptId || "").trim() || undefined,
    });
  }

  return { waivers, issues };
}

function applyWaivers(issues: TagIssue[], waivers: Waiver[]): void {
  for (const entry of issues) {
    if (entry.code.startsWith("CT-WAIVER-")) {
      continue;
    }

    const match = waivers.find((waiver) => {
      if (waiver.code !== entry.code) {
        return false;
      }

      if (waiver.file && waiver.file !== entry.file) {
        return false;
      }

      if (waiver.conceptId && waiver.conceptId !== entry.conceptId) {
        return false;
      }

      return true;
    });

    if (!match) {
      continue;
    }

    entry.waived = true;
    entry.waiverId = match.id;
  }
}

function assignKeyValue(source: string, target: Partial<Waiver>): void {
  const separator = source.indexOf(":");
  if (separator <= 0) {
    return;
  }

  const key = source.slice(0, separator).trim();
  const value = unquote(source.slice(separator + 1).trim());

  if (
    key === "id" ||
    key === "code" ||
    key === "file" ||
    key === "conceptId" ||
    key === "owner" ||
    key === "reason" ||
    key === "expiresAt" ||
    key === "approvedBy"
  ) {
    (target as Record<string, string>)[key] = value;
  }
}

function unquote(value: string): string {
  const trimmed = value.trim();
  if (
    (trimmed.startsWith('"') && trimmed.endsWith('"')) ||
    (trimmed.startsWith("'") && trimmed.endsWith("'"))
  ) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}

function issue(
  code: string,
  severity: "CRITICAL" | "HIGH" | "MEDIUM",
  message: string,
  file: string,
  line: number,
  tag?: ExtractedTag,
  conceptId?: string,
): TagIssue {
  return {
    code,
    severity,
    message,
    file,
    line,
    symbol: tag?.symbol,
    conceptId: conceptId || tag?.concept.id,
  };
}

function compareIssues(left: TagIssue, right: TagIssue): number {
  const severityRank = { CRITICAL: 0, HIGH: 1, MEDIUM: 2 };
  const leftRank = severityRank[left.severity];
  const rightRank = severityRank[right.severity];

  if (leftRank !== rightRank) {
    return leftRank - rightRank;
  }

  if (left.file !== right.file) {
    return left.file.localeCompare(right.file);
  }

  if (left.line !== right.line) {
    return left.line - right.line;
  }

  return left.code.localeCompare(right.code);
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

function normalizeSpecPath(pathValue: string): string {
  const normalized = pathValue.replace(/\\/g, "/").replace(/^\.\//, "").trim();

  const anchor = "docs/features/";
  const anchorIndex = normalized.lastIndexOf(anchor);
  if (anchorIndex >= 0) {
    return normalized.slice(anchorIndex);
  }

  return normalized;
}

function fail(entries: TagIssue[]): never {
  for (const entry of entries) {
    const remediation = ` | remediation=CODE-TAG-REMEDIATION.md (code=${entry.code})`;
    console.log(
      `[code-tag:strict] ${entry.file}:${entry.line} | severity=${entry.severity} | code=${entry.code} | ${entry.message}${remediation}`,
    );
  }
  process.exit(1);
}
