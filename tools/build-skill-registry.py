#!/usr/bin/env python3
"""Build the public skill registry page + per-skill download zips.

Reads every skill folder under the four Arcanum tiers, extracts metadata from
its manifest (SKILL.md preferred, README.md fallback — handling YAML frontmatter
or a prose Identity/Purpose section), zips each skill MINUS its `development/`
package (the dev/experiment surface, never a runtime dependency), and emits
`docs/registry.html`.

Re-run this whenever skills change; never hand-edit the generated rows.
Stdlib only.
"""
from __future__ import annotations

import html
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # arcanum/
DOCS = ROOT / "docs"
DL = DOCS / "downloads"

TIERS = [
    ("arcana", "Arcana", "Sigils — single governed capabilities."),
    ("spells", "Spells", "Composed multi-sigil workflows."),
    ("formulae", "Formulae", "Foundational techniques sigils build on."),
    ("transmutations", "Transmutations", "Cross-cutting transforms."),
]

EXCLUDE_DIRS = {"development", "__pycache__", ".git", "node_modules"}
EXCLUDE_FILES = {".DS_Store"}

REPO = "cyberAlchemyAI/Arcanum"


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip().strip('"').strip("'")
    return fm


def strip_fm(text: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)


def section_para(text: str, heading_re: str) -> str:
    """First real paragraph under a markdown heading matching heading_re."""
    m = re.search(rf"^#{{1,4}}\s*{heading_re}.*?$", text, re.I | re.M)
    if not m:
        return ""
    rest = text[m.end():]
    for block in re.split(r"\n\s*\n", rest):
        b = block.strip()
        if not b:
            continue
        if b.startswith("#"):
            break
        if b.startswith(("-", "|", ">")):
            continue
        b = re.sub(r"<[^>]+>", "", b).strip()
        if b:
            return b
    return ""


def first_para(text: str) -> str:
    for block in re.split(r"\n\s*\n", text):
        b = block.strip()
        if not b or b.startswith(("#", "-", "|", ">")):
            continue
        b = re.sub(r"<[^>]+>", "", b).strip()
        if b:
            return b
    return ""


def clean_desc(d: str) -> str:
    d = re.sub(r"\s+", " ", d).strip()
    # frontmatter descriptions often start "Use when: ..." — keep as-is.
    if len(d) > 280:
        d = d[:277].rstrip() + "…"
    return d


def extract(skill_dir: Path, tier: str) -> dict | None:
    manifest = None
    for cand in ("SKILL.md", "README.md"):
        if (skill_dir / cand).is_file():
            manifest = skill_dir / cand
            break
    if manifest is None:
        return None  # no runtime contract (e.g. integration-spec: dev-only)

    text = manifest.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(text)
    body = strip_fm(text)

    name = fm.get("name") or ""
    if not name:
        m = re.search(r"Canonical ID:\s*`?([\w-]+)`?", body)
        name = m.group(1) if m else skill_dir.name

    desc = fm.get("description") or section_para(body, r"Purpose") or first_para(body)
    desc = clean_desc(desc) or "(no description)"

    version = fm.get("version") or "—"
    domain = fm.get("domain") or ""

    has_dev = (skill_dir / "development").is_dir()
    return {
        "slug": skill_dir.name,
        "name": name,
        "tier": tier,
        "desc": desc,
        "version": version,
        "domain": domain,
        "path": f"{tier}/{skill_dir.name}",
        "has_dev": has_dev,
    }


def build_zip(skill_dir: Path, out_zip: Path) -> tuple[int, int]:
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    files = 0
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(skill_dir.rglob("*")):
            rel = p.relative_to(skill_dir)
            if any(part in EXCLUDE_DIRS for part in rel.parts):
                continue
            if p.is_file() and p.name not in EXCLUDE_FILES:
                z.write(p, str(Path(skill_dir.name) / rel))
                files += 1
    return files, out_zip.stat().st_size


def human_size(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.0f} KB"
    return f"{n / (1024 * 1024):.1f} MB"


NAV = [
    ("index.html", "Home"),
    ("system.html", "The System"),
    ("saturn.html", "Saturn"),
    ("craft.html", "Craft"),
    ("method.html", "Method"),
    ("registry.html", "Skills"),
    ("paper.html", "Paper"),
    ("blog.html", "Blog"),
    ("who-we-are.html", "About"),
]


def nav_html(active: str) -> str:
    out = ['    <nav id="primary-nav" aria-label="Primary navigation">']
    for href, label in NAV:
        cls = ' class="active" aria-current="page"' if href == active else ""
        out.append(f'      <a href="{href}"{cls}>{label}</a>')
    out.append("    </nav>")
    return "\n".join(out)


