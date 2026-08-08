# -*- coding: utf-8 -*-
"""One DOM pass: the pair metric, the pale census, and the colour of any words
named on the command line. Summary lines only."""
import sys

sys.stdout.reconfigure(encoding="utf-8")
WATCH = [w.lower() for w in sys.argv[1:]]
BASE = "http://127.0.0.1:8765/"

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  let tot = 0, ok = 0;
  const seen = {}, unv = {}, raw = {}, sole = {}, itk = {};
  document.querySelectorAll('#results > article.entry').forEach(c => {
    c.querySelectorAll('.truku').forEach(b => {
      const sp = [...b.querySelectorAll(SEL)];
      if (!sp.length) return;
      tot++;
      if (sp.every(s => s.classList.contains('w-mod'))) ok++;
      else {
        const bad = [...new Set(sp.filter(s => !s.classList.contains('w-mod'))
                       .map(s => (s.textContent||'').trim().toLowerCase()))];
        if (bad.length === 1) sole[bad[0]] = (sole[bad[0]] || 0) + 1;
      }
    });
    c.querySelectorAll(SEL).forEach(s => {
      const t = (s.textContent || '').trim().toLowerCase();
      seen[t] = (seen[t] || 0) + 1;
      if (s.classList.contains('w-unv')) unv[t] = (unv[t] || 0) + 1;
      if (s.classList.contains('w-raw')) raw[t] = (raw[t] || 0) + 1;
      if (s.closest('.truku')) itk[t] = (itk[t] || 0) + 1;
    });
  });
  return {tot, ok, seen, unv, raw, sole, itk}; }"""

from playwright.sync_api import sync_playwright        # noqa: E402

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(BASE)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(BASE + "?q=%CC%81")
    pg.wait_for_timeout(22000)
    d = pg.evaluate(JS)
    b.close()

print("pairs %d/%d = %.4f%%" % (d["ok"], d["tot"], 100.0 * d["ok"] / d["tot"]))
print("pale %d spans / %d types   green %d spans / %d types   sole-blocked %d"
      % (sum(d["unv"].values()), len(d["unv"]),
         sum(d["raw"].values()), len(d["raw"]), sum(d["sole"].values())))
for w in WATCH:
    print("  %-12s seen=%-3d pale=%-3d green=%-3d inTruku=%-3d sole=%d"
          % (w, d["seen"].get(w, 0), d["unv"].get(w, 0), d["raw"].get(w, 0),
             d["itk"].get(w, 0), d["sole"].get(w, 0)))
