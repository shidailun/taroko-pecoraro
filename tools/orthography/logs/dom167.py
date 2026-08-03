# -*- coding: utf-8 -*-
"""Batch 167: a root in -aw writes -ag- before a suffix. Nothing was misspelled.

**The worksheet's top row was a false question.** Sheet 1 ranked `dagi` first —
four pale words, ten occurrences, and the modern wordlist glosses `dagi` 要煮飯.
Cooking rice has nothing to do with his SPADAO card, so the sheet was about to
ask a speaker whether `pspdagi` is a cooking word. It is not, and no speaker
should have to be asked.

**He was right and the wordlist has the whole family.** His GIFT root is SPADAO,
and modern Truku prints `pspadaw` 慷慨（不計價的送人）, `pnpadaw` 送過的禮物,
`emppadaw` 將…作為禮物 and `pnspadaw`. The map already wrote his unsuffixed forms
onto them — 4 `pspadaw` and 4 `pnspadaw` were dark on the page before this batch.
Only the four SUFFIXED slots fell through, and `roots()`, finding nothing better,
reached inside `pspdagi` and pulled out the rice.

**The alternation is regular and it is his, not ours.** A root ending in `-aw`
takes `-ag-` when a suffix follows: the raw text carries 76 such pairs against 2
counterexamples. `pspdagun` IS the modern slot of `pspadaw`; there is no error to
correct, only a rung that was missing. Hence `awag()`, rung 10.

**Longest-first, or it lands on the wrong card.** The wordlist files `padaw` as
「是 spadaw 不可靠的人 的詞根（無意義詞）」— an entry its own derivatives refute.
Candidates are therefore walked longest-first, exactly as batch 165 settled for
`syncopated`, so the search stops at `pspadaw` and never at `padaw`. The rule
also refuses to fire without a gloss of his to agree with, refuses when the word
is already listed, and treats a `<n>` in the first two positions as the infix it
is rather than a letter of the stem.

**Three refusals are pinned below.** `pkagi` has no `-ag-` stem long enough,
`knsrhagan` and `pnslhagan` reach no `-aw` word the gloss agrees with. If a later
widening sweeps them up, the rule has stopped reading his Chinese.

+10 occurrences, all four values off honest pale onto listed modern words.
DOM 97.4022% -> 97.4247% (43,316 / 1,113 / 32).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# The four suffixed slots the rung fills, in the spelling -ag- implies.
GAIN = {"pspdagan": 3, "pspdagun": 3, "pnspdagan": 3, "pspdagi": 1}

# The unsuffixed halves of the same paradigm, dark before this batch. They are
# the reason the rung is safe: the map had already landed on the GIFT card.
PIN_GIFT = {"pspadaw": 4, "pnspadaw": 4}

# `awag()` looked at these and said no. A rule that fires here is guessing.
PIN_REFUSED = {"pkagi": 1, "knsrhagan": 2, "pnslhagan": 2}

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
    gift = pg.evaluate(SPANS, sorted(PIN_GIFT))
    refd = pg.evaluate(SPANS, sorted(PIN_REFUSED))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(gift, PIN_GIFT, "dark", "GIFT")
check(refd, PIN_REFUSED, "pale", "REFUSED")

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43316:
    fail.append("census: dark fell to %d, below this batch's 43,316" % tally["dark"])
if pct < 97.424:
    fail.append("census: dark fell back below 97.4247%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d slots / %d occ filled by the -aw ~ -ag- rung"
      % (len(GAIN), sum(GAIN.values())))
print("PIN  %d gift-card occ already dark; %d occ the rung refuses"
      % (sum(PIN_GIFT.values()), sum(PIN_REFUSED.values())))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
