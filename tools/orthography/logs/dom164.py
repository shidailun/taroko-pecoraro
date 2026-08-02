# -*- coding: utf-8 -*-
"""Batch 164: three holes that were not in any rung, but underneath all of them.

Every batch since 145 has widened a rung. This one did not touch a rung's
judgement at all — it fixed three places where the evidence never reached a
rung to be judged.

**(a) `roots()` peels ONE prefix.** A value that carries two comes back from it
with an empty candidate list, and an empty list is not a refusal by any
particular rule — it is invisibility to all eleven at once, because every rung
opens by asking `roots()` for something to read. `dmtqsurux` is dm+t+`qsurux`
魚, `kmspusu` is km+s+`pusu` 根本, `ndjyamu` is n+d+`jyamu` 屬你們的 against his
own 你族人中的一個. 465 of the 807 pale types — 665 occurrences, 55% of the
census — decomposed to nothing whatever, and that was the largest single block
left on the board.

The peel is written as a FALLBACK and not as a widening, and that is the whole
of its safety. `no_chinese()` refuses a value whose candidates fall into more
than one root group, so handing an extra candidate to a value that already has
some can turn a clean one-group reading into a tie and DE-verify it — the one
direction the "widening only adds" invariant does not cover. Firing only on an
empty list makes that impossible by construction. Measured: 0 removed.

Six of the 26 arrivals were substring accidents and are pinned in the new
HAND_NOT_STACK, read one at a time against his sentences. The pin belongs to
the peel rather than to a rung because the claim being refused is the peel's:
`empnalu` is his 將會變好、康復 and so belongs to `malu` 好, the root batch 161
already refused `mnalu` over, not to `alu` 陷阱線 a snare line.

**(b) The gap between `unglossed_root()` and `no_chinese()`.**
`unglossed_root()` exists for a root the wordlist lists but never glossed — its
docstring says the hole is "in the GLOSS TABLE, not a morphology gap", and this
file has convicted that hole by name twice. But it can only fire where HIS
Chinese exists to compare the root's paradigm against. `no_chinese()` is the
rule for where his Chinese is absent — and it requires a GLOSSED root.

So a value with neither — no Chinese of his, and a listed root nobody glossed —
falls between the two and no rule in the file can see it. `nglngu` is the shape:
`lngu` is listed, bare, and the wordlist inflects it thirteen ways. A root
inflected a dozen ways is a word whether or not anyone wrote down what it means.
The witness is `unglossed_root()`'s own, minus the comparison there is nothing
to compare: four-letter floor, unfrozen, `derived()` yielding two DISTINCT
affixes, the whole-or-VSUF final-vowel test.

It runs only when the glossed candidate list is empty, and that ordering is
load-bearing: `stmaqun`'s glossed candidates `taqi`/`tmaq` are two real roots
that must keep refusing (dom163's assertion), while its unglossed `stmaqi`/
`tmaqi` are one group and would have bypassed them. It stays pale below.

**(c) The floor was standing in for a guard.** Batch 163 dropped
`outvoted()`'s root floor from 4 to 3. (b)'s floor is dropped the same way, and
the number is replaced by what it was a proxy for: a root has to be
pronounceable. Four letters keeps `hng` out by accident; requiring a vowel keeps
it out for the reason — Truku writes no schwa, so a listed form with no vowel at
all is a consonant cluster the wordlist filed, not a syllable anyone says.
`smhngi` is the one this refuses and the only thing the floor was buying.

48 occurrences, 41 values, 0 de-verified, 0 new pale types.
DOM 97.2335% -> 97.3415%.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# (a) the second prefix peel.
GAIN_STACK = {
    "ddquyu": 2, "dkmthidaw": 2, "dmtqsurux": 1, "dnjiyal": 1, "gggar": 1,
    "kksiyuk": 1, "kmspusu": 1, "kndduwaan": 2, "ksramal": 1, "mdduwa": 2,
    "mmqduriq": 1, "mngahan": 1, "mntraqil": 1, "mnttatuk": 1, "ndduwa": 1,
    "ndjyamu": 1, "ndtlealay": 1, "nsslupung": 1, "pkdgdangi": 1,
    "pngnnakan": 1,
}

# (b) no Chinese of his AND a listed root nobody glossed.
GAIN_GAP = {
    "ksnani": 1, "nglngu": 1, "nsleelug": 1, "nsrhuqan": 1, "pknhuri": 1,
    "pktleetuun": 1, "pnkpngpung": 1, "pnkrrusan": 1, "pnsilung": 1,
    "pnsqrasan": 1, "pntblayan": 1, "ppsqdug": 1, "pspngun": 1, "pstrmai": 1,
    "ptbnahani": 1, "pttuyun": 1,
}

# (c) the floor at three, with the vowel doing the guarding.
GAIN_FLOOR = {"pdqan": 1, "pnsnmaan": 3, "qnali": 1, "taya": 2, "thnaw": 1}

GAIN = dict(GAIN_STACK)
GAIN.update(GAIN_GAP)
GAIN.update(GAIN_FLOOR)

# The six substring accidents the second peel found, pinned in HAND_NOT_STACK.
# Each reaches a listed root only through the stack, and in each the root it
# reaches is a coincidence: `dmtsapat` against his 放蕩 family and not `sapat`
# 舖床; `empkduriq` landing on `uriq` 肚子痛的聲音 when his word is `qduriq`
# 逃跑, which `mmqduriq` above reaches correctly; `empnalu` on `alu` 陷阱線
# when his is 康復; `ntnring` on `ring` 常笑 when its sibling `mtnring` is his
# 流汗; `mtkkrang` on the onomatopoeion 碗掉下來破碎的聲音 when his `kkrang` is
# 發抖; `spsdharun` on `hari` 一點 with no morphology behind it at all.
PIN_STACK = {
    "dmtsapat": 1, "empkduriq": 1, "empnalu": 1, "ntnring": 1,
    "mtkkrang": 1, "spsdharun": 1,
}

# (b) must not reach these. The first five are HAND_NOT_NC pins that the new
# fallback would otherwise re-admit through a different door — the rung's own
# entry guard is what keeps them out, and this asserts it still runs first.
# `stmaqun` is the ordering claim: two real roots in the glossed pass, which
# the unglossed pass must never get the chance to override.
PIN_GAP = {
    "mslangan": 1, "empslangan": 1, "ggitan": 1, "mtgtmaq": 1, "tmukan": 1,
    "stmaqun": 2, "tnaga": 2,
}
# `tnaga` is the one the regression suite caught, and it is the reason the
# suite is run before the commit rather than after. The fallback reached it
# through `taga` 等 and coloured it verified; dom161 had asserted it pale.
# Batch 161's refusal was epistemic and not a missing rule — `tnaga` is in the
# C-n- infix class, where `<n>` perfective and `<m>` actor-focus share a slot,
# so the token is either t-n-aga on `taga` or his typewriter's n for the m of
# `tmaga`, and nothing on the card decides which. A rule that reaches a word
# is not thereby entitled to it: **an earlier batch's deliberate refusal
# outranks a later batch's newly-widened reach.** Pinned in HAND_NOT_NC.

# (c)'s refusal: `hng` is a consonant cluster, not a syllable.
PIN_FLOOR = {"smhngi": 1}

PIN = dict(PIN_STACK)
PIN.update(PIN_GAP)
PIN.update(PIN_FLOOR)

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
if tally["dark"] < 43279:
    fail.append("census: dark fell to %d, below this batch's 43,279" % tally["dark"])
if pct < 97.3333:
    fail.append("census: dark fell back below 97.3333%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occ  (stack %d, gap %d, floor %d)"
      % (len(GAIN), sum(GAIN.values()), sum(GAIN_STACK.values()),
         sum(GAIN_GAP.values()), sum(GAIN_FLOOR.values())))
print("PIN %d values / %d occ still pale  (stack %d, gap %d, floor %d)"
      % (len(PIN), sum(PIN.values()), sum(PIN_STACK.values()),
         sum(PIN_GAP.values()), sum(PIN_FLOOR.values())))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