def card(s: dict) -> str:
    e = html.escape
    zip_href = f"downloads/{s['tier']}/{s['slug']}.zip"
    dev_tag = (
        '<span class="mini" title="The development/ experiment package is excluded from the download">dev package excluded</span>'
        if s["has_dev"]
        else ""
    )
    domain = f'<span class="mini">{e(s["domain"])}</span>' if s["domain"] else ""
    return f"""        <article class="card" data-search="{e((s['slug'] + ' ' + s['name'] + ' ' + s['desc'] + ' ' + s['domain']).lower())}">
          <div class="card-head">
            <code class="cname">{e(s['name'])}</code>
            <span class="ver">{e(s['version'])}</span>
          </div>
          <p class="cdesc">{e(s['desc'])}</p>
          <div class="meta">{domain}{dev_tag}<span class="mini">{s['files']} files · {human_size(s['size'])}</span></div>
          <div class="cactions">
            <a class="dl" href="{zip_href}" download>⬇ {e(s['slug'])}.zip</a>
            <a class="src" href="https://github.com/{REPO}/tree/main/{s['path']}">Source ↗</a>
          </div>
        </article>"""


def render(skills: list[dict], skipped: list[str]) -> str:
    by_tier = {t[0]: [s for s in skills if s["tier"] == t[0]] for t in TIERS}
    total = len(skills)

    subnav_links = " ".join(
        f'<a href="#{tid}">{label} <span class="ct">{len(by_tier[tid])}</span></a>'
        for tid, label, _ in TIERS
    )

    sections = []
    for tid, label, blurb in TIERS:
        rows = sorted(by_tier[tid], key=lambda s: s["slug"])
        cards = "\n".join(card(s) for s in rows)
        sections.append(f"""    <section id="{tid}">
      <div class="inner">
        <div class="section-head">
          <p class="eyebrow">{label} · {len(rows)}</p>
          <h2>{label}</h2>
          <p>{html.escape(blurb)}</p>
        </div>
        <div class="cards">
{cards}
        </div>
      </div>
    </section>""")

    skipped_note = ""
    if skipped:
        skipped_note = (
            '<p class="note">Not yet released (development-only, no runtime contract): '
            + ", ".join(f"<code>{html.escape(x)}</code>" for x in skipped)
            + ".</p>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="The Arcanum skill registry — download any sigil, spell, formula, or transmutation on its own. Generated from each skill's manifest.">
  <title>Skill registry — CyberAlchemy</title>
  <style>
    :root {{
      --ink:#151515; --muted:#626262; --paper:#fdfaf3; --surface:#fffdf8;
      --line:#e3ded2; --red:#e60023; --orange:#e85d18; --teal:#088f8a;
      --green:#2f8b57; --blue:#2e6bb8; --violet:#5c55b8;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color-scheme: light;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ margin:0; background:var(--paper); color:var(--ink); }}
    a {{ color: inherit; }}
    .topbar {{ position:fixed; top:0; left:0; right:0; z-index:20; display:flex; justify-content:space-between; align-items:center; gap:18px; padding:14px clamp(18px,4vw,52px); background:rgba(253,250,243,.88); border-bottom:1px solid rgba(227,222,210,.84); backdrop-filter:blur(14px); }}
    .brand {{ display:inline-flex; align-items:center; gap:11px; min-width:180px; font-weight:850; text-decoration:none; }}
    .brand img {{ width:34px; height:34px; object-fit:contain; }}
    nav {{ display:flex; justify-content:flex-end; flex-wrap:wrap; gap:6px; }}
    nav a {{ min-height:34px; padding:7px 10px; border-radius:6px; color:var(--muted); text-decoration:none; font-size:13px; font-weight:760; }}
    nav a:hover {{ background:#f2eee3; color:var(--ink); }}
    nav a.active {{ color:var(--ink); background:#f2eee3; box-shadow:inset 0 -2px 0 var(--red); }}
    .nav-toggle {{ display:none; align-items:center; justify-content:center; width:42px; height:36px; padding:0; border:1px solid var(--line); border-radius:7px; background:var(--surface); color:var(--ink); font-size:17px; line-height:1; cursor:pointer; }}
    .nav-toggle:hover {{ background:#f2eee3; }}
    @media (max-width:940px) {{
      .topbar {{ flex-direction:row; flex-wrap:wrap; align-items:center; }}
      .nav-toggle {{ display:inline-flex; }}
      .topbar nav {{ display:none; width:100%; margin-top:8px; flex-direction:column; gap:2px; }}
      .topbar nav.open {{ display:flex; }}
      .topbar nav a {{ padding:11px 10px; font-size:15px; }}
    }}
    .subnav {{ position:fixed; top:61px; left:0; right:0; z-index:15; display:flex; flex-wrap:wrap; gap:4px 16px; align-items:center; padding:8px clamp(18px,5vw,70px); background:rgba(253,250,243,.93); border-bottom:1px solid var(--line); backdrop-filter:blur(10px); }}
    .subnav .on {{ color:var(--muted); font-size:11px; font-weight:850; letter-spacing:.08em; text-transform:uppercase; margin-right:2px; }}
    .subnav a {{ color:var(--muted); text-decoration:none; font-size:13px; font-weight:740; display:inline-flex; align-items:center; gap:5px; }}
    .subnav a:hover {{ color:var(--ink); }}
    .subnav .ct {{ font-size:11px; color:#fff; background:var(--muted); border-radius:999px; padding:0 6px; line-height:16px; }}
    section {{ padding:clamp(40px,6vw,70px) clamp(18px,5vw,70px); border-bottom:1px solid var(--line); scroll-margin-top:120px; }}
    .inner {{ max-width:1180px; margin:0 auto; }}
    .hero {{ padding:128px clamp(18px,5vw,70px) 40px; border-bottom:1px solid var(--line); background:#fbf8ef; }}
    .hero .inner {{ max-width:1180px; }}
    .eyebrow {{ display:inline-flex; gap:8px; margin:0 0 16px; color:var(--red); font-size:13px; font-weight:850; text-transform:uppercase; }}
    h1,h2,h3 {{ margin:0; letter-spacing:0; }}
    h1 {{ font-size:clamp(40px,6vw,76px); line-height:.95; max-width:900px; }}
    h2 {{ font-size:clamp(24px,3.2vw,40px); line-height:1.05; }}
    p {{ margin:0; color:var(--muted); font-size:16px; line-height:1.62; }}
    .lead {{ max-width:760px; margin-top:20px; color:#2c2c2c; font-size:clamp(18px,2.2vw,22px); line-height:1.55; }}
    .tools {{ display:flex; flex-wrap:wrap; gap:12px; align-items:center; margin-top:24px; }}
    #q {{ flex:1; min-width:240px; max-width:460px; padding:12px 15px; border:1px solid var(--line); border-radius:8px; background:var(--surface); font:inherit; font-size:15px; color:var(--ink); }}
    .count {{ font-size:14px; color:var(--muted); font-weight:700; }}
    .section-head {{ margin-bottom:22px; }}
    .section-head p {{ max-width:720px; margin-top:10px; }}
    .cards {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:14px; }}
    .card {{ display:flex; flex-direction:column; padding:18px; border:1px solid var(--line); border-radius:10px; background:var(--surface); box-shadow:0 8px 22px rgba(22,22,22,.05); }}
    .card-head {{ display:flex; justify-content:space-between; align-items:baseline; gap:10px; }}
    .cname {{ font-size:16px; font-weight:800; color:var(--ink); font-family:ui-monospace, SFMono-Regular, Menlo, monospace; }}
    .ver {{ font-size:12px; color:var(--muted); font-weight:750; white-space:nowrap; }}
    .cdesc {{ margin-top:9px; font-size:14px; color:#383838; line-height:1.5; flex:1; }}
    .meta {{ display:flex; flex-wrap:wrap; gap:6px; margin-top:12px; }}
    .mini {{ font-size:11px; font-weight:750; color:#6f5a3c; background:#f1eadc; border-radius:999px; padding:3px 8px; }}
    .cactions {{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-top:14px; }}
    .dl {{ display:inline-flex; align-items:center; min-height:38px; padding:8px 14px; border-radius:7px; background:var(--ink); color:#fff; text-decoration:none; font-weight:800; font-size:14px; }}
    .dl:hover {{ background:#000; }}
    .src {{ font-size:13px; font-weight:740; color:var(--blue); text-decoration:none; }}
    .src:hover {{ text-decoration:underline; }}
    .note {{ margin-top:18px; font-size:13px; color:var(--muted); }}
    .note code, .install code {{ background:#f1eadc; border-radius:4px; padding:1px 5px; font-size:12px; }}
    .install {{ margin-top:18px; padding:16px 18px; border:1px solid var(--line); border-radius:10px; background:var(--surface); }}
    .install code.block {{ display:block; margin-top:8px; padding:12px 14px; background:#151515; color:#fdfaf3; border-radius:7px; font-size:12.5px; overflow-x:auto; white-space:pre; }}
    .empty {{ color:var(--muted); font-size:14px; padding:14px 0; }}
    .footer {{ padding:28px clamp(18px,5vw,70px); background:#151515; color:#fdfaf3; }}
    .footer p {{ color:#c7c1b5; }}
    @media (max-width:680px) {{ .topbar {{ position:static; align-items:flex-start; flex-direction:column; }} nav {{ justify-content:flex-start; }} .subnav {{ position:static; }} .hero {{ padding-top:40px; }} }}
  </style>
</head>
<body id="top">
  <header class="topbar">
    <a class="brand" href="index.html" aria-label="CyberAlchemy home">
      <img src="assets/cyberalchemy-mark.svg" alt="">
      <span>CyberAlchemy</span>
    </a>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false" aria-controls="primary-nav">☰</button>
{nav_html("registry.html")}
  </header>
  <div class="subnav"><span class="on">Tiers</span> {subnav_links}</div>

  <main>
    <section class="hero">
      <div class="inner">
        <p class="eyebrow">Skill registry</p>
        <h1>Download any Arcanum skill on its own.</h1>
        <p class="lead">{total} skills across four tiers. Each download is the skill's runtime surface — manifest, templates, scripts, tools — with the <code>development/</code> experiment package stripped out. Drop one into <code>.claude/skills/</code> or <code>.agents/skills/</code> and it is discoverable.</p>
        <div class="tools">
          <input id="q" type="search" placeholder="Filter skills by name, purpose, or domain…" aria-label="Filter skills">
          <span class="count" id="count">{total} shown</span>
        </div>
        <div class="install">
          Prefer to wire every skill into your agent at once? One command installs the whole library into Claude Code and Codex:
          <code class="block">curl -fsSL https://raw.githubusercontent.com/{REPO}/main/tools/install_arcanum.sh | bash -s -- --target . --profiles claude,repo-codex --sigils all --spells all</code>
        </div>
        {skipped_note}
      </div>
    </section>

{chr(10).join(sections)}
    <p class="empty" id="empty" style="display:none; padding:40px clamp(18px,5vw,70px);">No skills match your filter.</p>
  </main>

  <footer class="footer">
    <div class="inner">
      <h3>CyberAlchemy</h3>
      <p>Generated from each skill's manifest by <code>tools/build-skill-registry.py</code>. Re-run on change — never hand-edited.</p>
      <p style="margin-top:12px"><a href="https://www.linkedin.com/in/vladimir-rondelli/" style="color:#fdfaf3;font-weight:820;text-decoration:underline">Work with me → LinkedIn</a></p>
    </div>
  </footer>

  <script>
    (function () {{
      var b = document.querySelector('.nav-toggle');
      var n = document.querySelector('.topbar nav');
      if (b && n) {{
        b.addEventListener('click', function () {{
          var open = n.classList.toggle('open');
          b.setAttribute('aria-expanded', open ? 'true' : 'false');
        }});
        n.addEventListener('click', function (e) {{
          if (e.target.tagName === 'A') {{ n.classList.remove('open'); b.setAttribute('aria-expanded', 'false'); }}
        }});
      }}
    }})();
    const q = document.getElementById('q');
    const count = document.getElementById('count');
    const empty = document.getElementById('empty');
    const cards = Array.from(document.querySelectorAll('.card'));
    const sections = Array.from(document.querySelectorAll('main section[id]'));
    function apply() {{
      const t = q.value.trim().toLowerCase();
      let shown = 0;
      cards.forEach(c => {{
        const hit = !t || c.dataset.search.includes(t);
        c.style.display = hit ? '' : 'none';
        if (hit) shown++;
      }});
      sections.forEach(s => {{
        const any = s.querySelectorAll('.card:not([style*="none"])').length;
        s.style.display = any ? '' : 'none';
      }});
      empty.style.display = shown ? 'none' : '';
      count.textContent = shown + (shown === 1 ? ' shown' : ' shown');
    }}
    q.addEventListener('input', apply);
  </script>
</body>
</html>
"""


def main() -> int:
    skills: list[dict] = []
    skipped: list[str] = []

    for tid, _, _ in TIERS:
        tdir = ROOT / tid
        if not tdir.is_dir():
            continue
        for sdir in sorted(tdir.iterdir()):
            if not sdir.is_dir() or sdir.name == "templates":
                continue
            meta = extract(sdir, tid)
            if meta is None:
                skipped.append(f"{tid}/{sdir.name}")
                continue
            files, size = build_zip(sdir, DL / tid / f"{sdir.name}.zip")
            meta["files"] = files
            meta["size"] = size
            skills.append(meta)

    (DOCS / "registry.html").write_text(render(skills, skipped), encoding="utf-8")

    print(f"registry.html written · {len(skills)} skills · {len(skipped)} skipped")
    by_tier: dict[str, int] = {}
    for s in skills:
        by_tier[s["tier"]] = by_tier.get(s["tier"], 0) + 1
    for tid, label, _ in TIERS:
        print(f"  {label:<16} {by_tier.get(tid, 0)}")
    if skipped:
        print("  skipped (dev-only): " + ", ".join(skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
