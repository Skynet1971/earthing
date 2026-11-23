"""Vector diagrams shared by the PDFs and the wiki (ReportLab graphics, exportable to SVG).

Each diagram is a concept sketch of a rule stated in the cited sources; it is not a wiring diagram
for a specific product. Diagram text uses the built-in Helvetica font and plain ASCII so that the
same drawing renders identically in the PDF and as an SVG file in the wiki.
"""
from reportlab.graphics.shapes import Drawing, Rect, Line, PolyLine, Polygon, Circle, String, Group   # vector primitives
from reportlab.lib import colors   # colour objects

C = {   # diagram palette (matches tools/pdfkit.py)
    "navy": "#0F2A47", "ink": "#1F2937", "muted": "#6B7280", "line": "#9CA3AF", "paper": "#F8FAFC",
    "green": "#2F9E44", "yellow": "#FACC15", "amber": "#D97706", "red": "#DC2626", "blue": "#2563EB",
    "teal": "#0E7490", "purple": "#7C3AED", "orange": "#EA580C", "sky": "#E8F0FE", "mint": "#E9F7EC",
    "sand": "#FEF4E2", "rose": "#FDECEC", "lilac": "#F1EAFE", "white": "#FFFFFF", "ground": "#D6C7A8",
}

def hx(name):
    """Palette name or #hex -> colour object."""
    return colors.HexColor(C.get(name, name))   # palette lookup with hex fallback

