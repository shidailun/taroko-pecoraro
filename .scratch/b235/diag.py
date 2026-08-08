# -*- coding: utf-8 -*-
"""Why do 64 paired rows carry a different French gloss? Two readings: the pass
is misaligned, or the gloss itself renders differently in the two spellings
(`glossCites` colours Truku names inside a French gloss, so it must). Print the
first few and the per-card box counts, which are mode-independent if the pairing
is sound."""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.join(".scratch", "b235"))
URL = "http://127.0.0.1:8765/index.html"
JS = open(os.path.join(".scratch", "b235", "harvest.py"),
          encoding="utf-8").read()
JS = JS[JS.index('JS = r"""') + 9:JS.index('"""\n\nfrom playwright')]

from playwright.sync_api import sync_playwright  # noqa: E402

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto(URL)
    got = {}
    for mode in ("modern", "orig"):
        pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','%s')"
                    % mode)
        pg.goto(URL + "?q=%CC%81")
        pg.wait_for_timeout(22000)
        got[mode] = pg.evaluate(JS)
    b.close()

MOD, ORIG = got["modern"], got["orig"]
print("boxes: modern %d, orig %d" % (len(MOD), len(ORIG)))

# per-card counts: mode-independent if the two passes see the same book
cm, co = {}, {}
for r in MOD:
    cm[r["hw"]] = cm.get(r["hw"], 0) + 1
for r in ORIG:
    co[r["hw"]] = co.get(r["hw"], 0) + 1
print("distinct card labels: modern %d, orig %d | same multiset: %s"
      % (len(cm), len(co), sorted(cm.values()) == sorted(co.values())))

bad = [(m, o) for m, o in zip(MOD, ORIG) if m["fr"] != o["fr"]]
print("rows whose FR differs: %d" % len(bad))
for m, o in bad[:4]:
    print("---- i=%d  card %s / %s" % (m["i"], m["hw"], o["hw"]))
    print("  mod  :", m["text"][:70])
    print("  orig :", o["text"][:70])
    print("  fr M :", m["fr"][:70])
    print("  fr O :", o["fr"][:70])
