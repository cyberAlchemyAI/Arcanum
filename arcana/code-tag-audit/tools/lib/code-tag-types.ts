export type Concern = "biz" | "sys";

export type SourceLanguage = "ts" | "tsx" | "js" | "jsx" | "py";

export type Severity = "CRITICAL" | "HIGH" | "MEDIUM";

export type Mode = "strict" | "warn";

export type ExtractedEdge = {
  edge: string;
  to: string;
  evidence?: string;
};

export type ExtractedSpecRef = {
  path: string;
  line?: number;
  section?: string;
};

export type ExtractedConcept = {
  id: string;
  type: string;
  concern?: Concern | string;
  spec_ref?: ExtractedSpecRef;
};

export type ExtractedTag = {
  file: string;
  line: number;
  symbol: string;
  language: SourceLanguage;
  concept: ExtractedConcept;
  edges: ExtractedEdge[];
};

export type TagIssue = {
  code: string;
  severity: Severity;
  message: string;
  file: string;
  line: number;
  symbol?: string;
  conceptId?: string;
  detail?: string;
  waived?: boolean;
  waiverId?: string;
};

export type ExtractionOutput = {
  meta: {
    generatedAt: string;
    mode: Mode;
    include: string[];
    root: string;
  };
  tags: ExtractedTag[];
  issues: TagIssue[];
  stats: {
    scannedFiles: number;
    taggedSymbols: number;
    issues: number;
  };
};

export type CanonicalEdgeRule = {
  edge: string;
  fromRaw: string;
  toRaw: string;
  fromTypes: Set<string>;
  toTypes: Set<string>;
};

export type ConceptCatalogEntry = {
  id: string;
  type: string;
  specPath: string;
  line: number;
};

export type Waiver = {
  id: string;
  code: string;
  file?: string;
  conceptId?: string;
  owner: string;
  reason: string;
  expiresAt: string;
  approvedBy?: string;
};
