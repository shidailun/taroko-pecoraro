# -*- coding: utf-8 -*-
"""Batch 148: 房子 and 家 are the same thing and share no character.

`_agrees` decides whether his Chinese and the root's modern gloss mean the same
by looking for a shared bigram, then a shared character. That is a proxy, and
this codebase already said so — in the note that hand-refused `mkpakaw`:

    The RIGHT root is sitting beside it — `pakaw` 有刺的野草, the thorny weed,
    his gloss exactly — and shares no character with him at all, **which is the
    whole reason `_agrees` is a proxy and not a measure.**

432 pale values / 742 occurrences were refused by that proxy, and reading them
shows the same failure over and over: 房子 against 住屋；家, 不容易 against
困難的, 取代 against 頂替……的位置－繼承, 不露面 against 採取行動躲藏, 去警戒
against 守衛們——守望者們. One meaning, two ways of writing it, nothing in common.

So a third tier: **SYN**, a hand-written table of Chinese expressions that name
one concept, each line read off an actual refused pair and carrying it in a
comment. Twenty-six lines. It is a table and not a measure, and it is checked
into the analyser where it can be argued with.

**Every member is at least two characters, and that is the guard.** It is STOP's
lesson again. 一 is in STOP because it is inside everything, which is why
`kingal` 一個 could never reach his SNKINGAL 單一的; two-character 一個/單一/一次
give that back without giving back the bare 一, and 家 stays out while 住屋 and
房子 do the work — a one-character 家 would match inside 大家, 國家 and 家人 and
hand this rule the SISUN failure. The table asserts the floor at import.

**A line groups what is interchangeable, not what is associated.** `paux` 犁田
against his KPAUX 翻轉（前後）——互換位置 is deliberately NOT in the table and is
the single most expensive omission, 15 occurrences across KMPAUX, KPAUX, KPAUXI,
PAUXUN and PKPAUX. Ploughing does turn the soil over. But 犁田 and 翻轉 are not
the same word, and "related if you think about it" is the exact reasoning SISUN
punishes. They are asserted still pale below, with `sisun` beside them.

**The unpredicted hits are the check that it generalizes rather than overfits.**
Fifteen of the 50 were not among the pairs the table was read from, and all
fifteen were read by hand and are right: `mkingal` (同義詞=Mpxal)=僅僅一次 off
`kingal`, `skkuyuh` 亡妻—已故的（妻子）off `kuyuh` 太太, `prbung` 使埋葬 and
`mrbung` 設下陷阱 off the one `rbung` 深坑 (which is why the pit takes two lines,
not one — a grave is not a snare even though the hole is), the whole `sblus`
變淡 family, `trbuqun`, `ptgxali`, `pkbuyan`, `lhlihun`, and `traqil`/`mtraqil`,
which reach it through `vouched_root` rather than `regular`.

`mkpakaw` comes OUT of HAND_NOT_REGULAR — the hand refusal existed only because
the tier it needed did not.

+50 values / 101 occurrences, 0 de-verified, 2 relevelled. No new level, so
nothing renumbers.

Census after: modern dark 42,815 / pale 1,618 / green 32 = **96.2892%** (from
96.0621%), original 43,292 / 1,638 / 32 = 96.2858%, 1,967 cards, 0 page errors in
both modes.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

GAIN = {
    "rnirih": 4, "mkriqu": 4, "mkpakaw": 4, "lhlihan": 4, "snkingal": 3,
    "shmuan": 3, "pncipiq": 3, "mtliing": 3, "mrbnaw": 3, "dmpgdadak": 3,
    "dmbiyax": 3, "trbuqi": 2, "tkuwax": 2, "stgxal": 2, "qdqutan": 2,
    "psblus": 2, "psblsun": 2, "pqrngul": 2, "pnkmanun": 2, "pnbilaq": 2,
    "pkuwax": 2, "pkbuyu": 2, "nluan": 2, "mtrbung": 2, "msquwaq": 2,
    "mskingal": 2, "mqrngul": 2, "mkuwax": 2, "mkrbung": 2, "mkeeman": 2,
    "kmtgxal": 2, "kmpkrdax": 2, "empkrdax": 2, "empkeeman": 2,
    "empasapah": 2, "empakuyuh": 2,
}

# What the table refuses to say. The `paux` family is 15 occurrences and the
# most expensive line NOT written: 犁田 turns soil, 翻轉 turns anything, and
# they are not the same word. `sisun` is the standing case — he glosses it 縫
# and `sisi` is a wine-strainer — and `knslaan` 饑餓虛脫 against `sla` 大外衣
# stays hand-refused, since 大 was never a synonym of anything.
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
if tally["dark"] < 42815:
    fail.append("census: dark fell to %d, below this batch's 42,815" % tally["dark"])
if pct < 96.0:
    fail.append("census: dark fell back below 96%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d of the 50 asserted dark / %d occurrences" % (len(GAIN), sum(GAIN.values())))
print("PIN  %d still pale (%d occ) — what SYN refuses to say" % (len(PIN), sum(PIN.values())))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
