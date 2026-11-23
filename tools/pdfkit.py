"""Colour PDF kit: one theme, reusable building blocks, and a document builder (ReportLab).

Every colour, font and block style used by the library's PDFs is defined here so that
all documents look the same. See .claude/skills/colour-pdf/SKILL.md for the rules.
"""
import datetime, pathlib   # build date and file paths
from reportlab.lib import colors   # colour objects
from reportlab.lib.pagesizes import A4   # page size used by every document
from reportlab.lib.units import mm   # millimetre unit
from reportlab.lib.styles import ParagraphStyle   # paragraph style definition
from reportlab.lib.enums import TA_LEFT, TA_CENTER   # text alignment constants
from reportlab.pdfbase import pdfmetrics   # font registry
from reportlab.pdfbase.ttfonts import TTFont   # TrueType font loader
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, NextPageTemplate, KeepTogether, Flowable, HRFlowable)   # layout engine parts
from reportlab.platypus.tableofcontents import TableOfContents   # automatic contents page
from reportlab.graphics.shapes import Drawing, Circle, Line, Polygon, Rect, String, PolyLine   # vector shapes for icons
from reportlab.graphics import renderPDF   # draws vector drawings on the PDF canvas

FONT_DIR = pathlib.Path(__file__).resolve().parent / "fonts"   # fonts are vendored so builds are reproducible
PAGE_W, PAGE_H = A4   # page width and height in points
MARGIN = 17 * mm   # left/right page margin
TOP = 22 * mm   # top margin (below the header band)
BOTTOM = 18 * mm   # bottom margin (above the footer)
FRAME_W = PAGE_W - 2 * MARGIN   # usable text width

# ---------------------------------------------------------------- palette
PAL = {   # the one palette; documents choose an accent by name
    "navy": "#0F2A47",   # cover background and main headings
    "ink": "#1F2937",   # body text
    "muted": "#6B7280",   # captions, footers
    "line": "#D1D5DB",   # hairlines and table grid
    "paper": "#F8FAFC",   # zebra rows and soft panels
    "teal": "#0E7490",   # accent: data / network
    "green": "#2F9E44",   # accent: earthing (protective-earth green)
    "yellow": "#FACC15",   # protective-earth yellow (stripe motif)
    "amber": "#D97706",   # accent: lightning / warning
    "red": "#DC2626",   # danger / do-not
    "blue": "#2563EB",   # notes / sources
    "purple": "#7C3AED",   # accent: automation / site notes
    "orange": "#EA580C",   # accent: solar / power
    "pink": "#DB2777",   # accent: security
}
TINT = {   # light background tints paired with the strong colours above
    "green": "#E9F7EC", "red": "#FDECEC", "amber": "#FEF4E2", "blue": "#E8F0FE", "purple": "#F1EAFE",
    "teal": "#E3F4F7", "orange": "#FDEEE3", "pink": "#FCE7F1", "navy": "#E6ECF3",
}

def col(name):
    """Return a ReportLab colour for a palette name or a #hex string."""
    return colors.HexColor(PAL.get(name, name))   # palette lookup with hex fallback

def tint(name):
    """Return the light tint that belongs to an accent colour."""
    return colors.HexColor(TINT.get(name, "#F3F4F6"))   # neutral grey when no tint is defined

# ---------------------------------------------------------------- fonts
def register_fonts():
    """Register the vendored fonts once; body = Liberation Sans, symbols = DejaVu Sans."""
    if "Body" in pdfmetrics.getRegisteredFontNames():   # already registered in this process
        return   # nothing to do
    pdfmetrics.registerFont(TTFont("Body", str(FONT_DIR / "LiberationSans-Regular.ttf")))   # regular text
    pdfmetrics.registerFont(TTFont("Body-Bold", str(FONT_DIR / "LiberationSans-Bold.ttf")))   # bold text
    pdfmetrics.registerFont(TTFont("Body-Italic", str(FONT_DIR / "LiberationSans-Italic.ttf")))   # italic text
    pdfmetrics.registerFont(TTFont("Body-BoldItalic", str(FONT_DIR / "LiberationSans-BoldItalic.ttf")))   # bold italic text
    pdfmetrics.registerFont(TTFont("Sym", str(FONT_DIR / "DejaVuSans.ttf")))   # wide symbol coverage
    pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-Italic", boldItalic="Body-BoldItalic")   # lets <b>/<i> work

