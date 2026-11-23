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

SITE = re.compile(r"\[\[([a-z_]+):([^\]:]+)(?::(\d+(?:-\d+)?))?\]\]")   # site-record citation [[repo:path:line]] (private documents only)

def site_chip(m, used):
    """Purple chip for a site record; records the file so it is listed at the end of the document."""
    repo, path, line = m.group(1), m.group(2), m.group(3)   # parts of the token
    used.add((repo, path))   # remember the file
    return f'&nbsp;<font size="6.6" color="{k.PAL["purple"]}">[{repo}: {esc(path)}{":" + line if line else ""}]</font>'   # chip markup

def chip(ref, page, section):
    """Citation chip markup: small coloured '[R18 p.12]' that links to the source list."""
    return f'&nbsp;<font size="6.6" color="{k.PAL["blue"]}"><a href="#ref{ref}">[R{ref}&nbsp;p.{page}]</a></font>'   # internal link

def lint(doc):
    """Authoring rule check: author-written text that contains a digit must carry a {{FACT}} citation.

    Applies to leads, paragraphs, callouts, number tiles, captions, checklist items and table rows
    (a table row passes when any of its cells carries a citation). Headings are exempt.
    Returns a list of problems; the build stops if the list is not empty.
    """
    bad = []   # problems found
    def need(where, text):   # one rule check
        bare = SITE.sub("", re.sub(c.TOKEN, "", str(text)))   # text without citation tokens
        if re.search(r"\d", bare) and not (c.TOKEN.search(str(text)) or SITE.search(str(text))):   # digit present, no citation
            bad.append(f"{where}: {str(text)[:90]}")   # record it
    for si, sec in enumerate(doc["sections"]):   # every chapter
        if sec.get("lead"): need(f"s{si} lead", sec["lead"])   # intro paragraph
        for bi, b in enumerate(sec.get("blocks", [])):   # every block
            w = f"s{si} b{bi}"   # location label
            if "p" in b: need(w, b["p"])   # paragraph
            if "callout" in b: need(w + " callout", b["callout"].get("title", "") + " " + b["callout"].get("text", ""))   # callout
            if "numbers" in b: [need(w + " tile", n["value"] + " " + n["label"]) for n in b["numbers"]]   # tiles
            if "diagram" in b: need(w + " caption", b["diagram"].get("caption", ""))   # figure caption
            if "checklist" in b: [need(w + " check", i) for i in b["checklist"]]   # checklist items
            if "table" in b:   # table rows (the caption may state a general note without numbers)
                for ri, row in enumerate(b["table"]["rows"]): need(f"{w} row{ri}", " | ".join(map(str, row)))   # whole row
                if b["table"].get("caption"): need(w + " table caption", b["table"]["caption"])   # caption
            if "facts" in b: [need(w + " fact text", i["text"]) for i in b["facts"] if isinstance(i, dict) and i.get("text")]   # custom wording
    return bad   # empty list = clean

