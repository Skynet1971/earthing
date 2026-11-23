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

def earthing_systems():
    """TN-S, TN-C-S and TT side by side."""
    g = Dg(480, 230, "Supply earthing systems: TN-S, TN-C-S and TT")   # canvas
    g.soil(40)   # ground strip
    for i, (name, kind) in enumerate([("TN-S", "tns"), ("TN-C-S (PME)", "tncs"), ("TT", "tt")]):   # three panels
        x0 = 12 + i * 156   # left edge of this panel
        g.d.add(Rect(x0, 44, 148, 148, fillColor=None, strokeColor=hx("line"), strokeWidth=0.6, rx=4, ry=4))   # panel frame
        g.text(x0 + 74, 180, name, size=9, color="navy", anchor="middle", bold=True)   # panel title
        g.d.add(Circle(x0 + 20, 140, 9, fillColor=None, strokeColor=hx("ink"), strokeWidth=1.1))   # transformer winding 1
        g.d.add(Circle(x0 + 20, 126, 9, fillColor=None, strokeColor=hx("ink"), strokeWidth=1.1))   # transformer winding 2
        g.text(x0 + 20, 106, "source", size=6.5, color="muted", anchor="middle")   # source label
        g.box(x0 + 98, 60, 44, 100, ["House"], fill="paper", stroke="navy", size=7)   # consumer installation
        g.wire([x0 + 29, 150, x0 + 98, 150], "red", 1.5); g.text(x0 + 60, 153, "L", size=6.5, color="red", anchor="middle")   # line conductor
        g.wire([x0 + 20, 117, x0 + 20, 100])   # neutral point down to the source earth
        g.earth(x0 + 20, 70); g.pe([x0 + 20, 100, x0 + 20, 70])   # source earth electrode
        if kind == "tns":   # separate N and PE from the source
            g.wire([x0 + 29, 135, x0 + 98, 135], "blue", 1.5); g.text(x0 + 60, 138, "N", size=6.5, color="blue", anchor="middle")   # neutral
            g.pe([x0 + 20, 100, x0 + 60, 100, x0 + 60, 120, x0 + 98, 120]); g.text(x0 + 75, 110, "PE", size=6.5, color="green", anchor="middle")   # protective conductor from the source
            g.tag(x0 + 48, 110, 1)   # marker 1
        elif kind == "tncs":   # combined PEN in the supply, split at the origin
            g.wire([x0 + 20, 100, x0 + 45, 100, x0 + 45, 135, x0 + 98, 135], "blue", 2.0)   # PEN conductor (blue)
            g.wire([x0 + 45, 100, x0 + 45, 135, x0 + 98, 135], "green", 0.8, dash=[3, 3])   # green dashes = combined function
            g.text(x0 + 70, 138, "PEN", size=6.5, color="blue", anchor="middle")   # PEN label
            g.dot(x0 + 104, 135); g.pe([x0 + 104, 135, x0 + 104, 112]); g.text(x0 + 120, 120, "N + PE", size=6.2, color="muted", anchor="middle")   # split point inside the house
            g.pe([x0 + 75, 135, x0 + 75, 70]); g.earth(x0 + 75, 70)   # additional earthing of the PEN along the supply
            g.tag(x0 + 120, 145, 2)   # marker 2
        else:   # TT: consumer's own electrode
            g.wire([x0 + 29, 135, x0 + 98, 135], "blue", 1.5); g.text(x0 + 60, 138, "N", size=6.5, color="blue", anchor="middle")   # neutral only
            g.pe([x0 + 120, 60, x0 + 120, 46]); g.earth(x0 + 120, 46)   # consumer earth electrode
            g.tag(x0 + 134, 54, 3)   # marker 3
    g.legend([("power", "line"), ("data", "neutral (blue)"), ("pe", "protective earth")], y=6)   # legend
    return g.d   # finished drawing

