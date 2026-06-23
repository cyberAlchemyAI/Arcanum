#!/usr/bin/env python3
"""Render manuscript.md into the reading-learning-package HTML template.

Honors templates/learning-package.html ({{title}} / {{body}}) as the base and
augments its stylesheet for code blocks, tables, and the analogy callout so the
package is print-ready.
"""
import pathlib
import markdown

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE.parents[1] / "templates" / "learning-package.html"
MANUSCRIPT = HERE / "manuscript.md"
OUT = HERE / "learning-package.html"

TITLE = "Craft + Goal in Five Minutes"

EXTRA_CSS = """
    main { max-width: 820px; }
    h1 { margin-bottom: 0.2rem; }
    h3 { color: #46525c; font-weight: 500; margin-top: 0; }
    h2 { margin-top: 2.2rem; border-bottom: 1px solid #e3e8ee; padding-bottom: 0.3rem; }
    pre { background: #0f172a; color: #e2e8f0; padding: 1rem; border-radius: 8px;
          overflow-x: auto; line-height: 1.4; font-size: 0.9rem; }
    pre code { background: none; padding: 0; color: inherit; }
    blockquote { border-left: 4px solid #546a7b; padding: 0.4rem 1rem; margin: 1.4rem 0;
                 background: #f5f8fb; color: #2b3a44; }
    table { border-collapse: collapse; width: 100%; margin: 1.2rem 0; font-size: 0.92rem; }
    th, td { border: 1px solid #d6dee6; padding: 0.45rem 0.6rem; text-align: left; vertical-align: top; }
    th { background: #eef2f7; }
    hr { border: none; border-top: 1px solid #e3e8ee; margin: 2rem 0; }
  </style>"""

body_html = markdown.markdown(
    MANUSCRIPT.read_text(encoding="utf-8"),
    extensions=["tables", "fenced_code", "sane_lists"],
)

html = TEMPLATE.read_text(encoding="utf-8")
html = html.replace("{{title}}", TITLE)
html = html.replace("  </style>", EXTRA_CSS, 1)
html = html.replace("{{body}}", body_html)
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT} ({len(html)} bytes)")
