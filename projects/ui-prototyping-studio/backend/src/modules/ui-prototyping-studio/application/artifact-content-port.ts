/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.ArtifactContentPort
 *     type: Port
 *
 * M0b — the artifact content port (SWU-M0b). The mutation-execution recorder lane
 * needs to read the current prototype HTML, STAGE a candidate at a temp ref (NOT head),
 * then COMMIT it atomically or DISCARD it (DEC-MUTATION-EXEC-015 two-gate apply).
 * The existing StudioSessionStorePort had zero HTML read/write methods — this closes
 * the "unbuildable substrate" finding (s7-A1). `removeRevision` is L3 (SWU-M3).
 */
export interface StagedArtifact {
  /** Opaque staged reference (not the head; discardable). */
  readonly stagedRef: string;
  /** Canonical content hash of the staged HTML (candidateHtmlHash). */
  readonly hash: string;
}

export interface ArtifactContentPort {
  /** Return the HTML at a committed or staged ref, or null if absent. */
  readHtml(ref: string): string | null;
  /** Stage candidate HTML at a temp ref; returns the ref + canonical hash. Idempotent by hash. */
  stageHtml(html: string): StagedArtifact;
  /** Promote a staged ref to a committed artifact ref (atomic); returns the committed ref. */
  commitHtml(stagedRef: string): string;
  /** Drop a staged candidate with no trace (reject / accept-diff discard path). */
  discardStagedHtml(stagedRef: string): void;
  /** D1a — the on-disk path for a ref (for "open this in a browser"), or null if not file-backed. */
  pathForRef(ref: string): string | null;
}