class Dg:
    """Small drawing helper so each diagram reads as a list of boxes, wires and labels."""
    def __init__(self, w, h, title=None):
        self.d = Drawing(w, h); self.w, self.h = w, h   # canvas and its size
        self.d.add(Rect(0, 0, w, h, fillColor=hx("white"), strokeColor=hx("line"), strokeWidth=0.6, rx=6, ry=6))   # framed background
        if title: self.text(12, h - 17, title, size=10.5, color="navy", bold=True)   # diagram title

    def text(self, x, y, s, size=7.5, color="ink", anchor="start", bold=False):
        """Single line of text."""
        self.d.add(String(x, y, s, fontName="Helvetica-Bold" if bold else "Helvetica", fontSize=size, fillColor=hx(color), textAnchor=anchor))   # label

    def lines(self, x, y, rows, size=7.5, color="ink", anchor="middle", bold_first=False, lead=None):
        """Several lines of text stacked downward from y."""
        lead = lead or size * 1.22   # line spacing
        for i, s in enumerate(rows):   # one String per row
            self.text(x, y - i * lead, s, size=size, color=color, anchor=anchor, bold=(bold_first and i == 0))   # stacked label

    def box(self, x, y, w, h, rows, fill="paper", stroke="navy", size=7.5, color="ink", r=4, sw=1.1, dash=None):
        """Rounded box with centred multi-line label (first row bold). x,y = bottom-left."""
        self.d.add(Rect(x, y, w, h, fillColor=hx(fill) if fill else None, strokeColor=hx(stroke), strokeWidth=sw, rx=r, ry=r, strokeDashArray=dash))   # the box
        rows = [rows] if isinstance(rows, str) else rows   # accept one string or a list
        lead = size * 1.22   # line spacing
        top = y + h / 2.0 + (len(rows) - 1) * lead / 2.0 - size * 0.35   # baseline of the first row (vertically centred)
        self.lines(x + w / 2.0, top, rows, size=size, color=color, bold_first=True)   # label

    def wire(self, pts, color="ink", width=1.4, dash=None):
        """Poly-line through the given points [x1,y1,x2,y2,...]."""
        self.d.add(PolyLine(pts, strokeColor=hx(color), strokeWidth=width, strokeDashArray=dash, fillColor=None, strokeLineJoin=1))   # the wire

    def pe(self, pts, width=2.4):
        """Protective-earth / bonding conductor: green line with yellow dashes."""
        self.wire(pts, "green", width)   # green base
        self.wire(pts, "yellow", width * 0.45, dash=[4, 4])   # yellow dashes on top

    def earth(self, x, y, s=9):
        """Earth symbol hanging below the point x,y."""
        self.d.add(Line(x, y, x, y - s * 0.6, strokeColor=hx("green"), strokeWidth=1.6))   # stem
        for i, half in enumerate((1.0, 0.65, 0.3)):   # three shortening bars
            yy = y - s * (0.6 + 0.32 * i); self.d.add(Line(x - s * half, yy, x + s * half, yy, strokeColor=hx("green"), strokeWidth=1.6))   # bar

    def spd(self, x, y, label="SPD", w=30, h=16, fill="sand"):
        """Surge protective device symbol centred on x,y (amber box)."""
        self.d.add(Rect(x - w / 2.0, y - h / 2.0, w, h, fillColor=hx(fill), strokeColor=hx("amber"), strokeWidth=1.3, rx=3, ry=3))   # device body
        self.text(x, y - 2.6, label, size=7, color="amber", anchor="middle", bold=True)   # device label

    def dot(self, x, y, r=2.2, color="ink"):
        """Connection dot."""
        self.d.add(Circle(x, y, r, fillColor=hx(color), strokeColor=None))   # filled dot

    def tag(self, x, y, n, color="navy"):
        """Numbered marker (white number in a filled circle) that the caption or legend explains."""
        self.d.add(Circle(x, y, 6.2, fillColor=hx(color), strokeColor=hx("white"), strokeWidth=0.8))   # marker disc
        self.text(x, y - 2.7, str(n), size=7.5, color="white", anchor="middle", bold=True)   # marker number

    def bolt(self, x, y, s=26, color="amber"):
        """Lightning bolt; x,y = top-left, s = height."""
        pts = [(0.45, 0), (0.05, -0.55), (0.36, -0.55), (0.18, -1.0), (0.78, -0.40), (0.47, -0.40), (0.72, 0)]   # outline in unit coordinates
        flat = [v for px, py in pts for v in (x + px * s, y + py * s)]   # flatten to [x1,y1,...]
        self.d.add(Polygon(flat, fillColor=hx(color), strokeColor=None))   # filled bolt

    def soil(self, y=24, base=17):
        """Ground strip between y=base and y (the space below 'base' is kept white for the legend)."""
        self.d.add(Rect(1, base, self.w - 2, y - base, fillColor=hx("ground"), strokeColor=None))   # soil band
        self.d.add(Line(1, y, self.w - 1, y, strokeColor=hx("muted"), strokeWidth=0.8))   # ground line

    def legend(self, items, x=12, y=30, step=None):
        """Legend row: items = [(kind, text)], kind in pe|power|data|spd|tagN."""
        step = step or (self.w - 2 * x) / float(len(items))   # equal spacing
        for i, (kind, label) in enumerate(items):   # draw each legend entry
            xx = x + i * step   # left edge of this entry
            if kind == "pe": self.pe([xx, y + 3, xx + 20, y + 3])   # earth conductor sample
            elif kind == "power": self.wire([xx, y + 3, xx + 20, y + 3], "red", 1.6)   # power sample
            elif kind == "data": self.wire([xx, y + 3, xx + 20, y + 3], "blue", 1.6)   # data sample
            elif kind == "dc": self.wire([xx, y + 3, xx + 20, y + 3], "orange", 1.6)   # DC sample
            elif kind == "spd": self.spd(xx + 10, y + 3, "SPD", w=22, h=11)   # SPD sample
            self.text(xx + 25, y + 0.5, label, size=6.8, color="muted")   # legend text