def lpz_zones():
    """Lightning protection zones with SPDs at the boundaries."""
    g = Dg(480, 250, "Lightning protection zones (LPZ) and where SPDs go")   # canvas
    g.soil(40)   # ground strip
    g.d.add(Rect(150, 41, 240, 140, fillColor=hx("sky"), strokeColor=hx("navy"), strokeWidth=1.3))   # building = LPZ 1
    for x in (160, 380):   # air-termination rods on the roof corners
        g.d.add(Line(x, 181, x, 212, strokeColor=hx("muted"), strokeWidth=2)); g.d.add(Circle(x, 213, 2, fillColor=hx("muted"), strokeColor=None))   # rod and tip
    g.wire([160, 212, 110, 41], "muted", 0.8, dash=[3, 3]); g.wire([380, 212, 430, 41], "muted", 0.8, dash=[3, 3])   # edge of the protected volume (sketch)
    g.text(78, 200, "LPZ 0A", size=9, color="amber", anchor="middle", bold=True); g.text(78, 189, "direct strike possible", size=6.5, color="muted", anchor="middle")   # zone 0A
    g.text(124, 120, "LPZ 0B", size=8.5, color="amber", anchor="middle", bold=True)   # zone 0B
    g.text(196, 165, "LPZ 1", size=9, color="teal", anchor="middle", bold=True)   # zone 1
    g.d.add(Rect(285, 60, 90, 70, fillColor=hx("mint"), strokeColor=hx("green"), strokeWidth=1.2, rx=3, ry=3))   # equipment cabinet = LPZ 2
    g.text(330, 118, "LPZ 2", size=9, color="green", anchor="middle", bold=True)   # zone 2
    g.box(300, 70, 60, 26, ["Equipment"], fill="white", stroke="blue", size=7)   # protected equipment
    g.bolt(18, 200, 34)   # lightning
    g.wire([10, 95, 150, 95], "red", 1.6); g.text(14, 99, "power / data line", size=6.8, color="ink")   # incoming line
    g.spd(150, 95, "SPD"); g.wire([165, 95, 285, 95], "red", 1.6); g.spd(285, 95, "SPD"); g.wire([300, 83, 285, 83])   # SPDs at both boundaries
    g.tag(150, 115, 1); g.tag(285, 115, 2)   # markers
    g.legend([("power", "line entering the zones"), ("spd", "SPD at a zone boundary")], y=6)   # legend
    return g.d   # finished drawing

def spd_db_wiring():
    """SPD in the main distribution board with backup protection and short leads."""
    g = Dg(480, 250, "SPD in the main distribution board")   # canvas
    g.d.add(Rect(110, 30, 280, 190, fillColor=hx("paper"), strokeColor=hx("navy"), strokeWidth=1.3, rx=5, ry=5))   # board enclosure
    g.text(250, 207, "Main distribution board (origin of the installation)", size=7.5, color="navy", anchor="middle", bold=True)   # board label
    g.text(20, 168, "Supply", size=7.5, color="ink", bold=True)   # incoming supply label
    g.wire([20, 160, 150, 160], "red", 1.7); g.wire([20, 145, 150, 145], "blue", 1.7)   # incoming L and N
    g.box(150, 138, 46, 30, ["Main", "switch"], fill="white", stroke="ink", size=6.8)   # main switch
    g.wire([196, 160, 360, 160], "red", 1.7); g.wire([196, 145, 360, 145], "blue", 1.7)   # busbars to the final circuits
    g.text(366, 157, "to circuits", size=6.5, color="muted")   # onward label
    g.dot(225, 160, color="red"); g.wire([225, 160, 225, 125], "red", 1.5)   # tap for the SPD branch
    g.box(210, 102, 30, 22, ["OCPD"], fill="white", stroke="red", size=6.5)   # backup overcurrent device
    g.wire([225, 102, 225, 88], "red", 1.5)   # to the SPD line terminal
    g.dot(260, 145, color="blue"); g.wire([260, 145, 260, 88], "blue", 1.5)   # neutral to the SPD
    g.d.add(Rect(212, 62, 62, 26, fillColor=hx("sand"), strokeColor=hx("amber"), strokeWidth=1.3, rx=3, ry=3))   # SPD body
    g.text(243, 72, "SPD", size=8, color="amber", anchor="middle", bold=True)   # SPD label
    g.box(200, 36, 120, 14, ["Earth bar"], fill="mint", stroke="green", size=6.5)   # board earth bar
    g.pe([243, 62, 243, 50])   # SPD earth to the earth bar
    g.pe([320, 43, 420, 43, 420, 30]); g.text(424, 50, "to MET /", size=6.5, color="green"); g.text(424, 42, "earth electrode", size=6.5, color="green")   # bar to the main earthing terminal
    g.wire([290, 160, 290, 60], "amber", 0.8, dash=[2, 2]); g.wire([286, 160, 294, 160], "amber", 0.8); g.wire([286, 60, 294, 60], "amber", 0.8)   # length bracket
    g.text(298, 110, "lead length:", size=6.5, color="amber"); g.text(298, 101, "keep short", size=6.5, color="amber")   # bracket label
    g.tag(195, 75, 1); g.tag(200, 113, 2); g.tag(318, 128, 3); g.tag(230, 56, 4)   # markers
    g.legend([("power", "line"), ("data", "neutral (blue)"), ("pe", "earth"), ("spd", "surge protector")], y=6)   # legend
    return g.d   # finished drawing

