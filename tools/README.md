# Tools

| Script | What it does |
|---|---|
| `download_references.py` | Downloads every source in `references/catalog.yaml` into `references/pdf/` (web pages are printed to PDF). |
| `extract_text.py` | Writes page-marked text (`=== PAGE n ===`) for each PDF: `python3 -I tools/extract_text.py references/pdf references/local/text` |
| `print_page.js` | Prints one web page to an A4 PDF with Playwright: `node tools/print_page.js URL out.pdf` |
| `verify_facts.py` | Checks every extracted fact's verbatim quote against its page, keeps fact IDs stable, applies `content/fact_corrections.json`, and writes `content/facts.json` (public) and `references/local/` (restricted). `python3 tools/verify_facts.py references/local/readers references/local/text` |
| `show_facts.py` | Lists verified facts for authors (`--topic`, `--src`, `--grep`, `--private`). |
| `build_pdfs.py` | Builds the PDFs from `content/docs/*.yaml` (public) and `content/private/*.yaml` (private, local only); runs the citation lint. |
| `build_wiki.py` | Writes the wiki pages and SVG diagrams into `wiki/`. |
| `preview_diagrams.py` | Renders diagrams one per page for visual checking. |
| `pdfkit.py`, `diagrams.py`, `content.py` | Theme and building blocks, vector diagrams, shared loaders. |

## Adding facts from a new source

1. Download the PDF to `references/pdf/NN_Publisher_Title.pdf` and add its catalogue entry.
2. `python3 -I tools/extract_text.py references/pdf references/local/text`
3. Have the facts written to `references/local/readers/facts_X.json` as a list of
   `{"topic", "claim", "quote", "file", "page", "section"}` (quote verbatim from that page).
4. `python3 tools/verify_facts.py references/local/readers references/local/text`. Existing IDs never change.

## Correcting a fact

Add `"ID": {"claim": "faithful wording", "reason": "why"}` (or `{"drop": true, "reason": "..."}`) to
`content/fact_corrections.json`, rerun `verify_facts.py`, then rebuild the PDFs and the wiki.
