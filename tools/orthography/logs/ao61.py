"""Closing measurement for the -ao class: does the rendered page still write a
word-final vowel pair the orthography does not use?

Before this session: charRules turned his -ao into -au (the o>u rule), and 13
mapped keys kept -ao/-au/-o outright. Count every coloured span in modern mode by
its last two letters, split brown/green, and name every survivor.
"""
import sys, collections, io, re
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto("http://127.0.0.1:8765/")
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=%CC%81", wait_until="networkidle")
    n = pg.eval_on_selector_all(".card", "e=>e.length")
    spans = pg.eval_on_selector_all(
        ".w-mod, .w-raw",
        "es=>es.map(e=>[e.textContent, e.className])")
    b.close()

print("%d cards, %d coloured spans" % (n, len(spans)))
c = collections.Counter()
surv = collections.Counter()
for txt, cls in spans:
    t = re.sub(r"[^A-Za-z']", "", txt)
    if len(t) < 3:
        continue
    suf = t[-2:].lower()
    kind = "brown" if "w-mod" in cls else "GREEN"
    c[(suf, kind)] += 1
    if suf in ("ao", "au", "eo", "io", "oo", "uo") or t[-1:].lower() == "o":
        surv[(t.lower(), kind)] += 1

print("\n-- word-final vowel pairs, as rendered --")
for suf in ("aw", "ao", "au", "ay", "ai", "uy", "ui", "ow"):
    br, gr = c.get((suf, "brown"), 0), c.get((suf, "GREEN"), 0)
    print("   -%-3s brown %5d   green %5d" % (suf, br, gr))

print("\n-- every span still ending in a bare o, or in -ao/-au --")
for (t, kind), k in sorted(surv.items(), key=lambda x: -x[1]):
    print("   %-6s %-22s x%d" % (kind, t, k))
if not surv:
    print("   (none)")
