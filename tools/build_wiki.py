#!/usr/bin/env python3
"""Generate the wiki (GitHub-flavoured markdown) from the same content as the PDFs.

Usage: python3 tools/build_wiki.py [--out wiki]
Writes wiki/Home.md, one page per public document, wiki/Sources.md, wiki/_Sidebar.md and the
diagrams as wiki/img/*.svg. Private documents are never written to the wiki.
"""
import re, sys, html, pathlib, datetime   # standard library
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))   # import sibling modules
import content as c   # catalogue, facts, citations
import diagrams   # diagram registry (exported as SVG)

REPO_URL = "https://github.com/Skynet1971/earthing"   # main repository (PDF links)
PDF_URL = "pdf/"   # PDFs are copied into the wiki itself (wiki/pdf/), so they open from the wiki
SERIES = "Earthing, Bonding, Surge & Lightning Protection Library"   # same series name as the PDFs
LABEL = {"do": "✅ **DO**", "dont": "⛔ **DO NOT**", "warn": "⚠️ **WARNING**", "note": "ℹ️ **NOTE**", "site": "📍 **CHECK ON SITE**"}   # callout labels

def page_name(doc):
    """Wiki page name for a document, e.g. '04-CCTV-cameras,-recorders-and-PoE-switches'."""
    t = re.sub(r"[^A-Za-z0-9 ,&()-]", "", doc["title"]).strip()   # keep wiki-safe characters
    return f'{doc["id"]}-' + t.replace(" ", "-")   # GitHub wiki page naming uses dashes for spaces

def md_inline(text):
    """Convert the small ReportLab markup subset used in content files to markdown."""
    t = str(text)   # work on a string
    t = re.sub(r"</?b>", "**", t); t = re.sub(r"</?i>", "*", t)   # bold and italic
    t = re.sub(r"<br\s*/?>", " ", t).replace("&nbsp;", " ")   # line breaks and non-breaking spaces
    t = re.sub(r"<sub>(.*?)</sub>", r"<sub>\1</sub>", t); t = re.sub(r"<super>(.*?)</super>", r"<sup>\1</sup>", t)   # sub/superscript
    return html.unescape(t)   # &amp; etc. back to characters

def chip(ref, page, section):
    """Citation as a small superscript link to the source list of the page."""
    return f'<sup>[R{ref} p.{page}](#sources-cited-on-this-page)</sup>'   # anchor generated from the heading below

def cell(text):
    """Table cell: inline markdown with pipes escaped."""
    return md_inline(text).replace("|", "\\|")   # a pipe would split the cell

