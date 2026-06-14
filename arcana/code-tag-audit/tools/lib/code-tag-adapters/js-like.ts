import { parseDomainspecYamlBlock } from "../code-tag-yaml";
import type { ExtractedTag, SourceLanguage, TagIssue } from "../code-tag-types";

export function extractJsLikeTags(
  raw: string,
  file: string,
  language: Extract<SourceLanguage, "ts" | "tsx" | "js" | "jsx">,
): { tags: ExtractedTag[]; issues: TagIssue[] } {
  const tags: ExtractedTag[] = [];
  const issues: TagIssue[] = [];
  const lines = raw.split(/\r?\n/);

  const blockRegex = /\/\*\*([\s\S]*?)\*\//g;
  let match: RegExpExecArray | null;

  while ((match = blockRegex.exec(raw)) !== null) {
    const fullBlock = match[0] || "";
    const body = match[1] || "";

    const startLine = lineNumberFromIndex(raw, match.index);
    const endLine = startLine + fullBlock.split(/\r?\n/).length - 1;

    const normalized = normalizeDocBlock(body);
    if (!/^\s*domainspec\s*:/m.test(normalized)) {
      continue;
    }

    const symbol = detectNextSymbol(lines, endLine + 1);
    const parsed = parseDomainspecYamlBlock(
      normalized,
      file,
      startLine,
      symbol,
    );
    issues.push(...parsed.issues);

    if (!parsed.parsed) {
      continue;
    }

    tags.push({
      file,
      line: startLine,
      symbol,
      language,
      concept: parsed.parsed.concept,
      edges: parsed.parsed.edges,
    });
  }

  return { tags, issues };
}

function normalizeDocBlock(raw: string): string {
  return raw
    .split(/\r?\n/)
    .map((line) => line.replace(/^\s*\*\s?/, ""))
    .join("\n");
}

function lineNumberFromIndex(raw: string, index: number): number {
  let line = 1;
  for (let i = 0; i < index; i += 1) {
    if (raw.charCodeAt(i) === 10) {
      line += 1;
    }
  }
  return line;
}

function detectNextSymbol(lines: string[], lineNumber: number): string {
  const start = Math.max(0, lineNumber - 1);
  const end = Math.min(lines.length, start + 15);

  const patterns = [
    /^(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_][A-Za-z0-9_]*)\b/,
    /^(?:export\s+)?class\s+([A-Za-z_][A-Za-z0-9_]*)\b/,
    /^(?:export\s+)?const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=/,
    /^(?:export\s+)?let\s+([A-Za-z_][A-Za-z0-9_]*)\s*=/,
    /^(?:export\s+)?var\s+([A-Za-z_][A-Za-z0-9_]*)\s*=/,
    /^(?:export\s+)?interface\s+([A-Za-z_][A-Za-z0-9_]*)\b/,
    /^(?:export\s+)?type\s+([A-Za-z_][A-Za-z0-9_]*)\b/,
  ];

  for (let i = start; i < end; i += 1) {
    const line = (lines[i] || "").trim();
    for (const pattern of patterns) {
      const m = pattern.exec(line);
      if (m?.[1]) {
        return m[1];
      }
    }
  }

  return "unknown";
}
