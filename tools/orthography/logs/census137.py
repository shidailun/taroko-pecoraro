# -*- coding: utf-8 -*-
"""Batch 137: the wider corpus reaching the tier that DECIDES spellings.

Batch 136 gave build_verified.py the parquet reading of the ILRDF collections
(361,630 tokens against the xlsx export's 272,150) and deliberately stopped
there: verification only asks whether a string occurs, while the MAP asks which
spelling is right, and that is a larger claim.

Two words change on the page and this checks both, in both spelling modes:

  MBUA   mbuwa -> embuwa   his form was never in the omnibus at all; `embuwa`
                           is, glossed 有氣泡, over his root `buwa` 氣泡. It had
                           been held at `mbuwa` by ONE token in the xlsx.
  MIXALASI mihalasi -> miharasi   a village. The corpus names it in the clear:
                           「故改名為 Miharasi。漢語翻成 見晴」 — Japanese
                           見晴らし, so his l is that word's r, and tier N had
                           frozen an l that was never there.

The census is the load-bearing part. Widening a corpus must not move anything
else, and the first run proved it can: three words lost an attested spelling to
a single new transcript token each.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"
COUNT = """() => {
  const r = {dark: 0, PALE: 0, GREEN: 0};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    r[n.className.indexOf('w-mod') >= 0 ? 'dark'
      : n.className.indexOf('w-unv') >= 0 ? 'PALE' : 'GREEN'] += 1;
  }
  return r; }"""
SPANS = """(ws) => { const r = {};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const t = n.textContent.trim().toLowerCase();
    if (ws.indexOf(t) < 0) continue;
    const s = n.className.indexOf('w-mod') >= 0 ? 'dark'
            : n.className.indexOf('w-unv') >= 0 ? 'PALE' : 'GREEN';
    (r[t] = r[t] || {})[s] = (r[t][s] || 0) + 1;
  } return r; }"""
GAIN = ["embuwa", "miharasi"]
GONE = ["mbuwa", "mihalasi", "empurug", "embrinah", "emphuqil"]

with sync_playwright() as p:
    b = p.chromium.launch()
    for mode in ("modern", "pecoraro"):
        ctx = b.new_context()
        ctx.add_init_script(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','%s')" % mode)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL)
        pg.wait_for_timeout(6000)
        cards = pg.locator("article.entry").count()
        c = pg.evaluate(COUNT)
        tot = c["dark"] + c["PALE"] + c["GREEN"]
        print("[%s] cards %d   dark %d  pale %d  green %d   dark %.4f%%"
              % (mode, cards, c["dark"], c["PALE"], c["GREEN"],
                 100.0 * c["dark"] / tot if tot else 0))
        if mode == "modern":
            print("   gained:", pg.evaluate(SPANS, GAIN))
            print("   gone  :", pg.evaluate(SPANS, GONE))
        print("   page errors:", len(errs), errs[:2])
        ctx.close()
    b.close()