def render_doc(doc, catalog, facts):
    """Return (markdown, cites) for one document."""
    cites = c.Cites(catalog, facts)   # citation tracker
    T = lambda s: md_inline(cites.expand(s, chip))   # author text with citations
    out = [f"> {SERIES} · **{doc.get('badge', '')}** · content version {doc.get('version', '1.0')}", "",
           f"# {doc['title']}", "", f"*{doc.get('subtitle', '')}*", "",
           f"**Applies to:** {doc.get('applies_to', '')}", "",
           f'<a href="{PDF_URL}{doc["id"]}_{doc["slug"]}.pdf"><img src="img/btn_{doc["id"]}.svg" height="64" alt="Download the PDF"></a> '
           f'<a href="PDF-library"><img src="img/btn_library.svg" height="64" alt="All PDFs"></a>', "",
           "> ℹ️ Information only. Every technical statement cites a source and PDF page; it does not replace the "
           "wiring code that applies at the site, the product manuals, or a qualified and registered person.", ""]   # page header
    for sec in doc["sections"]:   # every chapter
        out += [f"## {sec['title']}", ""]   # chapter heading
        if sec.get("lead"): out += [T(sec["lead"]), ""]   # intro paragraph
        for b in sec.get("blocks", []):   # blocks in order
            if "h2" in b: out += [f"### {b['h2']}", ""]   # sub-heading
            elif "p" in b: out += [T(b["p"]), ""]   # paragraph
            elif "meta" in b: out += [md_inline(b["meta"]), ""]   # text about the library itself
            elif "index" in b:   # table of the other public documents
                out += ["| Sheet | Title and scope | Wiki page |", "|---|---|---|"] + [f"| {cell(d.get('badge', d['id']))} | **{cell(d['title'])}** — {cell(d.get('applies_to', ''))} | [{d['id']}]({page_name(d)}) |" for d in c.load_docs() if not d.get("private") and d["id"] != doc["id"]] + [""]   # rows
            elif "facts" in b:   # cited fact bullets
                for item in b["facts"]:   # one bullet each
                    fid, wording = c.fact_text(facts, item)   # ID and wording
                    lab = cites.label(fid)   # citation (records the use)
                    body = T(wording) if isinstance(item, dict) else md_inline(html.escape(wording, quote=False))   # wording as markdown
                    out.append(f"- {body}{chip(*lab) if lab else ''}")   # bullet with chip
                out.append("")   # blank line after the list
            elif "callout" in b:   # GitHub alert block: coloured box with an icon
                cb = b["callout"]   # definition
                kind = {"do": "TIP", "dont": "CAUTION", "warn": "WARNING", "note": "NOTE", "site": "IMPORTANT"}[cb["kind"]]   # alert type per callout kind
                body = [f"> **{LABEL[cb['kind']].split('**')[1]}: {md_inline(cb.get('title', ''))}**"] + ([">", f"> {T(cb['text'])}"] if cb.get("text") else [])   # title and text
                out += [f"> [!{kind}]"] + body + [""]   # the alert
            elif "numbers" in b:   # key numbers as a one-row table
                ns = b["numbers"]   # tiles
                out += ["| " + " | ".join(f"**{cell(n['value'])}**" for n in ns) + " |", "|" + "---|" * len(ns),
                        "| " + " | ".join(cell(cites.expand(n["label"], chip)) for n in ns) + " |", ""]   # value row and label row
            elif "table" in b:   # data table
                tb = b["table"]   # definition
                out += ["| " + " | ".join(cell(h) for h in tb["head"]) + " |", "|" + "---|" * len(tb["head"])]   # header
                out += ["| " + " | ".join(cell(cites.expand(x, chip)) for x in row) + " |" for row in tb["rows"]]   # rows
                if tb.get("caption"): out += ["", f"*{T(tb['caption'])}*"]   # caption
                out.append("")   # spacing
            elif "diagram" in b:   # SVG image + caption
                dg = b["diagram"]   # definition
                out += [f'<a href="img/{dg["name"]}.svg"><img src="img/{dg["name"]}.svg" alt="{dg["name"]}" width="100%"></a>', "",
                        "*Click the diagram to open it full size.* " + f"*{T(dg.get('caption', ''))}*", ""]   # full-width image, click to enlarge, caption
            elif "explainer" in b:   # animated SVG, full width, click to open
                ex = b["explainer"]   # definition
                out += [f'<a href="img/{ex["name"]}.svg"><img src="img/{ex["name"]}.svg" alt="{ex["name"]}" width="100%"></a>', "",
                        f"*Animated: the steps play in a loop. Click to open full size.* {T(ex.get('caption', ''))}", ""]   # image and caption
            elif "checklist" in b:   # task list
                out += [f"- [ ] {T(i)}" for i in b["checklist"]] + [""]   # unticked boxes
    out += ["## Sources cited on this page", "",
            "`[R18 p.12]` = reference 18 below, PDF page 12 (page index of the PDF file). Each cited statement was checked "
            "against a verbatim quote from that page.", "", "| Ref | Document | PDF pages cited |", "|---|---|---|"]   # source table header
    for s, pages in cites.sources_used():   # every cited source
        out.append(f"| R{s['ref']} | **{cell(s['title'])}** — {cell(s['publisher'])} · {cell(s['edition'])} · {cell(s['jurisdiction'])} · [link]({s['url']}) | {c.page_ranges(pages)} |")   # one row
    out += ["", f"*Generated from `content/docs/{doc['_file']}` on {datetime.date.today().isoformat()}. Do not edit this page in the wiki; edit the content file.*", ""]   # footer
    if cites.missing: raise SystemExit(f"{doc['_file']}: unknown fact IDs {sorted(cites.missing)}")   # same check as the PDF build
    btn = next(i for i, l in enumerate(out) if 'img/btn_' in l)   # the download-button line
    out.insert(0, out.pop(btn)); out.insert(1, "")   # buttons first on the page
    return "\n".join(out), cites   # page text

