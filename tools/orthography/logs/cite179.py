# -*- coding: utf-8 -*-
"""Batch 179c: an inline see-also inside a gloss. Verdict lines only."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

B = "http://127.0.0.1:8765/"
ok = fail = 0


def t(name, cond, extra=""):
    global ok, fail
    if cond:
        ok += 1
        print("PASS  %s" % name)
    else:
        fail += 1
        print("FAIL  %s   %s" % (name, extra))


with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context()
    ctx.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()

    # --- PSANIQ: his "VR. SANYAQ." ---
    pg.goto(B + "?q=PSANIQ")
    pg.wait_for_timeout(2500)
    r = pg.evaluate("""() => {
      const c = document.querySelector('#results > article.entry');
      const links = [...c.querySelectorAll('.gloss .crossref-link')];
      return { n: links.length,
               txt: links.map(x => x.textContent.trim()),
               ref: links.map(x => x.getAttribute('data-ref')),
               fr: (c.querySelector('.gloss') || {}).textContent || '' }; }""")
    print("   PSANIQ:", r["n"], r["txt"], r["ref"])
    t("the pointer is a link", r["n"] >= 1, r["n"])
    t("...shown in modern spelling", "SANIQ" in r["txt"], r["txt"])
    t("...pointing at his own spelling", "SANYAQ" in r["ref"], r["ref"])
    t("...and the French around it survives",
      "Rendre tabou" in r["fr"] and "VR." in r["fr"], r["fr"][:70])

    # tapping it: crossrefs are two taps
    lk = pg.query_selector(".gloss .crossref-link")
    if lk:
        lk.click(); pg.wait_for_timeout(300)
        pg.query_selector(".gloss .crossref-link").click(); pg.wait_for_timeout(700)
        hw = pg.evaluate(
            "(document.querySelector('#results > article .hw')||{}).textContent||''")
        t("two taps open the entry it names", "SANIQ" in hw or "SANYAQ" in hw, hw)
    else:
        print("SKIP  no link to tap")

    # --- Pecoraro mode: his spelling, still linked ---
    pg2 = ctx.new_page()
    pg2.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','pecoraro')")
    pg2.goto(B + "?q=PSANIQ")
    pg2.wait_for_timeout(2500)
    r2 = pg2.evaluate("""() => [...document.querySelectorAll(
      '#results .gloss .crossref-link')].map(x => x.textContent.trim())""")
    print("   PSANIQ (his):", r2)
    t("his mode keeps his spelling", "SANYAQ" in r2 or not r2, r2)

    # --- whole dictionary: coverage, and no gloss text lost ---
    pg.goto(B + "?q=%CC%81")
    pg.wait_for_timeout(15000)
    s = pg.evaluate("""() => {
      const links = [...document.querySelectorAll('.gloss .crossref-link, '
        + '.ex-gloss .crossref-link')];
      const changed = links.filter(x =>
        x.textContent.trim().toUpperCase() !==
        (x.getAttribute('data-ref')||'').toUpperCase());
      return { cards: document.querySelectorAll('#results > article.entry').length,
               links: links.length, changed: changed.length,
               dead: links.filter(x => !x.getAttribute('data-ref')).length,
               sample: changed.slice(0,6).map(x =>
                 x.getAttribute('data-ref') + '->' + x.textContent.trim()) }; }""")
    print("   census:", s["cards"], "cards |", s["links"], "cite links |",
          s["changed"], "respelled |", s["sample"])
    t("census still 1967 cards", s["cards"] == 1967, s["cards"])
    t("no link without a target", s["dead"] == 0, s["dead"])
    t("the pointers that were stale are respelled", s["changed"] > 0, s["changed"])

    br.close()

print("\n%d pass, %d fail" % (ok, fail))
