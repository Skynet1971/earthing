#!/usr/bin/env python3
"""Build a full-width website (GitHub Pages) from the generated wiki pages.

The GitHub wiki has a fixed page width set by GitHub. This site shows the same pages, animations and
PDFs using the whole browser width. Usage: python3 tools/build_wiki.py && python3 tools/build_site.py
Output: site/ (index.html, one .html per wiki page, img/, pdf/).
"""
import re, sys, html, shutil, pathlib   # standard library
import markdown   # python-markdown (pip install markdown)

ROOT = pathlib.Path(__file__).resolve().parent.parent   # repository root
WIKI, SITE = ROOT / "wiki", ROOT / "site"   # input and output folders
ALERT = {"TIP": ("tip", "💡 Tip"), "CAUTION": ("caution", "⛔ Caution"), "WARNING": ("warning", "⚠️ Warning"),
         "NOTE": ("note", "ℹ️ Note"), "IMPORTANT": ("important", "📍 Important")}   # GitHub alert kinds -> CSS class and label

CSS = """
:root{--navy:#0F2A47;--ink:#1F2937;--muted:#6B7280;--line:#E5E7EB;--paper:#F8FAFC;--green:#2F9E44;--amber:#D97706;--red:#DC2626;--blue:#2563EB;--purple:#7C3AED;--teal:#0E7490}
*{box-sizing:border-box}body{margin:0;font-family:"Segoe UI",Helvetica,Arial,sans-serif;color:var(--ink);background:#fff;font-size:17px;line-height:1.6}
.top{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:16px;padding:10px 24px;background:var(--navy);color:#fff;
 border-bottom:6px solid transparent;border-image:repeating-linear-gradient(45deg,#2F9E44 0 12px,#FACC15 12px 24px) 6}
.top a{color:#fff;text-decoration:none;font-weight:700}.top .sp{flex:1}
.wrap{display:grid;grid-template-columns:300px 1fr;min-height:100vh}
nav{position:sticky;top:64px;align-self:start;height:calc(100vh - 64px);overflow:auto;padding:18px 18px 40px;background:var(--paper);border-right:1px solid var(--line);font-size:15px}
nav ul{padding-left:18px;margin:6px 0 14px}nav a{color:var(--blue);text-decoration:none}nav a:hover{text-decoration:underline}
main{padding:24px 40px 80px;min-width:0}
main img{max-width:100%;height:auto}
h1{font-size:34px;color:var(--navy);margin:.3em 0}h2{font-size:26px;color:var(--navy);border-bottom:2px solid var(--line);padding-bottom:6px;margin-top:1.6em}h3{font-size:20px;color:var(--teal)}
table{border-collapse:collapse;width:100%;margin:12px 0 20px}th{background:var(--navy);color:#fff;text-align:left}th,td{padding:8px 10px;border:1px solid var(--line);vertical-align:top}
tr:nth-child(even) td{background:var(--paper)}
blockquote{margin:12px 0;padding:8px 16px;border-left:5px solid var(--line);background:var(--paper);color:var(--muted)}
.alert{margin:14px 0;padding:10px 16px;border-left:6px solid;border-radius:8px}.alert .t{font-weight:700;margin:0 0 4px}
.tip{border-color:var(--green);background:#E9F7EC}.tip .t{color:var(--green)}.caution{border-color:var(--red);background:#FDECEC}.caution .t{color:var(--red)}
.warning{border-color:var(--amber);background:#FEF4E2}.warning .t{color:var(--amber)}.note{border-color:var(--blue);background:#E8F0FE}.note .t{color:var(--blue)}
.important{border-color:var(--purple);background:#F1EAFE}.important .t{color:var(--purple)}
sup a{font-size:12px;color:var(--blue);text-decoration:none}
@media (max-width:900px){.wrap{grid-template-columns:1fr}nav{position:static;height:auto;border-right:0;border-bottom:1px solid var(--line)}main{padding:16px}}
"""   # full-width layout: menu on the left, content uses the rest of the screen

def alerts(md):
    """Turn GitHub alert blocks (> [!TIP] ...) into coloured HTML boxes."""
    out, lines, i = [], md.split("\n"), 0   # result, input lines, position
    while i < len(lines):   # walk the lines
        m = re.match(r"^> \[!(\w+)\]\s*$", lines[i])   # start of an alert
        if m and m.group(1) in ALERT:   # a known alert kind
            body = []; i += 1   # collect its lines
            while i < len(lines) and lines[i].startswith(">"): body.append(lines[i][1:].lstrip()); i += 1   # strip the quote marker
            cls, label = ALERT[m.group(1)]   # style
            inner = markdown.markdown("\n".join(body), extensions=["tables"])   # render the body
            out += ["", f'<div class="alert {cls}"><p class="t">{label}</p>{inner}</div>', ""]   # HTML box
            continue   # next line already loaded
        out.append(lines[i]); i += 1   # ordinary line
    return "\n".join(out)   # converted text

def links(h):
    """Point wiki page links at the .html files (Home -> index.html)."""
    def fix(m):   # one href
        u = m.group(1)   # link target
        if u.startswith(("http", "#", "img/", "pdf/", "mailto:")) or "." in u.split("#")[0]: return m.group(0)   # leave files and external links
        page, _, frag = u.partition("#")   # page and anchor
        return f'href="{"index" if page == "Home" else page}.html{"#" + frag if frag else ""}"'   # local page
    return re.sub(r'href="([^"]+)"', fix, h)   # rewrite every href

def page(title, nav, body):
    """Wrap one page in the site layout."""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{html.escape(title)}</title><style>{CSS}</style></head><body>'
            f'<div class="top"><a href="index.html">⚡ Earthing, bonding, surge &amp; lightning protection</a><span class="sp"></span>'
            f'<a href="PDF-library.html">📥 PDF library</a><a href="Sources.html">📖 Sources</a></div>'
            f'<div class="wrap"><nav>{nav}</nav><main>{body}</main></div></body></html>')   # document

def main():
    if SITE.exists(): shutil.rmtree(SITE)   # rebuilt from scratch
    SITE.mkdir(); shutil.copytree(WIKI / "img", SITE / "img"); shutil.copytree(WIKI / "pdf", SITE / "pdf")   # assets
    nav = links(markdown.markdown((WIKI / "_Sidebar.md").read_text()))   # menu from the wiki sidebar
    n = 0   # page count
    for f in sorted(WIKI.glob("*.md")):   # every wiki page
        if f.name.startswith("_"): continue   # sidebar is not a page
        md = alerts(f.read_text())   # coloured boxes
        body = links(markdown.markdown(md, extensions=["tables", "toc", "md_in_html"]))   # HTML body
        name = "index" if f.stem == "Home" else f.stem   # output file name
        title = re.search(r"^# (.+)$", f.read_text(), re.M)   # first heading as the browser title
        (SITE / f"{name}.html").write_text(page(title.group(1) if title else f.stem, nav, body)); n += 1   # write the page
    print(f"site: {n} pages -> site/ (open site/index.html)")   # summary

if __name__ == "__main__":
    main()   # run when called as a script
