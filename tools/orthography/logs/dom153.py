# -*- coding: utf-8 -*-
"""Batch 153: SAIS. A speaker read it, and the trap was a spelling all along.

Eight batches of rules refused his SISUN 縫. Every one of them was right, and
every one of them was solving the wrong problem.

**What the rules saw.** His sew paradigm is printed on his own SAIS card:
`° Smais, sais, sisi, sisan, sisun.` The derived slots drop the `a`, so the
modern form he is reaching for looks like `sisi` — and `sisi` IS a modern Truku
word, listed and glossed 用來濾酒的工具（用黃藤編的濾酒袋）, the rattan bag you
strain millet wine through. A different word. So `regular()` read that gloss,
compared it with 縫, refused, and every rule built afterwards inherited the
refusal: batch 145 pinned it, 146 through 151 each re-checked it, and 152 was
the first rule that could ask the paradigm directly and got the same answer,
because no inflection of `sisi` means 縫 either.

**What a speaker saw in one line.** `sniisan` is the preterite locative focus
of *sew*. The modern language writes this paradigm with a LONG vowel where his
typewriter wrote one:

    his SISI    ->  siisi     imperative patient focus, -i
    his SISAN   ->  siisan    locative focus, -an
    his SISUN   ->  siisun    patient focus irrealis, -un
    his SNISAN  ->  sniisan   preterite locative focus, <n> ... -an

All four are in attested_modern.json; `siisi` and `siisan` also occur in the
ILRDF parquets. NONE of his four spellings is listed. And the bare root `siis`
is not listed either — which is the whole reason no rule could ever have got
there. Rules 2, 4, 5 and 6 all reach for a listed root and ask what it means;
this paradigm has no listed root to ask, and the only listed neighbour was the
wine-strainer.

**A spelling error cannot be inferred away, and the refusals were what kept it
findable.** Had any batch widened a rule far enough to swallow `sisun`, the
dictionary would have printed the word as `sisun` — a form modern Truku does
not have — and scored itself dark for it. It would have looked finished. The
pin is what kept the question open long enough to be asked of someone who knew.

**The metric understates it, and one entry shows why.** Fifteen occurrences of
the paradigm are dark, but only 13 of them are new, because `sisi` was ALREADY
dark: it is a listed modern word, so
rule 1 verified it at sight — as the wine-strainer. It was wrong and counted as
right. It is still dark now, as `siisi`, for the true reason. **Six occurrences
go the other way**: his causatives `psisi`, `psisan`, `psisun` now render
`psiisi`, `psiisan`, `psiisun`, which the wordlist does not list, so they turn
pale. That is the correct direction. An honest pale beats a false dark, and a
batch that only ever moves the number up is not measuring anything.

Ruled by a Truku speaker, 2026-08-02. Four hand entries in manual_map.json
under `_sais_paradigm`.

+13 occurrences net (26 values off the old spellings, 3 values / 6 occ onto
honest pale spellings). Census after: modern dark 43,009 / pale 1,424 /
green 32 = **96.7255%** (from 96.6963%), 1,967 cards, 0 page errors.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# The sew paradigm, in the spelling modern Truku actually writes.
GAIN = {"siisun": 5, "siisan": 5, "sniisan": 3, "siisi": 2}

# His causatives, honestly pale: the wordlist lists no p- form of this root, so
# the app must go on proposing rather than asserting them. If these ever go
# dark without a speaker or a listing behind them, the respelling has been
# allowed to carry verification with it, which it must never do.
PALE = {"psiisan": 3, "psiisun": 2, "psiisi": 1}

# And the wine-strainer is still the wine-strainer. `sisi` was the word the
# whole trap turned on; it must not survive anywhere as a sew form.
GONE = ["sisun", "sisan", "snisan"]

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
    pale = pg.evaluate(SPANS, sorted(PALE))
    gone = pg.evaluate(SPANS, sorted(GONE))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(pale, PALE, "pale", "PALE")
for w in GONE:
    if gone.get(w):
        fail.append("GONE %s: still rendered in modern mode, got %s" % (w, gone[w]))

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43009:
    fail.append("census: dark fell to %d, below this batch's 43,009" % tally["dark"])
if pct < 96.6667:
    fail.append("census: dark fell back below 96.6667%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occ dark — the sew paradigm as Truku writes it, "
      "13 of them newly so" % (len(GAIN), sum(GAIN.values())))
print("     (`siisi`'s 2 were dark already, as the wine-strainer)")
print("PALE %d values / %d occ — his causatives, honestly unlisted"
      % (len(PALE), sum(PALE.values())))
print("GONE %d of his spellings no longer rendered" % len(GONE))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
