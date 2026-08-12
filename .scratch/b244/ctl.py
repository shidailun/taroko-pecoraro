# -*- coding: utf-8 -*-
"""why control A did not refuse: what does the page hold after the patch?"""
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
URL = "http://127.0.0.1:8765/"

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto(URL)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(URL + "?q=colophon")
    pg.wait_for_timeout(4000)
    print("plain ?q=colophon ->", pg.evaluate(
        "() => [...document.querySelectorAll('#results > article.entry .hw')]"
        ".map(e => e.textContent.trim())"))
    print("results html len:", pg.evaluate(
        "() => (document.getElementById('results')||{}).innerHTML.length"))
    hit = pg.evaluate("""() => {
      let n = 0;
      (window.ENTRIES||[]).forEach(e => { if (e.hw === 'COLOPHON') { e.tag=''; n++; } });
      const box = document.getElementById('search');
      const fire = v => { box.value = v;
        box.dispatchEvent(new Event('input', {bubbles: true})); };
      fire('zzzz'); fire('colophon');
      return n; }""")
    pg.wait_for_timeout(2000)
    print("patched", hit, "->", pg.evaluate(
        "() => [...document.querySelectorAll('#results > article.entry .hw')]"
        ".map(e => e.textContent.trim())"))
    print("spans in hw:", pg.evaluate(
        "() => [...document.querySelectorAll('#results > article.entry .hw')]"
        ".map(e => e.querySelectorAll('span.w-mod, span.w-unv, span.w-raw').length)"))
    b.close()
