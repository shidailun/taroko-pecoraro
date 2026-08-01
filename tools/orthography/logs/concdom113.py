# -*- coding: utf-8 -*-
"""Does the concordance render, fill on open, and point back correctly?

Anchored per CARD, not per page: `?q=KENSAT` returns several cards and the first
details block on the page belonged to a different entry, which made the first run
of this check report seventeen rows for an entry that has none.

Also counts the blocks over the whole dictionary (?q=%CC%81 renders all 1,967
cards) so the shipped index can be compared against the offline measurement.
"""
import re
import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")

CARDS = ["KA", "TAMA", "MOBOX", "KENSAT", "MISO", "XBUI", "GASUT"]

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    ctx.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))

    for q in CARDS:
        pg.goto("http://127.0.0.1:8765/?q=" + q)
        pg.wait_for_timeout(2200)
        # the card whose own headword is the query, in either spelling
        got = pg.evaluate("""(q) => {
          for (const a of document.querySelectorAll('article.entry')) {
            const hw = a.querySelector('.hw');
            if (!hw) continue;
            const d = a.querySelector(':scope > details.conc');
            if (hw.textContent.trim().toUpperCase().replace(/[^A-Z]/g,'')
                === q.replace(/[^A-Z]/g,''))
              return { hw: hw.textContent.trim(), has: !!d,
                       head: d ? d.querySelector('summary').textContent : '' };
          }
          return null;
        }""", q)
        if not got:
            print("%-8s card not found" % q)
            continue
        if not got["has"]:
            print("%-8s %-14s no block" % (q, got["hw"]))
            continue
        print("\n%-8s %s" % (q, got["head"].strip()))
        pg.evaluate("""(q) => {
          for (const a of document.querySelectorAll('article.entry')) {
            const hw = a.querySelector('.hw');
            const d = a.querySelector(':scope > details.conc');
            if (d && hw.textContent.trim().toUpperCase().replace(/[^A-Z]/g,'')
                === q.replace(/[^A-Z]/g,'')) { d.querySelector('summary').click(); return; }
          }
        }""", q)
        pg.wait_for_timeout(500)
        rows = pg.evaluate("""() => {
          const d = document.querySelector('details.conc[open]');
          return [...d.querySelectorAll('.conc-row')].map(r => [
            r.querySelector('.truku').textContent.trim(),
            r.querySelector('.conc-src') ? r.querySelector('.conc-src').textContent.trim() : '']);
        }""")
        print("         %d rows" % len(rows))
        for t, s in rows[:3]:
            print("         %-56s %s" % (t[:56], s))

    # one tap on the source pointer must land on that card
    pg.goto("http://127.0.0.1:8765/?q=TAMA")
    pg.wait_for_timeout(2200)
    pg.query_selector("details.conc summary").click()
    pg.wait_for_timeout(400)
    src = pg.query_selector(".conc-src")
    want = re.sub(r"^→\s*", "", src.inner_text().strip())
    src.click()
    pg.wait_for_timeout(1500)
    print("\none-tap source link: → %s  landed on %s"
          % (want, pg.query_selector("article.entry .hw").inner_text().strip()))

    # the whole book, to compare with the offline count
    pg.goto("http://127.0.0.1:8765/?q=%CC%81")
    pg.wait_for_timeout(9000)
    n = pg.evaluate("""() => {
      const d = [...document.querySelectorAll('article.entry > details.conc')];
      let rows = 0;
      for (const x of d) rows += +(x.querySelector('summary').textContent
        .match(/\\((\\d+)\\)/) || [0, 0])[1];
      return [document.querySelectorAll('article.entry').length, d.length, rows];
    }""")
    print("\nwhole dictionary: %d cards, %d with a concordance, %d rows" % tuple(n))
    print("page errors: %s" % (errs or "none"))
    b.close()
