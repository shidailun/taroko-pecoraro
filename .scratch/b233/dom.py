# -*- coding: utf-8 -*-
"""[batch 233 probe] Where psaanaq renders, and in what scope. Verdicts only."""
import sys, importlib.util, json, io
sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location("dom232", "tools/orthography/logs/dom232.py")
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
from playwright.sync_api import sync_playwright

JS = """() => {
  const out = {spans: [], cards: []};
  for (const art of document.querySelectorAll('#results > article.entry')) {
    const hw = (art.querySelector('.hw') || {}).textContent || '';
    let hit = false;
    for (const s of art.querySelectorAll('span.w-mod, span.w-unv, span.w-raw')) {
      const t = (s.textContent || '').toLowerCase().trim();
      if (t !== 'psaanaq' && t !== 'psaanak' && t !== 'pseanak') continue;
      hit = true;
      const inTruku = !!s.closest('.truku');
      out.spans.push([hw, t, s.className, inTruku,
                      (s.parentElement||{}).className || '']);
    }
    if (hit) out.cards.push(hw);
  }
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(M.URL)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(M.URL + "?q=%CC%81")
    pg.wait_for_timeout(22000)
    D = pg.evaluate(JS)
    b.close()
for r in D["spans"]:
    print("%-14s %-10s %-18s inTruku=%s parent=%s" % (r[0][:14], r[1], r[2], r[3], r[4][:24]))
print("cards:", D["cards"])
