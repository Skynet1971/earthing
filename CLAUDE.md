# Earthing, bonding, surge & lightning protection library

Colour PDF sheets and a wiki on earthing, bonding, surge protection and lightning protection for a
house and its equipment (distribution boards, CCTV, network, PoE, antennas, gate motors, intercoms,
alarms, electric fences, PLCs, solar PV). Every statement is traceable to a page of a published source.

## Rules

1. **Accuracy first.** Every technical statement in a document cites a verified fact `{{ID}}`
   (`content/facts.json`). A fact exists only if its verbatim quote was found on the cited page of the
   source PDF (`tools/verify_facts.py`). Nothing from memory. No guessed numbers. If information is
   missing, write that it is missing.
2. **Do not strengthen or merge sources.** "should" stays "should". Conflicting sources go in a
   "where the sources disagree" table, without picking a winner. Name the jurisdiction of the source.
3. **Never present the SANS 10142-1 Ed 3.3 public-enquiry draft as the published standard.** It is a
   draft circulated for comment only; its own terms restrict it to local use, so it is `private: true`
   and its facts and quotes stay in `references/local/` (git-ignored).
4. **Copyright.** Reference PDFs (`references/pdf/`) are not committed; `tools/download_references.py`
   re-fetches them from the URLs in `references/catalog.yaml`. Sources marked `quotes: local` keep their
   quotes out of the repository.
5. **This repository is public.** Site-specific documents (the owner's own equipment, records, layouts) are `private: true`,
   live in `content/private/` and are built into `private/`; both folders are git-ignored. Never commit or publish them. No addresses, IPs, passwords or names in public files.
6. **Generated files are never edited by hand:** `docs/pdf/*.pdf`, `wiki/*.md`, `wiki/img/*.svg`.
   Change `content/docs/*.yaml`, `tools/*.py` or the catalogue and rebuild.
7. Code comments: one comment per line explaining it (owner's preference).

## Making or changing a document

Load the skill `.claude/skills/colour-pdf/SKILL.md`. Short version:

```bash
python3 tools/show_facts.py --topic SPD --grep "lead length"   # find facts
python3 tools/build_pdfs.py 04                                  # build one sheet (lint + citations checked)
python3 tools/build_wiki.py                                     # regenerate the wiki pages
```

## Layout

| Path | What |
|---|---|
| `content/docs/*.yaml` | one file per public document |
| `content/private/*.yaml` | site-specific documents (git-ignored) |
| `content/facts.json` | verified facts (claim, page, section, source, quote) |
| `references/catalog.yaml` | the source documents and their citation numbers (R01...) |
| `references/pdf/` | downloaded PDFs (git-ignored) |
| `references/local/` | restricted quotes and facts (git-ignored) |
| `tools/` | verifier, PDF kit, diagrams, builders |
| `docs/pdf/` | generated PDFs |
| `wiki/` | generated wiki pages (published to the GitHub wiki by `.github/workflows/wiki.yml`) |
| `private/` | generated site-specific PDFs (git-ignored) |
