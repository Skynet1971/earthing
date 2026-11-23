"""Extract page-marked text from every PDF: python3 -I tools/extract_text.py references/pdf references/local/text"""
import subprocess, sys, pathlib   # standard library only
src = pathlib.Path(sys.argv[1]); dst = pathlib.Path(sys.argv[2])   # input PDF dir, output text dir
for pdf in sorted(src.glob("*.pdf")):   # every downloaded PDF
    n = int([l for l in subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout.splitlines() if l.startswith("Pages")][0].split()[1])   # page count
    out = dst / (pdf.stem + ".txt")   # one text file per PDF
    with out.open("w") as fh:
        for p in range(1, n + 1):   # page by page so page numbers are exact
            t = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
            fh.write(f"\n=== PAGE {p} ===\n{t}")   # marker = PDF page index (not printed page number)
    print(f"{n:4d} pages {out.stat().st_size:9d} bytes  {out.name}")
