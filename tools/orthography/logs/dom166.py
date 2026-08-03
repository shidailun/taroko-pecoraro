# -*- coding: utf-8 -*-
"""Batch 166: he doubted his own root, wrote the doubt down, and was right.

**p. 284 is a card about making things and we printed roads on it.** His S"LU
and SM"LU cards both carry the tag `(R. = "LU ?)` and cross-reference "LU
(p. 386) 路－通道－道理（意義）－方法. We followed the pointer: S"LU -> `seelug`,
Sm"lu -> `smeelug`, Sn"lu -> `sneelug`, Snluwan -> `sneelugan`. Every one is a
road word, on a card glossed 計劃－預謀 and 決定.

The root is SALU 'to make, to repair'. Tgdaya salu = to make, smalu is the
actor focus, snluwan is the preterite locative focus. Ruled by a speaker,
2026-08-03. "LU itself is untouched and was never in question — elu in Tgdaya,
elug in modern Truku, and every form on that card stays as it is.

**Modern Truku had the whole paradigm in the wordlist the entire time**: `salu`
修理, `smalu` and `smmalu` 製作, `snalu` 用...做的, `psalu` 請…製造或修理,
`sluun` 要被製作, and `sluan` / `snluan` listed unglossed. `sluun` is the proof:
modern Truku writes the syncopated stem `slu-` in exactly the slot where he
wrote S"LU, so his `"` is the reduced vowel of *salu* and not a glottal standing
in for *elu*.

**The page had already been spelling it correctly everywhere else.** Before this
patch there were 5 `salu`, 13 `smalu`, 6 `snalu` and 3 `snluan` on the page,
rendered from raw tokens he typed without the `"`. Only the four tokens carrying
his reduced-vowel mark were misrouted, and they were misrouted because a rule
believed a pointer he had explicitly flagged. That is the whole bug: 13
occurrences on two cards, in a family the dictionary otherwise gets right.

**Two of the thirteen were counted as correct.** `seelug` and `smeelug` are
listed modern words, so rule 1 verified them at sight — the same shape as the
SISUN trap: a spelling error wearing a verification's clothes, scoring itself
dark. The metric cannot see this class of error at all. Only a reader can.

**And it settles the question dom165 left open.** Batch 165 refused two pointers
that sat inside a question mark (`tbowyak`, `empsibus`) on the argument that he
marks his own uncertainty scrupulously, but could not say whether `(R. = X ?)`
in a TAG meant he doubted the root or doubted his spelling of it. It means he
doubted the root, and here he was right to. The tag pattern is now evidence
AGAINST the pointer it contains, not a weaker version of evidence for it.

+5 occurrences net (13 respelled, 4 of them off honest pale onto listed forms,
2 off false darks). DOM 97.3910% -> 97.4022% (43,306 / 1,123 / 32).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# The make paradigm, in the spelling modern Truku writes and the speaker ruled.
GAIN = {"snluan": 7, "salu": 10, "smalu": 16, "snalu": 7}

# The road words that were standing on p. 284. None may render anywhere now:
# `seelug` and `smeelug` were DARK, verified at sight as listed modern words.
GONE = ["seelug", "smeelug", "sneelug", "sneelugan"]

# p. 386 is untouched. If a sweep of the (R. = X ?) tag ever takes these with
# it, the fix has been over-applied: he was right about this card.
PIN_ROAD = {"elug": 91}

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
    gain = pg.evaluate(SPANS, sorted(GAIN))
    gone = pg.evaluate(SPANS, sorted(GONE))
    road = pg.evaluate(SPANS, sorted(PIN_ROAD))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(road, PIN_ROAD, "dark", "ROAD")
for w in GONE:
    if gone.get(w):
        fail.append("GONE %s: still rendered, %s" % (w, gone[w]))

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43306:
    fail.append("census: dark fell to %d, below this batch's 43,306" % tally["dark"])
if pct < 97.402:
    fail.append("census: dark fell back below 97.4022%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occ in the make paradigm"
      % (len(GAIN), sum(GAIN.values())))
print("GONE %d road spellings no longer rendered anywhere" % len(GONE))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
