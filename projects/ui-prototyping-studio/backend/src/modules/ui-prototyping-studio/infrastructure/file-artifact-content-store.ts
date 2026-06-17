import {
  existsSync,
  mkdirSync,
  readFileSync,
  renameSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { join } from "node:path";

import type {
  ArtifactContentPort,
  StagedArtifact,
} from "../application/artifact-content-port.js";
import { canonicalHash } from "../domain/canonicalize.js";

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.FileArtifactContentStore
 *     type: Adapter
 *
 * File-backed ArtifactContentPort. Staged candidates live under <root>/staged/,
 * committed artifacts under <root>/committed/. Refs are content-addressed:
 *   staged ref    = "staged:<hash>"
 *   committed ref = "artifact:<hash>"
 */
interface Options {
  rootDir: string;
}

export function createFileArtifactContentStore(
  options: Options,
): ArtifactContentPort {
  const stagedDir = join(options.rootDir, "staged");
  const committedDir = join(options.rootDir, "committed");

  const ensure = (dir: string) => {
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  };
  const pathForRef = (ref: string): string | null => {
    const [kind, hash] = ref.split(":");
    if (!hash) return null;
    if (kind === "staged") return join(stagedDir, `${hash}.html`);
    if (kind === "artifact") return join(committedDir, `${hash}.html`);
    return null;
  };

  return {
    readHtml(ref: string): string | null {
      const p = pathForRef(ref);
      if (!p || !existsSync(p)) return null;
      return readFileSync(p, "utf8");
    },

    stageHtml(html: string): StagedArtifact {
      ensure(stagedDir);
      const hash = canonicalHash(html);
      writeFileSync(join(stagedDir, `${hash}.html`), html, "utf8");
      return { stagedRef: `staged:${hash}`, hash };
    },

    commitHtml(stagedRef: string): string {
      const src = pathForRef(stagedRef);
      const hash = stagedRef.split(":")[1];
      if (!src || !hash || !existsSync(src)) {
        throw new Error(`NO_STAGED_CANDIDATE: ${stagedRef}`);
      }
      ensure(committedDir);
      const dest = join(committedDir, `${hash}.html`);
      renameSync(src, dest); // atomic within a filesystem
      return `artifact:${hash}`;
    },

    discardStagedHtml(stagedRef: string): void {
      const p = pathForRef(stagedRef);
      if (p && existsSync(p)) rmSync(p);
    },

    pathForRef(ref: string): string | null {
      return pathForRef(ref);
    },
  };
}
