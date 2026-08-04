# -*- coding: utf-8 -*-
"""Census of the four spelling states, off the rendered page (batch 196).

The fourth state, `w-cls`, is ADDITIVE: a class-only span carries both `w-mod`
and `w-cls`, so every harness that counts dark by selecting `.w-mod` keeps
counting it. This script is the one that has to see the difference, so it asks
for the computed colour too — a class that renders in the same brown as `w-mod`
is a class that is not there, and the CSS is decided by specificity and order,
which no amount of reading the stylesheet settles as well as asking the page.

    python tools/orthography/logs/brown196.py      (needs the local server up)
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "http://127.0.0.1:8765/?q=%CC%81"

DOM = r"""() => {
  const st = {};
  const seen = {};
  let colMod = '', colCls = '', colUnv = '', colRaw = '';
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const c = n.className;
    const s = c.indexOf('w-cls') >= 0 ? 'class'
            : c.indexOf('w-mod') >= 0 ? 'dark'
            : c.indexOf('w-unv') >= 0 ? 'pale' : 'green';
    st[s] = (st[s] || 0) + 1;
    const t = (n.textContent || '').trim().toLowerCase();
    (seen[s] = seen[s] || {})[t] = 1;
    if (s === 'class' && !colCls) colCls = getComputedStyle(n).color;
    if (s === 'dark' && !colMod) colMod = getComputedStyle(n).color;
    if (s === 'pale' && !colUnv) colUnv = getComputedStyle(n).color;
    if (s === 'green' && !colRaw) colRaw = getComputedStyle(n).color;
  }
  const types = {};
  for (const k in seen) types[k] = Object.keys(seen[k]).length;
  return {occ: st, types: types,
          colours: {dark: colMod, class: colCls, pale: colUnv, green: colRaw}};
}"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context()
    ctx.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()
    pg.goto(URL)
    pg.wait_for_timeout(15000)
    r = pg.evaluate(DOM)
    br.close()

o, t, c = r["occ"], r["types"], r["colours"]
tot = sum(o.values())
print("occurrences  dark %d  class %d  pale %d  green %d  total %d"
      % (o.get("dark", 0), o.get("class", 0), o.get("pale", 0),
         o.get("green", 0), tot))
print("distinct     dark %d  class %d  pale %d  green %d"
      % (t.get("dark", 0), t.get("class", 0), t.get("pale", 0),
         t.get("green", 0)))
print("all dark (w-mod, both kinds): %d = %.4f%%"
      % (o.get("dark", 0) + o.get("class", 0),
         100.0 * (o.get("dark", 0) + o.get("class", 0)) / tot))
print("colours      dark %s | class %s | pale %s | green %s"
      % (c["dark"], c["class"], c["pale"], c["green"]))
print("DISTINCT COLOUR: %s" % ("yes" if c["class"] and c["class"] != c["dark"]
                               else "NO — the class is invisible"))
json.dump(r, io.open(os.path.join(HERE, "brown196.json"), "w",
                     encoding="utf-8", newline="\n"), ensure_ascii=False)
