# -*- coding: utf-8 -*-
"""The six legend figures, from the DOM. Summary line only."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context()
    ctx.add_init_script("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()
    pg.goto("http://127.0.0.1:8765/?q=%CC%81"); pg.wait_for_timeout(30000)
    r = pg.evaluate("""() => {
      const b = {mod:{}, cls:{}, unv:{}, raw:{}};
      for (const s of document.querySelectorAll('#results .w-mod,#results .w-unv,#results .w-raw')) {
        const k = s.classList.contains('w-cls') ? 'cls'
                : s.classList.contains('w-mod') ? 'mod'
                : s.classList.contains('w-unv') ? 'unv' : 'raw';
        const t = s.textContent.trim().toLowerCase();
        b[k][t] = (b[k][t]||0)+1;
      }
      const o = {}; for (const k in b)
        o[k] = [Object.values(b[k]).reduce((a,c)=>a+c,0), Object.keys(b[k]).length];
      o.cards = document.querySelectorAll('#results > article.entry').length;
      return o; }""")
    tot = r["mod"][0]+r["cls"][0]+r["unv"][0]+r["raw"][0]
    print("cards %d  total %d | dark %d/%d  class %d/%d  pale %d/%d  green %d/%d"
          % (r["cards"], tot, r["mod"][0], r["mod"][1], r["cls"][0], r["cls"][1],
             r["unv"][0], r["unv"][1], r["raw"][0], r["raw"][1]))
    br.close()
