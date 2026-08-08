# -*- coding: utf-8 -*-
"""[batch 233 probe] The five GREEN-side rows of batch 225's compound-tag sweep.
Price them from the DOM (scope + count), then ask the gloss test of the dark
side. Verdicts only."""
import sys, importlib.util, re, json
sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location("dom232", "tools/orthography/logs/dom232.py")
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
from playwright.sync_api import sync_playwright

PAIRS = [("LQBUX", "lqbux", "l'qbuç"), ("PGDGIT", "pgdgit", "pg'dgit"),
         ("SLAP", "slap", "silap"), ("XK'LAO", "xk'lao", "xq'lao"),
         ("XNU", "xnu", "x'nu"), ("PSAANAK", "psaanak", "psaanaq")]
MM = M.modern_map(); AM, AG, BG, PG = M.sources(); CNT = M.his_tokens()

def modern(w):
    k = re.sub("[’ʼ\"ʔ]", "'", w.lower()).replace("ł", "l")
    return MM.get(k) or M.char_rules(k)

want = {}
for hw, dark, pale in PAIRS:
    want[modern(dark)] = (hw, "dark-side")
    want[modern(pale)] = (hw, "var-side")

JS = """(WANT) => {
  const out = [];
  for (const art of document.querySelectorAll('#results > article.entry')) {
    const hw = (art.querySelector('.hw')||{}).textContent || '';
    for (const s of art.querySelectorAll('span.w-mod, span.w-unv, span.w-raw')) {
      const t = (s.textContent||'').toLowerCase().trim();
      if (!WANT.includes(t)) continue;
      out.push([hw, t, s.className, !!s.closest('.truku'),
                (s.parentElement||{}).className||'']);
    }
  }
  return out;
}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(M.URL)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(M.URL + "?q=%CC%81"); pg.wait_for_timeout(22000)
    rows = pg.evaluate(JS, sorted(want))
    b.close()

import collections
agg = collections.Counter()
tru = collections.Counter()
cls = {}
for hw, t, c, inT, par in rows:
    agg[t] += 1
    if inT: tru[t] += 1
    cls.setdefault(t, set()).add(c.strip())

print("%-12s %-12s %-10s %6s %6s %-10s %s" % ("card", "token", "value", "spans", "inTruku", "class", "his"))
for hw, dark, pale in PAIRS:
    for lbl, t in (("dark", dark), ("var ", pale)):
        v = modern(t)
        print("%-12s %-12s %-10s %6d %6d %-10s %s"
              % (hw if lbl == "dark" else "", t, v, agg.get(v, 0), tru.get(v, 0),
                 ",".join(sorted(cls.get(v, []))) [:10], CNT.get(t)))

print("\n-- gloss of the dark side, and whether the variant reaches anything")
for hw, dark, pale in PAIRS:
    dv, pv = modern(dark), modern(pale)
    g = (M.gl(AG, dv) or M.gl(BG, dv) or M.gl(PG, dv) or ["-"])[0]
    print("%-10s %-10s %-26s | var %-10s attested=%s charRules=%s"
          % (hw, dv, str(g)[:26], pv, pv in AM, M.char_rules(pale)))