def styles(accent):
    """Build the paragraph styles for one document, coloured with its accent."""
    register_fonts()   # fonts must exist before styles reference them
    a, ink = col(accent), col("ink")   # accent and body colours
    base = ParagraphStyle("base", fontName="Body", fontSize=9.6, leading=13.6, textColor=ink, alignment=TA_LEFT)   # body text
    return {
        "p": ParagraphStyle("p", parent=base, spaceAfter=5),   # normal paragraph
        "lead": ParagraphStyle("lead", parent=base, fontSize=11, leading=15.5, textColor=col("navy"), spaceAfter=7, keepWithNext=1),   # intro paragraph (kept with what follows)
        "h1": ParagraphStyle("h1", parent=base, fontName="Body-Bold", fontSize=15, leading=19, textColor=colors.white,
                             backColor=a, borderPadding=(7, 9, 7, 9), borderRadius=4, spaceBefore=12, spaceAfter=13, leftIndent=9, rightIndent=9, keepWithNext=1),   # chapter banner (never alone at a page foot)
        "h2": ParagraphStyle("h2", parent=base, fontName="Body-Bold", fontSize=11.5, leading=15, textColor=a, spaceBefore=9, spaceAfter=2, keepWithNext=1),   # section heading (kept with what follows)
        "bullet": ParagraphStyle("bullet", parent=base, leftIndent=13, bulletIndent=2, bulletFontName="Sym", bulletFontSize=7,
                                 bulletColor=a, spaceAfter=3.2),   # fact bullet
        "cell": ParagraphStyle("cell", parent=base, fontSize=8.4, leading=11),   # table body cell
        "cellh": ParagraphStyle("cellh", parent=base, fontName="Body-Bold", fontSize=8.4, leading=11, textColor=colors.white),   # table header cell
        "small": ParagraphStyle("small", parent=base, fontSize=7.6, leading=10, textColor=col("muted")),   # captions and notes
        "cap": ParagraphStyle("cap", parent=base, fontSize=8, leading=10.5, textColor=col("muted"), alignment=TA_CENTER, spaceAfter=7),   # figure caption
        "ct": ParagraphStyle("ct", parent=base, fontName="Body-Bold", fontSize=9.6, leading=12.5),   # callout title
        "cb": ParagraphStyle("cb", parent=base, fontSize=9.1, leading=12.6),   # callout body
        "num": ParagraphStyle("num", parent=base, fontName="Body-Bold", fontSize=17, leading=20, textColor=a, alignment=TA_CENTER),   # key-number value
        "numl": ParagraphStyle("numl", parent=base, fontSize=7.9, leading=10.2, alignment=TA_CENTER),   # key-number label
        "toc1": ParagraphStyle("toc1", parent=base, fontName="Body-Bold", fontSize=10, leading=15, textColor=col("navy")),   # contents level 1
        "toc2": ParagraphStyle("toc2", parent=base, fontSize=9, leading=12.5, leftIndent=12, textColor=ink),   # contents level 2
    }

# ---------------------------------------------------------------- small vector icons
def icon(kind, size=15):
    """Return a round vector icon: do (tick), dont (cross), warn (!), note (i), site (pin dot)."""
    colour = {"do": "green", "dont": "red", "warn": "amber", "note": "blue", "site": "purple"}[kind]   # icon colour per kind
    d, r = Drawing(size, size), size / 2.0   # square drawing and its radius
    d.add(Circle(r, r, r, fillColor=col(colour), strokeColor=None))   # filled disc
    w = dict(strokeColor=colors.white, strokeWidth=size * 0.13, strokeLineCap=1)   # white stroke settings
    if kind == "do":   # tick mark
        d.add(PolyLine([r * 0.55, r * 1.0, r * 0.9, r * 0.62, r * 1.5, r * 1.38], fillColor=None, **w))   # two-segment tick
    elif kind == "dont":   # cross
        d.add(Line(r * 0.62, r * 0.62, r * 1.38, r * 1.38, **w)); d.add(Line(r * 0.62, r * 1.38, r * 1.38, r * 0.62, **w))   # two diagonals
    elif kind == "warn":   # exclamation mark
        d.add(Line(r, r * 0.95, r, r * 1.5, **w)); d.add(Circle(r, r * 0.52, size * 0.075, fillColor=colors.white, strokeColor=None))   # bar and dot
    elif kind == "note":   # letter i
        d.add(Line(r, r * 0.5, r, r * 1.08, **w)); d.add(Circle(r, r * 1.48, size * 0.075, fillColor=colors.white, strokeColor=None))   # stem and dot
    else:   # site note: ring
        d.add(Circle(r, r, r * 0.42, fillColor=None, strokeColor=colors.white, strokeWidth=size * 0.13))   # white ring
    return d   # ready to place in a table cell

