# -*- coding: utf-8 -*-
"""Batch 205: the two homograph freezes the omnibus pairs caught, and the two
his own book refuses to let go of. Verdict lines only."""
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


def heads(pg, q):
    pg.goto(B + "?q=" + q)
    pg.wait_for_timeout(2200)
    return pg.evaluate("""() => [...document.querySelectorAll('#results .hw')]
        .map(h => h.textContent.trim() + '|' +
             (h.querySelector('.w-mod') ? 'dark' :
              h.querySelector('.w-unv') ? 'pale' : 'none'))""")


with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context()
    ctx.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()

    # --- the two ruled: dark AND right, where they were dark and wrong ---
    h = heads(pg, "TLAWAI")
    t("TLAWAI renders klaway 蝴蝶, not tlaway 箭步如飛",
      all(x.startswith("KLAWAY|dark") for x in h) and len(h) >= 1, h)
    h = heads(pg, "YUX")
    t("YUX renders iyux 堅持, on his own '參見IYUX 無疑更正確'",
      h and h[0] == "IYUX|dark", h)

    # --- the two refused: his own book cards BOTH senses ---
    h = heads(pg, "DIMA")
    t("DIMA still renders jima — his 已經 card is the running text",
      any(x.startswith("JIMA|dark") for x in h), h)
    t("...and he really does head three DIMA cards", len(h) >= 3, h)
    h = heads(pg, "DDIMA")
    t("DDIMA renders djima 竹子 — the reduplication is bamboo only",
      any(x.startswith("DJIMA|dark") for x in h), h)
    h = heads(pg, "QALO")
    t("QALO still renders qalu 食油 — both his examples are 豬油",
      any(x.startswith("QALU|dark") for x in h), h)

    # --- LAMIL: the false positive the omnibus gloss produced ---
    h = heads(pg, "LAMIL")
    t("LAMIL keeps ramil 拖鞋 — his gloss says 鞋子 and Mklamil is 穿鞋子",
      any(x.startswith("RAMIL|dark") for x in h), h)

    # --- no census regression ---
    pg.goto(B + "?q=%CC%81")
    pg.wait_for_timeout(30000)
    n = pg.evaluate(
        "document.querySelectorAll('#results > article.entry').length")
    t("whole-dictionary census still 1967 cards", n == 1967, n)

    br.close()

print("\n%d pass, %d fail" % (ok, fail))
