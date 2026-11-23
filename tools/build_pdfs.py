#!/usr/bin/env python3
"""Build the colour PDF documents from content/docs/*.yaml and the verified facts.

Usage: python3 tools/build_pdfs.py [doc-id ...]     (no arguments = build every document)
Public documents go to docs/pdf/; documents marked 'private: true' go to private/ (not committed).
"""
import re, sys, pathlib, subprocess   # standard library
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))   # allow importing the sibling modules
import pdfkit as k   # theme and building blocks
import content as c   # catalogue, facts and citation handling
import diagrams   # vector diagrams
from reportlab.platypus import Paragraph, Spacer, PageBreak, KeepTogether   # flowables used directly here

ROOT = c.ROOT   # repository root
OUT_PUBLIC = ROOT / "docs" / "pdf"   # committed PDFs
OUT_PRIVATE = ROOT / "private"   # site-specific PDFs (ignored by git)
SERIES = "Earthing, Bonding, Surge & Lightning Protection Library"   # series name printed on every document
NOTICE = ("<b>Information only.</b> This document summarises published guidance and cites the source and page of every "
          "technical statement. It does not replace the wiring code that applies at the site, the product manuals, or the "
          "judgement of a qualified and registered person. Sources come from different countries; where they differ, the "
          "wiring code that applies at the site decides. Work inside distribution boards and on lightning protection "
          "systems is for qualified persons only.")   # cover notice

def esc(text):
    """Escape characters that would break ReportLab's paragraph markup (used for fact claims)."""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")   # full escape

def amp(text):
    """Escape bare ampersands in author-written text while keeping the allowed inline tags."""
    return re.sub(r"&(?!#?\w+;)", "&amp;", str(text))   # leave existing entities alone

def chip(ref, page, section):
    """Citation chip markup: small coloured '[R18 p.12]' that links to the source list."""
    return f'&nbsp;<font size="6.6" color="{k.PAL["blue"]}"><a href="#ref{ref}">[R{ref}&nbsp;p.{page}]</a></font>'   # internal link

