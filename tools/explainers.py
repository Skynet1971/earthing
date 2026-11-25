"""Animated explainer graphics (SVG with CSS and SMIL animation) for the wiki, with still frames for the PDFs.

Each explainer illustrates a mechanism stated in verified facts; the caption in the content file carries the
citations. Numbers drawn inside an explainer must come from the facts named in its docstring.
Readability rules: drawn on a 960 x 540 canvas, no text below 17 px, sans-serif font chain, and the picture
must make sense at the still time (the moment used for the PDF frame).
"""
import html   # escaping of label text

FONT = "Segoe UI, Helvetica, Arial, sans-serif"   # Windows, macOS and Linux all have one of these
C = {"navy": "#0F2A47", "ink": "#1F2937", "muted": "#6B7280", "line": "#9CA3AF", "paper": "#F8FAFC", "white": "#FFFFFF",
     "green": "#2F9E44", "yellow": "#FACC15", "amber": "#D97706", "red": "#DC2626", "blue": "#2563EB", "teal": "#0E7490",
     "orange": "#EA580C", "purple": "#7C3AED", "sky": "#E8F0FE", "mint": "#E9F7EC", "sand": "#FEF4E2", "rose": "#FDECEC",
     "lilac": "#F1EAFE", "soil": "#D6C7A8", "glow": "#FFF7CC"}   # same palette as the PDFs

class Svg:
    """Tiny SVG writer: collects elements, then wraps them with the shared style sheet."""
    def __init__(self, title, accent, w=960, h=540):
        self.w, self.h, self.items, self.css = w, h, [], []   # canvas, element list, extra CSS
        self.add(f'<rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="{C["white"]}" stroke="{C["line"]}"/>')   # framed background
        self.add(f'<rect x="0" y="0" width="{w}" height="58" rx="14" fill="{C[accent]}"/><rect x="0" y="40" width="{w}" height="18" fill="{C[accent]}"/>')   # coloured title band
        self.add(self._pe_stripe(0, 58, w, 6))   # green/yellow earth stripe under the band
        self.text(24, 39, title, 26, "white", weight="700")   # title

    def add(self, s):
        """Append raw SVG markup."""
        self.items.append(s); return self   # chainable

    def _pe_stripe(self, x, y, w, h):
        """Green/yellow diagonal stripe (protective earth motif)."""
        return (f'<defs><pattern id="pe" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                f'<rect width="8" height="16" fill="{C["green"]}"/><rect x="8" width="8" height="16" fill="{C["yellow"]}"/></pattern></defs>'
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#pe)"/>')   # patterned band

    def text(self, x, y, s, size=18, color="ink", anchor="start", weight="400", cls=""):
        """Text label (size in px; never below 17 by rule)."""
        size = max(size, 17)   # readability rule
        c = C.get(color, color)   # palette lookup
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" text-anchor="{anchor}" font-weight="{weight}"{f" class=\"{cls}\"" if cls else ""}>{html.escape(s)}</text>')   # the label
        return self   # chainable

    def box(self, x, y, w, h, rows, fill="paper", stroke="navy", size=18, cls=""):
        """Rounded box with centred lines of text (first line bold)."""
        g = f'<g{f" class=\"{cls}\"" if cls else ""}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{C[fill]}" stroke="{C[stroke]}" stroke-width="2.5"/>'   # box
        rows = [rows] if isinstance(rows, str) else rows   # one or more lines
        lead = size * 1.25   # line spacing
        top = y + h / 2 - (len(rows) - 1) * lead / 2 + size * 0.35   # first baseline (vertically centred)
        for i, r in enumerate(rows):   # each line
            g += f'<text x="{x + w / 2}" y="{top + i * lead}" font-size="{max(size, 17)}" fill="{C["ink"]}" text-anchor="middle" font-weight="{700 if i == 0 else 400}">{html.escape(r)}</text>'   # line
        self.add(g + "</g>"); return self   # close the group

    def line(self, pts, color="ink", width=4, dash=None, cls="", extra=""):
        """Poly-line through points [(x, y), ...]."""
        d = " ".join(f"{x},{y}" for x, y in pts)   # point list
        self.add(f'<polyline points="{d}" fill="none" stroke="{C.get(color, color)}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"'
                 f'{f" stroke-dasharray=\"{dash}\"" if dash else ""}{f" class=\"{cls}\"" if cls else ""} {extra}/>')   # the line
        return self   # chainable

    def pe(self, pts, width=6, cls=""):
        """Protective earth / bonding conductor: green with yellow dashes."""
        self.line(pts, "green", width, cls=cls); self.line(pts, "yellow", width * 0.42, dash="10 10", cls=cls); return self   # two strokes

    def earth(self, x, y, s=16, color="green"):
        """Earth symbol below the point x, y."""
        c = C[color]   # colour
        self.add(f'<g stroke="{c}" stroke-width="4" stroke-linecap="round"><line x1="{x}" y1="{y}" x2="{x}" y2="{y + s}"/>'
                 f'<line x1="{x - s}" y1="{y + s}" x2="{x + s}" y2="{y + s}"/><line x1="{x - s * 0.62}" y1="{y + s * 1.45}" x2="{x + s * 0.62}" y2="{y + s * 1.45}"/>'
                 f'<line x1="{x - s * 0.25}" y1="{y + s * 1.9}" x2="{x + s * 0.25}" y2="{y + s * 1.9}"/></g>')   # stem and three bars
        return self   # chainable

    def spd(self, x, y, label="SPD", w=78, h=40, cls=""):
        """Surge protective device (amber box) centred on x, y."""
        return self.box(x - w / 2, y - h / 2, w, h, label, fill="sand", stroke="amber", size=17, cls=cls)   # amber box

    def bolt(self, x, y, s=90, cls="flash"):
        """Lightning bolt with its top-left at x, y."""
        pts = [(0.45, 0), (0.05, 0.55), (0.36, 0.55), (0.18, 1.0), (0.78, 0.40), (0.47, 0.40), (0.72, 0)]   # outline
        d = " ".join(f"{x + px * s},{y + py * s}" for px, py in pts)   # scaled points
        self.add(f'<polygon class="{cls}" points="{d}" fill="{C["yellow"]}" stroke="{C["amber"]}" stroke-width="3"/>'); return self   # bolt

    def dots(self, path, color, n=4, dur=2.0, r=8, cls=""):
        """Charges moving along an SVG path string (SMIL animateMotion)."""
        g = f'<g{f" class=\"{cls}\"" if cls else ""}>'   # group (phase class controls visibility)
        for i in range(n):   # evenly spaced along the path
            g += (f'<circle r="{r}" fill="{C[color]}" stroke="white" stroke-width="2"><animateMotion dur="{dur}s" repeatCount="indefinite" '
                  f'begin="{-dur * i / n:.2f}s" path="{path}"/></circle>')   # one moving dot
        self.add(g + "</g>"); return self   # close

    def step(self, x, y, n, label, color, cls):
        """Step legend entry: numbered disc and text; the class animates its highlight."""
        self.add(f'<g class="{cls}"><rect x="{x - 8}" y="{y - 26}" width="{self.w - x - 16}" height="38" rx="9" fill="{C[color]}" opacity="0.13"/>'
                 f'<circle cx="{x + 14}" cy="{y - 7}" r="15" fill="{C[color]}"/>'
                 f'<text x="{x + 14}" y="{y - 1}" font-size="18" fill="white" text-anchor="middle" font-weight="700">{n}</text>'
                 f'<text x="{x + 40}" y="{y}" font-size="18" fill="{C["ink"]}">{html.escape(label)}</text></g>')   # entry
        return self   # chainable

    def render(self):
        """Return the complete SVG document."""
        css = ("text{font-family:" + FONT + "}"
               ".flash{animation:flash var(--cycle) infinite}"
               "@keyframes flash{0%,6%{opacity:1}3%{opacity:.25}12%,100%{opacity:.35}}"
               ".flow{stroke-dasharray:14 12;animation:flow 1s linear infinite}@keyframes flow{to{stroke-dashoffset:-26}}"
               "@media (prefers-reduced-motion: reduce){*{animation:none!important}}") + "".join(self.css)   # shared animations
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
                f'role="img" font-family="{FONT}"><style>{css}</style>' + "".join(self.items) + "</svg>")   # document

