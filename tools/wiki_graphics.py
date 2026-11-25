"""Colour graphics for the wiki front page: an animated banner and one picture card per document."""
import html, textwrap   # escaping and line wrapping

FONT = "Segoe UI, Helvetica, Arial, sans-serif"   # sans-serif chain (Windows has no Helvetica)
ACC = {"green": "#2F9E44", "amber": "#D97706", "teal": "#0E7490", "blue": "#2563EB", "purple": "#7C3AED",
       "orange": "#EA580C", "navy": "#0F2A47", "red": "#DC2626", "pink": "#DB2777"}   # accent colours (same as the PDFs)
ICON = {"00": "book", "01": "earth", "02": "bolt", "03": "board", "04": "camera", "05": "network", "06": "antenna", "07": "gate",
        "08": "shield", "09": "chip", "10": "sun", "11": "rack", "12": "meter", "13": "pin", "14": "earth", "15": "bolt", "16": "camera"}   # icon per document

def icon(kind, x, y):
    """White line icon (about 56 px) with its top-left corner at x, y."""
    a = f'stroke="white" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="translate({x},{y})"'   # common style
    shapes = {
        "earth": '<path d="M28 4v22M8 26h40M16 36h24M24 46h8"/>',   # earth symbol
        "bolt": '<path d="M32 2 12 32h14l-6 24 24-34H30l6-20z" fill="white"/>',   # lightning bolt
        "board": '<rect x="4" y="6" width="48" height="44" rx="4"/><path d="M14 18v20M26 18v20M38 18v20"/>',   # distribution board
        "camera": '<rect x="4" y="14" width="38" height="24" rx="4"/><path d="M42 22l12-6v20l-12-6M16 38v12h12"/>',   # camera
        "network": '<circle cx="28" cy="10" r="6"/><circle cx="10" cy="44" r="6"/><circle cx="46" cy="44" r="6"/><path d="M28 16v12M28 28 14 40M28 28l14 12"/>',   # network nodes
        "antenna": '<path d="M28 8v46M12 14h32M16 24h24M20 34h16"/>',   # antenna
        "gate": '<path d="M4 50h48M8 14v36M18 14v36M28 14v36M38 14v36M48 14v36M8 14h40"/>',   # gate
        "shield": '<path d="M28 4 6 12v14c0 14 10 24 22 28 12-4 22-14 22-28V12z"/><path d="M18 28l7 7 13-14"/>',   # alarm shield
        "chip": '<rect x="12" y="12" width="32" height="32" rx="4"/><path d="M20 4v8M36 4v8M20 44v8M36 44v8M4 20h8M4 36h8M44 20h8M44 36h8"/>',   # PLC chip
        "sun": '<circle cx="28" cy="28" r="11"/><path d="M28 2v8M28 46v8M2 28h8M46 28h8M10 10l6 6M40 40l6 6M46 10l-6 6M16 40l-6 6"/>',   # sun
        "rack": '<rect x="8" y="4" width="40" height="48" rx="3"/><path d="M14 16h28M14 28h28M14 40h28"/>',   # rack
        "meter": '<path d="M6 40a22 22 0 0 1 44 0"/><path d="M28 40l12-14"/><circle cx="28" cy="40" r="3" fill="white"/>',   # meter dial
        "pin": '<path d="M28 54S10 34 10 22a18 18 0 0 1 36 0c0 12-18 32-18 32z"/><circle cx="28" cy="22" r="6"/>',   # map pin
        "book": '<path d="M28 12C20 6 10 6 4 8v40c6-2 16-2 24 4 8-6 18-6 24-4V8c-6-2-16-2-24 4zM28 12v40"/>',   # book
    }
    return f'<g {a}>{shapes[kind]}</g>'   # icon group

def short_badge(doc, animated):
    """Badge text that fits next to the icon: 'GUIDE 1' for visual guides, '08 · ALARMS & FENCES' for sheets."""
    b = doc.get("badge", "")   # full badge
    if animated: return b.split(" · ")[0].replace("VISUAL ", "")   # e.g. GUIDE 1 (the ribbon says animated)
    return b.replace("SHEET ", "")[:24]   # e.g. 08 · ALARMS & FENCES

