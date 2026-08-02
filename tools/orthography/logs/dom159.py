# -*- coding: utf-8 -*-
"""Batch 159: SA'SO is SEESU, and the informant answers NTA.

**Two claims, and they are different KINDS of claim.** That is the point of
this batch and the reason they are logged together rather than apart.

**1. SA'SO → SEESU, on the paradigm.** His entry is

    SA'SO (S'so ?) (R)   沉靜－羞怯－羞恥心
      Sa'so bi !         真丟臉！/ 呸！
      Msa'so (Ms'so)     羞怯的－沉靜的－有禮的－知羞的
      Knsa'so            純真、羞怯、禮貌的強烈程度－謙遜
      Psa'so (pgsa'so ?) 使平靜－使不那麼放肆

and the modern wordlist holds that paradigm, slot for slot, under `seesu`:
`mseesu` 安靜, `mgseesu` 默默的;文靜, `mnegseesu` 文靜的, `ttgseesu` 溫柔；謙和,
`tgseesuay` 使慎重, plus bare `knseesu`, `gseesu`, `tgseesu`. His 沉靜 and their
安靜/文靜 share 靜; his 謙遜 and their 謙和 share 謙. Even the exclamation slot
survives — his `Sa'so bi !` against their `kmseesu` 好壞哦！

**Bare `seesu` is glossed 看輕人, and it loses to its own paradigm.** This is the
third time: batch 154 took `siyang` where the wordlist says 肉 and the paradigm
says 肥, and batch 157 took `liwaq` where the wordlist says 化妝 and the glossary
says 銀 for a root that means shine. A root's one-line gloss is one editor
choosing one noun; five inflections agreeing is the root. `pseesu` verifies at
level 5 — **the outvoted rung, fired by the machinery, not by hand** — which is
the build saying the same thing in its own words.

Four keys go in, on his RAW tokens [batch 155]: `sa'so`→seesu (which replaces a
standing IDENTITY entry — it had been left alone for want of a modern twin),
`msa'so`/`ms'so`→mseesu, `knsa'so`→knseesu. **`psa'so` and `pgsa'so` were
written off in advance as unlisted, and they went dark anyway** — the root
projection propagated the respelling for free once the root moved, and the
ordinary derived rungs then reached them at 5 and 4. The listed-twin gate is a
gate on RESPELLINGS; it was never the only road to dark, and predicting
otherwise was my error, not the build's.

His own bracketed variant `S'so` reaches `ssu` by a rule already in place, not by
this batch. `Msa'so (Ms'so)` collapses to one span once both spell `Mseesu`,
which is why the page holds one span fewer than before at 44,463.

**2. NTA, spoken for.** 20 occurrences, the largest pale word on the page by a
factor of three, and the first entry in the new `HAND_SPOKEN` — a fifth kind of
evidence, and the only one in this build that is a person rather than a
document. It widens `seen` and never `lex`, like the parquets, the Bible and the
names.

**Batch 146 refused it on the grounds that Klokah lists it under 都達, so it is
Toda and not Truku. That is bad reasoning and it is retracted here.** Where a
corpus happened to record a form is not evidence about where the form is absent,
and it cannot outweigh a Truku dictionary that prints the word with a usage
note — 邀請前往（唯一使用的形式，與 LITA 並用）— and eight examples.

The corpus miss is real, was re-measured, and is recorded rather than explained
away: **0 hits in the 40,760-word wordlist, 0 in the 2,058 types of the Truku
Bible, 0 in 14,600 parquet types, 0 in 11,820 spoken types.** What that shows is
that no modern Truku TEXT we hold spells it — and his own note says why, because
`Nta da ! ... Kia ! Lita da !` is a hortative interjection, which is exactly what
a Bible and a wordlist have no slot for. Its frame is all dark and all attested:
`ita`/`ta` 我們, `nita` 我們的, `nnita` 咱們的, `lita` 一起. `nta` is the one
member no written source caught.

The shortlist was a list of questions no corpus can answer, put to a speaker one
by one. This is the first answer, and it is filed as an answer — printed on its
own line by build_verified.py so that no later reader can mistake it for a
wordlist hit.

+6 values / 36 occurrences, 0 de-verified. Census after: modern dark 43,112 /
pale 1,319 / green 32 = **96.9615%** (from 96.8784%), 1,967 cards, 0 page errors.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# The shame root. `pseesu` 5 and `pgseesu` 4 are the derived rungs reaching what
# the respelling gate had refused.
GAIN = {"seesu": 8, "mseesu": 2, "knseesu": 2, "pseesu": 2, "pgseesu": 2}

# The informant's word. If this ever falls back to pale, HAND_SPOKEN has been
# dropped or renamed, and the answer he gave has been lost.
SPOKEN = {"nta": 20}

# Its frame — every neighbour of `nta` that a written source does hold. These
# were dark before this batch and are asserted so that widening `seen` by one
# hand-ruled type cannot be confused with having moved them.
FRAME = {"nita": 22, "nnita": 4, "lita": 3, "ita": 37}

# His spellings must render nowhere [batch 155: a key that matches nothing is
# silent].
GONE = ["saso", "msaso", "msso", "knsaso", "psaso", "pgsaso"]

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
    spoken = pg.evaluate(SPANS, sorted(SPOKEN))
    frame = pg.evaluate(SPANS, sorted(FRAME))
    gone = pg.evaluate(SPANS, sorted(GONE))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(spoken, SPOKEN, "dark", "SPOKEN")
check(frame, FRAME, "dark", "FRAME")
for w in GONE:
    if gone.get(w):
        fail.append("GONE %s: his spelling still renders, %s" % (w, gone[w]))

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43112:
    fail.append("census: dark fell to %d, below this batch's 43,112" % tally["dark"])
if pct < 96.6667:
    fail.append("census: dark fell back below 96.6667%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN   %d values / %d occ — the 羞恥 root, on its paradigm not its gloss"
      % (len(GAIN), sum(GAIN.values())))
print("SPOKEN nta dark at %d — HAND_SPOKEN, the informant and not a corpus"
      % SPOKEN["nta"])
print("FRAME  %d values / %d occ — nta's written neighbours, unmoved"
      % (len(FRAME), sum(FRAME.values())))
print("GONE   %d of his spellings render nowhere" % len(GONE))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