def main():
    out_dir = c.ROOT / (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "wiki")   # output folder
    (out_dir / "img").mkdir(parents=True, exist_ok=True)   # folders
    for old in out_dir.glob("*.md"): old.unlink()   # pages are fully regenerated
    catalog, facts = c.load_catalog(), c.load_facts()   # public data only
    diagrams.export_svg(out_dir / "img")   # SVG diagrams
    import explainers   # animated explainers (pure Python, no browser needed)
    for name, fn in explainers.EXPLAINERS.items(): (out_dir / "img" / f"{name}.svg").write_text(fn()[0])   # animated SVG for the wiki
    docs = [d for d in c.load_docs() if not d.get("private")]   # public documents only
    index = []   # rows for the home page
    for doc in docs:   # one page per document
        text, cites = render_doc(doc, catalog, facts)   # render it
        name = page_name(doc); (out_dir / f"{name}.md").write_text(text)   # write the page
        index.append((doc, name, len(cites.used)))   # remember it for the index
    import wiki_graphics as wg   # banner and cards
    import shutil, subprocess, zipfile   # copying, thumbnails, zip
    pdf_dir = out_dir / "pdf"; pdf_dir.mkdir(exist_ok=True)   # PDFs inside the wiki
    for old in pdf_dir.glob("*"): old.unlink()   # fully regenerated
    from pypdf import PdfReader   # page counts for the buttons
    pages = {}   # document id -> page count
    for doc, name, _ in index:   # every public document
        src = c.ROOT / "docs" / "pdf" / f'{doc["id"]}_{doc["slug"]}.pdf'   # built PDF
        if not src.exists(): continue   # not built (should not happen in CI)
        shutil.copy2(src, pdf_dir / src.name); pages[doc["id"]] = len(PdfReader(str(src)).pages)   # copy and count
        (out_dir / "img" / f'btn_{doc["id"]}.svg').write_text(wg.button(f'Download PDF · {pages[doc["id"]]} pages', doc.get("accent", "navy")))   # download button
        if shutil.which("pdftoppm"):   # cover thumbnail (poppler-utils)
            subprocess.run(["pdftoppm", "-png", "-r", "45", "-f", "1", "-l", "1", "-singlefile", str(src), str(out_dir / "img" / f'thumb_{doc["id"]}')], check=True)   # first page as PNG
    (out_dir / "img" / "btn_library.svg").write_text(wg.button("All PDFs", "navy"))   # library button
    with zipfile.ZipFile(pdf_dir / "all_pdfs.zip", "w", zipfile.ZIP_DEFLATED) as z:   # everything in one download
        for f in sorted(pdf_dir.glob("*.pdf")): z.write(f, f.name)   # add each PDF
    lib = ["# 📥 PDF library", "", f'<a href="{PDF_URL}all_pdfs.zip"><img src="img/btn_all.svg" height="64" alt="Download all PDFs"></a>', "",
           "Every sheet as a colour PDF. Click a cover to open the PDF; the wiki page has the animated version.", "", "<table>"]   # library page
    (out_dir / "img" / "btn_all.svg").write_text(wg.button(f"Download all {len(pages)} PDFs (zip)", "green"))   # zip button
    cells = [f'<td width="25%" align="center"><a href="{PDF_URL}{doc["id"]}_{doc["slug"]}.pdf"><img src="img/thumb_{doc["id"]}.png" width="100%" alt="{html.escape(doc["title"])}"></a><br>'
             f'<b>{html.escape(doc.get("badge", ""))}</b><br>{html.escape(doc["title"])}<br><a href="{name}">wiki page</a> · {pages.get(doc["id"], "?")} pages</td>' for doc, name, _ in index if doc["id"] in pages]   # one cell per PDF
    lib += ["<tr>" + "".join(cells[i:i + 4]) + "</tr>" for i in range(0, len(cells), 4)] + ["</table>", ""]   # rows of four
    (out_dir / "PDF-library.md").write_text("\n".join(lib))   # write the library page
    (out_dir / "img" / "home_banner.svg").write_text(wg.banner(len(index), len(catalog), len(facts)))   # animated banner
    for doc, name, _ in index: (out_dir / "img" / f'card_{doc["id"]}.svg').write_text(wg.card(doc))   # one card per document
    def grid(rows):   # HTML table of linked cards, three per row
        cells = [f'<td width="33%"><a href="{name}"><img src="img/card_{doc["id"]}.svg" width="100%" alt="{html.escape(doc["title"])}"></a></td>' for doc, name, _ in rows]   # one cell per card
        return ["<table>"] + ["<tr>" + "".join(cells[i:i + 3]) + "</tr>" for i in range(0, len(cells), 3)] + ["</table>", ""]   # rows of three
    guides = [r for r in index if r[0].get("badge", "").startswith("VISUAL")]   # animated visual guides
    sheets = [r for r in index if not r[0].get("badge", "").startswith("VISUAL")]   # reference sheets
    home = ['<a href="Sources"><img src="img/home_banner.svg" width="100%" alt="Earthing, bonding, surge and lightning protection library"></a>', "",
            '<a href="PDF-library"><img src="img/btn_library.svg" height="64" alt="All PDFs"></a> <a href="pdf/all_pdfs.zip"><img src="img/btn_all.svg" height="64" alt="Download all PDFs"></a>', "",
            "> [!TIP]", "> **New here? Start with the three animated visual guides.** They show how earthing works, how a surge reaches a PoE camera and why surge-protector wires must be short. Every picture carries citations to its sources.", "",
            "## ▶ Animated visual guides", ""] + grid(guides) + ["## 📚 Reference sheets", ""] + grid(sheets) + [
            "## How to read these pages", "",
            "> [!NOTE]", "> Every technical statement ends with a small citation such as <sup>R18 p.19</sup>: reference 18 on the [Sources](Sources) page, PDF page 19. "
            "Each cited statement was checked against a verbatim quote from that page and reviewed independently.", "",
            "> [!WARNING]", "> These pages summarise published guidance. They do not replace the wiring code that applies at the site, the product manuals, "
            "or a qualified and registered person. Where sources from different countries disagree, each page shows both sides.", "",
            "| Colour in the pictures | Meaning |", "|---|---|", "| 🔴 red line | power (line conductor) |", "| 🔵 blue line | neutral, data or signal |",
            "| 🟠 orange line | photovoltaic d.c. |", "| 🟢🟡 green with yellow stripes | protective earth and bonding conductors |", "| 🟧 amber box | surge protective device (SPD) |", "",
            f"[All {len(catalog)} source documents](Sources) · {len(facts)} verified facts · generated {datetime.date.today().isoformat()}", ""]   # home page
    (out_dir / "Home.md").write_text("\n".join(home))   # write the home page
    src = ["# Source documents", "", "Citation numbers (R..) are the same in every sheet. The PDFs themselves are not stored in the repository; "
           "`tools/download_references.py` downloads them from these URLs.", "", "| Ref | Document | Publisher | Edition | Jurisdiction |", "|---|---|---|---|---|"]   # sources page
    for s in sorted(catalog.values(), key=lambda x: x["ref"]):   # every catalogued source
        src.append(f"| R{s['ref']} | [{cell(s['title'])}]({s['url']}) | {cell(s['publisher'])} | {cell(s['edition'])} | {cell(s['jurisdiction'])} |")   # row
    (out_dir / "Sources.md").write_text("\n".join(src) + "\n")   # write the sources page
    side = ["**[🏠 Home](Home)**", "", "**[📥 PDF library](PDF-library)**", "", "**▶ Animated guides**", ""] + [f"- [{doc['title'].split(': ', 1)[-1]}]({name})" for doc, name, _ in index if doc.get("badge", "").startswith("VISUAL")] + \
           ["", "**📚 Reference sheets**", ""] + [f"- [{doc.get('badge', doc['id'])}]({name})" for doc, name, _ in index if not doc.get("badge", "").startswith("VISUAL")] + ["", "[📖 Sources](Sources)"]   # sidebar: guides first
    (out_dir / "_Sidebar.md").write_text("\n".join(side) + "\n")   # write the sidebar
    print(f"wiki: {len(index)} pages + Home, Sources, _Sidebar, {len(diagrams.DIAGRAMS)} SVG diagrams -> {out_dir.relative_to(c.ROOT)}")   # summary

if __name__ == "__main__":
    main()   # run when called as a script
