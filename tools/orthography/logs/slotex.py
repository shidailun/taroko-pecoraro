# -*- coding: utf-8 -*-
"""How many of the 998 generated slot pages actually carry example sentences?
Driven through the search box and Enter, which is the reader's own path."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context()
    ctx.add_init_script("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page(); pg.goto("http://127.0.0.1:8765/"); pg.wait_for_timeout(1500)
    words = []
    pg.click("#btn-alpha"); pg.wait_for_timeout(400)
    letters = pg.evaluate("""() => Array.from(document.querySelectorAll('#sheet-content button'))
        .map(e => e.textContent.trim()).filter(t => t.length <= 2)""")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    for L in letters:
        pg.click("#btn-alpha"); pg.wait_for_timeout(250)
        pg.get_by_text(L, exact=True).last.click(); pg.wait_for_timeout(800)
        words += pg.evaluate("""() => Array.from(document.querySelectorAll(
            '.entry.idx-slot .stub-hw')).map(e => e.textContent.trim())""")
    print("slot pages:", len(words))
    withex = rows = noex = 0
    for w in words:
        pg.fill("#search", w)
        pg.press("#search", "Enter")
        n = pg.evaluate("""() => { const c = document.querySelector('article.entry.slot');
            return c ? c.querySelectorAll('.conc-row').length : -1; }""")
        if n < 0: noex += 1
        elif n: withex += 1; rows += n
    print("carry >=1 example: %d   example rows in all: %d   unreachable by search: %d"
          % (withex, rows, noex))
    b.close()
