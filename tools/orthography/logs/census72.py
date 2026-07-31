"""The canonical census, run the same way every time so the numbers compare.

Reads the RENDERED page in modern mode, not entries.js -- the two are different
instruments and only the DOM knows what the reader actually shows. Counts
case-folded and length>2, which is what every green figure quoted in this review
has meant: a one- or two-letter token and a capitalised headword are not
separate unknown words.

green  = w-raw  = UNVERIFIED (no curated table has a key for it)
brown  = w-mod  = a table decided it
grey   = French/abbreviation apparatus, greyed before respellable() ever runs
"""
import sys, collections, re
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.context.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=%CC%81", wait_until="networkidle")
    pg.wait_for_timeout(1200)
    got = pg.evaluate("""() => {
        const out = {mod:[], raw:[], prose:[]};
        for (const el of document.querySelectorAll('.w-mod')) out.mod.push(el.textContent);
        for (const el of document.querySelectorAll('.w-raw')) out.raw.push(el.textContent);
        for (const el of document.querySelectorAll('.prose,.meta-abbr')) out.prose.push(el.textContent);
        out.cards = document.querySelectorAll('article,.entry,.card').length;
        return out;
    }""")
    b.close()


def norm(ws):
    c = collections.Counter()
    for w in ws:
        w = (w or "").strip().lower()
        if len(w) > 2 and re.match(r"^[a-zà-ſ'’]+$", w):
            c[w] += 1
    return c


mod, raw = norm(got["mod"]), norm(got["raw"])
gt, go = len(raw), sum(raw.values())
bt, bo = len(mod), sum(mod.values())
print("GREEN  (unverified) %5d types  %6d occurrences" % (gt, go))
print("BROWN  (decided)    %5d types  %6d occurrences" % (bt, bo))
print()
print("modern-spelling rate  %.2f%% by type   %.2f%% by occurrence"
      % (100.0 * bt / (bt + gt), 100.0 * bo / (bo + go)))
print()
print("--- the green tail, by how often he uses it ---")
for w, n in raw.most_common(40):
    print("   %2dx %s" % (n, w))
