# -*- coding: utf-8 -*-
"""Both-mode census + the batch-125 words in the DOM."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"
SPANS = """(ws) => { const r = {};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const t = n.textContent.trim().toLowerCase();
    if (ws.indexOf(t) < 0) continue;
    const s = n.className.indexOf('w-mod') >= 0 ? 'dark'
            : n.className.indexOf('w-unv') >= 0 ? 'PALE' : 'GREEN';
    (r[t] = r[t] || {})[s] = (r[t][s] || 0) + 1;
  } return r; }"""
WATCH = ["pgyai", "pgiai", "pgiyai", "knshyaan", "knsxeaan", "knshiyaan",
         "pgyaan", "pgyaun", "knshiya", "shiya", "pgaya", "mpgaya"]

with sync_playwright() as p:
    b = p.chromium.launch()
    for mode in ("modern", "original"):
        ctx = b.new_context()
        ctx.add_init_script(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','%s')" % mode)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL)
        pg.wait_for_timeout(9000)
        c = {k: pg.evaluate('()=>document.querySelectorAll("span.%s").length' % k)
             for k in ("w-mod", "w-unv", "w-raw")}
        cards = pg.evaluate('()=>document.querySelectorAll("article.entry").length')
        t = sum(c.values())
        print("%-9s %s  total %d  dark %.4f%%  cards %d  errors %d"
              % (mode, c, t, 100.0 * c["w-mod"] / t, cards, len(errs)))
        if mode == "modern":
            seen = pg.evaluate(SPANS, WATCH)
        ctx.close()
    b.close()

print("\n-- the batch-125 values in the DOM")
for w in WATCH:
    print("   %-10s %s" % (w, seen.get(w) or "absent"))
