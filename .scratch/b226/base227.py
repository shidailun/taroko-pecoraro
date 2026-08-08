# -*- coding: utf-8 -*-
"""Batch 227 baseline: the DOM before anything is written."""
import io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  let tot = 0, ok = 0;
  const seen = {}, unv = {}, inTruku = {};
  document.querySelectorAll('#results > article.entry').forEach(c => {
    c.querySelectorAll('.truku').forEach(b => {
      const sp = [...b.querySelectorAll(SEL)];
      if (!sp.length) return;
      tot++;
      if (sp.every(s => s.classList.contains('w-mod'))) ok++;
    });
    c.querySelectorAll(SEL).forEach(s => {
      const t = (s.textContent || '').trim().toLowerCase();
      seen[t] = (seen[t] || 0) + 1;
      if (s.classList.contains('w-unv')) unv[t] = (unv[t] || 0) + 1;
      if (s.closest('.truku')) inTruku[t] = (inTruku[t] || 0) + 1;
    });
  });
  return {tot: tot, ok: ok, seen: seen, unv: unv, inTruku: inTruku}; }"""
WATCH = ["smur", "smul", "samul", "snmul", "smamul", "pseanak", "psaanaq", "psaniq"]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto("http://127.0.0.1:8765/")
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=%CC%81")
    pg.wait_for_timeout(22000)
    d = pg.evaluate(JS)
    b.close()
tot, ok = d["tot"], d["ok"]
unv, seen, itk = d["unv"], d["seen"], d["inTruku"]
print("pairs %d/%d = %.4f%%" % (ok, tot, 100.0 * ok / tot))
print("pale span types %d   pale spans %d   span types %d"
      % (len(unv), sum(unv.values()), len(seen)))
for w in WATCH:
    print("   %-9s seen=%-3d pale=%-3d inTruku=%-3d" %
          (w, seen.get(w, 0), unv.get(w, 0), itk.get(w, 0)))
json.dump(d, io.open(".scratch/b226/base.json", "w", encoding="utf-8"))
