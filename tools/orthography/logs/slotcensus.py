# -*- coding: utf-8 -*-
"""Census the generated slot pages from the DOM: walk every letter of the A-Z
listing and count the rows that are slots rather than forms."""
import sys, re, collections
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

tot = collections.Counter()
rows = []
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context()
    ctx.add_init_script("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page(); pg.goto("http://127.0.0.1:8765/"); pg.wait_for_timeout(1500)
    pg.click("#btn-alpha"); pg.wait_for_timeout(400)
    letters = pg.evaluate("""() => Array.from(
        document.querySelectorAll('#sheet-content button, #sheet-content .alpha-key, #sheet-content a'))
        .map(e => e.textContent.trim()).filter(t => t.length <= 2)""")
    print("letters:", letters)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    for L in letters:
        pg.click("#btn-alpha"); pg.wait_for_timeout(300)
        pg.get_by_text(L, exact=True).last.click()
        pg.wait_for_timeout(900)
        d = pg.evaluate("""() => ({
          slots: Array.from(document.querySelectorAll('.entry.idx-slot')).map(
            e => [e.querySelector('.stub-hw').textContent.trim(),
                  e.querySelector('.stub-gloss').textContent.trim()]),
          all: document.querySelectorAll('article.entry.idx').length })""")
        tot["rows"] += d["all"]; tot["slots"] += len(d["slots"])
        rows += d["slots"]
        print("%-3s rows %4d  slots %3d" % (L, d["all"], len(d["slots"])))
    b.close()

print("\nTOTAL rows %d   slot pages %d" % (tot["rows"], tot["slots"]))
lab = collections.Counter()
for w, g in rows:
    m = re.match(r"([a-z ]+?) (?:focus|form) of", g)
    lab[m.group(1) if m else ("unlabelled" if g.startswith("form of") else g.split(" of ")[0])] += 1
for k, v in lab.most_common():
    print("   %-20s %d" % (k, v))
print("\nsample:", rows[:6])