def phases(svg, cycle, windows):
    """Add CSS that shows class p<i> only during its time window (fractions of the cycle) and dims other steps."""
    svg.css.append(f"svg{{--cycle:{cycle}s}}")   # cycle length used by .flash
    for i, (a, b) in enumerate(windows, 1):   # one window per phase
        a, b = int(a * 100), int(b * 100)   # percentages
        def frames(lo):   # keyframes: off before the window, on inside it, off after it (no fade when it ends at 100 %)
            k = [f"0%{{opacity:{1 if a == 0 else lo}}}"]   # start of the cycle
            if a > 0: k += [f"{a - 1}%{{opacity:{lo}}}", f"{a}%{{opacity:1}}"]   # switch on at the window start
            k += [f"{b}%{{opacity:1}}"]   # stay on to the window end
            if b < 100: k += [f"{b + 1}%{{opacity:{lo}}}", f"100%{{opacity:{lo}}}"]   # switch off after the window
            return "".join(k)   # keyframe text
        svg.css.append(f".p{i}{{animation:p{i} {cycle}s infinite}}@keyframes p{i}{{{frames(0)}}}")   # visible window
        svg.css.append(f".s{i}{{animation:s{i} {cycle}s infinite}}@keyframes s{i}{{{frames(.35)}}}")   # step highlight