def pv_protection():
    """Rooftop PV: frame bonding, d.c. and a.c. SPDs."""
    g = Dg(480, 260, "Rooftop PV: bonding and surge protection points")   # canvas
    g.soil(40)   # ground strip
    g.d.add(Polygon([150, 170, 290, 230, 430, 170], fillColor=hx("paper"), strokeColor=hx("navy"), strokeWidth=1.2))   # roof
    g.d.add(Rect(150, 41, 280, 129, fillColor=None, strokeColor=hx("navy"), strokeWidth=1.2))   # walls
    g.d.add(Polygon([200, 192, 270, 222, 285, 216, 215, 186], fillColor=hx("blue"), strokeColor=hx("navy"), strokeWidth=0.8))   # PV array on the roof
    g.text(318, 222, "PV array + frame", size=6.8, color="navy")   # array label
    g.spd(170, 182, "DC SPD", w=38)   # optional SPD near the array
    g.d.add(Rect(149, 172, 42, 20, fillColor=None, strokeColor=hx("amber"), strokeWidth=0.7, strokeDashArray=[2, 2]))   # dashed = optional
    g.wire([208, 189, 189, 182], "orange", 1.6)   # array to the optional SPD
    g.wire([170, 174, 170, 120, 205, 120], "orange", 1.6)   # d.c. cable to the inverter
    g.spd(222, 120, "DC SPD", w=36)   # SPD at the inverter input
    g.box(240, 100, 54, 40, ["Inverter"], fill="sand", stroke="orange", size=7)   # inverter
    g.wire([294, 120, 312, 120], "red", 1.6); g.spd(328, 120, "AC SPD", w=34); g.wire([345, 120, 360, 120], "red", 1.6)   # a.c. side with SPD
    g.box(360, 96, 56, 48, ["Distribution", "board"], fill="white", stroke="navy", size=6.8)   # distribution board
    g.box(220, 52, 120, 16, ["Equipotential bonding bar"], fill="mint", stroke="green", size=6.5)   # bonding bar
    g.pe([245, 190, 245, 160, 200, 160, 200, 60, 220, 60])   # frame bonding conductor (sketch)
    g.pe([267, 100, 267, 68]); g.pe([222, 112, 222, 68]); g.pe([328, 112, 328, 68, 340, 60])   # inverter and SPD earths to the bar
    g.pe([388, 96, 388, 60, 340, 60]); g.pe([280, 52, 280, 34]); g.earth(280, 34)   # board earth and bar to electrode
    g.tag(198, 170, 1); g.tag(222, 142, 2); g.tag(140, 200, 3); g.tag(328, 142, 4); g.tag(208, 52, 5)   # markers
    g.legend([("dc", "PV d.c."), ("power", "a.c."), ("pe", "bonding / earth"), ("spd", "SPD (dashed = optional)")], y=6)   # legend
    return g.d   # finished drawing

