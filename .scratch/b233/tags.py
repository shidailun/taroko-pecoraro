# -*- coding: utf-8 -*-
"""[batch 233 probe] Every span on the six compound-tag cards, as the DOM has
them. Verdict rows only."""
import sys, importlib.util
sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location("dom232", "tools/orthography/logs/dom232.py")
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
from playwright.sync_api import sync_playwright
CARDS = ["LQBUX", "PGDGIT", "SLAP", "XK'LAO", "XNU", "PSAANAK"]
JS = """(CARDS) => {
  const out = [];
  for (const art of document.querySelectorAll('#results > article.entry')) {
    const hw = ((art.querySelector('.hw')||{}).textContent||'').trim();
    if (!CARDS.includes(hw)) continue;
    for (const s of art.querySelectorAll('span.w-mod, span.w-unv, span.w-raw')) {
      const p = (s.parentElement||{});
      out.push([hw, s.textContent, s.className.trim(), !!s.closest('.truku'),
                (p.className||p.tagName||'').toString().slice(0,14)]);
    }
  }
  return out;
}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(M.URL)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(M.URL + "?q=%CC%81"); pg.wait_for_timeout(22000)
    rows = pg.evaluate(JS, CARDS)
    b.close()
seen = set()
for hw, t, c, inT, par in rows:
    k = (hw, t, c, inT, par)
    if k in seen: continue
    seen.add(k)
    if par in ("hw", "tag") or c != "w-mod":
        print("%-9s %-14s %-6s inTruku=%-5s %s" % (hw, t, c, inT, par))
print("cards seen:", sorted(set(r[0] for r in rows)))