# ------------------------------------------------------------------ explainers
def ex_fault_path():
    """How a fault is cleared in a TN-C-S supply. Facts: J039, J040 (PEN carries the earth-fault current back
    to the transformer), D047 (0.4 s automatic disconnection for socket-outlet circuits in TN systems)."""
    s = Svg("How the earth makes a fault switch itself off (TN-C-S supply)", "green", h=560)   # canvas
    phases(s, 12, [(0.0, 0.33), (0.33, 0.66), (0.66, 1.0)])   # three steps of 4 s
    s.add(f'<rect x="20" y="410" width="920" height="22" fill="{C["soil"]}"/>')   # ground
    s.add(f'<circle cx="95" cy="190" r="36" fill="none" stroke="{C["ink"]}" stroke-width="4"/><circle cx="95" cy="240" r="36" fill="none" stroke="{C["ink"]}" stroke-width="4"/>')   # transformer
    s.text(95, 115, "Supply", 18, "ink", "middle", "700").text(95, 136, "transformer", 17, "muted", "middle")   # transformer label
    s.line([(95, 276), (95, 330)], "ink", 4)   # star point lead
    s.pe([(95, 330), (95, 395)]); s.earth(95, 395)   # supply earth
    s.add(f'<rect x="300" y="90" width="620" height="315" rx="12" fill="{C["paper"]}" stroke="{C["navy"]}" stroke-width="3"/>')   # house
    s.text(318, 118, "House", 20, "navy", weight="700")   # house label
    s.line([(131, 175), (470, 175)], "red", 6)   # L to the protective device
    s.text(200, 165, "L", 19, "red", weight="700")   # L label
    s.line([(131, 255), (360, 255)], "blue", 7); s.line([(131, 255), (360, 255)], "green", 3, dash="12 12")   # PEN conductor
    s.text(128, 236, "PEN (N + PE combined)", 17, "blue", weight="700")   # PEN label (between L and PEN, clear of the PE riser)
    s.add(f'<circle cx="360" cy="255" r="8" fill="{C["ink"]}"/>')   # split point at the origin
    s.line([(360, 255), (700, 255)], "blue", 6); s.text(560, 247, "N", 19, "blue", weight="700")   # neutral inside the house
    s.pe([(360, 255), (360, 345), (420, 345)])   # PE to the main earthing terminal
    s.box(420, 325, 190, 42, "Main earthing terminal", fill="mint", stroke="green", size=17)   # MET
    s.pe([(610, 345), (830, 345), (830, 300)])   # PE to the appliance case
    s.box(470, 150, 120, 50, ["Protective", "device"], fill="white", stroke="ink", size=17)   # breaker / RCD box
    s.add(f'<g class="p3"><rect x="470" y="150" width="120" height="50" rx="10" fill="{C["rose"]}" stroke="{C["red"]}" stroke-width="3"/>'
          f'<text x="530" y="182" font-size="19" fill="{C["red"]}" text-anchor="middle" font-weight="700">OPEN</text></g>')   # tripped state
    s.line([(590, 175), (700, 175)], "red", 6)   # L to the appliance
    s.add(f'<rect x="700" y="140" width="190" height="160" rx="12" fill="{C["sky"]}" stroke="{C["blue"]}" stroke-width="3"/>')   # appliance metal case
    s.text(795, 130, "Appliance (metal case)", 18, "navy", "middle", "700")   # appliance label above the case
    s.add(f'<polyline points="730,175 745,175 755,160 770,190 785,160 800,190 815,175 860,175 860,255 700,255" fill="none" stroke="{C["ink"]}" stroke-width="3"/>')   # heating element
    s.add(f'<g class="p2"><polygon points="760,230 772,248 790,244 778,260 790,276 770,268 760,286 752,266 732,270 746,256 734,240 752,244" fill="{C["red"]}"/></g>')   # fault spark
    s.dots("M131,175 L470,175 L590,175 L700,175 L745,175 L860,175 L860,255 L700,255 L360,255 L131,255", "amber", 6, 2.4, cls="p1")   # normal current loop
    s.dots("M131,175 L470,175 L590,175 L700,175 L765,175 L765,250 L830,300 L830,345 L610,345 M420,345 L360,345 L360,255 L131,255", "red", 6, 2.0, cls="p2")   # fault current loop
    s.step(40, 462, 1, "Normal: current goes out on L and returns on the neutral.", "blue", "s1")   # step 1
    s.step(40, 503, 2, "Fault: L touches the metal case. Current returns on PE and the PEN to the transformer.", "red", "s2")   # step 2
    s.step(40, 544 - 2, 3, "The protective device opens automatically (TN: within 0.4 s for socket-outlet circuits).", "green", "s3")   # step 3
    return s.render(), 6.0   # SVG and still time

