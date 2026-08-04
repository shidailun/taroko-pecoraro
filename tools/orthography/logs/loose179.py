# -*- coding: utf-8 -*-
"""Batch 179b: principle 2 — a sentence hit answers with sentences.
Verdict lines only."""
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


def shape(pg):
    return pg.evaluate("""() => {
      const a = [...document.querySelectorAll('#results > article')];
      return {
        n: a.length,
        full: a.filter(x => x.className === 'entry').length,
        loose: a.filter(x => x.classList.contains('loose')).length,
        word: a.filter(x => x.classList.contains('word')).length,
        slot: a.filter(x => x.classList.contains('slot')).length,
        head: document.querySelectorAll('.loose-head').length,
        rows: document.querySelectorAll('.entry.loose .conc-row').length,
        src: document.querySelectorAll('.entry.loose .conc-src[data-ref]').length,
      }; }""")


with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context()
    ctx.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()

    # --- 1. qmpahan: the word card, then sentences, no root cards ---
    pg.goto(B + "?q=qmpahan")
    pg.wait_for_timeout(3000)
    s = shape(pg)
    print("   qmpahan:", s)
    t("word page still ranks first", s["word"] == 1)
    t("no full root card hauled in", s["full"] == 0, s["full"])
    t("sentences instead", s["loose"] > 0, s["loose"])
    t("one heading", s["head"] == 1, s["head"])
    t("every row names its source", s["rows"] == s["src"] and s["rows"] > 0,
      (s["rows"], s["src"]))

    # every rendered sentence really contains the query
    bad = pg.evaluate("""() => [...document.querySelectorAll('.entry.loose .conc-row')]
      .filter(r => (r.querySelector('.truku').textContent||'').toLowerCase()
        .normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').indexOf('qmpahan') < 0)
      .length""")
    t("no sentence without the query", bad == 0, bad)

    # --- 2. the source pointer opens the entry on one tap ---
    h0 = pg.evaluate("history.length")
    pg.eval_on_selector(".entry.loose .conc-src[data-ref]", "e => e.click()")
    pg.wait_for_timeout(700)
    t("source pointer opens a card",
      pg.evaluate("document.querySelectorAll('#results > article').length") >= 1)
    t("...and pushed one history entry",
      pg.evaluate("history.length") == h0 + 1, pg.evaluate("history.length"))
    pg.go_back(); pg.wait_for_timeout(600)
    t("BACK returns to the sentence list",
      shape(pg)["loose"] > 0, shape(pg))

    # --- 3. a headword query is untouched: BUYO still renders whole ---
    pg.goto(B + "?q=BUYO")
    pg.wait_for_timeout(2500)
    s = shape(pg)
    print("   BUYO:", s)
    t("a headword query still gets the full card", s["full"] >= 1, s)
    t("...with its sub-forms",
      pg.evaluate("document.querySelectorAll('.subentry').length") >= 5,
      pg.evaluate("document.querySelectorAll('.subentry').length"))

    # --- 4. sub-form order is the derivational one (principle 1) ---
    for q, want in (("K'MUX", ["Skmux", "Pskmux"]),
                    ("BUYO", ["BBuyu", "Bbuyu", "Pkbuyu", "Tnbuyan",
                              "Kmubui (kmbui?)"])):
        pg.goto(B + "?q=" + q)
        pg.wait_for_timeout(2500)
        got = pg.evaluate("""() => [...document.querySelectorAll(
          '#results > article.entry:not(.loose) .subentry .sub-form')]
          .map(x => x.textContent.trim())""")
        t("%s sub-order" % q, got[:len(want)] == want, got[:6])

    # --- 5. a gloss-only hit keeps its whole card ---
    pg.goto(B + "?q=palissade")
    pg.wait_for_timeout(2500)
    s = shape(pg)
    print("   palissade:", s)
    t("a French-gloss hit is not emptied", s["full"] + s["loose"] > 0, s)

    # --- 6. no census regression ---
    pg.goto(B + "?q=%CC%81")
    pg.wait_for_timeout(15000)
    n = pg.evaluate("document.querySelectorAll('#results > article.entry').length")
    t("whole-dictionary census still 1967 cards", n == 1967, n)
    lo = pg.evaluate("document.querySelectorAll('.entry.loose').length")
    t("...and none of them is a sentence card", lo == 0, lo)

    br.close()

print("\n%d pass, %d fail" % (ok, fail))