def gate_motor():
    """Sliding gate operator with earth spike, surge protection and low-voltage cables."""
    g = Dg(480, 240, "Sliding gate operator: earthing and cables")   # canvas
    g.soil(50)   # ground strip
    for x in range(30, 230, 16): g.d.add(Line(x, 60, x, 140, strokeColor=hx("muted"), strokeWidth=1.2))   # gate bars
    g.d.add(Rect(26, 60, 200, 80, fillColor=None, strokeColor=hx("ink"), strokeWidth=1.4)); g.text(126, 147, "Gate", size=7.5, color="ink", anchor="middle", bold=True)   # gate leaf
    g.d.add(Rect(10, 55, 450, 4, fillColor=hx("muted"), strokeColor=None))   # rail / base line
    g.d.add(Rect(236, 51, 70, 8, fillColor=hx("line"), strokeColor=None))   # concrete base
    g.box(240, 59, 62, 62, ["Operator"], fill="lilac", stroke="purple", size=7.2)   # gate operator
    g.spd(271, 76, "SPD", w=28, h=13)   # surge protection inside the operator
    g.pe([256, 69, 256, 40]); g.earth(256, 40)   # earth spike next to the operator
    g.box(390, 150, 72, 40, ["House", "board"], fill="paper", stroke="navy", size=7)   # supply board
    g.wire([400, 150, 400, 100, 302, 100], "red", 1.6); g.text(352, 136, "mains cable with PE", size=6.5, color="red", anchor="middle")   # mains supply
    g.pe([420, 150, 420, 92, 302, 92])   # protective earth with the mains cable
    g.d.add(Rect(330, 60, 10, 60, fillColor=hx("muted"), strokeColor=None)); g.text(335, 124, "intercom", size=6.5, color="blue", anchor="middle")   # intercom post
    g.wire([302, 70, 330, 70], "blue", 1.5)   # intercom cable
    g.wire([240, 112, 214, 112, 214, 175], "blue", 1.5); g.d.add(Rect(208, 175, 12, 18, fillColor=hx("sky"), strokeColor=hx("blue"))); g.text(214, 197, "beam", size=6.5, color="blue", anchor="middle")   # safety beam cable
    g.tag(270, 40, 1); g.tag(440, 106, 2); g.tag(271, 100, 3); g.tag(318, 80, 4)   # markers
    g.legend([("power", "mains"), ("data", "low-voltage cables"), ("pe", "earth"), ("spd", "surge protection")], y=6)   # legend
    return g.d   # finished drawing

def fence_energizer():
    """Electric fence energizer earthing and lightning diverter."""
    g = Dg(480, 250, "Electric fence energizer: earth spikes and lightning diverter")   # canvas
    g.soil(70)   # ground strip
    for x in range(20, 200, 30): g.d.add(Line(x, 70, x, 170, strokeColor=hx("muted"), strokeWidth=2))   # fence posts
    g.wire([20, 160, 200, 160], "red", 1.4); g.wire([20, 130, 200, 130], "green", 1.4); g.wire([20, 100, 200, 100], "red", 1.4)   # live and earth fence wires
    g.text(110, 178, "Fence (live + earth wires)", size=7, color="ink", anchor="middle", bold=True)   # fence label
    g.d.add(Rect(330, 71, 140, 130, fillColor=hx("paper"), strokeColor=hx("navy"), strokeWidth=1.2)); g.text(400, 190, "Building", size=7.5, color="navy", anchor="middle", bold=True)   # building
    g.box(340, 130, 60, 34, ["Energizer"], fill="lilac", stroke="purple", size=7)   # energizer on the wall
    g.wire([340, 158, 260, 158, 260, 160, 200, 160], "red", 1.5)   # live output to the fence
    g.spd(250, 140, "Diverter", w=40)   # lightning diverter between energizer and fence
    g.wire([250, 158, 250, 148], "red", 1.2)   # diverter tap on the live lead
    g.pe([340, 136, 300, 136, 300, 100, 220, 100, 220, 70])   # energizer earth terminal to the spikes
    for x in (220, 250, 280): g.pe([x, 100, x, 70]); g.earth(x, 70)   # three earth spikes
    g.pe([250, 132, 250, 100])   # diverter earth to the spike line
    g.wire([220, 76, 280, 76], "ink", 0.7); g.text(250, 80, "spacing", size=6.5, color="ink", anchor="middle")   # spacing dimension
    g.pe([440, 71, 440, 60]); g.earth(440, 60); g.text(440, 80, "building earth", size=6.5, color="green", anchor="middle")   # building earth electrode
    g.wire([290, 76, 430, 76], "ink", 0.7, dash=[3, 2]); g.text(372, 80, "separation", size=6.5, color="ink", anchor="middle")   # separation distance
    g.tag(320, 120, 1); g.tag(206, 80, 2); g.tag(250, 122, 3); g.tag(330, 90, 4)   # markers
    g.legend([("power", "live (pulse) wire"), ("pe", "earth wire / spikes"), ("spd", "lightning diverter")], y=6)   # legend
    return g.d   # finished drawing

