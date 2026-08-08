# -*- coding: utf-8 -*-
"""batch 235 — the MIRROR of batch 231: two words of his the register writes as
one.

Batch 231 found the join direction — his typewriter fusing a clitic to its host
(`isoka`, `kasayang`), where the map value has to be TWO words. The split
direction has no mention anywhere in the record: two ADJACENT tokens of his
whose values, concatenated, are a listed modern word, with at least one side
pale. If that is real, the pale side is not a spelling question at all.

Taken from the DOM, because that is the only place the whole chain is visible
(batch 219), and span order inside a `.truku` box is his word order. Prints
verdicts, not cards.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.abspath(".")
ORTH = os.path.join(H, "tools", "orthography")
URL = "http://127.0.0.1:8765/index.html"


def L(n):
    return json.load(io.open(os.path.join(ORTH, n), encoding="utf-8"))


ATT = set(L("attested_modern.json"))
G = [L("attested_gloss.json"), L("bible_gloss.json"), L("parquet_gloss.json")]


def gl(w):
    out = []
    for D in G:
        g = D.get(w) or []
        out += g if isinstance(g, list) else [g]
    return [str(x) for x in out]


from playwright.sync_api import sync_playwright  # noqa: E402

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto(URL)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(URL + "?q=%CC%81")
    pg.wait_for_timeout(22000)
    rows = pg.evaluate(r"""() => {
      const SEL = 'span.w-mod, span.w-unv, span.w-raw';
      const out = [];
      document.querySelectorAll('#results > article.entry').forEach(c => {
        const hw = ((c.querySelector('.hw')||{}).textContent||'').trim();
        c.querySelectorAll('.truku').forEach(box => {
          const sp = [...box.querySelectorAll(SEL)];
          if (sp.length < 2) return;
          out.push([hw, (box.textContent||'').trim().slice(0,90),
                    sp.map(s => [(s.textContent||'').trim().toLowerCase(),
                                 s.classList.contains('w-mod') ? 1 : 0])]);
        });
      });
      return out;
    }""")
    b.close()

print("boxes with >= 2 spans: %d" % len(rows))

hits = {}
pairs = 0
for hw, txt, sp in rows:
    for i in range(len(sp) - 1):
        (a, da), (bb, db) = sp[i], sp[i + 1]
        if " " in a or " " in bb or not a or not bb:
            continue
        if da and db:
            continue                      # both dark: nothing pale to buy
        j = re.sub(r"[^a-z']", "", a + bb)
        if len(j) < 4 or j not in ATT:
            continue
        pairs += 1
        k = (a, bb, j)
        hits.setdefault(k, [0, set()])
        hits[k][0] += 1
        hits[k][1].add(hw)

print("adjacent pale-side pairs whose join is LISTED: %d occurrences, %d types"
      % (pairs, len(hits)))
for (a, bb, j), (n, cards) in sorted(hits.items(), key=lambda x: -x[1][0]):
    print("  %-12s + %-12s = %-16s %2dx  %s | %s"
          % (a, bb, j, n, ",".join(sorted(cards))[:28],
             "; ".join(gl(j))[:46] or "(no gloss)"))
