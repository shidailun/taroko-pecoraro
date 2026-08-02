# -*- coding: utf-8 -*-
"""Batch 142: 大 and 小 are meanings, and STOP had swallowed them.

STOP states its own test in its first line — "characters that carry no meaning
on their own, so sharing one is not agreement" — and then lists 大 and 小 among
the pronouns and particles. Big and small are meanings. They were swept in with
the function words and then silently refused the two adjectives a Formosan
wordlist glosses most often: `paru` IS 大的 and `bilaq` IS 小, so his 使自己變小者
could not agree with 小 and `msbilaq` stayed pale.

Measured alone: **+10 values, 0 de-verified, 0 relevelled**. Eight are his own
word for big or small and are what the character was always for —

    mkparu   長大——使自己變大        `paru` 大的
    msbilaq  自我謙抑者——使自己變小者  `bilaq` 小
    tbilaq   確實小——非常小          `bilaq` 小
    skparu   用以使…長大——用以發展    `paru` 大的
    psblaqan 使謙卑——使之變小        `sblaqa` 別小看
    psblaqi  使謙卑——使之變小
    knblaqan 渺小——微不足道          `bilaq` 小, syncopated
    empsparu (no gloss gate at its level)

— and two are coincidences, pinned in HAND_NOT_REGULAR:

    knslaan  his 饑餓虛脫－精疲力竭 against `sla` 大外衣, a large outer garment.
             Nothing in common but the 大.
    mkpakaw  his 位於荊棘叢中的 against `pak`+`-aw` 老鷹抓小雞的動作, the
             hawk-and-chicks game, on the 小 of 小雞. The RIGHT root is sitting
             beside it — `pakaw` 有刺的野草, the thorny weed, his gloss exactly —
             and it shares no character with him at all, which is the whole
             reason `_agrees` is a proxy and not a measure.

**人 was tested identically and REFUSED**, though it fails the same "carries
meaning" test. In these two wordlists it is overwhelmingly a FRAME rather than a
word — 使人X "make someone X", X的人 "one who Xs", the agent nominalizer — and
dropping it buys 9 of which the first read is the proof: `pngraq` 使人變傻 "make
a fool of someone" agreeing with `ngraq` 比女人陰蒂的手勢 on the 人 of 女人. 上
likewise: +13, but `mtama` 當上父親的人 agrees with `tama` 上帝 on the 上 of a
verbal complement, and it would have let `mttama` and `tmtama` back in through a
second door the batch before had just shut. 下 and 中 alone buy nothing at all.

Census after: modern dark 42,167 / pale 2,266 / green 32 = **94.8319%** (from
94.7892%), original 42,640 / 2,290 / 32 = 94.8356%, 1,967 cards, 0 page errors
in both modes.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

GAIN = {"empsparu": 2, "knblaqan": 2, "mkparu": 3, "msbilaq": 3,
        "psblaqan": 2, "psblaqi": 1, "skparu": 4, "tbilaq": 2}

# the two coincidences. The rule REACHES both; HAND_NOT_REGULAR is the only
# thing keeping them pale, and `mkpakaw` is the one to watch — its right root is
# in the same list and shares no character with him.
PIN = {"knslaan": 2, "mkpakaw": 4}

# 人 and 上 were tested and refused; these are what would fall in first if
# either were ever dropped from STOP.
STOPPED = {"pngraq": 3, "mtama": 2, "mttama": 3, "tmtama": 2}

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
    stopped = pg.evaluate(SPANS, sorted(STOPPED))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(pin, PIN, "pale", "PIN")
check(stopped, STOPPED, "pale", "STOPPED")

tot = sum(tally.values())
if tally["dark"] < 42167:
    fail.append("census: dark fell to %d, below this batch's 42,167" % tally["dark"])

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], 100.0 * tally["dark"] / tot))
print("GAIN %d values / %d occurrences now dark" % (len(GAIN), sum(GAIN.values())))
print("PIN  %d coincidences still pale   STOPPED %d values 人/上 would have bought"
      % (len(PIN), len(STOPPED)))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
