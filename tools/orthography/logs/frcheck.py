"""IS THE FRENCH BEING MANGLED ON SCREEN?

reconcile.py says the tag on KMALAO carries the French word "probablement", and
that charRules turns it into "prubabrement" (o>u, l>r). If that reaches the DOM,
modern mode is not merely mis-COLOURING French apparatus, it is REWRITING it --
the reader sees a corrupted French sentence, which is a different and much worse
class of defect than a green word.

Renders the live page in modern mode and greps the actual text for the mangled
forms, then reports the surrounding element so the scale is visible.
"""
import re, sys, io, collections
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

SUSPECT = ["prubabrement", "reduit", "cunnu", "furme", "muts", "ggar", "kaubu",
           "prus", "purter", "sans duute", "priuri", "sinun", "vurtex"]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.context.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=%CC%81", wait_until="networkidle")
    pg.wait_for_timeout(2500)
    body = pg.inner_text("body")

    # every element the app painted green, with its full parent text
    green = pg.eval_on_selector_all(
        ".w-raw",
        "els => els.map(e => [e.textContent, "
        "  (e.closest('.tag') ? 'tag' : e.closest('.paradigm') ? 'paradigm' : "
        "   e.closest('.crossref') ? 'crossref' : 'other'), "
        "  (e.parentElement ? e.parentElement.textContent.slice(0,110) : '')])")
    b.close()

print("=== mangled-French probe against the rendered page ===")
for s in SUSPECT:
    n = body.lower().count(s)
    print("%-16s %s" % (s, ("%d hit(s)" % n) if n else "-"))

print("\n=== every green token, grouped by where it lives ===")
byloc = collections.Counter(loc for _, loc, _ in green)
print(byloc.most_common())

print("\n=== greens inside tag / paradigm / crossref ===")
seen = set()
for txt, loc, parent in green:
    if loc == "other":
        continue
    k = (txt, loc)
    if k in seen:
        continue
    seen.add(k)
    print("%-14s [%-9s] %s" % (txt, loc, " ".join(parent.split())[:100]))
