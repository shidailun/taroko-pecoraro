# -*- coding: utf-8 -*-
"""What does the page really do with `kgus`? Search order, and what the KUGUS
card shows, in both spelling modes. Read from the DOM, never from the map."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

ORDER = """() => {
  const out = [];
  document.querySelectorAll('article.entry, .stub').forEach(n => {
    const hw = n.querySelector('.hw, .stub-form');
    out.push((n.className.indexOf('stub') >= 0 ? 'stub  ' : 'card  ') +
             (hw ? hw.textContent.trim() : n.textContent.trim().slice(0, 40)));
  });
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for mode in ("modern", "original"):
        ctx = b.new_context()
        ctx.add_init_script(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','%s')" % mode)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        for q in ("kgus", "kmgus", "kugus"):
            pg.goto("http://127.0.0.1:8765/?q=" + q)
            pg.wait_for_timeout(3500)
            res = pg.evaluate(ORDER)
            print("\n[%s] q=%s  -> %d results, errors %d" % (mode, q, len(res), len(errs)))
            for r in res[:8]:
                print("     " + r)
        ctx.close()
    b.close()
