#!/usr/bin/env python3
"""Verify every extracted fact against the source PDF text, then write content/facts.json.

A fact is kept only when its verbatim quote is found in the text of the cited PDF.
Usage: python3 tools/verify_facts.py <dir with facts_*.json> [<dir with page-marked .txt files>]
"""
import json, re, sys, pathlib, unicodedata   # standard library only

ROOT = pathlib.Path(__file__).resolve().parent.parent   # repository root
OUT = ROOT / "content" / "facts.json"   # verified facts consumed by the PDF and wiki builders
REJ = ROOT / "references" / "local" / "facts_rejected.json"   # facts whose quote could not be found (local audit file)
LOCAL = ROOT / "references" / "local"   # files that must not be committed (restricted sources)
TOPICS = {"FUND", "LIGHT", "SPD", "DATA", "CCTV", "ANT", "RACK", "SITE", "TEST", "SAFE"}   # allowed topic codes

def norm(s):
    """Normalise text so that layout differences do not break the comparison."""
    s = unicodedata.normalize("NFKC", s)   # fold ligatures (fi, fl) and compatibility characters
    s = s.replace("­", "")   # drop soft hyphens inserted by PDF producers
    s = s.translate(str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", "−": "-"}))   # unify quotes and dashes
    s = re.sub(r"\s+", " ", s)   # collapse every whitespace run to one space
    return s.strip().lower()   # compare case-insensitively

def squeeze(s):
    """Stricter fallback form: remove all whitespace (handles words split across lines/columns)."""
    return re.sub(r"\s+", "", norm(s))   # whitespace-free normalised string

def load_pages(txt):
    """Split one page-marked text file into {page_number: text}."""
    parts = re.split(r"\n=== PAGE (\d+) ===\n", "\n" + txt.read_text(errors="replace"))   # markers written by the extractor
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts) - 1, 2)}   # odd items are page numbers, even items are text

def main():
    facts_dir = pathlib.Path(sys.argv[1])   # directory holding facts_*.json from the readers
    text_dir = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else facts_dir.parent / "text"   # page-marked text directory
    cache, kept, rejected = {}, [], []   # per-file page cache, accepted facts, rejected facts
    import hashlib   # quote fingerprints keep IDs stable between runs
    pinned = {}   # (source stem, quote fingerprint) -> ID already published
    for old in (OUT, LOCAL / "facts_private.json"):   # IDs issued by earlier runs
        if old.exists():
            for f in json.loads(old.read_text()): pinned[(f["source"], f["quote_sha256"])] = f["id"]   # remember each one
    used = set(pinned.values())   # IDs that must never be reused for a different fact
    for fj in sorted(facts_dir.glob("facts_*.json")):   # one file per reader
        letter = fj.stem.split("_")[1]   # reader letter becomes the fact-ID prefix
        nxt = 1 + max([int(i[1:]) for i in used if i[0] == letter] or [0])   # next free number for this reader
        for n, f in enumerate(json.loads(fj.read_text()), 1):   # every fact in the file
            key = (pathlib.Path(str(f.get("file", ""))).stem, hashlib.sha256(norm(str(f.get("quote", ""))).encode()).hexdigest()[:16])   # identity of the fact
            if key in pinned: f["id"] = pinned[key]   # same fact as before: keep its ID
            else: f["id"] = f"{letter}{nxt:03d}"; nxt += 1; used.add(f["id"])   # new fact: next unused ID
            name = pathlib.Path(str(f.get("file", ""))).name   # ignore any directory part
            if not name.endswith(".txt"):   # readers may have given the PDF name
                name = pathlib.Path(name).stem + ".txt"   # map to the text file name
            src = text_dir / name   # text file for the cited source
            if not src.exists() or f.get("topic") not in TOPICS or not f.get("quote") or not f.get("claim"):   # structural checks
                f["reject"] = "bad structure or unknown source/topic"; rejected.append(f); continue   # reject and move on
            pages = cache.setdefault(name, load_pages(src))   # parse the source once
            q, qs = norm(f["quote"]), squeeze(f["quote"])   # both comparison forms of the quote
            if len(qs) < 25:   # too short to be meaningful evidence
                f["reject"] = "quote too short"; rejected.append(f); continue   # reject and move on
            hits = [p for p, t in pages.items() if q in norm(t)] or [p for p, t in pages.items() if qs in squeeze(t)]   # exact match first, then whitespace-free match
            if not hits:   # the quote is not in the document at all
                f["reject"] = "quote not found in source"; rejected.append(f); continue   # reject and move on
            try: stated = int(f.get("page"))   # page the reader reported
            except (TypeError, ValueError): stated = -1   # unusable page number
            f["page"] = stated if stated in hits else min(hits, key=lambda p: abs(p - stated))   # keep the stated page if valid, else the nearest real hit
            f["source"] = pathlib.Path(name).stem   # catalogue key = file stem
            f.pop("file", None)   # the key above replaces the file name
            kept.append(f)   # accepted
    import yaml   # YAML for the catalogue flags
    cat = {s["key"]: s for s in yaml.safe_load((ROOT / "references" / "catalog.yaml").read_text())["sources"]}   # catalogue entries by key
    unknown = sorted({f["source"] for f in kept} - set(cat))   # sources that are not catalogued
    if unknown: raise SystemExit(f"sources missing from references/catalog.yaml: {unknown}")   # the catalogue must be complete
    public, private, local_quotes = [], [], {}   # committed facts, restricted-source facts, quotes that may not be reproduced
    for f in kept:   # apply the per-source rules
        s = cat[f["source"]]   # catalogue entry of the fact's source
        f["quote_sha256"] = hashlib.sha256(norm(f["quote"]).encode()).hexdigest()[:16]   # fingerprint of the evidence quote (same as the ID key)
        if s.get("private"):   # the source's own terms restrict its use
            private.append(f); continue   # keep the whole fact out of the repository
        if s.get("quotes") == "local":   # the source forbids reproduction
            local_quotes[f["id"]] = f.pop("quote")   # keep the quote only on this machine
        public.append(f)   # committed fact
    LOCAL.mkdir(parents=True, exist_ok=True)   # local-only folder (ignored by git)
    (LOCAL / "facts_private.json").write_text(json.dumps(private, indent=1, ensure_ascii=False) + "\n")   # restricted-source facts
    (LOCAL / "quotes_local.json").write_text(json.dumps(local_quotes, indent=1, ensure_ascii=False) + "\n")   # non-reproducible quotes
    OUT.write_text(json.dumps(public, indent=1, ensure_ascii=False) + "\n")   # write verified public facts
    REJ.write_text(json.dumps(rejected, indent=1, ensure_ascii=False) + "\n")   # write the audit list
    print(f"public {len(public)}  private {len(private)}  quotes kept local {len(local_quotes)}")   # split summary
    by = {}   # per-source counter
    for f in kept: by[f["source"]] = by.get(f["source"], 0) + 1   # count accepted facts per source
    for k in sorted(by): print(f"{by[k]:4d}  {k}")   # report per source
    print(f"kept {len(kept)}  rejected {len(rejected)}")   # overall result
    for f in rejected: print("  REJECT", f["id"], f["reject"], "|", str(f.get("quote"))[:70])   # show each rejection

if __name__ == "__main__":
    main()   # run when called as a script
