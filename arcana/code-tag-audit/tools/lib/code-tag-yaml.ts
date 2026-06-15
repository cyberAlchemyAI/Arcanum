import type {
  ExtractedConcept,
  ExtractedEdge,
  TagIssue,
} from "./code-tag-types";

type ParsedDomainspec = {
  concept: ExtractedConcept;
  edges: ExtractedEdge[];
};

export function parseDomainspecYamlBlock(
  yamlText: string,
  file: string,
  startLine: number,
  symbol?: string,
): { parsed: ParsedDomainspec | null; issues: TagIssue[] } {
  const issues: TagIssue[] = [];
  const lines = yamlText.split(/\r?\n/);

  let inDomainspec = false;
  let section: "none" | "concept" | "edges" = "none";
  let conceptSubsection: "none" | "spec_ref" = "none";

  const concept: ExtractedConcept = {
    id: "",
    type: "",
  };

  const edges: ExtractedEdge[] = [];
  let currentEdge: Partial<ExtractedEdge> | null = null;

  for (let i = 0; i < lines.length; i += 1) {
    const raw = lines[i] || "";
    const lineNo = startLine + i;
    const trimmed = raw.trim();

    if (!trimmed || trimmed.startsWith("#")) {
      continue;
    }

    if (!inDomainspec) {
      if (/^domainspec\s*:\s*$/.test(trimmed)) {
        inDomainspec = true;
      }
      continue;
    }

    if (/^(concept|edges)\s*:\s*$/.test(trimmed)) {
      if (trimmed.startsWith("concept")) {
        if (currentEdge) {
          pushEdge(currentEdge, edges);
          currentEdge = null;
        }
        section = "concept";
        conceptSubsection = "none";
      } else {
        if (currentEdge) {
          pushEdge(currentEdge, edges);
          currentEdge = null;
        }
        section = "edges";
        conceptSubsection = "none";
      }
      continue;
    }

    if (section === "concept") {
      const idMatch = /^id\s*:\s*(.+)$/.exec(trimmed);
      if (idMatch?.[1]) {
        concept.id = parseScalar(idMatch[1]);
        continue;
      }

      const typeMatch = /^type\s*:\s*(.+)$/.exec(trimmed);
      if (typeMatch?.[1]) {
        concept.type = parseScalar(typeMatch[1]);
        continue;
      }

      const concernMatch = /^concern\s*:\s*(.+)$/.exec(trimmed);
      if (concernMatch?.[1]) {
        concept.concern = parseScalar(concernMatch[1]);
        continue;
      }

      if (/^spec_ref\s*:\s*$/.test(trimmed)) {
        conceptSubsection = "spec_ref";
        concept.spec_ref = concept.spec_ref || { path: "" };
        continue;
      }

      if (conceptSubsection === "spec_ref") {
        const pathMatch = /^path\s*:\s*(.+)$/.exec(trimmed);
        if (pathMatch?.[1]) {
          concept.spec_ref = concept.spec_ref || { path: "" };
          concept.spec_ref.path = parseScalar(pathMatch[1]);
          continue;
        }

        const sectionMatch = /^section\s*:\s*(.+)$/.exec(trimmed);
        if (sectionMatch?.[1]) {
          concept.spec_ref = concept.spec_ref || { path: "" };
          concept.spec_ref.section = parseScalar(sectionMatch[1]);
          continue;
        }

        const lineMatch = /^line\s*:\s*(.+)$/.exec(trimmed);
        if (lineMatch?.[1]) {
          const rawLine = parseScalar(lineMatch[1]);
          if (/^[1-9][0-9]*$/.test(rawLine)) {
            concept.spec_ref = concept.spec_ref || { path: "" };
            concept.spec_ref.line = Number(rawLine);
          } else {
            issues.push(
              makeIssue(
                "CT-PARSE-004",
                "MEDIUM",
                `Invalid spec_ref.line '${rawLine}' (expected positive integer)`,
                file,
                lineNo,
                symbol,
              ),
            );
          }
          continue;
        }
      }

      continue;
    }

    if (section === "edges") {
      const edgeStart = /^-\s*edge\s*:\s*(.+)$/.exec(trimmed);
      if (edgeStart?.[1]) {
        if (currentEdge) {
          pushEdge(currentEdge, edges);
        }
        currentEdge = {
          edge: parseScalar(edgeStart[1]),
        };
        continue;
      }

      const toMatch = /^to\s*:\s*(.+)$/.exec(trimmed);
      if (toMatch?.[1]) {
        if (!currentEdge) {
          issues.push(
            makeIssue(
              "CT-PARSE-001",
              "CRITICAL",
              "Found 'to' before '- edge' in domainspec edges block",
              file,
              lineNo,
              symbol,
            ),
          );
          continue;
        }
        currentEdge.to = parseScalar(toMatch[1]);
        continue;
      }

      const evidenceMatch = /^evidence\s*:\s*(.+)$/.exec(trimmed);
      if (evidenceMatch?.[1]) {
        if (!currentEdge) {
          issues.push(
            makeIssue(
              "CT-PARSE-002",
              "CRITICAL",
              "Found 'evidence' before '- edge' in domainspec edges block",
              file,
              lineNo,
              symbol,
            ),
          );
          continue;
        }
        currentEdge.evidence = parseScalar(evidenceMatch[1]);
        continue;
      }
    }
  }

  if (currentEdge) {
    pushEdge(currentEdge, edges);
  }

  if (!inDomainspec) {
    issues.push(
      makeIssue(
        "CT-PARSE-003",
        "CRITICAL",
        "Could not find 'domainspec:' root in annotation block",
        file,
        startLine,
        symbol,
      ),
    );
    return { parsed: null, issues };
  }

  return {
    parsed: {
      concept,
      edges,
    },
    issues,
  };
}

function pushEdge(
  candidate: Partial<ExtractedEdge>,
  edges: ExtractedEdge[],
): void {
  if (!candidate.edge && !candidate.to) {
    return;
  }

  edges.push({
    edge: (candidate.edge || "").trim(),
    to: (candidate.to || "").trim(),
    evidence: candidate.evidence?.trim() || undefined,
  });
}

function parseScalar(value: string): string {
  const trimmed = value.trim();
  if (
    (trimmed.startsWith('"') && trimmed.endsWith('"')) ||
    (trimmed.startsWith("'") && trimmed.endsWith("'"))
  ) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}

function makeIssue(
  code: string,
  severity: "CRITICAL" | "HIGH" | "MEDIUM",
  message: string,
  file: string,
  line: number,
  symbol?: string,
): TagIssue {
  return {
    code,
    severity,
    message,
    file,
    line,
    symbol,
  };
}
