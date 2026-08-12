# -*- coding: utf-8 -*-
"""Explain the 2-span / 3-type disagreement with dom232 before reporting either.

dom232's pale figure is BOOK-WIDE (its second walk is unscoped) and it keys
EVERY span including whitespace-only ones; `pct.py` guards on empty text. Run
both keyings in one pass over one page load so the only variable is the code.
"""
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  const D = {seen: {}, unv: {}, raw: {}};       // dom232's exact keying
  const G = {seen: {}, unv: {}, raw: {}};       // pct.py's, empty guarded
  const bump = (d, k, t) => { d[k][t] = (d[k][t] || 0) + 1; };
  const tally = (d, s, guard) => {
    const t = (s.textContent || '').trim().toLowerCase();
    if (guard && !t) return;
    bump(d, 'seen', t);
    if (s.classList.contains('w-unv')) bump(d, 'unv', t);
    if (s.classList.contains('w-raw')) bump(d, 'raw', t);
  };
  document.querySelectorAll('#results > article.entry').forEach(c => {
    c.querySelectorAll(SEL).forEach(s => { tally(D, s, false);
                                           tally(G, s, true); });
  });
  return {D: D, G: G}; }"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    # dom232's exact setup: spelling forced modern, and a 22s settle. The
    # keying is not the variable (both tallies agree); the SETTLE is.
    pg.goto("http://127.0.0.1:8765/")
    pg.evaluate(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=%CC%81")
    pg.wait_for_timeout(22000)
    r = pg.evaluate(JS)
    b.close()

for nm in ("D", "G"):
    d = r[nm]
    print("%s  spans %d types %d | pale %d/%d | green %d/%d" % (
        nm, sum(d["seen"].values()), len(d["seen"]),
        sum(d["unv"].values()), len(d["unv"]),
        sum(d["raw"].values()), len(d["raw"])))
only = sorted(set(r["G"]["unv"]) ^ set(r["D"]["unv"]))
print("pale types differing between the two keyings: %d %s" % (
    len(only), only[:8]))
