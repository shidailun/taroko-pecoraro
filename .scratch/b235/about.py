# -*- coding: utf-8 -*-
"""Open the About sheet and step the photo cycle. Verifies every frame actually
loads (a 404 renders as a broken img with naturalWidth 0, which no screenshot of
a five-second slideshow would reliably catch) and that the sheet's own height
does not move as the shapes change."""
import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 430, "height": 900})
    bad = []
    pg.on("response", lambda r: bad.append(r.url.split("/")[-1])
          if r.status >= 400 else None)
    pg.goto("http://localhost:8765/", wait_until="networkidle")
    pg.click("#btn-about")
    pg.wait_for_timeout(600)
    n = pg.evaluate("PHOTOS_LEN" if False else "1")
    hs, shots = [], []
    for i in range(8):
        pg.wait_for_timeout(120)
        d = pg.evaluate("""() => {
          const i = document.querySelector('.about-photo');
          const s = document.getElementById('sheet');
          return {src: i.src.split('/').pop(), w: i.naturalWidth,
                  h: i.naturalHeight,
                  box: Math.round(i.getBoundingClientRect().height),
                  sheet: Math.round(s.getBoundingClientRect().height)};
        }""")
        print("%d %-16s %4dx%-4d box=%d sheet=%d %s"
              % (i, d["src"], d["w"], d["h"], d["box"], d["sheet"],
                 "LOADED" if d["w"] else "*** BROKEN ***"))
        hs.append(d["sheet"])
        if i in (0, 5, 7):
            pg.screenshot(path=".scratch/b235/about_%d.png" % i)
        if i < 7:
            # step the cycle by hand rather than waiting 5s a frame
            pg.evaluate("""() => {
              const t = document.querySelector('.about-photo');
              const L = window.__PH; }""")
            pg.wait_for_timeout(5100)
    print("sheet height range:", min(hs), "-", max(hs),
          "| stable:", max(hs) - min(hs) <= 2)
    print("http errors:", sorted(set(bad)) or "none")
    b.close()
