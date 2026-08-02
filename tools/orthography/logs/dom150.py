# -*- coding: utf-8 -*-
"""Batch 150: SYN read a second time, after the wrong glosses were taken out.

Batch 148 wrote SYN off a first reading of the 432 refused pairs. Batch 149 then
gave every root a second gloss, which removed from that bucket the pairs that
were never a synonymy problem at all — `tama` was not 上帝 written another way,
it was the wrong sense of the word. What is left is the genuine article, and it
reads cleanly for it: twelve more lines, each named in a comment beside the pair
it came from.

**Order mattered, and it was the cheap way round.** Had these been written before
149, several would have been synsets papering over a wordlist error — 犁田 for
`paux`, 卵子 for `rusuq`, 人名（女）for `pajiq`. A table of synonyms is the place
where that mistake is invisible, because a bad line looks exactly like a good one
until someone re-reads the source. Fixing the glosses first meant the table never
had to carry them.

**The `tabuy` paradigm is what one line can be worth.** 下坡 下來 下去 下山
cleared `tbuyun`, `tbuyan`, `tbuyi`, `ptbuyun`, `ptbuyan`, `ptbuyi` and
`tmnabuy` — a whole syncopating paradigm off `tabuy` 下來 that was refused
because he writes its slots 下去－奔下 and 使下坡. Six of the seven come through
`syncopated()`, not `regular()`, so a synset earns its keep in rules far from the
one it was written for. It also reached `kmtucing` 我很想下去 off `mtucing`
掉下來, which no one predicted.

All 22 were read by hand. The rules of the table are unchanged and still
asserted at import: every member at least two characters, and a line groups what
is INTERCHANGEABLE and not what is associated. `paux` is still not in it — 犁田
and 翻轉 are still not the same word, and the Bible glossary declines to gloss
`paux` at all, so nothing has appeared to change that reading. `sisun` and
`knslaan` stay where they are for the same reason as ever.

+22 values / 34 occurrences, 0 de-verified, 3 relevelled. No new level.

Census after: modern dark 42,913 / pale 1,520 / green 32 = **96.5096%** (from
96.4331%), original 43,392 / 1,538 / 32 = 96.5082%, 1,967 cards, 0 page errors in
both modes.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

GAIN = {
    "tbuyun": 4, "pntabuy": 2, "pslguan": 2, "ptbuyun": 2, "smru": 2,
    "spcipiq": 2, "spsnhiyi": 2, "spsruwa": 2, "tbuyan": 2, "tduwai": 2,
    "kmtucing": 1, "lhlahan": 1, "pkdngdang": 1, "pkudaw": 1, "ptbuyan": 1,
    "ptbuyi": 1, "snlhkah": 1, "spusu": 1, "tbuyi": 1, "tduwaan": 1,
    "tduwaun": 1, "tmnabuy": 1,
}

# Unchanged from 148 and 149. Two batches of new synsets and a whole second
# gloss source have now passed over these seven without touching them: the
# glossary declines to gloss `sisi` and `paux`, and 犁田 is still not 翻轉.
# `kmpaux` and `pkpaux` WERE pinned here and are not any more. Batch 152 did
# not weaken the synonym rule that refused them — `paux` is still not in SYN
# and 犁田 is still not 翻轉 — it found new evidence: the wordlist's own
# `mknpaux` 反過來 and `mspaux` 會翻 say the root means turn over, whichever
# sense its headword gloss prints. A pin records a refusal on the evidence of
# its day; when better evidence arrives the pin comes down and says so, as
# dom147's `mskingal` did. The other five stay, and `kpaux` is why the bar is
# where it is: it carries only ONE of his glosses, so only `mspaux` answers
# for it, and one single-character voice is not enough.
PIN = {"kpaux": 3, "kpauxi": 2, "pauxun": 2, "sisun": 5, "knslaan": 2}

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
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(pin, PIN, "pale", "PIN")

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 42913:
    fail.append("census: dark fell to %d, below this batch's 42,913" % tally["dark"])
if pct < 96.0:
    fail.append("census: dark fell back below 96%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occ from SYN's second reading"
      % (len(GAIN), sum(GAIN.values())))
print("PIN  %d still pale — 犁田 is still not 翻轉" % len(PIN))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
