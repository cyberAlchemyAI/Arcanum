import { createHash } from "node:crypto";

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.HtmlCanonicalizer
 *     type: Service
 *
 * M0c — the shared HTML canonicalizer (SWU-M0c). One module used on BOTH sides of
 * the proposer/validator seam, so a candidate's structural identity is stable and
 * the admission verdict is deterministic (DEC-MUTATION-EXEC-015). Pure, clock-free,
 * dependency-free. NOT a renderer — it normalizes structure for diff/attribution.
 *
 * Identity: domainspec-html-canon v1.4.0 (attribute-order normalization, whitespace
 * collapse, void-element normalization, od-id preservation).
 */
export const CANONICALIZER_IDENTITY = {
  name: "domainspec-html-canon",
  version: "1.4.0",
} as const;

const VOID_ELEMENTS = new Set([
  "area", "base", "br", "col", "embed", "hr", "img", "input",
  "link", "meta", "param", "source", "track", "wbr",
]);
const RAW_TEXT_ELEMENTS = new Set(["style", "script"]);

export interface CanonElement {
  readonly type: "element";
  readonly tag: string;
  readonly attrs: ReadonlyMap<string, string>;
  readonly children: readonly CanonNode[];
  /** Raw text for <style>/<script>; null otherwise. */
  readonly rawText: string | null;
}
export interface CanonText {
  readonly type: "text";
  readonly text: string;
}
export type CanonNode = CanonElement | CanonText;

interface MutableElement {
  type: "element";
  tag: string;
  attrs: Map<string, string>;
  children: CanonNode[];
  rawText: string | null;
}

/** Parse HTML into a canonical tree (whitespace-collapsed, attrs lowercased). */
export function parseHtml(html: string): readonly CanonNode[] {
  let i = 0;
  const root: CanonNode[] = [];
  const stack: MutableElement[] = [];
  const push = (n: CanonNode) => {
    const top = stack[stack.length - 1];
    (top ? top.children : root).push(n);
  };

  while (i < html.length) {
    const lt = html.indexOf("<", i);
    if (lt === -1) {
      pushText(html.slice(i));
      break;
    }
    if (lt > i) pushText(html.slice(i, lt));

    // comment
    if (html.startsWith("<!--", lt)) {
      const end = html.indexOf("-->", lt + 4);
      i = end === -1 ? html.length : end + 3;
      continue;
    }
    // doctype / declaration
    if (html[lt + 1] === "!") {
      const end = html.indexOf(">", lt);
      i = end === -1 ? html.length : end + 1;
      continue;
    }
    const gt = html.indexOf(">", lt);
    if (gt === -1) {
      pushText(html.slice(lt));
      break;
    }
    const rawTag = html.slice(lt + 1, gt).trim();
    i = gt + 1;

    if (rawTag.startsWith("/")) {
      const name = rawTag.slice(1).trim().toLowerCase();
      for (let s = stack.length - 1; s >= 0; s--) {
        if (stack[s]!.tag === name) {
          while (stack.length > s) finalize(stack.pop()!);
          break;
        }
      }
      continue;
    }

    const selfClose = rawTag.endsWith("/");
    const body = selfClose ? rawTag.slice(0, -1).trim() : rawTag;
    const { tag, attrs } = parseTag(body);
    const el: MutableElement = { type: "element", tag, attrs, children: [], rawText: null };

    if (VOID_ELEMENTS.has(tag) || selfClose) {
      push(freeze(el));
      continue;
    }
    if (RAW_TEXT_ELEMENTS.has(tag)) {
      const close = html.toLowerCase().indexOf(`</${tag}`, i);
      const end = close === -1 ? html.length : close;
      el.rawText = collapseWs(html.slice(i, end));
      const after = html.indexOf(">", end);
      i = after === -1 ? html.length : after + 1;
      push(freeze(el));
      continue;
    }
    stack.push(el);
  }
  while (stack.length) finalize(stack.pop()!);
  return root;

  function pushText(raw: string) {
    const t = collapseWs(raw);
    if (t.length > 0) push({ type: "text", text: t });
  }
  function finalize(el: MutableElement) {
    const top = stack[stack.length - 1];
    (top ? top.children : root).push(freeze(el));
  }
}

function parseTag(body: string): { tag: string; attrs: Map<string, string> } {
  const m = /^([a-zA-Z][\w:-]*)/.exec(body);
  const tag = (m?.[1] ?? body).toLowerCase();
  const attrs = new Map<string, string>();
  const attrRe = /([a-zA-Z_:][-\w:.]*)(?:\s*=\s*("[^"]*"|'[^']*'|[^\s"'>]+))?/g;
  attrRe.lastIndex = m ? m[0].length : 0;
  let a: RegExpExecArray | null;
  while ((a = attrRe.exec(body)) !== null) {
    const name = a[1]!.toLowerCase();
    let val = a[2] ?? "";
    if (val.length >= 2 && (val[0] === '"' || val[0] === "'")) val = val.slice(1, -1);
    if (!attrs.has(name)) attrs.set(name, val);
  }
  return { tag, attrs };
}

function collapseWs(s: string): string {
  return s.replace(/\s+/g, " ").trim();
}

function freeze(el: MutableElement): CanonElement {
  return { type: "element", tag: el.tag, attrs: el.attrs, children: el.children, rawText: el.rawText };
}

/** Deterministic serialization: sorted attributes, normalized whitespace. */
export function serialize(nodes: readonly CanonNode[]): string {
  return nodes.map(serializeNode).join("");
}
function serializeNode(n: CanonNode): string {
  if (n.type === "text") return n.text;
  const names = [...n.attrs.keys()].sort();
  const attrs = names.map((k) => ` ${k}="${n.attrs.get(k) ?? ""}"`).join("");
  if (VOID_ELEMENTS.has(n.tag)) return `<${n.tag}${attrs}>`;
  if (n.rawText !== null) return `<${n.tag}${attrs}>${n.rawText}</${n.tag}>`;
  return `<${n.tag}${attrs}>${serialize(n.children)}</${n.tag}>`;
}

/** Canonical HTML string — idempotent: canonicalizeHtml(canonicalizeHtml(x)) === canonicalizeHtml(x). */
export function canonicalizeHtml(html: string): string {
  return serialize(parseHtml(html));
}

/** Stable content hash over the canonical form. */
export function canonicalHash(html: string): string {
  return createHash("sha256").update(canonicalizeHtml(html), "utf8").digest("hex");
}
