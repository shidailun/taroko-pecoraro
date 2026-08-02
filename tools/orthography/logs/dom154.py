# -*- coding: utf-8 -*-
"""Batch 154: the bar counted agreement STRINGS, and unanimity scored one.

A correction, not a new rule. `outvoted()`'s evidence bar was written

    agree = {sh for _, sh in sup}
    if len(agree) < 2 and not strong:

— the number of distinct agreement *strings* — while logs/dom152.py describes
it in writing as "TWO independent inflections must agree" and its docstring says
"two independent supporters". Those are not the same test, and they come apart
in exactly the case where the evidence is strongest: **when every supporter
agrees on the SAME character, the set holds one item.**

`siyang` is the root that exposed it, and it was on the speaker shortlist as a
question no rule could settle. The wordlist glosses it 肉, meat; his `psiyang`
family is 使變肥－養肥, fattening a pig. Three inflections answer — `ksiyang` 肥,
`msiyang` 很肥;結實, `pksiyangay` 使肥大 — all on 肥, so `agree` was `{"肥"}`,
`len` 1, refused. Three voices saying one thing scored below two voices saying
two things. Counting supporters instead is one word of the diff, `len(sup)`.

**The coincidences the bar exists to catch are untouched, and that is the whole
argument for the change.** A coincidence is one supporter matching one fragment
— `taril` on the 方 of 地方, `pungu` on its one character — and one supporter is
one however you count it. All eight of those values are still pale below. What
moved is the class where a paradigm is UNANIMOUS, which the old test scored as
if it were the weakest evidence available rather than the strongest.

**Twelve roots, +25 occurrences, and two of them are the shortlist shrinking.**
`siyang` came off the list of roots needing a speaker; so did part of `liwaq`,
whose `pliwaq` carries two of his glosses — 使人去驅趕 and 使發亮 — and whose
`gnliwaq` 用…以趕走 and `lmiwaq` 趕走 answer the first of them, twice, against a
root the wordlist glosses 化妝/銀. dom152 named `liwaq` as a coincidence "on 發亮
for a root glossed 化妝", and that reading was right about the sense it looked
at; the 趕 sense is a different pair of supporters and a different claim. Its
`pkliwaq`, `skliwaq` and `spkliwaq` are still pale.

Also in: `qaya` 工具;財物 outvoted by `qmaya` 阻礙 and `smqaya` 妨礙 for his
使其成為障礙; `griq` 扭曲的話 by three inflections all reading 轉; `huriq`
剛出生的動物 by an entire 濕 paradigm (a newborn animal is a wet one, which is
how the gloss got there); `blai`, `qlqah`, `tatuk`.

**Two pinned by hand, in the new `HAND_NOT_OUTVOTED`.** `tnbusan` is the right
answer with a worthless argument — winnowing and 篩榖 sifting grain are the same
word, but the shared 去 is the one inside 過去, the past. `mhmadan` is the same
trap with a WRONG answer under it: 成為親戚, become a relative, agreeing with the
`hada` 熟 paradigm on the 成 of 成為. Neither 去 nor 成 goes into STOP for this;
both carry meaning, and they are worthless here only as the frame verb of a
gloss, which is the shape batch 142 measured for 人 and refused to drop.

+13 values / 25 occurrences, 0 de-verified. Census after: modern dark 43,034 /
pale 1,399 / green 32 = **96.7817%** (from 96.7255%), 1,967 cards, 0 page
errors.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# What unanimity buys once it is allowed to count.
GAIN = {
    "pliwaq": 4, "gmriq": 3, "psiyangun": 3, "psiyang": 2, "psiyangi": 2,
    "ptblai": 2, "mnqlqah": 2, "pkhuriq": 2, "psblai": 1, "empsiyang": 1,
    "psiyangan": 1, "empqaya": 1, "mttatuk": 1,
}

# dom152's COINCIDENCE list, minus the nine the corrected count admits. These
# eight are the bar still doing its job — one supporter, one fragment — and they
# are the load-bearing assertion in this file. If they ever go dark without the
# supporter requirement being argued down in writing, the correction has been
# read as a licence to widen rather than as a fix to a miscount.
COINCIDENCE = {
    "ptaril": 3, "ppungu": 2, "pkliwaq": 2, "skliwaq": 2, "spkliwaq": 2,
    "ssiyang": 2, "emptaril": 1, "emppungu": 1,
}

# The two hand pins. `tnbusan`'s answer is right and its argument is a particle;
# `mhmadan`'s answer is wrong. Both must stay pale.
PIN = {"tnbusan": 2, "mhmadan": 2}

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
    coin = pg.evaluate(SPANS, sorted(COINCIDENCE))
    pin = pg.evaluate(SPANS, sorted(PIN))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(coin, COINCIDENCE, "pale", "COINCIDENCE")
check(pin, PIN, "pale", "PIN")

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43034:
    fail.append("census: dark fell to %d, below this batch's 43,034" % tally["dark"])
if pct < 96.6667:
    fail.append("census: dark fell back below 96.6667%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occ — twelve roots their paradigms agree about "
      "unanimously" % (len(GAIN), sum(GAIN.values())))
print("COINCIDENCE %d values / %d occ still pale — one supporter is still one"
      % (len(COINCIDENCE), sum(COINCIDENCE.values())))
print("PIN  %d hand-refused: right answer, worthless argument / wrong answer"
      % len(PIN))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
