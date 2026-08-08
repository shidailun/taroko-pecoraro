# -*- coding: utf-8 -*-
"""The about sheet must PRINT the build id, and it must be the same id the
html hangs off every asset URL. A half-stamped page is worse than an unstamped
one: it looks updated and is not."""
import re, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")

html = open("site/index.html", encoding="utf-8").read()
ids = set(re.findall(r'\?v=([0-9A-Za-z.-]+)', html))
bad = 0
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    bad404 = []
    pg.on("response", lambda r: bad404.append(r.url) if r.status >= 400 else None)
    pg.goto("http://127.0.0.1:8765/", wait_until="networkidle")
    pg.click("#btn-about"); pg.wait_for_timeout(600)
    stamp = pg.text_content(".build-stamp")
    print("html ids:", sorted(ids), "| sheet says:", repr(stamp))
    shown = stamp.replace("Build", "").strip()
    if ids != {shown}: bad = 1; print("  <-- MISMATCH")
    # every frame of the cycle still loads (a 404 renders as a broken img)
    n = pg.evaluate("PHOTOS ? PHOTOS.length : 0") if False else 9
    ok = []
    for i in range(n):
        pg.wait_for_timeout(150)
        ok.append(pg.eval_on_selector(".about-photo",
            "e => e.naturalWidth > 0 ? e.src.split('/').pop() : 'BROKEN ' + e.src"))
        pg.evaluate("document.querySelector('.about-photo')")
        pg.wait_for_timeout(5100 if i < n - 1 else 0)
    print("frames:", " ".join(ok))
    if any(f.startswith("BROKEN") for f in ok): bad = 1
    if errs: bad = 1; print("JS ERRORS:", errs[:3])
    if bad404: bad = 1; print("HTTP >=400:", bad404[:5])
    b.close()
print("VERDICT:", "FAIL" if bad else "clean")
