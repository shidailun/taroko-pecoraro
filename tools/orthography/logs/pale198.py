# -*- coding: utf-8 -*-
"""Pale ranked by OCCURRENCE, off the rendered page (batch 198).

blockers.py ranks by sentence pairs, so a word spent on headwords and crossrefs
never reaches it — that is how `treura`, the biggest pale word on the page, was
invisible for sixty batches. This asks the DOM instead, and prints the displayed
modern value, its occurrence count, and how many of those sit inside an example
line (the ones a pair-based metric can see) versus everywhere else.

    python tools/orthography/logs/pale198.py [N]     (needs the local server up)
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "http://127.0.0.1:8765/?q=%CC%81"
TOP = int(sys.argv[1]) if len(sys.argv) > 1 else 40

DOM = r"""() => {
  const out = {};
  for (const n of document.querySelectorAll('span.w-unv')) {
    const t = (n.textContent || '').trim().toLowerCase();
    if (!t) continue;
    const o = out[t] || (out[t] = {n: 0, ex: 0});
    o.n++;
    if (n.closest('.ex, .example, .ex-t, .sub-ex')) o.ex++;
  }
  return out;
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

rows = sorted(r.items(), key=lambda kv: (-kv[1]["n"], kv[0]))
print("pale types %d  occurrences %d"
      % (len(rows), sum(v["n"] for _, v in rows)))
head = sum(v["n"] for _, v in rows[:TOP])
print("top %d carry %d occurrences (%.0f%% of pale)"
      % (TOP, head, 100.0 * head / max(1, sum(v["n"] for _, v in rows))))
for w, v in rows[:TOP]:
    print("  %-16s %3d   ex %d" % (w, v["n"], v["ex"]))
json.dump(r, io.open(os.path.join(HERE, "pale198.json"), "w",
                     encoding="utf-8", newline="\n"), ensure_ascii=False)
