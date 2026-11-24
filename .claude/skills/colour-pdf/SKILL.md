---
name: colour-pdf
description: Make or change a colour PDF document in this repository (earthing, bonding, surge and lightning protection library). Use when asked for a new sheet, a PDF, a visual document, a diagram, or to change the look, a section or a citation of an existing document. Covers the YAML document format, the citation rule, the colour theme, the building blocks, diagrams, the build and lint, and the visual check.
---

# Colour PDF documents

Every PDF in `docs/pdf/` is generated. Never edit a PDF, and never hand-write ReportLab code for one
document. Change the content file and rebuild.

```
content/docs/NN_name.yaml  ──┐
content/facts.json  ─────────┼──▶ tools/build_pdfs.py ──▶ docs/pdf/NN_slug.pdf
references/catalog.yaml  ────┤                       └──▶ (wiki) tools/build_wiki.py
tools/pdfkit.py + diagrams.py┘
```

## 1. The accuracy rule (non-negotiable)

1. **Every technical statement cites a verified fact.** Write `{{C014}}` (or `{{E065, C002}}`) at the
   end of the sentence. The ID must exist in `content/facts.json`. The build stops on an unknown ID.
2. **A fact exists only if its quote was found on the cited PDF page.** `tools/verify_facts.py` checks
   every quote against the page text and drops the rest. Never add a fact by hand to `facts.json`.
3. **Your own sentences may only restate what the cited facts say.** No added numbers, no
   strengthening ("may" stays "may", "should" stays "should"), no merging two sources into a rule
   neither states. If two sources conflict, show both in a table. Do not pick a winner.
4. **The lint stops the build if author text contains a digit without a citation** (leads,
   paragraphs, callouts, tiles, captions, checklist items, table rows). Headings are exempt.
5. Name the jurisdiction when it matters: "Per Motorola R56 (US practice)", "BEAMA (UK)",
   "SANS 10142-1 draft". Never present a draft standard as the published standard.
6. Sources with `private: true` in `references/catalog.yaml` (for example the SANS 10142-1 public-enquiry
   draft) may only be cited in documents marked `private: true`. Those are built into `private/` and are
   never committed.
7. Find facts with `python3 tools/show_facts.py --topic CCTV,DATA --src 26,39 --grep shield`.

## 2. Document format (`content/docs/NN_name.yaml`)

```yaml
id: "04"                      # two digits; file name prefix and sort order
slug: cctv_cameras_recorders  # PDF file name: docs/pdf/04_cctv_cameras_recorders.pdf
badge: "SHEET 04 · CCTV"      # cover badge and running header
title: "CCTV cameras, recorders and PoE switches"
subtitle: "One sentence on scope"
applies_to: "Plain list of equipment"
accent: teal                  # see the palette below
version: "1.0"
contents: true                # contents page (use for 4+ chapters)
private: false                # true = site-specific: file goes in content/private/, PDF in private/ (both git-ignored)
sections:
  - title: "1  Chapter title"           # chapter banner in the accent colour
    lead: "Intro paragraph.{{E059}}"    # optional, larger text
    blocks:
      - h2: "Sub-heading"
      - p: "Paragraph text.{{B002}}"
      - meta: "Text about the library itself (how to read it). Lint-exempt; never a technical statement; may not cite."
      - index: true                       # generated table of all public sheets
      - facts: [C008, C009, {id: E060, text: "Own shorter wording.{{E060}}"}]   # bullet list, chip added automatically
      - callout: {kind: do|dont|warn|note|site, title: "...", text: "...{{ID}}"}
      - numbers: [{value: "0.5 m", label: "what it is{{ID}}"}]                # 2-4 key-number tiles
      - table: {head: [...], widths: [0.3, 0.7], rows: [[...]], caption: "..."}
      - diagram: {name: camera_both_ends, caption: "(1) ...{{ID}}"}
      - checklist: ["Item to tick.{{ID}}"]
      - pagebreak: true
```

Plain bullets from `facts:` print the verified claim text unchanged. Prefer that. Use custom wording
only when the claim is too long, and then still cite the same ID inside the text.

## 3. Colour theme (one theme, `tools/pdfkit.py`)

| Accent name | Use for |
|---|---|
| `green` | earthing and bonding fundamentals, testing |
| `amber` | lightning, surge protective devices, distribution boards |
| `teal` | CCTV, data, network, racks |
| `blue` | antennas, masts, between buildings |
| `purple` | gate motors, intercoms, alarms, fences, PLCs |
| `orange` | solar PV, inverters, batteries |
| `navy` | overview, index, site-specific plans |

Fixed meanings, the same in every document:

- **Green with yellow stripes** = protective earth / bonding conductor (cover band, header line, diagrams).
- **Callouts:** green `do`, red `dont`, amber `warn`, blue `note`, purple `site` (check on site).
- **Wires in diagrams:** red = power, blue = data/signal, orange = PV d.c., green/yellow = earth, amber box = SPD.
- **Citation chips** are small blue `[R18 p.12]` links to the source table at the end of the document.

