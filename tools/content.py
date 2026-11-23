"""Shared content loader: reference catalogue, verified facts, document definitions and citation handling.

Used by tools/build_pdfs.py and tools/build_wiki.py so that the PDFs and the wiki always say the same thing.
"""
import json, pathlib, re   # standard library
import yaml   # PyYAML: content files are YAML

ROOT = pathlib.Path(__file__).resolve().parent.parent   # repository root
CATALOG = ROOT / "references" / "catalog.yaml"   # list of source documents
FACTS = ROOT / "content" / "facts.json"   # verified public facts
PRIVATE_FACTS = ROOT / "references" / "local" / "facts_private.json"   # facts from restricted sources (not committed)
DOCS = ROOT / "content" / "docs"   # one YAML file per public document
PRIVATE_DOCS = ROOT / "content" / "private"   # site-specific documents (git-ignored: the repository is public)
TOKEN = re.compile(r"\{\{([A-Z]\d{3}(?:\s*,\s*[A-Z]\d{3})*)\}\}")   # inline citation token, e.g. {{B017}} or {{B017, C004}}

def load_catalog():
    """Return {source_key: entry}; each entry gains 'ref' (citation number taken from the file-name prefix)."""
    cat = yaml.safe_load(CATALOG.read_text())   # parse the catalogue
    out = {}   # result map
    for s in cat["sources"]:   # every listed source
        s["ref"] = int(s["key"].split("_")[0])   # numeric prefix = citation number
        out[s["key"]] = s   # index by key
    return out   # catalogue map

def load_facts(include_private=False):
    """Return {fact_id: fact}. Private facts are added only on request and only if the local file exists."""
    facts = {f["id"]: f for f in json.loads(FACTS.read_text())}   # public facts
    if include_private and PRIVATE_FACTS.exists():   # restricted-source facts for private documents
        facts.update({f["id"]: f for f in json.loads(PRIVATE_FACTS.read_text())})   # merge them in
    return facts   # fact map

def load_docs():
    """Return the document definitions sorted by file name."""
    files = sorted(DOCS.glob("*.yaml")) + sorted(PRIVATE_DOCS.glob("*.yaml"))   # public documents, then private ones (git-ignored folder)
    docs = [yaml.safe_load(p.read_text()) | {"_file": p.name, "_private_dir": p.parent == PRIVATE_DOCS} for p in files]   # parse each YAML file
    for d in docs:   # a private document must live in content/private and a public one must not
        if bool(d.get("private")) != d["_private_dir"]: raise SystemExit(f'{d["_file"]}: private: true documents belong in content/private/, public ones in content/docs/')   # stop on a misplaced file
    return docs   # all documents

class Cites:
    """Resolves fact IDs to citation labels and remembers which sources and pages a document used."""
    def __init__(self, catalog, facts):
        self.catalog, self.facts = catalog, facts   # lookup tables
        self.used = {}   # {source_key: set(pages)} for the document being built
        self.missing = set()   # fact IDs referenced by content but not present in the fact store

    def label(self, fid):
        """Return (ref_number, page, section) for one fact and record the use; None when the fact is unknown."""
        f = self.facts.get(fid)   # look the fact up
        if f is None or f["source"] not in self.catalog:   # unknown fact or unknown source
            self.missing.add(fid); return None   # remember the problem
        self.used.setdefault(f["source"], set()).add(f["page"])   # record source and page
        return self.catalog[f["source"]]["ref"], f["page"], f.get("section", "")   # citation parts

    def ids(self, token_body):
        """Split the inside of a {{...}} token into fact IDs."""
        return [t.strip() for t in token_body.split(",")]   # comma-separated IDs

    def expand(self, text, render):
        """Replace every {{ID}} token in text using render(ref, page, section) -> str."""
        def sub(m):   # called for each token
            parts = [self.label(i) for i in self.ids(m.group(1))]   # resolve each ID
            return "".join(render(*p) for p in parts if p)   # render the known ones
        return TOKEN.sub(sub, text or "")   # substitute all tokens

    def sources_used(self):
        """Return [(entry, sorted_pages)] ordered by citation number."""
        rows = [(self.catalog[k], sorted(v)) for k, v in self.used.items()]   # entries with their cited pages
        return sorted(rows, key=lambda r: r[0]["ref"])   # numeric order

def page_ranges(pages):
    """Format a sorted page list compactly: [3,4,5,9] -> '3-5, 9'."""
    out, start, prev = [], None, None   # collected ranges and the open range
    for p in pages:   # walk the sorted pages
        if start is None: start = prev = p   # open the first range
        elif p == prev + 1: prev = p   # extend the open range
        else: out.append((start, prev)); start = prev = p   # close it and open a new one
    if start is not None: out.append((start, prev))   # close the last range
    return ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in out)   # text form

def fact_text(facts, item):
    """A 'facts' list item is either an ID or {id: ID, text: custom wording}; return (id, wording)."""
    if isinstance(item, dict):   # custom wording supplied by the document author
        return item["id"], item.get("text") or facts.get(item["id"], {}).get("claim", "")   # prefer the custom text
    return item, facts.get(item, {}).get("claim", "")   # default: the verified claim text
