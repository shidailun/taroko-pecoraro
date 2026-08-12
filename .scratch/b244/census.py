# -*- coding: utf-8 -*-
"""b244 — what do his two `note` cards render, and what is the green class?

COLOPHON is the printer's imprint at the end of the book (Paris, 128 R. du Bac,
Octobre 1976 - Juin 1977). It has no map entry, so `charRules()` fires on it:
o->u, l->r gives CURUPHUN, a Truku word the dictionary invented out of a French
one. This measures the green class before and after, book-wide and `.truku`
-scoped (batch 222: ask each question in its own scope), and reports what the
two note cards themselves put on screen.
"""
import sys
from collections import Counter

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  const cls = s => s.classList.contains('w-raw') ? 'green'
                 : s.classList.contains('w-unv') ? 'pale' : 'dark';
  const book = [], truku = [], notes = [];
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const hwEl = c.querySelector('.hw');
    const hw = hwEl ? (hwEl.textContent || '').trim() : '';
    const tag = (c.querySelector('.tag') || {}).textContent || '';
    c.querySelectorAll(SEL).forEach(s => {
      const row = {t: (s.textContent || '').trim(), c: cls(s), hw: hw};
      book.push(row);
    });
    c.querySelectorAll('.truku').forEach(box => {
      box.querySelectorAll(SEL).forEach(s => {
        truku.push({t: (s.textContent || '').trim(), c: cls(s), hw: hw});
      });
    });
    if (/^\s*note\s*$/.test(tag.trim()))
      notes.push({hw: hw, tag: tag.trim(),
                  spans: c.querySelectorAll('.hw ' + SEL).length});
  });
  return {book: book, truku: truku, notes: notes,
          cards: document.querySelectorAll('#results > article.entry').length};
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto("http://127.0.0.1:8765/")
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=%CC%81")
    pg.wait_for_timeout(22000)
    d = pg.evaluate(JS)
    b.close()

for scope in ("book", "truku"):
    rows = d[scope]
    by = Counter(r["c"] for r in rows)
    print("%-6s spans %5d   dark %5d  pale %4d  green %3d   types: pale %3d green %3d"
          % (scope, len(rows), by["dark"], by["pale"], by["green"],
             len(set(r["t"].lower() for r in rows if r["c"] == "pale")),
             len(set(r["t"].lower() for r in rows if r["c"] == "green"))))

green = [r for r in d["book"] if r["c"] == "green"]
print("GREEN inventory (book-wide), %d spans:" % len(green))
for r in green:
    print("   %-12s on card %s" % (r["t"], r["hw"]))

print("note cards: %d" % len(d["notes"]))
for n in d["notes"]:
    print("   hw=%-12r spans-in-hw=%d" % (n["hw"], n["spans"]))
print("cards rendered: %d" % d["cards"])
