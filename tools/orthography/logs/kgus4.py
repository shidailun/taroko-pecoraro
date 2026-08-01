# -*- coding: utf-8 -*-
"""Book-wide concordance totals, read off the summaries of all 1,967 cards.
Run before and after the grouping edit: the two numbers must be identical."""
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    ctx.add_init_script("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("http://127.0.0.1:8765/?q=%CC%81")
    pg.wait_for_timeout(9000)
    txt = pg.evaluate("""() => Array.from(
        document.querySelectorAll('details.conc > summary')).map(s => s.textContent)""")
    cards = pg.evaluate('()=>document.querySelectorAll("article.entry").length')
    b.close()

ns = [int(re.search(r"\((\d+)\)", t).group(1)) for t in txt]
print("cards %d   entries with a list %d   rows in all %d   page errors %d"
      % (cards, len(ns), sum(ns), len(errs)))
