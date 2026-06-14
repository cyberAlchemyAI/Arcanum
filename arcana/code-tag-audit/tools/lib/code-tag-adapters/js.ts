import { extractJsLikeTags } from "./js-like";

export function extractJsTags(
  raw: string,
  file: string,
  language: "js" | "jsx",
) {
  return extractJsLikeTags(raw, file, language);
}