# ------------------------------------------------------------------ diagrams
def camera_both_ends():
    """Outdoor PoE camera on an earthed pole, protected at both ends of the cable."""
    g = Dg(480, 250, "Outdoor PoE camera: protect both ends, keep the shield earthed")   # canvas
    g.soil(40)   # ground strip
    g.d.add(Rect(70, 25, 7, 150, fillColor=hx("line"), strokeColor=hx("muted"), strokeWidth=0.6))   # metal pole
    g.box(46, 175, 56, 24, ["Camera"], fill="sky", stroke="blue")   # camera on the pole
    g.spd(120, 150, "SPD 1")   # protector near the camera
    g.wire([74, 175, 74, 150, 105, 150], "blue", 1.6)   # camera to SPD 1
    g.wire([135, 150, 330, 150], "blue", 1.6)   # shielded cable run
    g.d.add(Rect(160, 144, 140, 12, fillColor=None, strokeColor=hx("muted"), strokeWidth=0.7, strokeDashArray=[3, 2], rx=6, ry=6))   # cable shield / conduit outline
    g.text(230, 160, "shielded cable (STP), shield continuous", size=6.8, color="muted", anchor="middle")   # cable label
    g.d.add(Rect(318, 25, 150, 175, fillColor=hx("paper"), strokeColor=hx("navy"), strokeWidth=1.2))   # building outline
    g.text(393, 188, "Building", size=8, color="navy", anchor="middle", bold=True)   # building label
    g.spd(345, 150, "SPD 2")   # protector at the building entry
    g.wire([360, 150, 392, 150], "blue", 1.6)   # SPD 2 to PoE switch
    g.box(392, 136, 66, 28, ["PoE switch", "/ recorder"], fill="sky", stroke="blue", size=7)   # power sourcing equipment
    g.box(360, 62, 98, 20, ["Main earthing bar"], fill="mint", stroke="green", size=7)   # common bonding point
    g.pe([345, 142, 345, 72, 360, 72])   # SPD 2 to the earthing bar
    g.pe([425, 136, 425, 82])   # PoE switch protective earth to the bar
    g.pe([409, 62, 409, 34]); g.earth(409, 34)   # bar to the building earth electrode
    g.pe([120, 142, 120, 100, 77, 100])   # SPD 1 bonded to the pole
    g.pe([73, 40, 73, 34]); g.earth(73, 34)   # pole earthed
    g.bolt(14, 222, 34)   # nearby lightning
    g.tag(120, 172, 1); g.tag(345, 172, 2); g.tag(445, 172, 3); g.tag(52, 100, 4)   # numbered markers explained in the caption
    g.legend([("data", "Ethernet / PoE"), ("pe", "earth / bonding"), ("spd", "surge protector")], y=6)   # legend
    return g.d   # finished drawing

def common_bonding():
    """All services and protectors bonded to one main earthing bar with short conductors."""
    g = Dg(480, 240, "One common bonding point for every service")   # canvas
    g.soil(40)   # ground strip
    g.d.add(Rect(120, 25, 345, 180, fillColor=hx("paper"), strokeColor=hx("navy"), strokeWidth=1.2))   # building outline
    g.text(292, 193, "Building", size=8, color="navy", anchor="middle", bold=True)   # building label
    g.box(150, 58, 150, 20, ["Main earthing terminal / bar"], fill="mint", stroke="green", size=7.2)   # the common point
    g.pe([225, 58, 225, 34]); g.earth(225, 34)   # bar to earth electrode
    ys = [(172, "Mains supply", "red", "SPD"), (142, "Telecom / data line", "blue", "SPD"), (112, "Antenna coax", "blue", "SPD")]   # incoming services
    for y, label, colr, dev in ys:   # draw each service entering at the same side
        g.text(10, y + 8, label, size=7, color="ink")   # service label
        g.wire([10, y, 150, y], colr, 1.6)   # service conductor into the building
        g.spd(165, y, dev)   # entry protector
        g.wire([180, y, 330, y], colr, 1.6)   # onward to the equipment
        g.pe([165, y - 8, 165, 78])   # short bond from protector to the bar
    g.text(10, 90, "Metal water / gas pipe", size=7, color="ink"); g.wire([10, 84, 150, 84], "muted", 3)   # metallic pipe
    g.pe([150, 84, 158, 84, 158, 78])   # pipe bonded to the bar
    g.box(330, 100, 120, 84, ["Equipment", "(recorder, switch,", "router, alarm, PLC)"], fill="sky", stroke="blue", size=7.2)   # protected equipment
    g.pe([390, 100, 390, 68, 300, 68])   # equipment protective earth to the same bar
    g.tag(196, 92, 1); g.tag(250, 44, 2); g.tag(345, 60, 3)   # numbered markers explained in the caption
    g.legend([("power", "power"), ("data", "signal / data"), ("pe", "earth / bonding"), ("spd", "entry protector")], y=6)   # legend
    return g.d   # finished drawing

DIAGRAMS = {   # registry: name used in content files -> drawing function
    "camera_both_ends": camera_both_ends,
    "common_bonding": common_bonding,
}

def export_svg(out_dir):
    """Write every diagram as an SVG file (used by the wiki builder)."""
    from reportlab.graphics import renderSVG   # imported lazily: only the wiki build needs it
    import pathlib   # path handling
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)   # target folder
    for name, fn in DIAGRAMS.items():   # every registered diagram
        renderSVG.drawToFile(fn(), str(out / f"{name}.svg"))   # write the SVG
    return sorted(DIAGRAMS)   # names written
