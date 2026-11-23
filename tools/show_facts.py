#!/usr/bin/env python3
"""Print verified facts compactly for authors: python3 tools/show_facts.py [--topic CCTV,DATA] [--src 26,39] [--grep word] [--private]"""
import sys, re, pathlib   # standard library
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))   # import sibling module
import content as c   # fact and catalogue loader
args = sys.argv[1:]   # command-line arguments
opt = lambda name: (args[args.index(name) + 1] if name in args else "")   # read the value after a flag
topics = set(filter(None, opt("--topic").split(",")))   # topic filter
srcs = set(filter(None, opt("--src").split(",")))   # source-number filter
pat = re.compile(opt("--grep"), re.I) if opt("--grep") else None   # text filter
cat = c.load_catalog()   # catalogue (for citation numbers)
for fid, f in sorted(c.load_facts(include_private="--private" in args).items()):   # every fact in ID order
    ref = f["source"].split("_")[0]   # citation number as text
    if topics and f["topic"] not in topics: continue   # topic filter
    if srcs and ref not in srcs: continue   # source filter
    if pat and not pat.search(f["claim"]): continue   # text filter
    print(f'{fid} {f["topic"]:5s} R{ref} p{f["page"]} | {f["claim"]}')   # one compact line per fact
