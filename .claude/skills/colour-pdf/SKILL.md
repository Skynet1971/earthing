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