def ex_surge_camera():
    """A nearby flash induces a surge on a PoE camera cable; protectors at both ends divert it to earth.
    Facts: C010 (cable picks up fields), C018 (PoE protectors divert surges to ground), E065 (one protector near the
    outdoor device, one at the building entry), C011/C012/C014 (shield diverts energy via an earthed PSE)."""
    s = Svg("How a surge reaches a PoE camera, and where it is diverted", "teal", h=600)   # canvas
    phases(s, 9, [(0.0, 0.25), (0.25, 0.62), (0.62, 0.85), (0.85, 1.0)])   # four steps
    s.add(f'<rect x="20" y="380" width="920" height="24" fill="{C["soil"]}"/>')   # ground
    s.bolt(395, 70, 120)   # nearby flash
    s.add(f'<rect x="118" y="150" width="16" height="230" fill="{C["line"]}"/>')   # metal pole
    s.box(70, 100, 130, 48, "Camera", fill="sky", stroke="blue", size=19)   # camera
    s.spd(200, 205, "SPD 1")   # protector near the camera
    s.line([(134, 148), (134, 205), (161, 205)], "blue", 5)   # camera to SPD 1
    s.add(f'<rect x="240" y="191" width="380" height="28" rx="14" fill="none" stroke="{C["muted"]}" stroke-width="2" stroke-dasharray="6 5"/>')   # cable shield outline
    s.line([(239, 205), (640, 205)], "blue", 5)   # cable run
    s.text(430, 248, "shielded cable (STP)", 17, "muted", "middle")   # cable label
    s.pe([(200, 225), (200, 300), (134, 300)]); s.pe([(126, 380), (126, 392)]); s.earth(126, 392, 12)   # SPD 1 bonded to the pole, pole earthed
    s.add(f'<rect x="610" y="100" width="320" height="280" rx="12" fill="{C["paper"]}" stroke="{C["navy"]}" stroke-width="3"/>')   # building
    s.text(770, 128, "Building", 20, "navy", "middle", "700")   # building label
    s.spd(680, 205, "SPD 2")   # protector at the entry
    s.line([(719, 205), (760, 205)], "blue", 5)   # SPD 2 to the switch
    s.box(760, 175, 150, 60, ["PoE switch", "(earthed)"], fill="sky", stroke="blue", size=18)   # PSE
    s.box(700, 305, 200, 42, "Main earthing bar", fill="mint", stroke="green", size=17)   # MET
    s.pe([(680, 225), (680, 326), (700, 326)]); s.pe([(835, 235), (835, 305)]); s.pe([(800, 347), (800, 392)]); s.earth(800, 392, 12)   # earths
    s.add(f'<g class="p1"><path d="M330,170 q20,-18 40,0 t40,0 t40,0" fill="none" stroke="{C["amber"]}" stroke-width="4"/>'
          f'<text x="455" y="160" font-size="18" fill="{C["amber"]}" text-anchor="middle" font-weight="700">induced voltage</text></g>')   # induction
    s.dots("M430,205 L240,205", "amber", 4, 1.6, r=9, cls="p2")   # surge travelling to the camera end
    s.dots("M430,205 L640,205", "amber", 4, 1.6, r=9, cls="p2")   # surge travelling to the building end
    s.dots("M200,225 L200,300 L134,300 L126,392", "amber", 3, 1.4, r=8, cls="p3")   # diverted at SPD 1
    s.dots("M680,225 L680,326 L800,326 L800,392", "amber", 3, 1.4, r=8, cls="p3")   # diverted at SPD 2
    s.add(f'<g class="p4"><circle cx="890" cy="160" r="22" fill="{C["green"]}"/><polyline points="879,160 887,168 902,151" fill="none" stroke="white" stroke-width="5" stroke-linecap="round"/></g>')   # protected tick
    s.step(40, 446, 1, "A nearby flash induces a voltage on the camera cable.", "amber", "s1")   # step 1
    s.step(40, 488, 2, "The surge travels along the cable towards both ends.", "red", "s2")   # step 2
    s.step(40, 530, 3, "SPD 1 and SPD 2 divert it to earth: the pole and the main earthing bar.", "green", "s3")   # step 3
    s.step(40, 572, 4, "Camera and switch are protected; the earthed switch gives the cable shield its path to earth.", "teal", "s4")   # step 4
    return s.render(), 4.2   # SVG and still time

