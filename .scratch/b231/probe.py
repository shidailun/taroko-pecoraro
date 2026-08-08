# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding="utf-8")
JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  let tot=0, ok=0; const seen={}, unv={}, itk={}, sole={};
  document.querySelectorAll('#results > article.entry').forEach(c => {
    c.querySelectorAll('.truku').forEach(b => {
      const sp=[...b.querySelectorAll(SEL)]; if(!sp.length) return; tot++;
      if (sp.every(s=>s.classList.contains('w-mod'))) ok++;
      else { const bad=[...new Set(sp.filter(s=>!s.classList.contains('w-mod'))
              .map(s=>(s.textContent||'').trim().toLowerCase()))];
             if (bad.length===1) sole[bad[0]]=(sole[bad[0]]||0)+1; } });
    c.querySelectorAll(SEL).forEach(s => {
      const t=(s.textContent||'').trim().toLowerCase();
      seen[t]=(seen[t]||0)+1;
      if (s.classList.contains('w-unv')) unv[t]=(unv[t]||0)+1;
      if (s.closest('.truku')) itk[t]=(itk[t]||0)+1; }); });
  return {tot,ok,seen,unv,itk,sole}; }"""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto("http://127.0.0.1:8765/")
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=%CC%81"); pg.wait_for_timeout(22000)
    d=pg.evaluate(JS); b.close()
print("pairs %d/%d = %.4f%%"%(d["ok"],d["tot"],100.0*d["ok"]/d["tot"]))
print("pale types %d spans %d   sole-blocked pairs %d over %d types"%(
    len(d["unv"]),sum(d["unv"].values()),sum(d["sole"].values()),len(d["sole"])))
for w in ("isu ka","ka sayang","isu","ka","sayang","isuka","kasayang","yianu","urang","sruweq"):
    print("  %-10s seen=%-3s pale=%-3s truku=%-3s sole=%s"%(w,d["seen"].get(w),d["unv"].get(w),d["itk"].get(w),d["sole"].get(w)))
json.dump(d, open(".scratch/b231/dom.json","w",encoding="utf-8"))
