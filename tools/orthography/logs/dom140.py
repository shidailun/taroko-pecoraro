# -*- coding: utf-8 -*-
"""Batch 140: if the name is close, use it.

Batches 138 and 139 required the edit to be a correspondence this book already
documents. That is the wrong bar for a name. A correspondence table is built
from words, and a name is exactly the thing that does not have to obey one — it
can be his ear, his typewriter, or the man's own family's spelling. Refusing
`qapi` because e>a is not in the table left a woman unnamed to protect a rule
that was never about her.

So the rule loosens to what actually identifies a name:

  * he declares it a name himself (`name (m)` / `name (f)`), and
  * exactly ONE registered name of an AGREEING TYPE is one edit away from the
    spelling his token puts on screen — his `name (m)` against 男名 or 男女共名,
    his `name (f)` against 女名 or 男女共名.

Nine more names, and the type test is what makes it safe rather than reckless:

  boin   -> buhin  男名     dado   -> kadu   男女共名   koxong -> kunung 女名
  pixeng -> pihang 男名     qepi   -> qapi   女名       syobao -> subaw  男名
  tibi   -> sibi   男名     unaq   -> unaw   男名       xatsö  -> hatu   男女共名

**Why the tag requirement, and not just closeness.** A token tier N flagged off
capitalisation has no type to agree with, and `xane` is why that matters: it is
one edit from `Hani` 男名 and it is not a name at all, it is a word in his
example `ASO NA SAO'LE XANE` under the entry for the possessive prefix N. Every
untagged token stays refused, `lübaq` and `hane` included.

**Where "close" does not identify anyone.** `akit` has six agreeing names one
edit away, `sidi` six, `uding` six. `ingay` — 24 occurrences, the heaviest name
in the book — has three, `engay`, `ungay` and `wingay`, and every one of them is
女名 against his `name (m)`. Nothing is chosen from a list; his spelling stands.

**The -Cwi set is left alone deliberately.** ATWI, APWI, SIDWI and SIPWI are four
of his names sharing a shape the register does not have, which reads as a
spelling convention of his rather than four separate slips — and SIDWI and SIPWI
would both land on `Siwi`, collapsing two names his book keeps apart. `atwi` has
a unique agreeing match (`amwi`, 8 occurrences) and is still refused on that
ground. One name is worth having; a distinction is worth keeping.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

FIX = {"buhin": 1, "kadu": 1, "kunung": 1, "pihang": 1, "qapi": 2,
       "subaw": 1, "sibi": 1, "unaw": 2, "hatu": 1}
# `qapi` and `unaw` are 2 because each value was already on the page: he writes
# QAPI himself (identity tier) beside QEPI, and UNAO sits on `unaw` through
# tier R beside UNAQ. Two of his spellings landing on one registered name is
# the register saying they were always the same name — the opposite of the
# SIDWI/SIPWI collapse, where nothing outside the guess says so.
WAS = ["buin", "dadu", "kuhung", "piheng", "qepi", "syubaw", "tibi", "unaq",
       "hatsu"]
# refused, and each for a different reason the docstring gives
KEEP = {"hane": 1, "lubaq": 3,          # no tag of his — tier N off capitals
        "miheng": 1,                    # his name (f), Mihing is 男名
        "ingay": 24, "akit": 10,        # no agreeing name / six of them
        "atwi": 8, "apwi": 4, "sidwi": 1, "sipwi": 2}   # the -Cwi set

SPANS = """(ws) => { const r = {};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const t = n.textContent.trim().toLowerCase();
    if (ws.indexOf(t) < 0) continue;
    const s = n.className.indexOf('w-mod') >= 0 ? 'dark'
            : n.className.indexOf('w-unv') >= 0 ? 'pale' : 'green';
    (r[t] = r[t] || {})[s] = (r[t][s] || 0) + 1;
  } return r; }"""

fail = []


def check(got, want, colour, label):
    for w, n in sorted(want.items()):
        seen = got.get(w) or {}
        if seen.get(colour, 0) != n or len(seen) != 1:
            fail.append("%s %s: want %d %s, got %s" % (label, w, n, colour, seen))


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    ctx.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL)
    pg.wait_for_timeout(6000)
    cards = pg.locator("article.entry").count()
    tally = pg.evaluate("""() => { const r = {dark: 0, pale: 0, green: 0};
      for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw'))
        r[n.className.indexOf('w-mod') >= 0 ? 'dark'
          : n.className.indexOf('w-unv') >= 0 ? 'pale' : 'green'] += 1;
      return r; }""")
    fix = pg.evaluate(SPANS, sorted(FIX))
    was = pg.evaluate(SPANS, sorted(WAS))
    keep = pg.evaluate(SPANS, sorted(KEEP))
    b.close()

check(fix, FIX, "dark", "FIX")
check(keep, KEEP, "pale", "KEEP")
for w in WAS:
    if w in FIX:
        continue        # `qepi` and `tibi` are his token AND were his value
    if was.get(w):
        fail.append("WAS %s: his old spelling still on the page as %s" % (w, was[w]))

tot = sum(tally.values())
print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], 100.0 * tally["dark"] / tot))
print("FIX %d names dark (%d occ)   KEEP %d refusals still pale (%d occ)"
      % (len(FIX), sum(FIX.values()), len(KEEP), sum(KEEP.values())))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
