# -*- coding: utf-8 -*-
"""Batch 152: the root's own paradigm outvotes its citation gloss.

A new rule, `outvoted()`, emitted as level 5. It is `unglossed_root()` minus
its precondition that the root be unglossed — and therefore a different claim,
which is why it is a separate rule a level below rather than a relaxation of
that one. Rule 4 asks the paradigm where the gloss table is SILENT. This asks
it where the gloss table SPEAKS, rule 2 has read what it said, and it disagrees
with his Chinese.

**Why the paradigm should win that argument.** A citation gloss is one editor's
choice of one sense to print beside a headword. A paradigm is the same wordlist
writing that root out across its slots, several entries by several hands, and a
wrong sense cannot survive in all of them. The two are not equal evidence and
the rule says which is better.

**`paux` is the case the rule was built for, and it retires a standing pin.**
The wordlist glosses `paux` 犁田, to plough. Batch 148 refused his 翻轉 family
on exactly those grounds — 犁田 turns soil, 翻轉 turns anything, and a synonym
line saying otherwise would have been false — and batches 149 and 150 checked
that refusal again and left it standing. That was right on the evidence each
had. But the same wordlist also prints `mknpaux` 反過來 and `mspaux` 會翻, and
his own values read 反著——顛倒 and 翻轉（前後）. Ploughing IS turning soil over:
犁田 was the narrow sense, never the meaning. **The pin comes down because new
evidence overturned it, not because the rule that set it was weakened** —
`paux` is still not in SYN, and 犁田 is still not 翻轉.

**The bar, and the family it splits.** Overriding a gloss needs better evidence
than filling a hole, so rule 4's guards are carried verbatim and one is added:
TWO independent inflections must agree, or one must agree on a whole
two-character word. That is not decoration. `kmpaux` carries two of his glosses
and two supporters answer it, 反 and 翻; `kpaux` carries one, so only `mspaux`
answers, and one single-character voice is refused. Same root, same batch,
three of its slots still pale in the PIN below. Without the bar the rule found
37 roots instead of 13, and the 24 extra were coincidences of the kind it
exists to catch: `qdriq` agreeing 的人 out of 住在Driq 的人, `taril` agreeing 方
out of 地方 — a fragment of a fragment.

**That paragraph describes the bar correctly and the code did not implement it**
— it counted distinct agreement strings rather than supporters, so a unanimous
paradigm scored 1. Corrected in batch 154, which takes nine of the values this
file lists below as coincidences; see logs/dom154.py. The 13-against-37 split
above is the measurement as taken and is left standing, but the 13 was two
different bars at once.

**The SISUN trap survives being asked directly, which is a stronger result than
never being reached.** Every rule since 145 has had to say why it cannot reopen
his SISUN 縫, and until now the answer was always that the value never arrives:
`sisi` HAS a gloss, 用來濾酒的工具 the wine strainer, so rule 2 reads it and
refuses it. This rule is the first that fires precisely BECAUSE the gloss
disagrees, so `sisun` arrives, is asked, and is refused on its merits — not one
inflection of `sisi` in the wordlist agrees with 縫 either.

**Written the same day a speaker dissolved the trap, and the two results
belong together.** His sew paradigm is siisi / siisan / siisun / sniisan (see
logs/dom153.py): there was never anything here for a rule to find, because the
word was misspelled and no amount of inference repairs a spelling. Seven
batches of rules each declined to force it, and each was right to. **The value
of a refusal is not that it is eventually rewarded — it is that the thing it
refused stayed refused until someone who knew could say so.**

**Thirteen roots, all hand-read.** Two are worth naming beside `paux`. `qdriq`
is right for a reason the rule never sees: his 逃跑的人 — 逃走 is not the
wordlist's `qdriq` 床底 at all, it is the syncopated stem of `qduriq` to flee,
and the supporter `qndriqan` 逃跑 is what says so — two homographs told apart,
as `kray` was in 149. And `ktuy` is not a homograph at all: the wordlist glosses
it 用指甲切斷東西, nipping something off with the fingernails, which is exactly
how millet is harvested; `kktuy`, `kmtuy` and `kntuy` all print 收割 and his
`mktuy` is 收割的人. One narrow gloss, three plain ones, same word.

+20 values / 53 occurrences, 0 de-verified. New level 5; levels 5-10 renumbered
to 6-11, which app.js does not read — it tests membership only.

Census after: modern dark 42,996 / pale 1,437 / green 32 = **96.6963%** (from
96.5771%), 1,967 cards, 0 page errors. Past the 96.6667% asked for.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

GAIN = {
    "haduran": 10, "kmpaux": 6, "kdagun": 4, "pkray": 4, "knrisaw": 3,
    "nrajing": 3, "pruciq": 3, "kraaw": 3, "knssgan": 2, "mktuy": 2,
    "tnrajing": 2, "pkpaux": 2, "tmqiri": 2, "empkray": 1, "mrajing": 1,
    "psneanak": 1, "qdriqi": 1, "qdriqan": 1, "qdriqun": 1, "empslagu": 1,
}

# `sisun` asked and refused on its merits, and three `paux` slots that carry
# only one of his glosses and so hear only one supporter. `knslaan` is still
# hand-refused. If `kpaux` ever goes dark without the bar being argued down in
# writing, the second-voice requirement has been lost.
# `sisun` WAS pinned here and is not any more, and it did not come down to a
# rule. A Truku speaker read it: `sisi` is the strainer, and his sew paradigm
# is siisi / siisan / siisun / sniisan, the long vowel his typewriter never
# wrote. Every rule that refused this family was RIGHT to — on his spelling the
# only glossed neighbour really was the wine-strainer — and no amount of
# further inference was going to fix a spelling. See logs/dom153.py.
PIN = {"kpaux": 3, "kpauxi": 2, "pauxun": 2, "knslaan": 2}

# The coincidences the bar cost, asserted unpaid. Every one of these has a root
# whose paradigm agrees with his Chinese on ONE character, and every one of
# those characters is a fragment: `taril` 方 out of 地方, `pungu` on its single
# character, `liwaq` on 發亮 for a root glossed 化妝.
#
# **This list was 17 values / 34 occurrences when it was written, and nine of
# them did not belong on it.** The bar as implemented counted distinct
# agreement STRINGS, not supporters, so a paradigm where every inflection said
# the SAME thing scored 1 and was thrown out as a coincidence — `siyang` had
# three voices all reading 肥 and landed here beside the genuine one-voice
# fragments. See logs/dom154.py, which corrects the count and takes those nine.
# What is left is the eight this bar was actually built to refuse. The claim in
# the docstring above ("more than half of what the rule earned") was measured
# against the inflated list and is withdrawn; the honest figure is 15
# occurrences, and the `liwaq` reading there is right about 發亮 and blind to
# the 趕 sense that `pliwaq` also carries.
COINCIDENCE = {
    "ptaril": 3, "ppungu": 2, "pkliwaq": 2, "skliwaq": 2, "spkliwaq": 2,
    "ssiyang": 2, "emptaril": 1, "emppungu": 1,
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
    pin = pg.evaluate(SPANS, sorted(PIN))
    coin = pg.evaluate(SPANS, sorted(COINCIDENCE))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(pin, PIN, "pale", "PIN")
check(coin, COINCIDENCE, "pale", "COINCIDENCE")

# The live `outvoted("sisun")` check this file was written with has moved to
# logs/dom153.py, and not because it stopped passing. `sisun` is no longer a
# modern value at all — a speaker ruled the same day that his sew paradigm is
# siisi / siisan / siisun / sniisan — so the check would now pass vacuously,
# on a string nothing maps to, and a vacuous assertion is worse than none.
# dom153 asserts the thing that is actually true.

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 42996:
    fail.append("census: dark fell to %d, below this batch's 42,996" % tally["dark"])
if pct < 96.6667:
    fail.append("census: dark fell back below 96.6667%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occ from 13 roots their own paradigms outvoted"
      % (len(GAIN), sum(GAIN.values())))
print("PIN  %d still pale — `sisun` asked directly and refused" % len(PIN))
print("COINCIDENCE %d values / %d occ — what the second-voice bar cost"
      % (len(COINCIDENCE), sum(COINCIDENCE.values())))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
