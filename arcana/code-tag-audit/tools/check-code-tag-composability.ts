#!/usr/bin/env tsx

// @ts-nocheck

import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

import { normalizeTypeName, toRelative } from "./lib/code-tag-rules";
import type {
  ExtractedTag,
  ExtractionOutput,
  Mode,
  Severity,
  TagIssue,
} from "./lib/code-tag-types";

type ComposabilityRule = {
  edge: string;
  fromType: string;
  toType: string;
  direction: "target-calls-source" | "source-calls-target";
  code: string;
  severity: Severity;
  expectation: string;
};

const rules: ComposabilityRule[] = [
  {
    edge: "enforces",
    fromType: "rule",
    toType: "operation",
    direction: "target-calls-source",
    code: "CT-COMP-001",
    severity: "HIGH",
    expectation: "Operation calls its enforcing rule",
  },
  {
    edge: "calculates",
    fromType: "calculation",
    toType: "operation",
    direction: "target-calls-source",
    code: "CT-COMP-002",
    severity: "HIGH",
    expectation: "Operation calls its calculation",
  },
  {
    edge: "applies",
    fromType: "policy",
    toType: "operation",
    direction: "target-calls-source",
    code: "CT-COMP-003",
    severity: "MEDIUM",
    expectation: "Operation calls its policy",
  },
  {
    edge: "exposes",
    fromType: "interface",
    toType: "operation",
    direction: "source-calls-target",
    code: "CT-COMP-004",
    severity: "HIGH",
    expectation: "Interface calls exposed operation",
  },
  {
    edge: "exposes",
    fromType: "interface",
    toType: "query",
    direction: "source-calls-target",
    code: "CT-COMP-005",
    severity: "HIGH",
    expectation: "Interface calls exposed query",
  },
  {
    edge: "mutates",
    fromType: "binding",
    toType: "operation",
    direction: "source-calls-target",
    code: "CT-COMP-006",
    severity: "HIGH",
    expectation: "Binding calls target operation",
  },
  {
    edge: "fetches",
    fromType: "binding",
    toType: "query",
    direction: "source-calls-target",
    code: "CT-COMP-007",
    severity: "HIGH",
    expectation: "Binding calls target query",
  },
  {
    edge: "orchestrates",
    fromType: "workflow",
    toType: "operation",
    direction: "source-calls-target",
    code: "CT-COMP-008",
    severity: "HIGH",
    expectation: "Workflow calls orchestrated operation",
  },
  {
    edge: "enforces-cross",
    fromType: "rule",
    toType: "operation",
    direction: "target-calls-source",
    code: "CT-COMP-009",
    severity: "HIGH",
    expectation: "Cross-feature operation calls enforcing rule",
  },
];

const rulesByEdge = new Map<string, ComposabilityRule[]>();
for (const rule of rules) {
  const existing = rulesByEdge.get(rule.edge) || [];
  existing.push(rule);
  rulesByEdge.set(rule.edge, existing);
}

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

if (!existsSync(inputPath)) {
  fail([
    issue(
      "CT-COMP-000",
      "CRITICAL",
      `Input not found: ${toRelative(inputPath)}`,
      toRelative(inputPath),
      1,
    ),
  ]);
}

const extraction = readExtraction(inputPath);
const rootPath = getRootPath(extraction);
const tags = extraction.tags;

const conceptToTags = new Map<string, ExtractedTag[]>();
for (const tag of tags) {
  const id = (tag.concept.id || "").trim();
  if (!id) {
    continue;
  }

  const existing = conceptToTags.get(id) || [];
  existing.push(tag);
  conceptToTags.set(id, existing);
}

let checks = 0;
let passedChecks = 0;
const issues: TagIssue[] = [];
const sourceCache = new Map<string, string>();

