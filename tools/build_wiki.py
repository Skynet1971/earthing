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
PDF_URL = REPO_URL + "/raw/HEAD/docs/pdf/"   # HEAD = the repository's default branch
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
           f"📄 **PDF:** [{doc['id']}_{doc['slug']}.pdf]({PDF_URL}{doc['id']}_{doc['slug']}.pdf)", "",
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
            elif "callout" in b:   # callout as a quote block
                cb = b["callout"]   # definition
                out += [f"> {LABEL[cb['kind']]} — **{md_inline(cb.get('title', ''))}**", ">", f"> {T(cb.get('text', ''))}", ""]   # label, title, text
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
            elif "checklist" in b:   # task list
                out += [f"- [ ] {T(i)}" for i in b["checklist"]] + [""]   # unticked boxes
    out += ["## Sources cited on this page", "",
            "`[R18 p.12]` = reference 18 below, PDF page 12 (page index of the PDF file). Each cited statement was checked "
            "against a verbatim quote from that page.", "", "| Ref | Document | PDF pages cited |", "|---|---|---|"]   # source table header
    for s, pages in cites.sources_used():   # every cited source
        out.append(f"| R{s['ref']} | **{cell(s['title'])}** — {cell(s['publisher'])} · {cell(s['edition'])} · {cell(s['jurisdiction'])} · [link]({s['url']}) | {c.page_ranges(pages)} |")   # one row
    out += ["", f"*Generated from `content/docs/{doc['_file']}` on {datetime.date.today().isoformat()}. Do not edit this page in the wiki; edit the content file.*", ""]   # footer
    if cites.missing: raise SystemExit(f"{doc['_file']}: unknown fact IDs {sorted(cites.missing)}")   # same check as the PDF build
    return "\n".join(out), cites   # page text

def main():
    out_dir = c.ROOT / (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "wiki")   # output folder
    (out_dir / "img").mkdir(parents=True, exist_ok=True)   # folders
    for old in out_dir.glob("*.md"): old.unlink()   # pages are fully regenerated
    catalog, facts = c.load_catalog(), c.load_facts()   # public data only
    diagrams.export_svg(out_dir / "img")   # SVG diagrams
    docs = [d for d in c.load_docs() if not d.get("private")]   # public documents only
    index = []   # rows for the home page
    for doc in docs:   # one page per document
        text, cites = render_doc(doc, catalog, facts)   # render it
        name = page_name(doc); (out_dir / f"{name}.md").write_text(text)   # write the page
        index.append((doc, name, len(cites.used)))   # remember it for the index
    home = [f"# {SERIES}", "",
            "Colour PDF sheets and wiki pages on earthing, bonding, surge protection and lightning protection for a house and its "
            "equipment. Every technical statement cites the source document and PDF page it comes from, and every cited "
            "statement was checked against a verbatim quote on that page.", "",
            "| Sheet | Wiki page | PDF | Sources |", "|---|---|---|---|"]   # home page header
    for doc, name, n in index:   # one row per document
        home.append(f"| {doc.get('badge', doc['id'])} | [{doc['title']}]({name}) | [PDF]({PDF_URL}{doc['id']}_{doc['slug']}.pdf) | {n} |")   # row
    home += ["", f"[All {len(catalog)} source documents](Sources) · {len(facts)} verified facts · generated {datetime.date.today().isoformat()}", ""]   # footer
    (out_dir / "Home.md").write_text("\n".join(home))   # write the home page
    src = ["# Source documents", "", "Citation numbers (R..) are the same in every sheet. The PDFs themselves are not stored in the repository; "
           "`tools/download_references.py` downloads them from these URLs.", "", "| Ref | Document | Publisher | Edition | Jurisdiction |", "|---|---|---|---|---|"]   # sources page
    for s in sorted(catalog.values(), key=lambda x: x["ref"]):   # every catalogued source
        src.append(f"| R{s['ref']} | [{cell(s['title'])}]({s['url']}) | {cell(s['publisher'])} | {cell(s['edition'])} | {cell(s['jurisdiction'])} |")   # row
    (out_dir / "Sources.md").write_text("\n".join(src) + "\n")   # write the sources page
    side = ["**[Home](Home)**", ""] + [f"- [{doc.get('badge', doc['id'])}]({name})" for doc, name, _ in index] + ["", "[Sources](Sources)"]   # sidebar
    (out_dir / "_Sidebar.md").write_text("\n".join(side) + "\n")   # write the sidebar
    print(f"wiki: {len(index)} pages + Home, Sources, _Sidebar, {len(diagrams.DIAGRAMS)} SVG diagrams -> {out_dir.relative_to(c.ROOT)}")   # summary

if __name__ == "__main__":
    main()   # run when called as a script
