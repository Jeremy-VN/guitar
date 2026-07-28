#!/usr/bin/env python3
"""Regenerate the site's contents pages from lessons.json.

Writes:
  index.html          - the top-level "Jeremy's Guitar" contents page
  lessons/index.html  - the dated lesson list

Run:  python3 build_index.py
"""
import json, html, pathlib

here = pathlib.Path(__file__).parent
lessons = json.loads((here / "lessons.json").read_text(encoding="utf-8"))
lessons.sort(key=lambda l: l["date"], reverse=True)          # newest first


def esc(s):
    return html.escape(str(s), quote=True)


# Shared look, so every contents page matches the lesson pages.
CSS = """  :root{--bg:#0f1115;--panel:#171a21;--panel2:#1e222b;--ink:#e8eaed;--muted:#9aa3b2;
    --accent:#e0b341;--accent2:#5aa9e6;--line:#2a2f3a;}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
  .wrap{max-width:820px;margin:0 auto;padding:40px 22px 90px;}
  header{border-bottom:1px solid var(--line);padding-bottom:22px;margin-bottom:26px;}
  h1{font-size:30px;margin:0 0 6px;letter-spacing:.3px;}
  .sub{color:var(--muted);font-size:14px;margin:0;}
  .back{display:inline-block;font-size:13.5px;margin-bottom:12px;color:var(--accent2);text-decoration:none;}
  .card{display:block;text-decoration:none;color:inherit;background:var(--panel);
    border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:14px 0;
    transition:border-color .15s ease, transform .15s ease, background .15s ease;}
  .card:hover{border-color:var(--accent2);background:#191d27;transform:translateY(-2px);}
  .date,.kind{display:inline-block;font-size:12.5px;font-weight:600;color:var(--accent);
    background:#231d0e;border:1px solid #4a3d18;border-radius:20px;padding:2px 11px;margin-bottom:10px;}
  .card h2{font-size:19px;margin:2px 0 6px;line-height:1.3;color:var(--ink);}
  .summary{color:#c4cad6;font-size:14.5px;margin:0 0 12px;}
  .tags{margin-bottom:10px;}
  .tag{display:inline-block;font-size:12px;color:var(--muted);background:var(--panel2);
    border:1px solid var(--line);border-radius:6px;padding:2px 8px;margin:0 5px 5px 0;}
  .open{font-size:13.5px;font-weight:600;color:var(--accent2);}
  .empty{color:var(--muted);}
  footer{margin-top:40px;color:var(--muted);font-size:12.5px;border-top:1px solid var(--line);padding-top:16px;}"""


def page(title, h1, sub, body, back=None, footer=""):
    back_html = f'    <a class="back" href="{back[1]}">&larr; {esc(back[0])}</a>\n' if back else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<style>
{CSS}
</style>
</head>
<body>
<div class="wrap">
  <header>
{back_html}    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
  </header>

{body}

  <footer>{footer}</footer>
</div>
</body>
</html>
"""


# ---------------------------------------------------------------- lessons page
cards = []
for l in lessons:
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in l.get("tags", []))
    # lessons.json stores repo-relative paths; this page already lives in lessons/
    href = l["file"].split("/")[-1]
    cards.append(f"""    <a class="card" href="{esc(href)}">
      <div class="date">{esc(l.get("date_display", l["date"]))}</div>
      <h2>{esc(l["title"])}</h2>
      <p class="summary">{esc(l["summary"])}</p>
      <div class="tags">{tags}</div>
      <span class="open">Open lesson &rarr;</span>
    </a>""")

count = len(lessons)
lessons_body = "\n".join(cards) if cards else '  <p class="empty">No lessons yet.</p>'
(here / "lessons").mkdir(exist_ok=True)
(here / "lessons" / "index.html").write_text(
    page(
        title="Guitar Lessons",
        h1="&#127928; Lessons",
        sub=f"{count} lesson{'s' if count != 1 else ''} &middot; tap a card to open",
        body=lessons_body,
        back=("Jeremy's Guitar", "../index.html"),
        footer="Each lesson is a self-contained page with audio references built in.",
    ),
    encoding="utf-8",
)

# ------------------------------------------------------------------- hub page
SECTIONS = [
    {
        "href": "lessons/index.html",
        "kind": "Lessons",
        "title": "Lessons",
        "summary": "Every lesson written up in full &mdash; theory, tab, and a play button on every "
                   f"box so you can hear the shape. {count} lesson{'s' if count != 1 else ''} so far.",
        "tags": ["Theory", "Tab", "Audio"],
        "open": "Open lessons",
    },
    {
        "href": "practice/index.html",
        "kind": "Practice",
        "title": "Practice Tools",
        "summary": "Fretboard note trainer, ear trainer, and the evidence review on how to practise "
                   "this properly. Runs in the browser, tracks your accuracy over time.",
        "tags": ["Fretboard", "Ear training", "Method"],
        "open": "Open practice tools",
    },
    {
        "href": "reference/index.html",
        "kind": "Reference",
        "title": "Reference",
        "summary": "The things worth looking up rather than memorising &mdash; the fretboard map, "
                   "octave and unison shapes, and capo maths.",
        "tags": ["Fretboard map", "Octaves", "Capo"],
        "open": "Open reference",
    },
]

hub_cards = []
for s in SECTIONS:
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in s["tags"])
    hub_cards.append(f"""    <a class="card" href="{s["href"]}">
      <div class="kind">{s["kind"]}</div>
      <h2>{s["title"]}</h2>
      <p class="summary">{s["summary"]}</p>
      <div class="tags">{tags}</div>
      <span class="open">{s["open"]} &rarr;</span>
    </a>""")

(here / "index.html").write_text(
    page(
        title="Jeremy's Guitar",
        h1="&#127928; Jeremy's Guitar",
        sub="Lessons, practice tools and reference &middot; everything runs in the browser",
        body="\n".join(hub_cards),
        footer="Built as I go. Lesson pages and practice tools are self-contained &mdash; "
               "nothing to install, works offline once loaded.",
    ),
    encoding="utf-8",
)

print(f"Wrote index.html (hub) and lessons/index.html with {count} lesson card(s).")
