"""Confirm the one dom65 'failure' is the cascade it looks like.

Changing sdxalan>sdharan re-derived his psdxalan through a generative tier:
psdxalan > psdharan. dom65 asserts neighbours are UNCHANGED, so a legitimate
re-derivation trips it. Check in the live DOM that the SDAXAL card now prints
psdharan, and that its gloss is the leaning sense it should be.
"""
import io, sys, json, re
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

H = "C:/dev/formosan/seediq/taroko-pecoraro/"
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
for k in ("sdaxal", "sdxalan", "psdaxal", "psdxalan", "smdaxal", "daxal"):
    print("   %-11s -> %s" % (k, MAP.get(k, "(green)")))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto("http://127.0.0.1:8765/")
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=SDAXAL", wait_until="networkidle")
    txt = pg.inner_text("body")
    b.close()

seg = txt[txt.find("SDAXAL"):txt.find("SDAXAL") + 1400] if "SDAXAL" in txt else txt[:1200]
print("\n=== live SDAXAL card, modern mode ===")
print(seg[:1200])
for w in ("sdharan", "psdharan", "sdxalan", "psdxalan", "sdahar", "psdahar"):
    print("   %-11s present in DOM: %s" % (w, bool(re.search(w, txt, re.I))))
