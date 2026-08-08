# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
JS = r"""() => {
  const out = [];
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const h = (c.querySelector('.hw') || {}).textContent || '';
    if (!/kbuyu|KUBWI|BUYO/i.test(c.textContent)) return;
    if (!/kbuyu|buyu/i.test(h)) return;
    const sp = [...c.querySelectorAll('span.w-mod, span.w-unv, span.w-raw')]
      .map(s => s.textContent.trim() + '[' + s.className + (s.closest('.truku') ? '|T' : '') + ']');
    out.push({hw: h.trim(), head: c.innerHTML.slice(0, 430), spans: sp});
  });
  return out; }"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto("http://127.0.0.1:8765/")
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=kbuyu")
    pg.wait_for_timeout(6000)
    d = pg.evaluate(JS); b.close()
for c in d:
    print("HW", c["hw"])
    print("  spans:", c["spans"])
    print("  html:", c["head"].replace("\n", " ")[:430])
    print()