def between_buildings():
    """Data link between two buildings: copper with SPDs and bonding, or fibre."""
    g = Dg(480, 240, "Cables between two buildings")   # canvas
    g.soil(46)   # ground strip
    for x0, name in ((20, "Building A"), (340, "Building B")):   # two buildings
        g.d.add(Rect(x0, 47, 120, 150, fillColor=hx("paper"), strokeColor=hx("navy"), strokeWidth=1.2)); g.text(x0 + 60, 185, name, size=7.5, color="navy", anchor="middle", bold=True)   # outline
        g.box(x0 + 30, 58, 60, 14, ["Earth bar"], fill="mint", stroke="green", size=6.5)   # each building's earth bar
        g.pe([x0 + 60, 58, x0 + 60, 32]); g.earth(x0 + 60, 32)   # each building's electrode
    g.text(240, 160, "Option A: copper cable", size=7, color="blue", anchor="middle", bold=True)   # option A label
    g.wire([110, 150, 370, 150], "blue", 1.6); g.spd(140, 150, "SPD"); g.spd(340, 150, "SPD")   # copper with SPDs at each entry
    g.pe([140, 142, 140, 72, 120, 72, 120, 65, 110, 65]); g.pe([340, 142, 340, 72, 360, 72, 360, 65, 370, 65])   # SPD earths to the bars
    g.pe([80, 32, 80, 28, 400, 28, 400, 32])   # buried bonding conductor between the electrodes
    g.text(240, 36, "earth conductor between the buildings", size=6.5, color="green", anchor="middle")   # label
    g.text(240, 118, "Option B: fibre, no metal", size=7, color="purple", anchor="middle", bold=True)   # option B label
    g.wire([110, 108, 370, 108], "purple", 1.6, dash=[6, 3])   # fibre link
    g.tag(140, 170, 1); g.tag(220, 22, 2); g.tag(320, 118, 3)   # markers
    g.legend([("data", "copper data cable"), ("pe", "earth / bonding"), ("spd", "SPD")], y=6)   # legend
    return g.d   # finished drawing

def antenna_mast():
    """Wall-mounted antenna mast with a straight vertical earthing conductor, and the coax entry."""
    g = Dg(480, 250, "Antenna mast and coax entry")   # canvas
    g.soil(40)   # ground strip
    g.d.add(Polygon([110, 150, 240, 205, 370, 150], fillColor=hx("paper"), strokeColor=hx("navy"), strokeWidth=1.2)); g.d.add(Rect(110, 41, 260, 109, fillColor=None, strokeColor=hx("navy"), strokeWidth=1.2))   # house
    g.d.add(Line(392, 120, 392, 236, strokeColor=hx("muted"), strokeWidth=2.4))   # mast fixed to the gable wall
    for y in (130, 170): g.d.add(Line(370, y, 392, y, strokeColor=hx("muted"), strokeWidth=1.6))   # wall brackets
    for y, w in ((232, 18), (224, 14), (216, 10)): g.d.add(Line(392 - w, y, 392 + w, y, strokeColor=hx("ink"), strokeWidth=1.4))   # antenna elements
    g.pe([398, 120, 398, 34]); g.earth(398, 34)   # straight vertical earthing conductor to its electrode
    g.wire([388, 210, 384, 210, 384, 130, 110, 130], "blue", 1.6)   # coax down the mast and into the house
    g.text(52, 134, "coax to the TV / radio", size=6.5, color="blue", anchor="middle")   # coax label
    g.spd(140, 130, "SPD")   # SPD / shield bond at entry
    g.box(130, 60, 100, 16, ["Main earthing terminal"], fill="mint", stroke="green", size=6.5)   # MET
    g.pe([140, 122, 140, 76]); g.pe([180, 60, 180, 34]); g.earth(180, 34); g.pe([230, 68, 398, 68])   # SPD to MET, MET to earth, bond to the mast conductor
    g.tag(412, 96, 1); g.tag(158, 145, 2); g.tag(118, 112, 3); g.tag(155, 90, 4)   # markers
    g.legend([("data", "coax"), ("pe", "earth / bonding"), ("spd", "SPD / shield bond")], y=6)   # legend
    return g.d   # finished drawing

def rack_bonding():
    """Equipment rack bonding to the earthing bar."""
    g = Dg(480, 240, "Equipment rack bonding")   # canvas
    g.d.add(Rect(120, 30, 130, 175, fillColor=hx("paper"), strokeColor=hx("ink"), strokeWidth=1.6)); g.text(170, 193, "Rack", size=8, color="ink", anchor="middle", bold=True)   # rack frame
    g.d.add(Rect(232, 40, 10, 155, fillColor=hx("mint"), strokeColor=hx("green"), strokeWidth=1.2)); g.text(256, 44, "rack busbar", size=6.5, color="green")   # rack bonding busbar
    for i, name in enumerate(["Patch panel", "Switch", "Router", "Recorder"]):   # rack-mounted equipment
        y = 160 - i * 34; g.box(132, y, 86, 24, [name], fill="sky", stroke="blue", size=7); g.pe([218, y + 12, 232, y + 12])   # device and its bond
    g.box(340, 100, 110, 20, ["Earthing bar"], fill="mint", stroke="green", size=7)   # wall earthing bar
    g.pe([242, 110, 340, 110]); g.pe([395, 100, 395, 50]); g.text(400, 70, "to the main earthing", size=6.5, color="green"); g.text(400, 61, "terminal / building earth", size=6.5, color="green")   # bonding conductors
    g.earth(395, 50)   # building earth
    g.tag(224, 196, 1); g.tag(290, 122, 2); g.tag(380, 80, 3)   # markers
    g.legend([("pe", "bonding conductor")], y=6)   # legend
    return g.d   # finished drawing

