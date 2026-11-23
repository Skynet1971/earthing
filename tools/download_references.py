#!/usr/bin/env python3
"""Download the reference documents listed in references/catalog.yaml into references/pdf/.

Usage: python3 tools/download_references.py [key-prefix ...]
Entries with kind 'webprint' are web pages; they are printed to PDF with Playwright/Chromium.
A download is kept only if the file starts with %PDF-. Existing files are not downloaded again.
"""
import sys, subprocess, pathlib   # standard library
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))   # import sibling module
import content as c   # catalogue loader

OUT = c.ROOT / "references" / "pdf"   # target folder (git-ignored)
UA = "Mozilla/5.0 (X11; Linux x86_64)"   # generic client name; no personal details

def fetch_pdf(url, dest):
    """Download a PDF with curl; return True when the result is a PDF."""
    subprocess.run(["curl", "-sS", "-L", "-m", "300", "-A", UA, "-o", str(dest), url], check=False)   # download (TLS verification stays on)
    ok = dest.exists() and dest.read_bytes()[:5] == b"%PDF-"   # magic-number check
    if not ok and dest.exists(): dest.unlink()   # remove an HTML error page saved under a .pdf name
    return ok   # result

def print_page(url, dest):
    """Print a web page to an A4 PDF with Playwright (Chromium)."""
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
          "try{await p.goto(process.argv[1],{waitUntil:'networkidle',timeout:90000});}catch(e){}"
          "await p.waitForTimeout(2000);await p.pdf({path:process.argv[2],format:'A4',printBackground:true});await b.close();})();")   # tiny print script
    subprocess.run(["node", "-e", js, url, str(dest)], check=False)   # run it
    return dest.exists() and dest.read_bytes()[:5] == b"%PDF-"   # result

def main():
    OUT.mkdir(parents=True, exist_ok=True)   # make the folder
    wanted = sys.argv[1:]   # optional key prefixes
    for key, s in sorted(c.load_catalog().items()):   # every catalogued source
        if wanted and not any(key.startswith(w) for w in wanted): continue   # filter
        dest = OUT / f"{key}.pdf"   # target file
        if dest.exists(): print(f"have  {key}"); continue   # already downloaded
        url = s.get("download", s["url"])   # direct download link if the landing page differs
        ok = print_page(url, dest) if s.get("kind") == "webprint" else fetch_pdf(url, dest)   # fetch or print
        print(("ok    " if ok else "FAIL  ") + key)   # report

if __name__ == "__main__":
    main()   # run when called as a script
