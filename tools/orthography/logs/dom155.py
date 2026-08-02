# -*- coding: utf-8 -*-
"""Batch 155: QAPAH. The vowel that told the stick root from the work root.

`qapah` was on the speaker shortlist as a gloss disagreement, and I put the
question to the speaker the wrong way round — "his 不穩定 against the wordlist's
鋪開／黏附". That was backwards. **不穩定 is the WORDLIST's citation gloss**, and
his family is 黏附的 / 黏著的 / 黏貼－使黏附 / 使攤鋪. The wordlist backs him
outright two entries later: `msqapah` 粘起來, `sqapah` 黏住（在）. And it labels
its own headword gloss as the derived one — `sgqapah` 不穩定（引申「容易被動
搖」）, 引申, an extension. Something lightly stuck on is something that wobbles.

**The speaker's ruling was not about the gloss at all.** Told that qapah is
*stick*, that Tgdaya's `qmepah` is work-in-a-field, and therefore that **qapah
is not qpah — the two differ by a vowel** — the diagnosis falls out of the root
resolver in one line:

    psqpahan   ->  qpah / qpahan / qpahi      ... all 工作
    psqapahan  ->  psqapah / sqapah / qapah   ... the stick root

His typewriter syncopated the a, and the syncopated spelling is a real and
common Truku word meaning something else. All three of `psqpahan`, `psqpahi`,
`psqpahun` had to be hand-pinned in HAND_NOT_UNGLOSSED to stop the build
verifying his 黏貼 words off 工作. **The pin was treating a symptom, and it is
gone** — not weakened but unreachable, because manual_map now respells them and
nothing emits those strings. A pin on a string nothing emits is the vacuous
assertion logs/dom152.py refused to leave standing.

Respelled, they verify at **rank 2** — `regular()`, the strongest rung there is
— off `sqapah` 黏住（在）against his 黏貼－使黏附. Under his spelling the best
they could ever have reached was rank 4, unglossed listed root, off `qpah`:
the right shape of claim about the wrong word. This is the second spelling
error a speaker has dissolved, after the SAIS paradigm in batch 153.

**And it nearly shipped as its own opposite.** The first cut of this batch
dropped the three pins and added manual_map keys `psqpahan`/`psqpahi`/
`psqpahun` — the NORMALISED forms. manual_map runs before normalisation, so
those keys matched nothing and failed silently; the pins were gone and the
respelling was not there. All three went dark anyway, at rank 4, off 工作 —
**the exact error the batch exists to fix.** The census read +8 occurrences,
0 de-verified, 96.7997%, digit for digit what it reads now. A gain of the
right size is not a gain of the right kind, and nothing in the census could
tell them apart. What caught it was the GONE list below, which asserts that
his spellings no longer render at all — an assertion about the words, not
about the number. Keys are on his raw tokens `psqpaxan`/`psqpaxe`/`psqpaxon`.

**One SYN line, and it is the weakest in the table.** 粘 and 黏 are one
morpheme in two hands, so the character tier could not see between his 黏附 and
`msqapah` 粘起來 at all. Every member is two characters, per SYN's own guard,
and they are interchangeable rather than associated — but this line is closer
to being a spelling than a synonym, and it is the only reason `mqapah` and
`tqapah` clear the two-supporter bar batch 154 corrected. It bought exactly
those five occurrences and nothing anywhere else in the dictionary: 0 values
lost, and the whole gain below is this one family.

**`pqapah` stays pale, and that is the result that makes the rest trustworthy.**
His 使攤鋪－使鋪墊, spreading and laying out, is the one sense of his that the
wordlist does NOT carry on this root — the spread family is a different word
entirely (`sapaw` 舖（舖床、舖葉等）, `sapat`, `smapaw`, `erasi` 用…舖在地上).
The speaker's ruling was *stick*, so the stick forms move and the spread form
does not.

+5 values / 8 occurrences, 0 de-verified. Census after: modern dark 43,042 /
pale 1,391 / green 32 = **96.7997%** (from 96.7817%), 1,967 cards, 0 page
errors.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# Two at rank 5 from the SYN line clearing batch 154's supporter bar, three at
# rank 2 from a respelling that put regular() on the right root.
GAIN = {
    "mqapah": 3, "tqapah": 2,
    "psqapahan": 1, "psqapahi": 1, "psqapahun": 1,
}

# His one spread-sense form. The wordlist has no 攤鋪 on this root — that is
# `sapaw`/`sapat`/`erasi`, a different word — and the speaker ruled *stick*.
# If this goes dark, the SYN line has been read as covering the whole entry
# rather than the sense a speaker actually vouched for.
PIN = {"pqapah": 1}

# His syncopated spellings, which resolve onto 工作. These must not render at
# all any more; if one comes back, the manual_map respelling has been lost and
# the HAND_NOT_UNGLOSSED pins that used to catch them are no longer there.
GONE = ["psqpahan", "psqpahi", "psqpahun"]

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
    gone = pg.evaluate(SPANS, sorted(GONE))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(pin, PIN, "pale", "PIN")
for w in GONE:
    if gone.get(w):
        fail.append("GONE %s: still rendered in modern mode, got %s" % (w, gone[w]))

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43042:
    fail.append("census: dark fell to %d, below this batch's 43,042" % tally["dark"])
if pct < 96.6667:
    fail.append("census: dark fell back below 96.6667%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occ — the stick root, told from the work root by a "
      "vowel" % (len(GAIN), sum(GAIN.values())))
print("PIN  %d — his spread sense, which the wordlist does not carry here"
      % len(PIN))
print("GONE %d syncopated spellings that resolved onto 工作" % len(GONE))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
