# -*- coding: utf-8 -*-
"""Batch 203: the six species, from the DOM. Verdict lines only."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
B = "http://127.0.0.1:8765/"
ok = fail = 0
def t(n, c, x=""):
    global ok, fail
    if c: ok += 1; print("PASS  %s" % n)
    else: fail += 1; print("FAIL  %s   %s" % (n, x))

WANT = [("TYAQONG","tyaqung"),("PISUX","pisuh"),("KDIYONG","kjiyung"),
        ("Q'MUX","qmux"),("DILAM","jiram"),("GAOGAN","gaugan"),("KLULU","klulu")]
with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context()
    ctx.add_init_script("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()
    for q, val in WANT:
        pg.goto(B + "?q=" + q.replace("'", "%27")); pg.wait_for_timeout(1800)
        r = pg.evaluate("""(v) => {
          const hs=[...document.querySelectorAll('#results > article .hw-line .hw')];
          const m=hs.map(h=>{const s=[...h.querySelectorAll('span')].filter(x=>x.className.match(/w-(mod|unv|raw|cls)/));
            return {txt:h.textContent.trim(), cls:s.map(x=>x.className).join('|'),
                    words:s.map(x=>x.textContent).join(' '),
                    dict:[...h.parentElement.querySelectorAll('.w-dict')].map(x=>x.textContent).join('')};});
          return m.filter(x=>x.words.toLowerCase().includes(v)); }""", val)
        t("%-8s -> %-8s dark-brown" % (q, val),
          bool(r) and all("w-cls" in x["cls"] and "w-mod" in x["cls"] for x in r),
          [x["cls"] for x in r] or "no card")
    # brackets
    # Each species has TWO cards -- his (R) root card and the thematic
    # animal/plant card -- so the bracket is owed once on each.
    for q, want, n in (("KDIYONG","(srcing)",2), ("KLULU","(tlulug)",2),
                       ("PISUX","",0), ("DILAM","",0)):
        pg.goto(B + "?q=" + q); pg.wait_for_timeout(1800)
        got = pg.evaluate("""() => [...document.querySelectorAll('#results > article .hw-line .w-dict')]
          .map(x=>x.textContent)""")
        t("%-8s bracket = %r x%d" % (q, want, n),
          got == [want] * n, got)
    # a bracket must NOT appear inside a running sentence
    pg.goto(B + "?q=KLULU"); pg.wait_for_timeout(1800)
    n = pg.evaluate("document.querySelectorAll('.example .truku .w-dict').length")
    t("no bracket inside klulu's example sentences", n == 0, n)
    # classic spelling shows neither
    ctx2 = br.new_context()
    ctx2.add_init_script("localStorage.setItem('taroko_pecoraro_spelling_v1','original')")
    pg2 = ctx2.new_page(); pg2.goto(B + "?q=KDIYONG"); pg2.wait_for_timeout(1800)
    t("classic mode: no bracket, his own spelling",
      pg2.evaluate("document.querySelectorAll('.w-dict').length") == 0
      and "kdiyong" in pg2.evaluate(
          "document.querySelector('#results .hw').textContent").lower(),
      pg2.evaluate("document.querySelector('#results .hw').textContent"))
    br.close()
print("\n%d pass, %d fail" % (ok, fail))
