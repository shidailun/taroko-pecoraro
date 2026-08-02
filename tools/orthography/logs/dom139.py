# -*- coding: utf-8 -*-
"""Batch 139: the register, asked the way it should have been asked, and its floor.

Batch 138's gate accepted a respelling when exactly one registered name was ONE
LETTER away. That is the wrong shape for a correspondence set: TAILONG needed
ai>ay AND o>u together and had to be done by hand. Composing the documented
correspondences instead, and asking over the value each token actually PUTS ON
SCREEN rather than over his raw token, reaches four more values. Two are taken:

  SERING `name (m)` -> Siring 男名, by the e>i that produced IXENG > ihing.
  YAGEX  `name (m)` -> Yagix 男女共名 — the `upix` failure again. His form
         already has the x; tier N ran x>h over it and printed `yageh`, which
         put it one letter from Yagih 女名 and got it refused in batch 138 for
         a type clash that was the tier's doing. Undo the x>h and his own
         spelling is one e>i from a name a man may bear.

Two are refused, and they are why the type-agreement clause is load-bearing:
`mixeng` is his `name (f)` and Mihing is 男名; `xane` and `lübaq` carry no tag
of his at all — tier N flagged them off capitalisation — so there is no type to
agree with, and `XANE` turns out not to be a name at all but a token in the
example `ASO NA SAO'LE XANE` under his entry for the possessive prefix N.
`hane` > `hani` would have renamed a grammatical particle after a man.

The floor is the other half. The register was asked for 氏族名 (NameType 3) and
屋名 (4) directly, every initial: **zero rows for 太魯閣族**. That is not a hole
in the register — **Truku naming is 親子連名**, a person's own name followed by
their father's, and clan and house names are other peoples' institutions (屋名
Paiwan and Rukai, 氏族名 Tsou and Saisiyat). The 1,792 harvested names are
男名/女名/男女共名 because that is all there is to have.

What is left is honestly out of reach at this bar: **58 values / 189 occurrences he himself
declares** `name (m)`/`name (f)`, plus 23 `name (.., jp)` values / 43 occurrences
that are a question about Japanese — none of them in the register under any
documented variant. liwis 38, akit 10, atwi 8, apwi 4, tiing 2, sipwi 2.
`pirin`>`piring` and `arin`>`aring` are refused again for the reason batch 138
gave: the register writes final -n freely (-in 46 / -ing 112), a 30/70 split,
not a correspondence.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

FIX = {"siring": 1, "yagix": 1}   # dark now
WAS = ["sering", "yageh"]         # and his old spellings gone from the page
# the refusals — the composed rules reach these and the type test throws them
# out, so they are the first thing to fall if that clause is ever dropped.
#
# SUPERSEDED BY BATCH 144, entirely. This batch's refusals were refusals to
# RESPELL a name from the register — the type test asks whether a 男名 may be
# respelled onto a 女名 — and every one of them stands: not one of these nine
# was renamed. What batch 144 changed is a different question, whether a name
# needs a register entry at all to shed the pale wash, and the answer is no,
# because a Japanese loan or a place name can never have one. So they are dark
# now with HIS OWN spelling, which is what the refusal protected. Kept and
# inverted rather than deleted, so a revert of 144 shows up here.
KEEP = {}
SUPERSEDED_144 = {"miheng": 1, "hane": 1, "lubaq": 3,
                  "pirin": 3, "arin": 2, "apin": 1, "liwis": 38, "akit": 10,
                  "atwi": 8}

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
    sup = pg.evaluate(SPANS, sorted(SUPERSEDED_144))
    b.close()

check(fix, FIX, "dark", "FIX")
check(sup, SUPERSEDED_144, "dark", "SUPERSEDED_144")
for w in WAS:
    if was.get(w):
        fail.append("WAS %s: his old spelling still on the page as %s" % (w, was[w]))

tot = sum(tally.values())
print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], 100.0 * tally["dark"] / tot))
print("FIX %d dark, %d old spelling gone   SUPERSEDED_144 %d dark, %d occ"
      % (len(FIX), len(WAS), len(SUPERSEDED_144), sum(SUPERSEDED_144.values())))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