def plc_cabling():
    """Control panel with PLC, shielded outdoor signal line and SPD."""
    g = Dg(480, 240, "PLC panel: functional earth, shields and outdoor lines")   # canvas
    g.d.add(Rect(20, 40, 200, 170, fillColor=hx("paper"), strokeColor=hx("navy"), strokeWidth=1.3)); g.text(120, 197, "Control panel", size=7.5, color="navy", anchor="middle", bold=True)   # panel
    g.box(35, 140, 60, 36, ["PSU"], fill="white", stroke="red", size=7); g.box(115, 140, 80, 36, ["PLC"], fill="lilac", stroke="purple", size=7)   # PSU and PLC
    g.wire([95, 158, 115, 158], "red", 1.4)   # supply to the PLC
    g.box(40, 52, 150, 14, ["Panel earth bar"], fill="mint", stroke="green", size=6.5)   # earth bar
    g.pe([65, 140, 65, 66]); g.pe([180, 140, 180, 66]); g.text(186, 100, "FE", size=6.5, color="green")   # PSU PE and PLC functional earth
    g.wire([155, 140, 155, 110, 205, 110], "blue", 1.5); g.spd(220, 110, "SPD")   # signal line to the panel entry SPD
    g.pe([220, 102, 220, 80, 150, 80, 150, 66])   # SPD earth to the panel bar
    g.wire([235, 110, 420, 110], "blue", 1.5); g.d.add(Rect(250, 104, 150, 12, fillColor=None, strokeColor=hx("muted"), strokeWidth=0.7, strokeDashArray=[3, 2], rx=6, ry=6))   # shielded outdoor cable
    g.text(325, 120, "shielded signal cable (outdoors)", size=6.5, color="muted", anchor="middle")   # cable label
    g.box(420, 96, 46, 28, ["Sensor"], fill="sky", stroke="blue", size=7)   # field sensor
    g.wire([5, 158, 35, 158], "red", 1.5); g.text(8, 162, "supply", size=6.3, color="red")   # incoming supply to the PSU
    g.wire([220, 180, 420, 180], "red", 1.5); g.box(420, 168, 46, 24, ["Outdoor", "load"], fill="white", stroke="red", size=6.3); g.text(325, 184, "power cable on a separate route", size=6.5, color="red", anchor="middle")   # separate power route
    g.wire([65, 176, 65, 180, 220, 180], "red", 1.5)   # power leaving the panel
    g.tag(196, 92, 1); g.tag(258, 96, 2); g.tag(220, 128, 3); g.tag(300, 150, 4)   # markers
    g.legend([("power", "power"), ("data", "signal"), ("pe", "earth / FE"), ("spd", "SPD")], y=6)   # legend
    return g.d   # finished drawing

DIAGRAMS = {   # registry: name used in content files -> drawing function
    "camera_both_ends": camera_both_ends,
    "common_bonding": common_bonding,
    "earthing_systems": earthing_systems,
    "lpz_zones": lpz_zones,
    "spd_db_wiring": spd_db_wiring,
    "pv_protection": pv_protection,
    "gate_motor": gate_motor,
    "fence_energizer": fence_energizer,
    "between_buildings": between_buildings,
    "antenna_mast": antenna_mast,
    "rack_bonding": rack_bonding,
    "plc_cabling": plc_cabling,
}

def export_svg(out_dir):
    """Write every diagram as an SVG file (used by the wiki builder)."""
    from reportlab.graphics import renderSVG   # imported lazily: only the wiki build needs it
    import pathlib   # path handling
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)   # target folder
    for name, fn in DIAGRAMS.items():   # every registered diagram
        renderSVG.drawToFile(fn(), str(out / f"{name}.svg"))   # write the SVG
    return sorted(DIAGRAMS)   # names written
