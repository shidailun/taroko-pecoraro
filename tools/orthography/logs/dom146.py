# -*- coding: utf-8 -*-
"""Batch 146: vouched()'s four-letter floor made its own headline example unreachable.

`vouched()`'s docstring opens with the clean case: "`xal` is the clean one: the
citation form is 0× — his own headword note says so, 從未見過此簡單形式 — while
`pxal` 147×, `msxal`, `smxal`, `snxal`, `pnxal` and `sxali` are all there."

`xal` is THREE LETTERS. `len(v) < 4` refused it on the first line, before any of
that was looked at. So did `niq` 存在－居住－擁有, `rut` 重壓於上, `hdu` 完成,
`yup` 吹, `pru` 引起傳染, and `muk` — where his card asks the question outright,
「這會不會是以下詞的詞根：SMUK ＝ 釘子，G'MUK ＝ 蓋子」, and the modern wordlist
answers it with gmukan, gmukaw, gmukay, gmuki, gmukun, gnmukan, kmukan, mukan
and smuk. Nine supporters, and the rule could not hear the question.

**The floor was borrowed reasoning.** Everywhere else in this file it guards a
root found INSIDE a longer string, where three letters are inside everything.
Here the root IS the whole word and the supporters are built by AFFIXING it, so
the only way the shape over-generates is the way `len(set(d.values())) >= 2`
already refuses — two supporters wearing different affixes.

What a shorter root really costs is anchoring, so the floor is replaced by a
tightening rather than removed: at three letters the agreement must come from
his STRONGEST Chinese, one he attached to the word AS A WORD, never an example
sentence. That is the same gate `vouched_root()`, `syncopated()` and `chained()`
already take, for the same reason, and batch 145 argued the general case — a
whole-clause translation shares a character with almost anything.

**The gate is not decoration; it is what keeps four values out.** They are
asserted still pale below:

  rih   his 幾乎－接近－大約－有點像 agreed with `krih` on the 工作 of a sentence
        about throwing your money away. A sentence gloss, and nothing else.
  nta   his 邀請前往（唯一使用的形式，與 LITA 並用）agreed with `ptntun` on 起 —
        and `ptntun` is not `nta`'s paradigm at all. **His NTA is n- on the
        two-letter `ta` 我們, the frame of `lita` = l- + `ita`**, and `lita`
        一起, `ita`/`ta` 我們 and `nnita` 咱們的 are all in the modern wordlist
        while `nta` is in none of it — nor once in the 361,630 parquet tokens.
        Two letters is below any floor this book can honestly set, so the
        largest pale word on the page stays pale, on the same honest answer
        batch 139 gave: the outside source was asked and did not know.
        **`nta` is dark as of batch 159, and the gate did not move.** It left by
        a door that did not exist here — `HAND_SPOKEN`, the informant — and the
        corpus miss recorded above is re-measured there and still stands, now
        across four written sources rather than two. "The outside source was
        asked and did not know" was the right answer to the question this batch
        could ask. It was never the same as "the word is not Truku", and when it
        was reported that way to the informant he corrected it.
  dup   his own note calls it a variant, 源自 DUP，而 DUP 最常實現為 DUK.
  klulu no supporters at all — `derived()` is empty, so the rule never applies.

+7 values / 25 occurrences, 0 de-verified, 0 relevelled, all seven at the
EXISTING level 3 — this widens a rule rather than adding one, so nothing
renumbers.

Census after: modern dark 42,690 / pale 1,743 / green 32 = **96.0081%** (from
95.9519%), original 43,166 / 1,764 / 32 = 96.0055%, 1,967 cards, 0 page errors in
both modes. **This is the batch that passes 96%.**
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

GAIN = {"xal": 9, "niq": 4, "muk": 3, "rut": 3, "hdu": 2, "pru": 2, "yup": 2}

# the three-letter roots the slot-gloss gate refuses, and `klulu` which has no
# paradigm to be vouched by. If the gate is ever dropped, `rih` is the first
# thing to fall.
# `nta` was the fourth member and is dark as of batch 159 — **not by this gate
# loosening, which is the whole point.** These three staying pale is the proof:
# they are the same gate, unchanged, and `nta` needed a person to speak for it.
PIN = {"dup": 7, "klulu": 7, "rih": 6}

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
if tally["dark"] < 42690:
    fail.append("census: dark fell to %d, below this batch's 42,690" % tally["dark"])
if pct < 96.0:
    fail.append("census: dark fell back below 96%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d three-letter roots / %d occurrences now dark"
      % (len(GAIN), sum(GAIN.values())))
print("PIN  %d still pale (%d occ) — the slot-gloss gate, and `klulu` has no "
      "paradigm" % (len(PIN), sum(PIN.values())))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