CALLOUT = {   # callout kinds: label and colour
    "do": ("DO", "green"), "dont": ("DO NOT", "red"), "warn": ("WARNING", "amber"),
    "note": ("NOTE", "blue"), "site": ("CHECK ON SITE", "purple"),
}

def callout(st, kind, title, body):
    """Coloured callout box with an icon, a bold title and body text (body may contain citation markup)."""
    label, colour = CALLOUT[kind]   # resolve label and colour
    head = Paragraph(f'<font color="{PAL[colour]}">{label}</font>&nbsp;&nbsp;{title}', st["ct"])   # coloured label + title
    inner = [head] + ([Paragraph(body, st["cb"])] if body else [])   # title then optional body
    t = Table([[icon(kind), inner]], colWidths=[9 * mm, FRAME_W - 9 * mm - 3])   # icon column + text column
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), tint(colour)),   # soft tinted background
        ("LINEBEFORE", (0, 0), (0, -1), 3, col(colour)),   # strong coloured bar on the left
        ("VALIGN", (0, 0), (-1, -1), "TOP"),   # align icon with the first text line
        ("LEFTPADDING", (0, 0), (0, 0), 7), ("RIGHTPADDING", (0, 0), (0, 0), 2),   # icon cell padding
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),   # vertical padding
    ]))
    return KeepTogether([t, Spacer(1, 6)])   # never split a callout across pages

def data_table(st, accent, head, rows, widths=None):
    """Table with a coloured header row, zebra rows and wrapped cells; widths are fractions of the text width."""
    n = len(head)   # number of columns
    widths = widths or [1.0 / n] * n   # equal columns unless given
    cw = [FRAME_W * w / sum(widths) for w in widths]   # convert fractions to points
    data = [[Paragraph(str(h), st["cellh"]) for h in head]] + [[Paragraph(str(c), st["cell"]) for c in r] for r in rows]   # wrap all cells
    t = Table(data, colWidths=cw, repeatRows=1)   # header repeats on each page
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), col(accent)),   # coloured header row
        ("VALIGN", (0, 0), (-1, -1), "TOP"),   # top-align text
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, col("line")),   # light row separators
        ("BOX", (0, 0), (-1, -1), 0.6, col("line")),   # outer border
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),   # horizontal padding
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),   # vertical padding
    ]
    cmds += [("BACKGROUND", (0, i), (-1, i), col("paper")) for i in range(2, len(data), 2)]   # zebra striping
    t.setStyle(TableStyle(cmds))   # apply the style
    return [t, Spacer(1, 7)]   # table followed by a gap

def number_tiles(st, accent, items):
    """Row of 'key number' tiles: big value, short label, citation. items = [(value, label_markup), ...]."""
    n = len(items)   # tiles per row
    gap = 4 * mm   # space between tiles
    w = (FRAME_W - gap * (n - 1)) / n   # width of each tile
    cells, widths = [], []   # table row and column widths
    for i, (value, label) in enumerate(items):   # build each tile
        cells.append([Paragraph(value, st["num"]), Paragraph(label, st["numl"])]); widths.append(w)   # value above label
        if i < n - 1: cells.append(""); widths.append(gap)   # spacer column between tiles
    t = Table([cells], colWidths=widths)   # single-row table
    cmds = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]   # shared padding
    for i in range(0, len(cells), 2):   # style only the tile columns
        cmds += [("BACKGROUND", (i, 0), (i, 0), tint(accent)), ("LINEABOVE", (i, 0), (i, 0), 2.2, col(accent))]   # tinted tile with coloured top edge
    t.setStyle(TableStyle(cmds))   # apply the style
    return KeepTogether([t, Spacer(1, 8)])   # keep the row intact

