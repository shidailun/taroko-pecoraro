# -*- coding: utf-8 -*-
"""Pre-ruling DOM state for batch 238: bsekan (his Bsqan) and tapak (his TAPAK).

Both are FURNITURE -- a sub-form-name parenthetical and a headword -- so batch
223 requires asserting `inTruku == 0` before ruling: neither can move the pair
metric, and a later batch must not read the flat number as a failed seam."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
URL = "http://127.0.0.1:8765/index.html"
WATCH = ["bsekan", "pskan", "tpskan", "bskanun", "pskanun",
         "tapak", "tapaq", "tmapaq", "mtapaq"]

from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page()
    pg.goto(URL)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(URL + "?q=%CC%81")
    pg.wait_for_timeout(22000)
    d = pg.evaluate(r"""(W) => {
      const SEL='span.w-mod, span.w-unv, span.w-raw';
      const out={}, where={};
      let tot=0, ok=0;
      document.querySelectorAll('#results > article.entry').forEach(c=>{
        const hw=(c.querySelector('.hw')||{}).textContent||'?';
        // pair metric: .truku boxes only
        c.querySelectorAll('.truku').forEach(box=>{
          const sp=[...box.querySelectorAll(SEL)];
          if(!sp.length) return; tot++;
          if(sp.every(s=>s.classList.contains('w-mod'))) ok++;
        });
        // census: book-wide, every span (batch 222)
        c.querySelectorAll(SEL).forEach(s=>{
          const t=(s.textContent||'').trim().toLowerCase();
          if(W.indexOf(t)<0) return;
          const cls=s.classList.contains('w-mod')?'dark':
                    (s.classList.contains('w-unv')?'pale':'green');
          const inT=!!s.closest('.truku');
          out[t]=out[t]||{dark:0,pale:0,green:0,inTruku:0};
          out[t][cls]++; if(inT) out[t].inTruku++;
          (where[t]=where[t]||[]).push(hw+':'+cls+(inT?':TRUKU':''));
        });
      });
      return {tot:tot, ok:ok, w:out, where:where};
    }""", WATCH)
    b.close()
print("PAIRS %d/%d  blocked %d" % (d["ok"], d["tot"], d["tot"] - d["ok"]))
for k in WATCH:
    v = d["w"].get(k)
    print("  %-9s %s   %s" % (k, v or "(no spans)",
                              (d["where"].get(k) or [])[:4]))
