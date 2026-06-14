import { parseDomainspecYamlBlock } from "../code-tag-yaml";
import type { ExtractedTag, TagIssue } from "../code-tag-types";

export function extractPyTags(
  raw: string,
  file: string,
): { tags: ExtractedTag[]; issues: TagIssue[] } {
  const tags: ExtractedTag[] = [];
  const issues: TagIssue[] = [];
  const lines = raw.split(/\r?\n/);

  for (let i = 0; i < lines.length; i += 1) {
    const declaration = (lines[i] || "").trim();
    const declMatch =
      /^(?:async\s+def|def|class)\s+([A-Za-z_][A-Za-z0-9_]*)\b/.exec(
        declaration,
      );
    if (!declMatch?.[1]) {
      continue;
    }

    const symbol = declMatch[1];
    const docStart = findDocstringStart(lines, i + 1);
    if (docStart < 0) {
      continue;
    }

    const parsedDoc = parseDocstring(lines, docStart, file, symbol);
    if (!parsedDoc) {
      continue;
    }

    if (!/^\s*domainspec\s*:/m.test(parsedDoc.content)) {
      continue;
    }

    const parsed = parseDomainspecYamlBlock(
      parsedDoc.content,
      file,
      parsedDoc.startLine,
      symbol,
    );
    issues.push(...parsed.issues);

    if (!parsed.parsed) {
      continue;
    }

    tags.push({
      file,
      line: parsedDoc.startLine,
      symbol,
      language: "py",
      concept: parsed.parsed.concept,
      edges: parsed.parsed.edges,
    });

    i = parsedDoc.endLine - 1;
  }

  return { tags, issues };
}

function findDocstringStart(lines: string[], from: number): number {
  let i = from;
  while (i < lines.length) {
    const line = (lines[i] || "").trim();
    if (!line) {
      i += 1;
      continue;
    }

    if (line.startsWith("#")) {
      i += 1;
      continue;
    }

    if (line.startsWith('"""') || line.startsWith("'''")) {
      return i;
    }

    return -1;
  }

  return -1;
}

function parseDocstring(
  lines: string[],
  startIndex: number,
  file: string,
  symbol: string,
): { content: string; startLine: number; endLine: number } | null {
  const first = lines[startIndex] || "";
  const trimmed = first.trim();

  const quote = trimmed.startsWith('"""') ? '"""' : "'''";
  const quotePos = first.indexOf(quote);
  if (quotePos < 0) {
    return null;
  }

  const afterStart = first.slice(quotePos + 3);
  const sameLineEnd = afterStart.indexOf(quote);

  if (sameLineEnd >= 0) {
    const content = afterStart.slice(0, sameLineEnd);
    return {
      content,
      startLine: startIndex + 1,
      endLine: startIndex + 1,
    };
  }

  const collected: string[] = [];
  for (let i = startIndex + 1; i < lines.length; i += 1) {
    const line = lines[i] || "";
    const endPos = line.indexOf(quote);
    if (endPos >= 0) {
      collected.push(line.slice(0, endPos));
      return {
        content: collected.join("\n"),
        startLine: startIndex + 1,
        endLine: i + 1,
      };
    }

    collected.push(line);
  }

  return {
    content: collected.join("\n"),
    startLine: startIndex + 1,
    endLine: lines.length,
  };
}