def build_doc(doc, catalog, facts):
    """Turn one document definition into a PDF; returns (path, cites)."""
    accent = doc.get("accent", "teal")   # accent colour of this document
    st = k.styles(accent)   # paragraph styles
    cites = c.Cites(catalog, facts)   # citation tracker for this document
    site_used = set()   # site records cited (private documents)
    if not doc.get("private") and SITE.search(str(doc)): raise SystemExit(f'{doc["_file"]}: site-record citations are only allowed in private documents')   # keep site data out of public files
    T = lambda s: SITE.sub(lambda m: site_chip(m, site_used), cites.expand(amp(s), chip))   # author text -> markup with citation chips
    story = []   # the flowables of the document body
    for sec in doc["sections"]:   # every chapter
        story.append(Paragraph(amp(sec["title"]), st["h1"]))   # chapter banner
        if sec.get("lead"): story.append(Paragraph(T(sec["lead"]), st["lead"]))   # optional intro paragraph
        for b in sec.get("blocks", []):   # blocks inside the chapter
            if "h2" in b:   # section heading
                story.append(Paragraph(amp(b["h2"]), st["h2"]))   # heading paragraph
            elif "p" in b:   # normal paragraph
                story.append(Paragraph(T(b["p"]), st["p"]))   # body text
            elif "meta" in b:   # text about the library itself (exempt from the citation lint; never technical content)
                if c.TOKEN.search(b["meta"]): raise SystemExit(f'{doc["_file"]}: a meta block must not cite facts')   # keep meta and facts apart
                story.append(Paragraph(amp(b["meta"]), st["p"]))   # body text
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
            elif "index" in b:   # table of all public documents, generated from content/docs (no author text)
                rows = [[f'<b>{esc(d.get("badge", d["id"]))}</b>', f'<b>{esc(d["title"])}</b><br/><font size="7.4" color="{k.PAL["muted"]}">{esc(d.get("applies_to", ""))}</font>', f'{d["id"]}_{d["slug"]}.pdf']
                        for d in c.load_docs() if not d.get("private") and d["id"] != doc["id"]]   # one row per other public document
                story += k.data_table(st, accent, ["Sheet", "Title and scope", "File"], rows, [0.2, 0.55, 0.25])   # the index table
            elif "prices" in b:   # observed web prices from a JSON file (data, not author text: every row carries its URL and date)
                import json   # local import: only this block needs it
                data = json.loads((c.ROOT / b["prices"]).read_text())   # suppliers file
                groups = b.get("groups", {})   # item-group number -> heading
                for g in sorted({r["item_group"] for r in data["prices"]}):   # one table per item group
                    rows = [r for r in data["prices"] if r["item_group"] == g]   # rows of this group
                    rows.sort(key=lambda r: (r["price_zar"] is None, r["price_zar"] or 0))   # cheapest first
                    story.append(Paragraph(esc(groups.get(str(g), f"Item group {g}")), st["h2"]))   # group heading
                    trs = [[f'<b>{esc(r["item"])}</b><br/><font size="7" color="{k.PAL["muted"]}">{esc(r.get("spec", ""))}</font>',
                            esc(r["seller"]),
                            (f'R {r["price_zar"]:,.2f}'.replace(",", " ") if r["price_zar"] is not None else "not shown") + f'<br/><font size="7">{esc(r.get("unit", ""))} · VAT {esc(r.get("vat", "not stated"))}</font>',
                            esc(r.get("in_stock", "not stated"))[:60],
                            f'<font size="6.5" color="{k.PAL["blue"]}"><a href="{esc(r["url"])}">{esc(r["url"][:60])}</a></font>' + ('' if r.get("confirmed") == "page" else '<br/><font size="6.5" color="#DC2626">search snippet only</font>')]
                           for r in rows]   # one row per observed price
                    story += k.data_table(st, accent, ["Product as listed", "Seller", "Price", "Stock (as shown)", "Page"], trs, [0.33, 0.13, 0.14, 0.15, 0.25])   # the table
            elif "sellers" in b:   # seller list from the same JSON file
                import json   # local import
                data = json.loads((c.ROOT / b["sellers"]).read_text())   # suppliers file
                trs = [[f'<b>{esc(x["name"])}</b><br/><font size="6.5" color="{k.PAL["blue"]}">{esc(x.get("website", ""))}</font>', esc(x.get("type", "")), esc(x.get("east_rand_branch", "not stated"))[:260]] for x in data["sellers"]]   # one row per seller
                story += k.data_table(st, accent, ["Seller", "Type", "East Rand branch (as the seller's site states)"], trs, [0.27, 0.13, 0.60])   # the table
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
    if site_used:   # private documents also list the owner's own records they cite
        story.append(Paragraph("Site records cited (owner's own repositories, read on the date of the build)", st["h2"]))   # sub-heading
        story += k.data_table(st, "purple", ["Repository", "File"], [[r, esc(f)] for r, f in sorted(site_used)], [0.25, 0.75])   # file list
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
        if private and not c.PRIVATE_FACTS.exists():   # private documents need the local-only files (not present in CI)
            print(f'skip  {doc["_file"]} (needs references/local/facts_private.json)'); continue   # cannot build it
        problems = lint(doc)   # authoring rule check
        if problems: raise SystemExit(f'{doc["_file"]}: numbers without a citation:\n  ' + "\n  ".join(problems))   # stop on violations
        facts = c.load_facts(include_private=private)   # fact store for this document
        path, cites = build_doc(doc, catalog, facts)   # build it
        print(f'built {path.relative_to(ROOT)}  ({len(cites.used)} sources)')   # progress line

if __name__ == "__main__":
    main()   # run when called as a script
