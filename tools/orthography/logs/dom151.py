# -*- coding: utf-8 -*-
"""Batch 151: the third reading of SYN, and where it stopped paying.

Seven more synonym lines off the same bucket batch 150 worked, written the same
way — one line per refused pair, each named in a comment beside the pair that
produced it. `lutut` 宗族血統 against his 親屬, `tqnay` 跟隨；陪同 against his
作伴, `peutux` 使…錯亂 against his 欺騙, `ttama` 停住（在上方）against his 坐著,
`pskraya` 記號 against his 標示, `tjiyal` 捕捉;釣到 against his 抓住, `shaya`
就這樣 against his 那樣.

**This is the batch that says the table is nearly read out.** 148 took 432
refused pairs and wrote a table worth 100-odd occurrences; 150 took the same
bucket after the glosses were fixed and got 34; this one gets 30 from seven
lines, and what is left in the bucket no longer looks like synonymy at all. It
looks like the four failures batch 150's re-bucketing named — a root nobody
glossed, no root in the lexicon, no Chinese of his, or a root whose gloss is
simply a different sense of the word. The last of those is what batch 152 is.

+14 values / 30 occurrences, 0 de-verified, 4 relevelled. No new level.

Census after: modern dark 42,943 / pale 1,490 / green 32 = **96.5771%** (from
96.5096%), original 43,423 / 1,507 / 32 = 96.5771%, 1,967 cards, 0 page errors
in both modes.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

GAIN = {
    "ptuhuy": 4, "empskraya": 3, "mslutut": 3, "mttama": 3, "pneutuxan": 3,
    "stqnay": 3, "snhaya": 2, "tmtama": 2, "ttjiyal": 2, "peutuxan": 1,
    "peutuxi": 1, "peutuxun": 1, "pslutut": 1, "tttama": 1,
}

# Five of the seven this file was written with. `kmpaux` and `pkpaux` were the
# other two and went dark in batch 152, on evidence rather than on a weakened
# rule — see logs/dom152.py, which carries the whole argument. `kpaux`,
# `kpauxi` and `pauxun` did NOT go with them and are the sharper assertion:
# the same root, the same batch, refused for want of a second voice.
# `sisun` WAS pinned here and is not any more, and it did not come down to a
# rule. A Truku speaker read it: `sisi` is the strainer, and his sew paradigm
# is siisi / siisan / siisun / sniisan, the long vowel his typewriter never
# wrote. Every rule that refused this family was RIGHT to — on his spelling the
# only glossed neighbour really was the wine-strainer — and no amount of
# further inference was going to fix a spelling. See logs/dom153.py.
PIN = {"kpaux": 3, "kpauxi": 2, "pauxun": 2, "knslaan": 2}

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
if tally["dark"] < 42943:
    fail.append("census: dark fell to %d, below this batch's 42,943" % tally["dark"])
if pct < 96.0:
    fail.append("census: dark fell back below 96%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occ from SYN's third reading"
      % (len(GAIN), sum(GAIN.values())))
print("PIN  %d still pale — including three `paux` slots batch 152 left" % len(PIN))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