def card(doc):
    """Picture card (360 x 200) for one document."""
    col = ACC.get(doc.get("accent", "navy"), ACC["navy"])   # accent colour
    animated = doc.get("badge", "").startswith("VISUAL")   # visual guides get a ribbon
    lines = textwrap.wrap(doc["title"].replace("Visual guide 1: ", "").replace("Visual guide 2: ", "").replace("Visual guide 3: ", ""), 27)[:3]   # wrapped title
    t = "".join(f'<text x="22" y="{118 + i * 26}" font-size="21" font-weight="700" fill="white">{html.escape(l)}</text>' for i, l in enumerate(lines))   # title lines
    rib = ('<g><rect x="232" y="16" width="112" height="30" rx="15" fill="white"/>'
           f'<text x="288" y="37" font-size="17" font-weight="700" fill="{col}" text-anchor="middle">▶ animated</text></g>') if animated else ""   # ribbon
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 200" width="360" height="200" font-family="{FONT}">'
            f'<style>text{{font-family:{FONT}}}</style>'
            f'<rect width="360" height="200" rx="16" fill="{col}"/>'
            f'<rect y="184" width="360" height="16" fill="url(#pe)"/><rect width="360" height="200" rx="16" fill="none" stroke="{col}" stroke-width="2"/>'
            f'<defs><pattern id="pe" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="7" height="14" fill="#2F9E44"/><rect x="7" width="7" height="14" fill="#FACC15"/></pattern></defs>'
            + icon(ICON.get(doc["id"], "book"), 20, 16) +
            f'<text x="88" y="38" font-size="17" font-weight="700" fill="white" opacity="0.92">{html.escape(short_badge(doc, animated))}</text>'
            + rib + t + "</svg>")   # card document

def banner(n_docs, n_sources, n_facts):
    """Animated front-page banner (960 x 300)."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 300" width="960" height="300" font-family="{FONT}">
<style>text{{font-family:{FONT}}}.fl{{animation:fl 4s infinite}}@keyframes fl{{0%,5%{{opacity:1}}2.5%{{opacity:.3}}10%,100%{{opacity:.25}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>
<defs><pattern id="pe" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="9" height="18" fill="#2F9E44"/><rect x="9" width="9" height="18" fill="#FACC15"/></pattern>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0F2A47"/><stop offset="1" stop-color="#16406B"/></linearGradient></defs>
<rect width="960" height="300" rx="18" fill="url(#g)"/><rect y="276" width="960" height="24" fill="url(#pe)"/>
<polygon class="fl" points="800,20 752,140 790,140 766,250 860,104 818,104 846,20" fill="#FACC15" stroke="#D97706" stroke-width="3"/>
<g stroke="#2F9E44" stroke-width="7" stroke-linecap="round"><line x1="900" y1="150" x2="900" y2="214"/><line x1="868" y1="214" x2="932" y2="214"/><line x1="880" y1="232" x2="920" y2="232"/><line x1="892" y1="250" x2="908" y2="250"/></g>
<circle r="7" fill="#FACC15"><animateMotion dur="1.6s" repeatCount="indefinite" path="M806,240 L900,150 L900,212"/></circle>
<text x="40" y="92" font-size="44" font-weight="800" fill="white">Earthing, bonding, surge</text>
<text x="40" y="144" font-size="44" font-weight="800" fill="white">and lightning protection</text>
<text x="40" y="186" font-size="21" fill="#DCE6F2">Boards, CCTV, PoE, network, gates, alarms, PLCs and solar</text>
<g font-size="18" font-weight="700"><rect x="40" y="208" width="190" height="40" rx="20" fill="#2F9E44"/><text x="135" y="234" fill="white" text-anchor="middle">{n_docs} documents</text>
<rect x="242" y="208" width="190" height="40" rx="20" fill="#0E7490"/><text x="337" y="234" fill="white" text-anchor="middle">{n_sources} sources</text>
<rect x="444" y="208" width="230" height="40" rx="20" fill="#D97706"/><text x="559" y="234" fill="white" text-anchor="middle">{n_facts} cited facts</text></g>
</svg>'''   # banner document

def button(label, accent="navy"):
    """Rounded colour button with a download arrow (height 64, width follows the label)."""
    col = ACC.get(accent, accent)   # button colour
    w = 90 + int(len(label) * 12.5)   # approximate width for 22 px bold text
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 64" width="{w}" height="64" font-family="{FONT}">'
            f'<style>text{{font-family:{FONT}}}</style><rect x="2" y="2" width="{w - 4}" height="60" rx="30" fill="{col}"/>'
            f'<g stroke="white" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M38 18v22M28 31l10 10 10-10M26 47h24"/></g>'
            f'<text x="62" y="40" font-size="22" font-weight="700" fill="white">{html.escape(label)}</text></svg>')   # button document
