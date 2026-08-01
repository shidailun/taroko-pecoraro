# -*- coding: utf-8 -*-
"""Where does the pale mass sit now? Types + occurrences, straight from the DOM.

No count is computed from modern_map.json — WORD_OVERRIDES, CLITIC_FORMS and the
prose guards never appear in it. Modern mode only; pale is `span.w-unv`.
"""
import sys, collections, json
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"
JS = """() => {
  const out = {mod: [], unv: [], raw: []};
  for (const n of document.querySelectorAll('span.w-mod'))
    out.mod.push(n.textContent.trim().toLowerCase());
  for (const n of document.querySelectorAll('span.w-unv'))
    out.unv.push(n.textContent.trim().toLowerCase());
  for (const n of document.querySelectorAll('span.w-raw'))
    out.raw.push(n.textContent.trim().toLowerCase());
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    ctx.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL)
    pg.wait_for_timeout(9000)
    cards = pg.evaluate('()=>document.querySelectorAll("article.entry").length')
    d = pg.evaluate(JS)
    b.close()

tot = len(d["mod"]) + len(d["unv"]) + len(d["raw"])
print("cards %d  page errors %d" % (cards, len(errs)))
print("dark %d (%.4f%%)   pale %d   green %d   total %d"
      % (len(d["mod"]), 100.0 * len(d["mod"]) / tot, len(d["unv"]),
         len(d["raw"]), tot))

pale = collections.Counter(d["unv"])
print("\npale: %d occurrences over %d types; %d are hapax"
      % (sum(pale.values()), len(pale),
         sum(1 for w, n in pale.items() if n == 1)))

print("\n-- top 60 pale types by occurrences")
for w, n in pale.most_common(60):
    print("   %5d  %s" % (n, w))

top40 = sum(n for _, n in pale.most_common(40))
print("\ntop 40 = %d occurrences = %.1f%% of the pale mass"
      % (top40, 100.0 * top40 / sum(pale.values())))

json.dump({w: n for w, n in pale.most_common()},
          open("pale136.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=0)
print("wrote tools/orthography/logs/pale136.json")
