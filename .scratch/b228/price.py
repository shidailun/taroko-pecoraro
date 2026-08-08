# -*- coding: utf-8 -*-
"""Price the reduplication seam from the DOM before opening it (batch 198).

Every pale span type on the page, bucketed:
  redup+base  doubled onset AND stripping it reaches a LISTED, GLOSSED word
  redup       doubled onset, no base reached
  other       not a reduplication at all
Reports pair cost per bucket. Summary lines only.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORTH = os.path.join(ROOT, "tools", "orthography")
L = lambda n: json.load(io.open(os.path.join(ORTH, n), encoding="utf-8"))
AM, AG = set(L("attested_modern.json")), L("attested_gloss.json")

JS = r"""() => {
  const SEL='span.w-mod, span.w-unv, span.w-raw';
  const unv={}, sole={}, inT={};
  document.querySelectorAll('#results > article.entry').forEach(c=>{
    c.querySelectorAll(SEL).forEach(s=>{
      const t=(s.textContent||'').trim().toLowerCase();
      if (s.classList.contains('w-unv')) unv[t]=(unv[t]||0)+1;
      if (s.closest('.truku') && s.classList.contains('w-unv')) inT[t]=(inT[t]||0)+1;
    });
    c.querySelectorAll('.truku').forEach(b=>{
      const sp=[...b.querySelectorAll(SEL)];
      if(!sp.length) return;
      const bad=[...new Set(sp.filter(s=>!s.classList.contains('w-mod'))
                              .map(s=>(s.textContent||'').trim().toLowerCase()))];
      if (bad.length===1) sole[bad[0]]=(sole[bad[0]]||0)+1;
    });
  });
  return {unv:unv, sole:sole, inT:inT}; }"""

with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page()
    pg.context.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=%CC%81", wait_until="networkidle")
    pg.wait_for_timeout(22000)
    d = pg.evaluate(JS); b.close()

V = "aeiou"


def is_redup(w):
    return len(w) > 2 and w[0] not in V and w[1] == w[0]


def base(w):
    """Strip the doubled onset; return (word, gloss) if listed and glossed."""
    b = w[1:]
    g = AG.get(b) or []
    g = g if isinstance(g, list) else [g]
    return (b, "／".join(g)) if b in AM and g else (b, None)


unv, sole, inT = d["unv"], d["sole"], d["inT"]
buck = {"redup+base": [], "redup": [], "other": []}
for w in sorted(unv):
    if not is_redup(w):
        buck["other"].append(w); continue
    _, g = base(w)
    buck["redup+base" if g else "redup"].append(w)

print("pale types %d, pale spans %d, sole-blocked pairs %d"
      % (len(unv), sum(unv.values()), sum(sole.values())))
for k in ("redup+base", "redup", "other"):
    ws = buck[k]
    print("  %-11s %3d types  %3d spans  %2d sole pairs  %2d in .truku"
          % (k, len(ws), sum(unv[w] for w in ws), sum(sole.get(w, 0) for w in ws),
             sum(inT.get(w, 0) for w in ws)))

print("\nredup+base — the bucket a widening would reach:")
for w in sorted(buck["redup+base"], key=lambda x: -sole.get(x, 0)):
    b, g = base(w)
    print("  %-13s pale %d  sole %d  <- %-11s %s"
          % (w, unv[w], sole.get(w, 0), b, (g or "")[:44]))
