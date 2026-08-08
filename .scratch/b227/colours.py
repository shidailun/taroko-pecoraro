# -*- coding: utf-8 -*-
"""Colour census, both scopes in one pass (batch 222). Summary line only."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  const cls = s => s.classList.contains('w-raw') ? 'green'
                 : s.classList.contains('w-unv') ? 'pale' : 'dark';
  const mk = () => ({dark:0, pale:0, green:0, cls:0,
                     T:{dark:new Set(), pale:new Set(), green:new Set()}});
  const book = mk(), tru = mk();
  let pairs = 0, okpairs = 0;
  document.querySelectorAll('#results > article.entry').forEach(c => {
    c.querySelectorAll('.truku').forEach(b => {
      const sp = [...b.querySelectorAll(SEL)];
      if (!sp.length) return;
      pairs++;
      if (sp.every(s => s.classList.contains('w-mod'))) okpairs++;
    });
    c.querySelectorAll(SEL).forEach(s => {
      const k = cls(s), t = (s.textContent||'').trim().toLowerCase();
      book[k]++; book.T[k].add(t);
      if (s.classList.contains('w-cls')) book.cls++;
      if (s.closest('.truku')) { tru[k]++; tru.T[k].add(t);
        if (s.classList.contains('w-cls')) tru.cls++; }
    });
  });
  const f = o => ({dark:o.dark, pale:o.pale, green:o.green, cls:o.cls,
                   tdark:o.T.dark.size, tpale:o.T.pale.size, tgreen:o.T.green.size});
  return {book:f(book), truku:f(tru), pairs:pairs, ok:okpairs}; }"""

with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page()
    pg.context.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=%CC%81", wait_until="networkidle")
    pg.wait_for_timeout(22000)
    d = pg.evaluate(JS); b.close()

for name in ("book", "truku"):
    o = d[name]
    n = o["dark"] + o["pale"] + o["green"]
    print("%-6s spans dark %d (%.3f%%)  pale %d  green %d  total %d "
          "| types dark %d pale %d green %d | class-brown %d"
          % (name, o["dark"], 100.0*o["dark"]/n, o["pale"], o["green"], n,
             o["tdark"], o["tpale"], o["tgreen"], o["cls"]))
print("pairs %d/%d = %.4f%%" % (d["ok"], d["pairs"], 100.0*d["ok"]/d["pairs"]))
