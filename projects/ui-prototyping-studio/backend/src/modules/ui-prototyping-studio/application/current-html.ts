import type { ArtifactContentPort } from "./artifact-content-port.js";
import type { StudioSessionStorePort } from "./ports.js";
import type { StudioSession } from "../domain/models.js";

/**
 * MW1 — resolve the CURRENT head HTML the candidate is validated/diffed against.
 *  - If the head revision carries a committed candidate hash, read that committed content.
 *  - Otherwise (no mutation yet) read the committed baseline variant HTML (MR1-registered).
 * Returns null when no real HTML is resolvable (e.g. stub-generated variants — chain dep on MR1).
 */
export function resolveCurrentHtml(
  session: StudioSession,
  store: StudioSessionStorePort,
  artifact: ArtifactContentPort,
): string | null {
  const head = session.revisionHeadId;
  if (head) {
    const revision = store
      .listRevisions(session.sessionId)
      .find((entry) => entry.revisionId === head);
    if (revision?.candidateHtmlHash) {
      return artifact.readHtml(`artifact:${revision.candidateHtmlHash}`);
    }
  }
  if (!session.baseline) return null;
  const baselineVariant = store
    .listVariants(session.sessionId)
    .find((variant) => variant.variantLabel === session.baseline!.label);
  if (!baselineVariant) return null;
  return artifact.readHtml(baselineVariant.htmlArtifactRef);
}