class CheckBox(Flowable):
    """Empty square tick box for printed checklists."""
    def __init__(self, colour, size=8.5):
        super().__init__(); self.colour, self.size = colour, size   # remember colour and size
        self.width = self.height = size   # flowable dimensions
    def draw(self):
        self.canv.setStrokeColor(self.colour); self.canv.setLineWidth(1)   # outline settings
        self.canv.roundRect(0, -1.5, self.size, self.size, 1.5, stroke=1, fill=0)   # the box itself

def checklist(st, accent, items):
    """Printable checklist: one tick box per line."""
    rows = [[CheckBox(col(accent)), Paragraph(i, st["cb"])] for i in items]   # box + text per item
    t = Table(rows, colWidths=[7 * mm, FRAME_W - 7 * mm])   # narrow box column
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5), ("LEFTPADDING", (0, 0), (0, -1), 2)]))   # compact rows
    return [t, Spacer(1, 6)]   # checklist followed by a gap

class Figure(Flowable):
    """Vector drawing scaled to the text width (or less) and centred."""
    def __init__(self, drawing, max_width=FRAME_W):
        super().__init__(); self.d = drawing   # keep the drawing
        self.s = min(1.0, max_width / drawing.width)   # scale down only when too wide
        self.width, self.height = drawing.width * self.s, drawing.height * self.s   # scaled size
        self.hAlign = "CENTER"   # centre in the frame
    def draw(self):
        self.canv.saveState(); self.canv.scale(self.s, self.s)   # apply the scale
        renderPDF.draw(self.d, self.canv, 0, 0); self.canv.restoreState()   # draw and restore

# ---------------------------------------------------------------- page furniture
def pe_stripe(c, x, y, w, h, seg=None):
    """Green/yellow slanted stripe band (protective-earth conductor motif)."""
    seg = seg or h * 2.2   # length of each colour segment
    c.saveState(); p = c.beginPath(); p.rect(x, y, w, h); c.clipPath(p, stroke=0, fill=0)   # clip to the band
    i, pos = 0, x - h   # segment counter and start position
    while pos < x + w:   # fill the whole band
        c.setFillColor(col("green") if i % 2 == 0 else col("yellow"))   # alternate the two colours
        q = c.beginPath(); q.moveTo(pos, y); q.lineTo(pos + seg, y); q.lineTo(pos + seg + h, y + h); q.lineTo(pos + h, y + h); q.close()   # slanted segment
        c.drawPath(q, stroke=0, fill=1); pos += seg; i += 1   # paint and advance
    c.restoreState()   # remove the clip

def earth_symbol(c, x, y, s, colour):
    """Earth (ground) symbol: stem plus three shortening bars; x,y = top of stem, s = scale."""
    c.saveState(); c.setStrokeColor(colour); c.setLineWidth(s * 0.09); c.setLineCap(1)   # line settings
    c.line(x, y, x, y - s * 0.55)   # vertical stem
    for k, half in enumerate((0.5, 0.33, 0.16)):   # three bars
        yy = y - s * (0.55 + 0.17 * k); c.line(x - s * half, yy, x + s * half, yy)   # each bar shorter than the last
    c.restoreState()   # restore canvas state

def bolt(c, x, y, s, colour, alpha=1.0):
    """Lightning bolt polygon; x,y = top-left, s = height."""
    pts = [(0.45, 0), (0.05, -0.55), (0.36, -0.55), (0.18, -1.0), (0.78, -0.40), (0.47, -0.40), (0.72, 0)]   # outline in unit coordinates
    c.saveState(); c.setFillColor(colour, alpha=alpha); p = c.beginPath()   # fill settings
    p.moveTo(x + pts[0][0] * s, y + pts[0][1] * s)   # start of outline
    for px, py in pts[1:]: p.lineTo(x + px * s, y + py * s)   # remaining points
    p.close(); c.drawPath(p, stroke=0, fill=1); c.restoreState()   # paint the bolt