def ex_potential_difference():
    """Separate earth vs one bonding point. Facts: B026 (50 A through a 300 ohm telecom earth electrode raises the
    telecom equipment 15 kV above the power network), B025 (common earth bar with short bond wires protects)."""
    s = Svg("Why separate earths destroy equipment (ITU-T K.66 example)", "red")   # canvas
    phases(s, 8, [(0.0, 0.2), (0.2, 1.0)])   # surge arrives, then voltage builds
    for x0, title, ok in ((20, "Separate telecom earth", False), (490, "One common bonding point", True)):   # two panels
        col = "green" if ok else "red"   # panel colour
        s.add(f'<rect x="{x0}" y="74" width="450" height="440" rx="12" fill="{C["mint"] if ok else C["rose"]}" stroke="{C[col]}" stroke-width="3"/>')   # panel
        s.text(x0 + 225, 106, title, 21, col, "middle", "700")   # panel title
        s.add(f'<rect x="{x0 + 10}" y="430" width="430" height="20" fill="{C["soil"]}"/>')   # ground
        s.box(x0 + 150, 150, 150, 70, ["Equipment", "(modem, router)"], fill="white", stroke="blue", size=18)   # equipment
        s.line([(x0 + 30, 170), (x0 + 150, 170)], "blue", 5); s.text(x0 + 30, 160, "telecom line", 17, "blue")   # telecom line
        s.line([(x0 + 300, 200), (x0 + 420, 200)], "red", 5); s.text(x0 + 330, 190, "mains", 17, "red")   # mains
        s.box(x0 + 290, 330, 150, 40, "Power earth", fill="mint", stroke="green", size=17)   # power earth bar
        s.pe([(x0 + 260, 220), (x0 + 260, 290), (x0 + 365, 290), (x0 + 365, 330)]); s.pe([(x0 + 365, 370), (x0 + 365, 430)]); s.earth(x0 + 365, 430, 12)   # equipment PE
        s.spd(x0 + 90, 250, "Protector", w=110)   # telecom primary protector
        s.line([(x0 + 90, 170), (x0 + 90, 230)], "blue", 4)   # line to the protector
        if ok:   # bonded: protector earth goes to the same bar with a short conductor
            s.pe([(x0 + 90, 270), (x0 + 90, 350), (x0 + 290, 350)]); s.text(x0 + 105, 390, "short bond to the same bar", 17, "green", weight="700")   # bond
        else:   # separate electrode
            s.pe([(x0 + 90, 270), (x0 + 90, 430)]); s.earth(x0 + 90, 430, 12); s.text(x0 + 104, 400, "own electrode, 300 Ω", 17, "red", weight="700")   # separate earth
        s.dots(f"M{x0 + 30},170 L{x0 + 90},170 L{x0 + 90},270 L{x0 + 90},{350 if ok else 430}", "amber", 3, 1.4, r=8, cls="p1")   # 50 A surge into the protector earth
        s.text(x0 + 225, 134, "50 A surge from the telecom line", 17, "ink", "middle")   # common label
    s.add(f'<g class="p2"><rect x="70" y="458" width="300" height="44" rx="10" fill="{C["red"]}"/>'
          f'<text x="220" y="488" font-size="21" fill="white" text-anchor="middle" font-weight="700">15 kV across the equipment</text></g>')   # left result
    s.add(f'<g class="p2"><rect x="565" y="458" width="300" height="44" rx="10" fill="{C["green"]}"/>'
          f'<text x="715" y="488" font-size="20" fill="white" text-anchor="middle" font-weight="700">protected by the common bar</text></g>')   # right result
    return s.render(), 5.0   # SVG and still time

def ex_spd_leads():
    """Why SPD leads must be short and bound. Facts: I027 (1 µH/m, about 1 kV per metre at 1 kA/µs), I028 (0.5 m),
    I030 (Up 600 V; 25 cm bound gave 630 V), I031 (unbound: 810 V with 25 cm, 2300 V with 2 m), K009 (2 m bound: 1200 V),
    K008 (equipment immunity 700 V in that example), I020 (category I equipment 1.5 kV)."""
    s = Svg("SPD wire length: BEAMA test results (bound vs unbound)", "amber")   # canvas
    s.css.append(".bar{transform-box:fill-box;transform-origin:bottom;animation:grow 8s infinite}"
                 "@keyframes grow{0%{transform:scaleY(0)}16%,94%{transform:scaleY(1)}100%{transform:scaleY(1)}}"
                 ".b2{animation-delay:.4s}.b3{animation-delay:.8s}.b4{animation-delay:1.2s}.b5{animation-delay:1.6s}")   # bars grow one after another
    s.add(f'<rect x="20" y="86" width="300" height="430" rx="12" fill="{C["paper"]}" stroke="{C["navy"]}" stroke-width="2"/>')   # left panel
    s.text(170, 116, "In the distribution board", 19, "navy", "middle", "700")   # panel title
    s.line([(44, 160), (296, 160)], "red", 7); s.text(48, 150, "line (point A)", 17, "red")   # busbar
    s.box(105, 232, 130, 56, "SPD", fill="sand", stroke="amber", size=21)   # SPD
    s.line([(170, 160), (170, 232)], "red", 5, cls="flow")   # lead l1
    s.box(70, 360, 200, 40, "Earth bar (point B)", fill="mint", stroke="green", size=17)   # earth bar
    s.pe([(170, 288), (170, 360)])   # lead l2
    s.text(190, 204, "l1", 19, "amber", weight="700").text(190, 332, "l2", 19, "amber", weight="700")   # lead labels
    s.text(170, 436, "≈ 1 kV per metre of lead", 18, "ink", "middle", "700")   # rule of thumb
    s.text(170, 460, "at 1 kA/µs (1 µH/m)", 17, "muted", "middle")   # basis
    s.text(170, 492, "preferably l1 + l2 ≤ 0.5 m", 18, "green", "middle", "700")   # recommendation
    x0, y0, hmax, vmax = 410, 450, 320, 2500   # chart origin, height, top of scale
    s.line([(x0, y0), (940, y0)], "ink", 2); s.line([(x0, y0), (x0, y0 - hmax - 10)], "ink", 2)   # axes
    for v in (500, 1000, 1500, 2000, 2500):   # gridlines
        y = y0 - hmax * v / vmax; s.line([(x0, y), (940, y)], "line", 1); s.text(x0 - 8, y + 6, f"{v} V", 17, "muted", "end")   # gridline + label
    for v, lab, col in ((700, "equipment in this test: 700 V", "green"), (1500, "category I equipment: 1.5 kV", "red")):   # reference levels
        y = y0 - hmax * v / vmax; s.line([(x0, y), (940, y)], col, 3, dash="10 8")   # dashed level line
        ly = 92 if v == 1500 else 116; s.line([(x0 + 10, ly - 6), (x0 + 60, ly - 6)], col, 3, dash="10 8"); s.text(x0 + 70, ly, lab, 17, col, "start", "700")   # legend entry above the chart
    bars = [("SPD", "alone", "600 V", 600, "navy"), ("25 cm", "bound", "630 V", 630, "green"), ("25 cm", "unbound", "810 V", 810, "amber"),
            ("2 m", "bound", "1 200 V", 1200, "orange"), ("2 m", "unbound", "2 300 V", 2300, "red")]   # BEAMA results
    for i, (l1, l2, val, v, col) in enumerate(bars):   # one bar each
        bx = x0 + 22 + i * 104; h = hmax * v / vmax   # position and height
        s.add(f'<rect class="bar b{i + 1}" x="{bx}" y="{y0 - h}" width="70" height="{h}" rx="6" fill="{C[col]}"/>')   # bar
        s.text(bx + 35, y0 - h + 26, val.replace(" V", ""), 18, "white", "middle", "700").text(bx + 35, y0 - h + 46, "V", 17, "white", "middle", "700")   # value inside the bar
        s.text(bx + 35, y0 + 26, l1, 17, "ink", "middle", "700").text(bx + 35, y0 + 48, l2, 17, "ink", "middle")   # two-line label
    return s.render(), 6.0   # SVG and still time

