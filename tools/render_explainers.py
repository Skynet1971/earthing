#!/usr/bin/env python3
"""Write the animated explainer SVGs and their still frames (PNG, used by the PDFs).

Usage: python3 tools/render_explainers.py [name ...]
Writes wiki/img/<name>.svg and docs/img/explainers/<name>.png (committed, because CI has no browser).
The still frame freezes every CSS and SMIL animation at the explainer's still time, using the
Playwright Chromium that is installed in this environment.
"""
import sys, json, pathlib, subprocess   # standard library
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))   # import sibling module
import explainers   # the explainer registry

ROOT = pathlib.Path(__file__).resolve().parent.parent   # repository root
SVG_DIR, PNG_DIR = ROOT / "wiki" / "img", ROOT / "docs" / "img" / "explainers"   # outputs
JS = r"""
const {chromium} = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[1]);
  const b = await chromium.launch(); const p = await b.newPage({deviceScaleFactor: 2});
  for (const j of jobs) {
    await p.setContent('<html><body style="margin:0;background:#fff">' + j.svg + '</body></html>');
    await p.evaluate(t => {
      const s = document.querySelector('svg'); s.pauseAnimations(); s.setCurrentTime(t);
      document.getAnimations().forEach(a => { a.pause(); a.currentTime = t * 1000; });
    }, j.t);
    await (await p.$('svg')).screenshot({path: j.out});
  }
  await b.close();
})();
"""   # freeze animations at time t and screenshot the SVG element

def main():
    SVG_DIR.mkdir(parents=True, exist_ok=True); PNG_DIR.mkdir(parents=True, exist_ok=True)   # folders
    names = sys.argv[1:] or sorted(explainers.EXPLAINERS)   # which explainers
    jobs = []   # screenshot jobs
    for n in names:   # each explainer
        svg, t = explainers.EXPLAINERS[n]()   # build it
        (SVG_DIR / f"{n}.svg").write_text(svg)   # animated version for the wiki
        jobs.append({"svg": svg, "t": t, "out": str(PNG_DIR / f"{n}.png")})   # still frame for the PDF
    subprocess.run(["node", "-e", JS, json.dumps(jobs)], check=True)   # render the stills
    for n in names: print(f"{n}: wiki/img/{n}.svg, docs/img/explainers/{n}.png")   # report

if __name__ == "__main__":
    main()   # run when called as a script
