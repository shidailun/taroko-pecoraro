# -*- coding: utf-8 -*-
"""[batch 233] Intersect the DOM's non-dark tag spans with batch 223's tag
shapes. Verdict rows only."""
import sys, io, json, re, importlib.util, collections
sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location("d", "tools/orthography/logs/dom232.py")
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
MM = M.modern_map()
src = io.open("site/entries.js", encoding="utf-8").read()
E = json.loads(src[src.index("["):src.rindex("]")+1])
ROOT = re.compile(r"(^|[\s(=-])R\.?(?=$|[\s)?=.-])")
UPPER = re.compile(r"[A-ZÇÖÀ-Ý'\"’]{3,}")
def key(w): return re.sub("[’ʼ\"ʔ]", "'", w.lower()).replace("ł", "l")
def modern(w): return MM.get(key(w)) or M.char_rules(key(w))
shape = {}
for e in E:
    tag = e.get("tag") or ""
    if not tag or not ROOT.search(tag): continue
    for seg in re.findall(r"\(([^()]*)\)", tag):
        for t in UPPER.findall(seg):
            if t in ("R", "VR") or key(t) == key(e.get("hw") or ""): continue
            shape.setdefault(modern(t), set()).add(
                "root" if ROOT.search(seg) else "variant")
from playwright.sync_api import sync_playwright
JS = """() => { const o=[];
  for (const a of document.querySelectorAll('#results > article.entry')) {
    const hw=((a.querySelector('.hw')||{}).textContent||'').trim();
    for (const g of a.querySelectorAll('.tag'))
      for (const s of g.querySelectorAll('span.w-unv, span.w-raw'))
        o.push([hw, g.textContent.trim(), s.textContent, s.className.trim()]);
  } return o; }"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.goto(M.URL)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(M.URL + "?q=%CC%81"); pg.wait_for_timeout(22000)
    rows = pg.evaluate(JS); b.close()
c = collections.Counter()
for hw, tag, t, cl in sorted(set(map(tuple, rows))):
    sh = shape.get(t.lower(), set()) or {"?"}
    c["/".join(sorted(sh))] += 1
    print("%-10s %-11s %-6s %-9s %s" % (hw, t, "pale" if "w-unv" in cl else "green",
                                        "/".join(sorted(sh)), tag[:30]))
print("shapes:", dict(c), "| rows:", len(set(map(tuple, rows))))