def ex_bound_leads():
    """What bound and unbound leads are. Facts: K004 (currents in and out of a shunt SPD flow in opposite directions),
    K005/K006 (close conductors: opposing fields cancel, inductance cancels), I029 (bind with cable ties or spiral wrap),
    I030 (25 cm bound 630 V), I031 (25 cm unbound 810 V)."""
    s = Svg("Bound or unbound (loose) SPD wires: what the words mean", "amber", h=600)   # canvas
    phases(s, 9, [(0.0, 0.33), (0.33, 0.66), (0.66, 1.0)])   # three steps
    s.css.append(".ring{animation:ring 1.2s ease-out infinite}@keyframes ring{0%{opacity:.9;transform:scale(.4)}100%{opacity:0;transform:scale(1.4)}}"
                 ".ring{transform-box:fill-box;transform-origin:center}")   # pulsing magnetic-field rings
    for x0, title, bound in ((20, "UNBOUND (loose): wires apart", False), (490, "BOUND: wires tied together", True)):   # two panels
        col = "green" if bound else "red"   # panel colour
        s.add(f'<rect x="{x0}" y="76" width="450" height="372" rx="12" fill="{C["mint"] if bound else C["rose"]}" stroke="{C[col]}" stroke-width="3"/>')   # panel
        s.text(x0 + 225, 108, title, 21, col, "middle", "700")   # panel title
        s.box(x0 + 20, 148, 110, 44, "A: line", fill="white", stroke="red", size=18)   # line connection
        s.box(x0 + 20, 330, 110, 44, "B: earth bar", fill="mint", stroke="green", size=17)   # earth bar
        s.box(x0 + 330, 220, 100, 80, "SPD", fill="sand", stroke="amber", size=22)   # SPD
        if bound:   # leads side by side
            ya, yb = 252, 268   # the two leads 16 px apart
            s.line([(x0 + 130, 170), (x0 + 160, 170), (x0 + 160, ya), (x0 + 330, ya)], "red", 6)   # l1
            s.pe([(x0 + 130, 352), (x0 + 180, 352), (x0 + 180, yb), (x0 + 330, yb)], width=6)   # l2
            for tx in (x0 + 215, x0 + 260, x0 + 305): s.add(f'<rect x="{tx - 5}" y="{ya - 10}" width="10" height="{yb - ya + 20}" rx="3" fill="{C["ink"]}"/>')   # cable ties
            s.text(x0 + 258, 216, "cable ties", 17, "ink", "middle", "700")   # tie label
            s.add(f'<g class="p2 p3"><circle class="ring" cx="{x0 + 250}" cy="{(ya + yb) / 2}" r="22" fill="none" stroke="{C["blue"]}" stroke-width="2" opacity=".4"/></g>')   # small residual field
            s.text(x0 + 225, 410, "opposite fields cancel: 630 V (25 cm)", 18, "green", "middle", "700")   # result
            path_in, path_out = f"M{x0 + 130},170 L{x0 + 160},170 L{x0 + 160},{ya} L{x0 + 330},{ya}", f"M{x0 + 330},{yb} L{x0 + 180},{yb} L{x0 + 180},352 L{x0 + 130},352"   # current paths
        else:   # leads apart, large loop
            s.line([(x0 + 130, 170), (x0 + 380, 170), (x0 + 380, 220)], "red", 6)   # l1 along the top
            s.pe([(x0 + 380, 300), (x0 + 380, 352), (x0 + 130, 352)], width=6)   # l2 along the bottom
            for cx, cy in ((x0 + 255, 170), (x0 + 255, 352)):   # a field ring around each wire
                s.add(f'<g class="p2 p3"><circle class="ring" cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{C["blue"]}" stroke-width="3"/></g>')   # field
            s.text(x0 + 175, 268, "big loop: fields", 17, "red", "middle", "700").text(x0 + 175, 290, "do not cancel", 17, "red", "middle", "700")   # loop label
            s.text(x0 + 225, 410, "810 V with the same 25 cm leads", 18, "red", "middle", "700")   # result
            path_in, path_out = f"M{x0 + 130},170 L{x0 + 380},170 L{x0 + 380},220", f"M{x0 + 380},300 L{x0 + 380},352 L{x0 + 130},352"   # current paths
        s.dots(path_in, "amber", 3, 1.4, r=8, cls="p1"); s.dots(path_out, "amber", 3, 1.4, r=8, cls="p1")   # current in on l1, out on l2
        s.text(x0 + (170 if not bound else 300), 160 if not bound else 238, "l1 in", 17, "red", "middle", "700")   # l1 label
        s.text(x0 + (170 if not bound else 300), 344 if not bound else 292, "l2 out", 17, "green", "middle", "700")   # l2 label
    s.step(40, 494, 1, "The surge current flows into the SPD on l1 and out on l2: opposite directions.", "amber", "s1")   # step 1
    s.step(40, 536, 2, "Unbound (loose): the wires are apart, so their opposite fields do not cancel.", "red", "s2")   # step 2
    s.step(40, 578, 3, "Bound: tied side by side, the opposite fields cancel and the voltage drops.", "green", "s3")   # step 3
    return s.render(), 7.5   # SVG and still time