def build_doc(doc, catalog, facts):
    """Turn one document definition into a PDF; returns (path, cites)."""
    accent = doc.get("accent", "teal")   # accent colour of this document
    st = k.styles(accent)   # paragraph styles
    cites = c.Cites(catalog, facts)   # citation tracker for this document
    T = lambda s: cites.expand(amp(s), chip)   # author text -> markup with citation chips
    story = []   # the flowables of the document body
    for sec in doc["sections"]:   # every chapter
        story.append(Paragraph(amp(sec["title"]), st["h1"]))   # chapter banner
        if sec.get("lead"): story.append(Paragraph(T(sec["lead"]), st["lead"]))   # optional intro paragraph
        for b in sec.get("blocks", []):   # blocks inside the chapter
            if "h2" in b:   # section heading
                story.append(Paragraph(amp(b["h2"]), st["h2"]))   # heading paragraph
            elif "p" in b:   # normal paragraph
                story.append(Paragraph(T(b["p"]), st["p"]))   # body text
            elif "facts" in b:   # list of verified facts, each with its citation
                for item in b["facts"]:   # one bullet per fact
                    fid, wording = c.fact_text(facts, item)   # resolve ID and wording
                    lab = cites.label(fid)   # citation parts (records the use)
                    text = (T(wording) if isinstance(item, dict) else esc(wording)) + (chip(*lab) if lab else "")   # wording + chip
                    story.append(Paragraph(text, st["bullet"], bulletText="●"))   # bullet paragraph
                story.append(Spacer(1, 3))   # small gap after the list
            elif "callout" in b:   # coloured callout box
                cb = b["callout"]   # callout definition
                story.append(k.callout(st, cb["kind"], amp(cb.get("title", "")), T(cb.get("text", ""))))   # build the box
            elif "numbers" in b:   # key-number tiles
                story.append(k.number_tiles(st, accent, [(amp(n["value"]), T(n["label"])) for n in b["numbers"]]))   # tiles row
            elif "table" in b:   # data table
                tb = b["table"]   # table definition
                rows = [[T(cell) for cell in row] for row in tb["rows"]]   # expand citations in every cell
                story += k.data_table(st, tb.get("accent", accent), [amp(h) for h in tb["head"]], rows, tb.get("widths"))   # build the table
                if tb.get("caption"): story.append(Paragraph(T(tb["caption"]), st["cap"]))   # optional caption
            elif "diagram" in b:   # vector diagram
                dg = b["diagram"]   # diagram definition
                fig = k.Figure(diagrams.DIAGRAMS[dg["name"]]())   # draw it
                cap = Paragraph(T(dg.get("caption", "")), st["cap"])   # caption with citations
                story.append(KeepTogether([Spacer(1, 4), fig, Spacer(1, 4), cap]))   # keep figure and caption together
            elif "checklist" in b:   # printable checklist
                story += k.checklist(st, accent, [T(i) for i in b["checklist"]])   # tick-box list
            elif "pagebreak" in b:   # forced page break
                story.append(PageBreak())   # new page
            else:   # unknown block type is an authoring error
                raise SystemExit(f'{doc["_file"]}: unknown block {list(b)}')   # stop the build
    # ---- closing chapter: the sources this document cited
    story.append(Paragraph("Sources cited in this document", st["h1"]))   # chapter banner
    story.append(Paragraph("A citation such as <b>[R18 p.12]</b> means reference 18 in the table below, PDF page 12. The page is the "
                           "page index of the PDF file, which can differ from the page number printed on the page. Each cited "
                           "statement was checked against a verbatim quote from that page (tools/verify_facts.py).", st["p"]))   # how to read citations
    rows = []   # source table rows
    for s, pages in cites.sources_used():   # every source that was cited
        title = (f'<a name="ref{s["ref"]}"/><b>{esc(s["title"])}</b><br/>{esc(s["publisher"])} · {esc(s["edition"])} · {esc(s["jurisdiction"])}'
                 f'<br/><font size="7" color="{k.PAL["blue"]}"><a href="{esc(s["url"])}">{esc(s["url"])}</a></font>')   # anchor, title, publisher, link
        rows.append([f'<b>R{s["ref"]}</b>', title, c.page_ranges(pages)])   # one row per source
    story += k.data_table(st, accent, ["Ref", "Document", "PDF pages cited"], rows, [0.08, 0.72, 0.20])   # the source table
    if cites.missing:   # content referenced facts that do not exist
        raise SystemExit(f'{doc["_file"]}: unknown fact IDs {sorted(cites.missing)}')   # stop the build
    meta = {   # cover and header metadata
        "title": doc["title"], "subtitle": doc.get("subtitle", ""), "accent": accent, "badge": doc.get("badge", ""), "series": SERIES,
        "notice": doc.get("notice", NOTICE),
        "facts": [("Applies to", amp(doc.get("applies_to", ""))), ("Based on", f"{len(cites.used)} cited source documents, listed at the end"),
                  ("Version", f'content {doc.get("version", "1.0")} · git {GIT}')],
    }
    out_dir = OUT_PRIVATE if doc.get("private") else OUT_PUBLIC   # private documents are not committed
    out_dir.mkdir(parents=True, exist_ok=True)   # make sure the folder exists
    path = out_dir / f'{doc["id"]}_{doc["slug"]}.pdf'   # output file name
    k.build(path, meta, story, contents=doc.get("contents", False))   # write the PDF
    return path, cites   # report back

def git_rev():
    """Short git commit id for the cover (or 'uncommitted')."""
    try: return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()   # current commit
    except Exception: return "uncommitted"   # no commit yet

GIT = git_rev()   # evaluated once per run

def main():
    wanted = set(sys.argv[1:])   # optional list of document IDs
    catalog = c.load_catalog()   # reference catalogue
    for doc in c.load_docs():   # every document definition
        if wanted and doc["id"] not in wanted: continue   # build only the requested ones
        private = bool(doc.get("private"))   # site-specific document?
        if private and not c.PRIVATE_FACTS.exists() and doc.get("needs_private_facts"):   # restricted facts are not available here
            print(f'skip  {doc["_file"]} (needs references/local/facts_private.json)'); continue   # cannot build it
        facts = c.load_facts(include_private=private)   # fact store for this document
        path, cites = build_doc(doc, catalog, facts)   # build it
        print(f'built {path.relative_to(ROOT)}  ({len(cites.used)} sources)')   # progress line

if __name__ == "__main__":
    main()   # run when called as a script
