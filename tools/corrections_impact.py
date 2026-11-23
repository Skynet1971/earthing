#!/usr/bin/env python3
"""List every place where author-written text cites a fact that was corrected or dropped in review.

Plain fact bullets update themselves (they print the verified claim). Author text (leads, paragraphs,
callouts, tables, captions, checklists, custom bullet wording) must be re-read by a person.
Usage: python3 tools/corrections_impact.py
"""
import json, sys, pathlib   # standard library
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))   # import sibling module
import content as c   # loaders and citation token pattern
corr = json.loads((c.ROOT / "content" / "fact_corrections.json").read_text())   # reviewed corrections
def walk(node, where):   # yield (location, text) for every author-written string
    if isinstance(node, dict):   # mapping
        if "id" in node and "text" in node and len(node) <= 2: yield where, node["text"]; return   # custom fact wording
        for k, v in node.items():
            if k in ("facts",): yield from walk([x for x in v if isinstance(x, dict)], where + "/facts"); continue   # only custom wording in fact lists
            yield from walk(v, f"{where}/{k}")   # descend
    elif isinstance(node, list):   # sequence
        for i, v in enumerate(node): yield from walk(v, f"{where}[{i}]")   # descend with index
    elif isinstance(node, str): yield where, node   # a text value
for doc in c.load_docs():   # every document, public and private
    for where, text in walk(doc.get("sections", []), doc["_file"]):   # every author string
        ids = {i for m in c.TOKEN.finditer(text) for i in c.Cites(None, None).ids(m.group(1))}   # fact IDs it cites
        hit = sorted(ids & set(corr))   # corrected ones
        if hit: print(f"{where}\n   cites {hit}: {text[:300]}\n")   # report it
