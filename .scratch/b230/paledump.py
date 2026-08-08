# -*- coding: utf-8 -*-
"""One DOM pass: every pale span type, with the card it sits on and that card's
Chinese. Written to .scratch/b230/pale.json for the offline meaning sweep."""
import io
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = "http://127.0.0.1:8765/"

JS = r"""() => {
  const out = {};
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const hw = (c.querySelector('.hw') ? c.querySelector('.hw').textContent : '').trim();
    const zh = [...c.querySelectorAll('.gloss-zh, .zh')].map(n => n.textContent).join(' ');
    c.querySelectorAll('span.w-unv').forEach(s => {
      const t = (s.textContent || '').trim().toLowerCase();
      if (!out[t]) out[t] = {n: 0, hw: hw, zh: zh.slice(0, 120)};
      out[t].n++;
    });
  });
  return out; }"""

from playwright.sync_api import sync_playwright        # noqa: E402

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(BASE)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(BASE + "?q=%CC%81")
    pg.wait_for_timeout(22000)
    d = pg.evaluate(JS)
    b.close()

json.dump(d, io.open(".scratch/b230/pale.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=0)
print("pale types %d  spans %d" % (len(d), sum(v["n"] for v in d.values())))