def ex_supply_earth():
    """Where the house earth comes from and what joins it. Facts: J041/J042 (supply point: neutral and earth bonded,
    earthing arrangement typically below 10 ohm), J039 (PEN provides the household earth in TN-C-S), B096/D085/H111/J076
    (all electrodes interconnected with the house earth), E077 (fence earth at least 2 m from other earths, security fence),
    J071 (no permanent neutral-earth bond downstream of the main switch)."""
    s = Svg("Where the house earth comes from, and what joins it", "green", h=664)   # canvas
    phases(s, 12, [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)])   # four steps
    s.add(f'<rect x="20" y="380" width="920" height="26" fill="{C["soil"]}"/>')   # ground
    s.add(f'<circle cx="80" cy="190" r="30" fill="none" stroke="{C["ink"]}" stroke-width="4"/><circle cx="80" cy="232" r="30" fill="none" stroke="{C["ink"]}" stroke-width="4"/>')   # transformer
    s.text(80, 124, "Supply", 18, "ink", "middle", "700").text(80, 145, "transformer", 17, "muted", "middle")   # label
    s.pe([(80, 262), (80, 392)]); s.earth(80, 392, 13)   # supply earth at the transformer
    s.add(f'<g class="s1"><rect x="92" y="300" width="182" height="58" rx="8" fill="{C["mint"]}" stroke="{C["green"]}" stroke-width="2"/>'
          f'<text x="183" y="324" font-size="17" text-anchor="middle" font-weight="700" fill="{C["green"]}">N and earth joined</text>'
          f'<text x="183" y="346" font-size="17" text-anchor="middle" fill="{C["ink"]}">typically &lt; 10 Ω</text></g>')   # supply earth label
    s.line([(110, 232), (300, 232)], "blue", 7); s.line([(110, 232), (300, 232)], "green", 3, dash="12 12")   # PEN cable
    s.text(205, 220, "PEN cable", 17, "blue", "middle", "700")   # PEN label
    s.dots("M110,232 L300,232", "amber", 3, 1.5, r=7, cls="p2")   # earth arriving on the PEN
    s.add(f'<rect x="300" y="96" width="420" height="284" rx="12" fill="{C["paper"]}" stroke="{C["navy"]}" stroke-width="3"/>')   # house
    s.text(510, 124, "House", 20, "navy", "middle", "700")   # house label
    s.box(320, 200, 150, 64, ["Supply-entry", "board"], fill="sand", stroke="amber", size=17)   # main board
    s.text(395, 290, "no N-E link after", 17, "red", "middle", "700").text(395, 311, "the main switch", 17, "red", "middle", "700")   # J071 reminder
    s.box(500, 214, 200, 40, "Main earth bar", fill="mint", stroke="green", size=18)   # consumer's earth terminal
    s.pe([(470, 234), (500, 234)])   # board to earth bar
    s.box(560, 140, 140, 40, "Other boards", fill="white", stroke="ink", size=17); s.pe([(630, 180), (630, 214)])   # added earth bars
    s.pe([(600, 254), (600, 392)]); s.earth(600, 392, 13); s.text(612, 372, "house rod", 17, "green", weight="700")   # house electrode
    s.add(f'<polygon points="760,150 820,96 880,150" fill="{C["sky"]}" stroke="{C["blue"]}" stroke-width="2"/>'); s.text(820, 140, "PV", 17, "blue", "middle", "700")   # roof PV
    s.add(f'<rect x="772" y="196" width="8" height="184" fill="{C["line"]}"/>'); s.box(744, 160, 64, 32, "Cam", fill="sky", stroke="blue", size=17)   # camera pole
    s.pe([(820, 150), (820, 392)]); s.earth(820, 392, 13); s.text(832, 300, "PV spike", 17, "green", weight="700")   # PV spike
    s.pe([(776, 380), (776, 392)]); s.earth(776, 392, 11)   # pole rod
    s.add(f'<g class="p3">'); s.pe([(700, 234), (900, 234)], width=7); s.add('</g>')   # bonding conductor (visible in step 3+)
    s.pe([(600, 418), (920, 418)], width=4)   # buried bond joining the rods
    s.pe([(776, 410), (776, 418)], width=4); s.pe([(820, 410), (820, 418)], width=4)   # rods to the buried bond
    s.dots("M600,418 L920,418", "green", 4, 2.0, r=6, cls="p3")   # bonding highlight
    s.add(f'<rect x="20" y="430" width="250" height="44" rx="10" fill="{C["lilac"]}" stroke="{C["purple"]}" stroke-width="2"/>')   # fence panel
    s.text(145, 458, "Fence energizer rods", 17, "purple", "middle", "700")   # fence label
    s.add(f'<g class="p4"><line x1="270" y1="452" x2="590" y2="452" stroke="{C["red"]}" stroke-width="3" stroke-dasharray="8 6"/>'
          f'<text x="430" y="444" font-size="18" fill="{C["red"]}" text-anchor="middle" font-weight="700">keep ≥ 2 m away, not joined</text></g>')   # fence separation
    s.step(40, 516, 1, "The supply earth starts at the transformer: neutral and earth joined, into the soil.", "green", "s1")   # step 1
    s.step(40, 558, 2, "In TN-C-S the PEN cable brings that earth to the house.", "blue", "s2")   # step 2
    s.step(40, 600, 3, "Every rod of the installation joins the house earth: house rod, PV spike, camera pole.", "teal", "s3")   # step 3
    s.step(40, 642, 4, "Exception: the electric-fence earth stays at least 2 m away (security fence).", "purple", "s4")   # step 4
    return s.render(), 7.0   # SVG and still time

