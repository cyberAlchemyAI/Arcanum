import { extractJsLikeTags } from "./js-like";

export function extractTsTags(
  raw: string,
  file: string,
  language: "ts" | "tsx",
) {
  return extractJsLikeTags(raw, file, language);
}
