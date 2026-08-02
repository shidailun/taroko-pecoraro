# -*- coding: utf-8 -*-
"""Batch 156: QDUG. A voice is not a spelling.

The speaker shortlist listed `qdug` as a gloss disagreement — his 告發 against
the wordlist's 欺騙 — and asked which one the word means. It is neither
question. **His gloss does not vary at all**: 告發－控告、指控 on `sqdugan`,
`sqdugi` and `sqdugun`, 使人被控告－叫人告發 on `psqdug`, 所提出的指控 on
`snqdugan`. Five slots, one reading, and 欺騙 appears nowhere in his family.

**The r is the sense.** Asked what the Truku Bible says, it splits the root
along a consonant:

    with r:  rmqdug 欺騙 / rnqdug 詭計；騙術 / rmnqdug 欺騙、引誘 /
             tmrqdug 誘餌、引誘、詐欺 / rqdug 很會欺騙 / prqdug 使欺騙
    plain :  smqdug 控告

Deceive, lure, bait — against accuse. His nine occurrences are all plain
s-forms, and `smqdug` 控告 is his own two characters. The wordlist's `smrqdug`
控告 was the single entry blurring the line, and the Bible glossary writes the
same word without the r.

**Why no rule could use that, and what the batch actually changes.** `smqdug`
resolves onto `sqdug` and `qdug` — his roots exactly — and `_gloss()` returns
控告 for it. It still could not be a supporter, because `derived()` swept
`self.lex`, and `smqdug` is a glossary headword that the wordlist does not
list. Batch 149 made the Bible glossary an additive gloss SOURCE and left its
headwords out of the population the paradigm rules read, so for seven batches a
word the build could READ was a word the build could not HEAR.

**`self.lex` licenses a spelling; `self.voices` supplies evidence, and those
are different jobs.** A word is in `lex` because the dictionary may PRINT it —
that is why the standing rule is that `seen` widens and `lex` never does, and
that rule is untouched here. Agreeing with a gloss is not a claim about how
anything is spelled. `voices` is `lex | bible_gloss`, it is read by `derived()`
and by nothing else, and the assertion at the bottom of this file checks that
mechanically rather than trusting the sentence.

**Twelve values, and the qdug family is only nine of them.** Two of the other
three are homographs the new voices break open, which is the `qdriq` shape from
batch 152:

    krwahan  his 吝惜的——執著的   root rwahi 打開   voice krwahi 顧惜；捨不得（給出）
    kdagi    his 多人合力扛抬     root dagi 要煮飯   voice pkdagan 使抬著（繞行）

In both the listed root is a different word — *open*, *cook rice* — and the
glossary's form is his gloss almost verbatim. `knsgan` 恐懼 gets `kksgun`
可畏；令人敬畏, and `preura` 清楚地 / `ptreurani` 去顯明 get `ptreura` 彰顯；顯明,
which is his 顯明 written out.

**`yus` is in on a spelling claim, not a meaning claim, and it should be read
that way.** His YUS is an interjection — 表示當下就要著手做某事的決定的感嘆詞，
常帶威脅意味 — and the paradigm that vouches it is `mayus` 劃界線, `yusay` 鑑界,
`pyusi` 劃成界線, drawing a boundary. Those are not the same word. Rank 3 claims
only that y-u-s is how modern Truku spells this string, which is true of both,
and the glossary's `ptyusi` 隔出房間；分隔 is what tipped an already-complete
paradigm over the threshold.

+12 values / 21 occurrences, 0 de-verified. Census after: modern dark 43,063 /
pale 1,370 / green 32 = **96.8470%** (from 96.7997%), 1,967 cards, 0 page
errors.
"""
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# All nine of his qdug occurrences, plus three homographs and two more the
# glossary's voices settle.
GAIN = {
    "knsgan": 4, "sqdugun": 3, "preura": 2, "ptreurani": 2, "snqdugan": 2,
    "psqdug": 2, "krwahan": 1, "kdagi": 1, "empkparu": 1, "yus": 1,
    "sqdugi": 1, "sqdugan": 1,
}

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


# The load-bearing structural claim: `voices` is evidence and nothing else.
# The docstring above says it is read by derived() alone; this checks it. If a
# second reader ever appears, the glossary has started doing a job that only
# `lex` is allowed to do, and the sentence that justified this batch is false.
SRC = io.open(os.path.join(os.path.dirname(__file__), os.pardir,
                           "inflection.py"), encoding="utf-8").read()
reads = len(re.findall(r"in self\.voices", SRC))
if reads != 1:
    fail.append("voices: %d readers, want exactly 1 (derived)" % reads)
if "self.voices = set(lex) | set(self.bgl)" not in SRC:
    fail.append("voices: definition changed shape")

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
    b.close()

check(gain, GAIN, "dark", "GAIN")

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43063:
    fail.append("census: dark fell to %d, below this batch's 43,063" % tally["dark"])
if pct < 96.6667:
    fail.append("census: dark fell back below 96.6667%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occ — nine of them his whole qdug family"
      % (len(GAIN), sum(GAIN.values())))
print("voices: %d reader (derived), as the docstring claims" % reads)
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