class Doc(BaseDocTemplate):
    """Document template: cover page, optional contents, body pages with coloured header and footer."""
    def __init__(self, path, meta):
        self.meta = meta   # title, subtitle, accent, doc number, series, date, notice
        self.accent = meta.get("accent", "teal")   # accent colour name
        self.section = ""   # current chapter title (shown in the header)
        self.page_h1 = None   # first chapter that starts on the current page
        super().__init__(str(path), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=TOP, bottomMargin=BOTTOM,
                         title=meta["title"], author=meta.get("series", ""), subject=meta.get("subtitle", ""))   # PDF metadata
        body = Frame(MARGIN, BOTTOM, FRAME_W, PAGE_H - TOP - BOTTOM, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)   # text frame
        self.addPageTemplates([PageTemplate(id="cover", frames=[body], onPage=self._cover),
                               PageTemplate(id="body", frames=[body], onPage=self._page, onPageEnd=self._page_end)])   # the two page layouts

    def beforeDocument(self):
        """Reset the running header at the start of every build pass (multiBuild runs several)."""
        self.section, self.page_h1 = "", None   # no chapter yet

    def _page_end(self, c, doc):
        """Write the chapter name into the header once the page content is known."""
        name = (self.page_h1 or self._carried)[:60]   # a chapter starting here wins over the one carried over
        left = f'{self.meta.get("badge", "")}  ·  {self.meta["title"]}'   # document badge and title
        room = FRAME_W - pdfmetrics.stringWidth(name, "Body", 8.5) - 12   # width left for the title
        while left and pdfmetrics.stringWidth(left, "Body-Bold", 8.5) > room: left = left[:-2].rstrip() + "…"   # shorten until it fits
        c.saveState(); c.setFillColor(colors.white)   # header text colour
        c.setFont("Body-Bold", 8.5); c.drawString(MARGIN, PAGE_H - 7.2 * mm, left)   # title, left side
        c.setFont("Body", 8.5); c.drawRightString(PAGE_W - MARGIN, PAGE_H - 7.2 * mm, name); c.restoreState()   # chapter name, right side

    def afterFlowable(self, fl):
        """Feed headings to the contents page, the PDF outline and the running header."""
        if isinstance(fl, Paragraph) and fl.style.name in ("h1", "h2"):   # only headings matter
            level = 0 if fl.style.name == "h1" else 1   # outline level
            text = fl.getPlainText()   # heading without markup
            key = f"h{self.seq.nextf('heading')}"   # unique bookmark name
            self.canv.bookmarkPage(key); self.canv.addOutlineEntry(text, key, level=level, closed=(level == 0))   # PDF outline entry
            self.notify("TOCEntry", (level, text, self.page, key))   # contents entry
            if level == 0:   # a chapter starts
                self.section = text   # it is now the current chapter
                if self.page_h1 is None: self.page_h1 = text   # first chapter starting on this page

    def _cover(self, c, doc):
        """Paint the cover page background, title block and notice."""
        m, a = self.meta, col(self.accent)   # metadata and accent colour
        split = PAGE_H * 0.40   # y where the dark block ends
        c.setFillColor(col("navy")); c.rect(0, split, PAGE_W, PAGE_H - split, stroke=0, fill=1)   # dark upper block
        bolt(c, PAGE_W - 78 * mm, PAGE_H - 22 * mm, 118 * mm, col("yellow"), alpha=0.16)   # large faint bolt
        earth_symbol(c, PAGE_W - 34 * mm, split + 46 * mm, 34 * mm, colors.white)   # earth symbol
        pe_stripe(c, 0, split - 5 * mm, PAGE_W, 5 * mm)   # green/yellow band under the block
        c.setFillColor(a); c.roundRect(MARGIN, PAGE_H - 44 * mm, 44 * mm, 9 * mm, 2 * mm, stroke=0, fill=1)   # document number badge
        c.setFillColor(colors.white); c.setFont("Body-Bold", 10); c.drawCentredString(MARGIN + 22 * mm, PAGE_H - 41 * mm, m.get("badge", ""))   # badge text
        c.setFont("Body", 10.5); c.setFillColor(colors.HexColor("#C7D2E0")); c.drawString(MARGIN, PAGE_H - 26 * mm, m.get("series", ""))   # series line
        title = Paragraph(m["title"], ParagraphStyle("ctitle", fontName="Body-Bold", fontSize=29, leading=34, textColor=colors.white))   # big title
        w, h = title.wrap(PAGE_W - 2 * MARGIN - 36 * mm, 200 * mm); title.drawOn(c, MARGIN, PAGE_H - 56 * mm - h)   # place the title
        sub = Paragraph(m.get("subtitle", ""), ParagraphStyle("csub", fontName="Body", fontSize=13, leading=18, textColor=colors.HexColor("#DCE6F2")))   # subtitle
        w2, h2 = sub.wrap(PAGE_W - 2 * MARGIN - 40 * mm, 100 * mm); sub.drawOn(c, MARGIN, PAGE_H - 56 * mm - h - 8 * mm - h2)   # place the subtitle
        y = split - 20 * mm   # start of the lower (white) area
        for label, value in m.get("facts", []):   # small label/value lines under the band
            c.setFont("Body-Bold", 8.5); c.setFillColor(a); c.drawString(MARGIN, y, label.upper())   # label
            v = Paragraph(value, ParagraphStyle("cv", fontName="Body", fontSize=10, leading=13.5, textColor=col("ink")))   # value text
            vw, vh = v.wrap(PAGE_W - 2 * MARGIN - 40 * mm, 60 * mm); v.drawOn(c, MARGIN + 40 * mm, y - vh + 9.5); y -= max(vh, 10) + 6   # place and move down
        note = Paragraph(m.get("notice", ""), ParagraphStyle("cn", fontName="Body", fontSize=8, leading=11, textColor=col("ink")))   # notice text
        nw, nh = note.wrap(PAGE_W - 2 * MARGIN - 12 * mm, 60 * mm)   # measure the notice
        c.setFillColor(tint("amber")); c.roundRect(MARGIN, 16 * mm, PAGE_W - 2 * MARGIN, nh + 9 * mm, 2 * mm, stroke=0, fill=1)   # notice panel
        c.setFillColor(col("amber")); c.rect(MARGIN, 16 * mm, 2.2, nh + 9 * mm, stroke=0, fill=1)   # coloured edge of the panel
        note.drawOn(c, MARGIN + 6 * mm, 16 * mm + 4.5 * mm)   # notice text inside the panel
        c.setFont("Body", 8); c.setFillColor(col("muted")); c.drawString(MARGIN, 9 * mm, m.get("footer", ""))   # build line

    def _page(self, c, doc):
        """Paint the header band and footer of a body page."""
        m, a = self.meta, col(self.accent)   # metadata and accent colour
        c.setFillColor(a); c.rect(0, PAGE_H - 11 * mm, PAGE_W, 11 * mm, stroke=0, fill=1)   # header band
        pe_stripe(c, 0, PAGE_H - 12.2 * mm, PAGE_W, 1.2 * mm, seg=9)   # thin green/yellow line under the band
        self._carried, self.page_h1 = self.section, None   # chapter carried over from the previous page; reset the per-page record
        c.setStrokeColor(col("line")); c.setLineWidth(0.5); c.line(MARGIN, 12.5 * mm, PAGE_W - MARGIN, 12.5 * mm)   # footer rule
        c.setFillColor(col("muted")); c.setFont("Body", 7.6); c.drawString(MARGIN, 8.5 * mm, m.get("footer", ""))   # build line
        c.setFont("Body-Bold", 8.5); c.setFillColor(a); c.drawRightString(PAGE_W - MARGIN, 8.5 * mm, f"Page {doc.page}")   # page number

def toc(st):
    """Contents flowable styled to match the theme."""
    t = TableOfContents(); t.levelStyles = [st["toc1"], st["toc2"]]; t.dotsMinLevel = 0   # two levels with dot leaders
    return t   # filled in automatically by multiBuild

def build(path, meta, story_body, contents=False):
    """Assemble cover + (optional) contents + body and write the PDF."""
    st = styles(meta.get("accent", "teal"))   # styles for this accent
    meta.setdefault("footer", f'{meta.get("series", "")}  ·  built {datetime.date.today().isoformat()}')   # default build line
    doc = Doc(path, meta)   # document template
    story = [NextPageTemplate("body"), PageBreak()]   # page 1 is the painted cover; text starts on page 2
    if contents:   # long documents get a contents page
        story += [Paragraph("Contents", st["h1"]), toc(st), PageBreak()]   # contents then a new page
    doc.multiBuild(story + story_body)   # two passes so page numbers in the contents are right
    return path   # path of the written file