Fonts are vendored in `tools/fonts/` (Liberation Sans for text, DejaVu Sans for symbols). Use the
real characters `Ω µ ² ≤ ≥ ±` in text. Never use Unicode sub/superscript digits; use `<sub>` / `<super>`.

## 4. Diagrams (`tools/diagrams.py`)

- One function per diagram, registered in `DIAGRAMS`. Build it with the `Dg` helper: `box`, `wire`,
  `pe` (earth conductor), `spd`, `earth`, `tag` (numbered marker), `bolt`, `soil`, `legend`.
- Diagrams are **concept sketches of a cited rule**, not product wiring diagrams. Say so in the caption.
- Put numbered `tag` markers on the drawing and explain each number in the caption, with citations.
- Diagram text: Helvetica, plain ASCII (the same drawing is exported to SVG for the wiki).
- Preview: `python3 tools/preview_diagrams.py /tmp/x.pdf name && pdftoppm -r 110 -png /tmp/x.pdf /tmp/x`
  then look at the PNG. Check that no text overlaps a line or box and nothing runs off the frame.

## 4a. Readability rules for diagrams (mandatory)

The owner could not read the first diagrams in the wiki. These rules exist so that never happens again.

1. **Minimum text size 8.5 pt at full size.** `Dg.text` enforces it: every size written in a diagram
   function is multiplied by `TEXT_SCALE` (1.25) and never drops below `MIN_TEXT` (8.5). Do not bypass
   `Dg.text` with raw `String(...)`. Do not lower these constants.
2. **Labels must fit.** A label never overflows its box, crosses a wire or sits on another label. Widen the
   box (`spd(..., w=...)`, `box(...)`) or move the label; do not shrink the text.
3. **Drawing size.** Draw at 480 pt wide (it then fills the PDF text width). If a diagram needs more than
   about 12 labels, split it into two diagrams instead of cramming it.
4. **Numbered markers** (`tag`) are 15 pt discs with 9 pt numbers; explain every marker in the caption.
5. **Wiki:** diagrams are SVG with the font chain `Helvetica, Arial, sans-serif`, shown at 100 % of the
   page width and linked to the full-size file (click to enlarge). `export_svg` and `build_wiki.py` do this;
   keep it.
6. **Check at real size before committing:** render with `tools/preview_diagrams.py` at 80 dpi and look at
   every diagram you changed. Text that is hard to read at 80 dpi is too small.

## 4b. Animated explainers (`tools/explainers.py`)

Animated SVGs for the wiki (CSS keyframes + SMIL `animateMotion`), with a still frame for the PDFs.

1. **Every number or rule drawn in an explainer comes from a verified fact.** Name the fact IDs in the
   function's docstring and cite them in the `explainer:` caption of every document that uses it.
   Step texts inside the picture must not say more than those facts (no "small residual" unless a fact says so).
2. **Canvas 960 px wide, text at least 17 px** (`Svg.text` enforces it), font chain `Segoe UI, Helvetica,
   Arial, sans-serif`. Moving charges must not stop on top of labels (end their paths at box edges).
3. **Steps:** use `phases()` windows and `step()` rows so the viewer sees what each phase means. The picture
   must make sense at its **still time** (the second value returned), which is the PDF frame.
4. Respect `prefers-reduced-motion` (already in the shared CSS).
5. After a change run `python3 tools/render_explainers.py` (needs the local Chromium) and **commit the PNGs**
   in `docs/img/explainers/`; CI has no browser. Look at every PNG before committing.
6. Use in a document: `- explainer: {name: ex_fault_path, caption: "...{{J039}}"}`. The wiki shows the animated
   SVG full width (click to enlarge); the PDF shows the still with "Animated in the wiki." in the caption.

## 4c. Wiki front page and callouts

- `tools/wiki_graphics.py` draws the animated banner and one colour card per document (icon per sheet id in
  `ICON`). Documents whose badge starts with `VISUAL` are listed first with an "animated" ribbon.
- Callouts become GitHub alert boxes: do = TIP, dont = CAUTION, warn = WARNING, note = NOTE, site = IMPORTANT.

## 5. Build and check

```bash
python3 tools/verify_facts.py <facts dir> <text dir>   # only when new facts were extracted
python3 tools/build_pdfs.py 04                          # one document, or no argument for all
pdftoppm -r 55 -png docs/pdf/04_*.pdf /tmp/p04          # render pages
```

Look at every rendered page before saying the document is done: cover, a body page with a
diagram, a table page and the source list. Check for overlapping text, empty pages, a callout split
across pages, and a header that shows the wrong chapter.

## 6. Adding a source

1. Download the PDF into `references/pdf/NN_Publisher_Title.pdf` (NN = next free number). Check that
   it starts with `%PDF-`. A web page can be printed to PDF with Playwright (see `tools/README.md`).
2. Add its entry to `references/catalog.yaml` (title, publisher, edition and jurisdiction exactly as
   printed, URL, `quotes: public|local`, `private: true` if its own terms restrict use).
3. Extract page-marked text, have the facts written to `facts_X.json` with verbatim quotes, run
   `tools/verify_facts.py`. Existing IDs never change; new facts get the next free number.
