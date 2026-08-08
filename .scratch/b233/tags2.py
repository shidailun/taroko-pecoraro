# -*- coding: utf-8 -*-
"""[batch 233 probe] Every span inside a `.tag` in the whole book, by colour.
Batch 226: the card furniture prints in the DOM's own case AND its own
spelling, so a probe keyed on HIS headword sees nothing."""
import sys, importlib.util, collections
sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location("dom232", "tools/orthography/logs/dom232.py")
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
from playwright.sync_api import sync_playwright
JS = """() => {
  const out = [];
  for (const art of document.querySelectorAll('#results > article.entry')) {
    const hw = ((art.querySelector('.hw')||{}).textContent||'').trim();
    for (const tag of art.querySelectorAll('.tag')) {
      for (const s of tag.querySelectorAll('span.w-mod, span.w-unv, span.w-raw')) {
        out.push([hw, tag.textContent.trim(), s.textContent, s.className.trim(),
                  !!s.closest('.truku')]);
      }
    }
  }
  return out;
}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(M.URL)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(M.URL + "?q=%CC%81"); pg.wait_for_timeout(22000)
    rows = pg.evaluate(JS)
    b.close()
c = collections.Counter(("w-mod" if "w-mod" in r[3].split() else
     "w-unv" if "w-unv" in r[3].split() else "w-raw") for r in rows)
print("tag spans:", dict(c), "| inTruku:", sum(1 for r in rows if r[4]))
print("\n-- every NON-dark span inside a tag")
for hw, tag, t, cl, inT in sorted(set(map(tuple, rows))):
    if "w-mod" not in cl.split():
        print("%-12s %-34s %-12s %s" % (hw, tag[:34], t, cl))
