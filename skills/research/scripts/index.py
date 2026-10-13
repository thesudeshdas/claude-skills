#!/usr/bin/env python3
"""Rebuild ~/research/index.html: a list of every research doc, newest first.

Reads the <title>, description and research:* meta tags from each top-level
*.html file. Run after writing or deleting a doc. Also writes
_assets/docs.js, the doc list research.js uses for the doc switcher and
the newer/older links (a script, not JSON, so it loads from file:// too).
"""
import html
import json
import os
import re
import sys
from pathlib import Path

out = Path(os.environ.get("RESEARCH_DIR", Path.home() / "research"))


def meta(src, name):
    m = re.search(r'<meta\s+name="%s"\s+content="([^"]*)"' % re.escape(name), src)
    return html.unescape(m.group(1)) if m else ""


docs = []
for path in out.glob("*.html"):
    if path.name == "index.html":
        continue
    src = path.read_text(encoding="utf-8", errors="replace")[:4000]
    t = re.search(r"<title>(.*?)</title>", src, re.S)
    docs.append({
        "file": path.name,
        "title": html.unescape(t.group(1).strip()) if t else path.stem,
        "desc": meta(src, "description"),
        "type": meta(src, "research:type") or "research",
        "date": meta(src, "research:date") or path.name[:10],
        "project": meta(src, "research:project"),
    })
docs.sort(key=lambda d: (d["date"], d["file"]), reverse=True)

esc = html.escape
types = sorted({d["type"] for d in docs})
items = "\n".join(
    f'<a class="card lib-item" href="{esc(d["file"])}" data-type-filter="{esc(d["type"])}">'
    f'<h3>{esc(d["title"])}</h3>'
    f'<span class="meta"><span class="type" data-type="{esc(d["type"])}">{esc(d["type"])}</span>'
    f'<span class="chip">{esc(d["date"])}</span>'
    + (f'<span class="chip">{esc(d["project"])}</span>' if d["project"] else "")
    + "</span>"
    + (f'<p>{esc(d["desc"])}</p>' if d["desc"] else "")
    + "</a>"
    for d in docs
)
buttons = '<button aria-pressed="true" data-f="">all</button>' + "".join(
    f'<button aria-pressed="false" data-f="{esc(t)}">{esc(t)}</button>' for t in types
)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>research</title>
<link rel="stylesheet" href="_assets/research.css">
<script src="_assets/research.js"></script>
</head>
<body>
<main class="wrap lib">
<header class="hero" style="padding:0">
  <h1>all <span class="grad">research</span></h1>
  <p class="lede">{len(docs)} doc{"" if len(docs) == 1 else "s"}, newest first</p>
</header>
<div class="filters">{buttons}</div>
<div class="lib-list">
{items or '<p class="muted">nothing here yet</p>'}
</div>
</main>
<script>
document.querySelectorAll(".filters button").forEach(function (b) {{
  b.addEventListener("click", function () {{
    document.querySelectorAll(".filters button").forEach(function (x) {{ x.setAttribute("aria-pressed", String(x === b)); }});
    document.querySelectorAll(".lib-item").forEach(function (i) {{ i.hidden = !!b.dataset.f && i.dataset.typeFilter !== b.dataset.f; }});
  }});
}});
</script>
</body>
</html>
"""
(out / "index.html").write_text(page, encoding="utf-8")

manifest = [{k: d[k] for k in ("file", "title", "type", "date", "project")} for d in docs]
(out / "_assets").mkdir(exist_ok=True)
(out / "_assets" / "docs.js").write_text(
    "window.RESEARCH_DOCS = " + json.dumps(manifest, ensure_ascii=False, indent=1) + ";\n",
    encoding="utf-8",
)
print(out / "index.html")
