# -*- coding: utf-8 -*-
"""Open the KGUS card, expand "Elsewhere in the dictionary", and show for each
row WHICH owned token pulled it in. That is the whole of the user's question."""
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    ctx.add_init_script("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()
    pg.goto("http://127.0.0.1:8765/?q=kgus")
    pg.wait_for_timeout(3500)

    own = pg.evaluate("""() => {
      const i = window.ENTRIES.findIndex(e => /KUGUS/i.test(e.hw || ''));
      return {i: i, hw: window.ENTRIES[i].hw,
              subs: (window.ENTRIES[i].subs || []).map(s => s.form + '  ¶ ' + (s.paradigm || ''))};
    }""")
    print("entry #%d  hw=%s" % (own["i"], own["hw"]))
    for s in own["subs"]:
        print("   sub:", s)

    det = pg.query_selector("details.conc")
    print("\nsummary text:", repr(det.query_selector("summary").inner_text()) if det else "NO CONC BLOCK")
    if det:
        det.query_selector("summary").click()
        pg.wait_for_timeout(900)
        rows = pg.query_selector_all("details.conc .conc-row")
        print("rows: %d\n" % len(rows))
        for r in rows:
            tk = r.query_selector(".truku").inner_text().strip()
            src = r.query_selector(".conc-src")
            hits = sorted(set(w.lower() for w in re.findall(r"[A-Za-z']+", tk)
                              if "gus" in w.lower()))
            print("   %-88s  <- %s   [%s]"
                  % (tk[:88], (src.inner_text().strip() if src else "?"), ",".join(hits)))
    b.close()
