# -*- coding: utf-8 -*-
import sys, importlib.util
sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location("dom232", "tools/orthography/logs/dom232.py")
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
from playwright.sync_api import sync_playwright
WANT = ["L'QBU", "PG'DGIT", "SILAP", "XQ'LAO", "X'NU", "PSAANAQ"]
JS = """(WANT) => {
  const out = [];
  for (const art of document.querySelectorAll('#results > article.entry')) {
    const hw = ((art.querySelector('.hw')||{}).textContent||'').trim();
    for (const tag of art.querySelectorAll('.tag')) {
      const raw = tag.getAttribute('data-orig') || '';
      const txt = tag.textContent.trim();
      const sp = [...tag.querySelectorAll('span.w-mod, span.w-unv, span.w-raw')]
        .map(s => [s.textContent, s.className.trim(), !!s.closest('.truku')]);
      out.push([hw, txt, sp]);
    }
  }
  return out;
}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(M.URL)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(M.URL + "?q=%CC%81"); pg.wait_for_timeout(22000)
    rows = pg.evaluate(JS, WANT); b.close()
HW = {"RQBUX", "PGDGIT", "SLAP", "HKRAW", "HNU", "PSEANAK", "SIRAP"}
for hw, txt, sp in rows:
    if hw in HW:
        print("%-9s %-30s %s" % (hw, txt[:30], sp))
