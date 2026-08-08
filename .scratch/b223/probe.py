# -*- coding: utf-8 -*-
import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
JS = r"""() => {
  const SEL='span.w-mod, span.w-unv, span.w-raw';
  let tot=0, ok=0; const card={};
  document.querySelectorAll('#results > article.entry').forEach(c=>{
    const hw=((c.querySelector('.hw')||{}).textContent||'').trim();
    c.querySelectorAll('.truku').forEach(b=>{
      const sp=[...b.querySelectorAll(SEL)];
      if(!sp.length) return;
      tot++; if(sp.every(s=>s.classList.contains('w-mod'))) ok++;
    });
    if(/PT"TO|^T"TO/.test(hw)){
      card[hw]=[...c.querySelectorAll(SEL)].map(s=>
        (s.textContent||'').trim()+':'+(s.classList.contains('w-unv')?'PALE':
          s.classList.contains('w-raw')?'green':'dark'));
    }
  });
  let pale=0; document.querySelectorAll('#results > article.entry span.w-unv')
    .forEach(()=>pale++);
  return {tot:tot, ok:ok, card:card, paleSpans:pale}; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto("http://127.0.0.1:8765/")
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=%CC%81")
    pg.wait_for_timeout(22000)
    r=pg.evaluate(JS); b.close()
print("PAIRS %d / %d = %.4f%%   pale spans book-wide %d"
      % (r["ok"], r["tot"], 100.0*r["ok"]/r["tot"], r["paleSpans"]))
for hw, sp in r["card"].items():
    print("  %s" % hw)
    print("     " + "  ".join(sp))