def ex_lpz():
    """Lightning protection zones. Facts: A063 (LPZ 0 full lightning current), A064 (LPZ 1 partial currents),
    A065 (LPZ 2 only remnants), A067 (SPD at 0/1 lightning current protection, at 1/2 overvoltage protection)."""
    s = Svg("Lightning protection zones: each boundary takes energy out", "blue")   # canvas
    zones = [(20, 330, "sand", "LPZ 0", "full current possible"), (350, 310, "sky", "LPZ 1", "partial lightning currents"),
             (660, 280, "mint", "LPZ 2", "only remnants")]   # zone bands
    for x, w, fill, name, sub in zones:   # draw each zone
        s.add(f'<rect x="{x}" y="80" width="{w}" height="300" fill="{C[fill]}"/>')   # zone background
        s.text(x + w / 2 + (30 if x == 20 else 0), 118, name, 24, "navy", "middle", "700").text(x + w / 2 + (30 if x == 20 else 0), 144, sub, 17, "ink", "middle")   # zone label (shifted clear of the bolt in LPZ 0)
    for x, lab1, lab2 in ((350, "SPD: lightning", "current protection"), (660, "SPD: overvoltage", "protection")):   # boundaries
        s.add(f'<rect x="{x - 5}" y="80" width="10" height="300" fill="{C["navy"]}"/>')   # wall
        s.spd(x, 352, "SPD", w=70); s.text(x, 410, lab1, 17, "amber", "middle", "700").text(x, 432, lab2, 17, "amber", "middle", "700")   # SPD and label
    s.css.append(".pulse{animation:move 4s linear infinite}@keyframes move{0%{transform:translateX(-60px);opacity:0}8%{opacity:1}92%{opacity:1}100%{transform:translateX(90px);opacity:0}}")   # pulses drift right
    for cx, amp in ((185, 120), (505, 60), (800, 22)):   # one impulse per zone, smaller each time
        s.add(f'<g class="pulse"><path d="M{cx - 70},320 L{cx - 25},320 L{cx - 12},{320 - amp} L{cx + 40},{320 - amp * 0.35} L{cx + 70},320" '
              f'fill="none" stroke="{C["red"]}" stroke-width="6" stroke-linejoin="round"/></g>')   # impulse shape
    s.bolt(28, 150, 70)   # strike in LPZ 0
    s.text(480, 488, "Each boundary combines bonding, shielding and a coordinated SPD.", 18, "ink", "middle")   # summary line
    return s.render(), 2.0   # SVG and still time

EXPLAINERS = {   # name used in content files -> function returning (svg text, still time in seconds)
    "ex_fault_path": ex_fault_path,
    "ex_surge_camera": ex_surge_camera,
    "ex_potential_difference": ex_potential_difference,
    "ex_spd_leads": ex_spd_leads,
    "ex_bound_leads": ex_bound_leads,
    "ex_lpz": ex_lpz,
    "ex_supply_earth": ex_supply_earth,
}
