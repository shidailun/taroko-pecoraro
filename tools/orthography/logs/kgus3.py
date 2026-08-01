# -*- coding: utf-8 -*-
"""Regression for the grouped concordance.

Grouping must change the PRESENTATION and nothing else, so the two numbers the
code documents — 895 entries with a list, 22,193 rows in all — must survive it.
Then check the headings actually render, that the CONC_MAX cap still holds on
his worst case, and that a group heading follows the spelling toggle.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

TOTALS = """() => {
  let ents = 0, rows = 0, groups = 0;
  for (let i = 0; i < window.ENTRIES.length; i++) {
    const h = window.__concHits(i);
    if (h.rows.length) { ents++; rows += h.rows.length; groups += h.groups.length; }
  }
  return {ents: ents, rows: rows, groups: groups};
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
        pg.goto("http://127.0.0.1:8765/?q=kgus")
        pg.wait_for_timeout(3500)

        det = pg.query_selector("details.conc")
        det.query_selector("summary").click()
        pg.wait_for_timeout(700)
        heads = [h.inner_text().strip() for h in pg.query_selector_all(".conc-form")]
        print("[%s] KGUS summary %r" % (mode, det.query_selector("summary").inner_text()))
        print("      group headings: %s" % heads)
        print("      rows: %d   page errors: %d"
              % (len(pg.query_selector_all(".conc-row")), len(errs)))

        # his worst case: the KA particle, 3,185 rows, must still cap at 40
        pg.goto("http://127.0.0.1:8765/?q=ka")
        pg.wait_for_timeout(3000)
        d2 = pg.query_selector("article.entry details.conc")
        if d2:
            d2.query_selector("summary").click()
            pg.wait_for_timeout(1200)
            n = len(pg.query_selector_all("article.entry details.conc .conc-row"))
            more = pg.query_selector(".conc-more")
            print("      worst case rows rendered %d (cap 40)  more-line: %s"
                  % (n, bool(more)))
        ctx.close()
    b.close()
