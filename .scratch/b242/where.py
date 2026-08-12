# -*- coding: utf-8 -*-
"""WHERE does the pale sit? Book-wide pale minus `.truku`-scoped pale is 112
spans; this asks what kind of node each one is in, because "outside .truku"
means his card furniture (batch 222) AND his French (batch 216), and those are
opposite answers to "is it even Truku?".
"""
import sys
from collections import Counter

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  const out = [];
  document.querySelectorAll('#results > article.entry').forEach(c => {
    c.querySelectorAll(SEL).forEach(s => {
      if (!s.classList.contains('w-unv') && !s.classList.contains('w-raw'))
        return;
      // name the nearest container that says what KIND of text this is
      const kinds = ['.truku', '.hw', '.sub-form', '.paradigm', '.tag',
                     '.gloss', '.crossref', '.meta-abbr', '.meta'];
      let where = 'other';
      for (const k of kinds) { if (s.closest(k)) { where = k; break; } }
      out.push({t: (s.textContent||'').trim().toLowerCase(), where: where,
                cls: s.classList.contains('w-raw') ? 'green' : 'pale',
                tag: (s.parentElement||{}).className || ''});
    });
  });
  return out; }"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto("http://127.0.0.1:8765/")
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=%CC%81")
    pg.wait_for_timeout(22000)
    rows = pg.evaluate(JS)
    b.close()

for cls in ("pale", "green"):
    sub = [r for r in rows if r["cls"] == cls]
    print("%s: %d spans / %d types" % (
        cls.upper(), len(sub), len(set(r["t"] for r in sub))))
    by = Counter(r["where"] for r in sub)
    for w, n in by.most_common():
        ts = sorted(set(r["t"] for r in sub if r["where"] == w))
        print("   %-11s %4d spans %3d types   e.g. %s" % (
            w, n, len(ts), " ".join(ts[:4])))