for (const sourceTag of tags) {
  const sourceType = normalizeTypeName(sourceTag.concept.type || "");
  for (const edge of sourceTag.edges) {
    const edgeLabel = (edge.edge || "").trim();
    const targetConceptId = (edge.to || "").trim();

    if (!edgeLabel || !targetConceptId) {
      continue;
    }

    const edgeRules = rulesByEdge.get(edgeLabel) || [];
    const conceptTargets = conceptToTags.get(targetConceptId) || [];
    if (conceptTargets.length === 0) {
      issues.push(
        issue(
          "CT-COMP-010",
          "MEDIUM",
          `Cannot evaluate '${edgeLabel}' composability: target concept '${targetConceptId}' is not tagged in code`,
          sourceTag.file,
          sourceTag.line,
          sourceTag,
          targetConceptId,
        ),
      );
      continue;
    }

    for (const edgeRule of edgeRules) {
      if (sourceType !== edgeRule.fromType) {
        continue;
      }

      const targets = conceptTargets.filter(
        (targetTag) =>
          normalizeTypeName(targetTag.concept.type || "") === edgeRule.toType,
      );

      if (targets.length === 0) {
        // For overloaded edges (e.g. exposes -> operation/query),
        // skip rule variants whose target type does not match this edge endpoint.
        continue;
      }

      checks += 1;

      let matched = false;

      if (edgeRule.direction === "target-calls-source") {
        const sourceSymbol = (sourceTag.symbol || "").trim();
        if (!hasValidSymbol(sourceSymbol)) {
          issues.push(
            issue(
              "CT-COMP-011",
              "MEDIUM",
              `Cannot evaluate '${edgeRule.edge}' composability because source symbol is missing or unknown`,
              sourceTag.file,
              sourceTag.line,
              sourceTag,
              targetConceptId,
            ),
          );
          continue;
        }

        matched = targets.some((targetTag) =>
          tagCallsSymbol(targetTag, sourceSymbol, rootPath, sourceCache),
        );
      } else {
        const callableTargets = targets.filter((targetTag) =>
          hasValidSymbol((targetTag.symbol || "").trim()),
        );

        if (callableTargets.length === 0) {
          issues.push(
            issue(
              "CT-COMP-012",
              "MEDIUM",
              `Cannot evaluate '${edgeRule.edge}' composability: target concept '${targetConceptId}' has no resolvable symbol`,
              sourceTag.file,
              sourceTag.line,
              sourceTag,
              targetConceptId,
            ),
          );
          continue;
        }

        matched = callableTargets.some((targetTag) =>
          tagCallsSymbol(
            sourceTag,
            (targetTag.symbol || "").trim(),
            rootPath,
            sourceCache,
          ),
        );
      }

      if (!matched) {
        issues.push(
          issue(
            edgeRule.code,
            edgeRule.severity,
            `Composability mismatch: ${edgeRule.expectation} for '${sourceTag.concept.id}' -> '${targetConceptId}' (${edgeRule.edge})`,
            sourceTag.file,
            sourceTag.line,
            sourceTag,
            targetConceptId,
          ),
        );
        continue;
      }

      passedChecks += 1;
    }
  }
}

issues.sort(compareIssues);

const blockingIssues = issues.filter(
  (entry) => entry.severity === "CRITICAL" || entry.severity === "HIGH",
);

const payload = {
  ok: blockingIssues.length === 0,
  mode,
  input: toRelative(inputPath),
  root: toRelative(rootPath),
  checks,
  passedChecks,
  issues: issues.length,
  blockingIssues: blockingIssues.length,
  report: issues,
};

if (outputPath) {
  writeFileSync(outputPath, JSON.stringify(payload, null, 2) + "\n", "utf-8");
}

if (jsonOnly) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  console.log(
    `check-code-tag-composability: checks=${payload.checks} passed=${payload.passedChecks} issues=${payload.issues} blocking=${payload.blockingIssues}`,
  );

  for (const entry of issues) {
    const remediation =
      " | remediation=CODE-TAG-REMEDIATION.md" +
      ` (code=${entry.code})`;
    console.log(
      `[code-tag-composability:${mode}] ${entry.file}:${entry.line} | severity=${entry.severity} | code=${entry.code} | ${entry.message}${remediation}`,
    );
  }
}

if (mode === "strict" && blockingIssues.length > 0) {
  process.exit(1);
}

process.exit(0);

function tagCallsSymbol(
  tag: ExtractedTag,
  symbol: string,
  root: string,
  cache: Map<string, string>,
): boolean {
  const absolutePath = resolveArtifactPath(root, tag.file);
  if (!existsSync(absolutePath)) {
    return false;
  }

  let raw = cache.get(absolutePath);
  if (raw === undefined) {
    const loaded = readFileSync(absolutePath, "utf-8");
    cache.set(absolutePath, loaded);
    raw = loaded;
  }

  const callPattern = new RegExp(`\\b${escapeRegExp(symbol)}\\s*\\(`);
  return callPattern.test(raw);
}

function hasValidSymbol(symbol: string): boolean {
  const trimmed = symbol.trim();
  return Boolean(trimmed) && trimmed !== "unknown";
}

function resolveArtifactPath(root: string, filePath: string): string {
  if (filePath.startsWith("/")) {
    return filePath;
  }
  return resolve(root, filePath);
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

function getRootPath(extraction: ExtractionOutput): string {
  const explicitRoot = (getArg("--root") || "").trim();
  if (explicitRoot) {
    return resolve(process.cwd(), explicitRoot);
  }

  const extractedRoot = (extraction.meta.root || "").trim();
  if (extractedRoot) {
    return extractedRoot.startsWith("/")
      ? extractedRoot
      : resolve(process.cwd(), extractedRoot);
  }

  return process.cwd();
}

function issue(
  code: string,
  severity: Severity,
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
  const severityRank: Record<Severity, number> = {
    CRITICAL: 0,
    HIGH: 1,
    MEDIUM: 2,
  };

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

function fail(entries: TagIssue[]): never {
  for (const entry of entries) {
    const remediation =
      " | remediation=CODE-TAG-REMEDIATION.md" +
      ` (code=${entry.code})`;
    console.log(
      `[code-tag-composability:strict] ${entry.file}:${entry.line} | severity=${entry.severity} | code=${entry.code} | ${entry.message}${remediation}`,
    );
  }
  process.exit(1);
  throw new Error("unreachable");
}

function escapeRegExp(input: string): string {
  return input.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
