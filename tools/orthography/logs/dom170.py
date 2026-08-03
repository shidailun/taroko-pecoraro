# -*- coding: utf-8 -*-
"""Batch 170: the winnowing card, and what a sheet row is really reporting.

**Sheet 1 row 4 grouped seven pale occurrences under `bus` 蒸氣洩出聲, and none
of them belong to it.** That was not a printing accident. The sheet is generated
from `roots()`, and `roots()` cuts every one of them onto `bus`:

    knsbusan -> ('bus', 'kns', 'an')      his SIBUS 甘蔗 -> 甜味—甜
    mbusi    -> ('bus', 'm',   'i')       his BOSI 帽子－鴨舌帽 -> 戴帽子
    snbusi   -> ('bus', 'sn',  'i')       his BOSI
    tnbusan  -> ('tbus', '', 'an') ...    his TBUS 使用簸箕 -> 簸揚的對象

So a worksheet row is a report on the ANALYSER, not on the book. Three of these
four cards are unreachable because the root the analyser needs is one it is not
allowed to see, and that is worth more than the row was.

**What moved: `tnbusan` -> `tnbsan`, 2 occurrences.**

Batch 154 had already read this pair and written down the right answer —
"Winnowing and sifting grain ARE the same word, so the rule's answer is right;
its argument is a particle" — then pinned it, because the only agreement
`outvoted()` could find was the 去 of 過去, the past. This batch supplies the
argument rather than overriding the refusal. Both stand.

The argument is not my reading of two glosses. **His card names the tool.** TBUS
is 使用簸箕（＝Bluxeng）在混合物, and `Bluxeng` is modern `bluhing` 簸箕 —
listed, 5x in the parquets, with `smbluhing` 用…簸箕 and `kbluhing` 做成簸箕
behind it. He points at the winnowing tray and the wordlist writes the act you do
with it: `tbus` 篩榖, `tmbus` 篩去…, `stubs` 為…篩去, `tbsan` 篩穀子的地方. Hence
the SYN line 簸揚 篩榖 篩穀 篩去 — the ACT only. 簸箕 is deliberately not a member,
because it would let his card agree with the 43-word `giya` 小簸箕 family, a
smaller tray off a different root. Blast radius measured first: 簸揚 occurs in one
of his entries and 篩 in one, so the line can reach one card.

**And the spelling had to change, which is the part no one asked for.** The
listed slot is `tbsan`, not `tbusan` — the vowel drops before `-an`. Measured
over the wordlist rather than assumed: of 388 CCVC roots, 55 drop the vowel
before `-an` and 45 keep it, so the bare rule is a coin flip. The n-perfective is
not: 22 of the 23 listed n-perfectives off those roots take the DROPPED shape
(`bnkgan`, `dngqan` 打鼾, `knrtan` 手術後, `snpgan` 數過, `qnslan` 夾, `snbtan`,
`pnrqan`, `gnqran`), and the one exception, `pnriqan`, is a doublet whose own
root also lists `pnrqan`. Neither `tnbsan` nor `tnbusan` occurs in the wordlist,
the parquets or the Bible, so this is a derived spelling either way — but one of
them follows a rule the language demonstrates 22 times.

**The 45 "kept" cases turn out to explain the minimal pair.** They are dominated
by sound words — `bras` 發出「bras」的聲音, `brut` 在「brut」聲, `bruh`
讓…「bruh」進入, `bsus` 用…「bsus」刺 — which keep their vowel because the vowel
IS the sound. That is exactly why `tbusan` 被噴到 (from `bus` the puff) and
`tbsan` 篩穀子的地方 (from `tbus` the sifting) are both listed and both correct.
The wordlist itself refutes the row's premise that these are one root.

**The five that did not move, and why each is blocked at the analyser.**

  knsbusan 3   `sibus` 甘蔗 is listed and its sisters `msibus` 甜的 / `ssibus`
               很甜 hit his 甜味—甜 exactly, and `psbusi` 用甘蔗來製糖 proves the
               language syncopates `sibus` > `sbus` before an affix. But
               `roots()` never offers `sibus`: the syncope is INSIDE the root,
               and no rung can agree with a gloss it is never handed. The
               spelling on the page is already right; only the proof is missing.
  mbusi    1   The informant ruled it 2026-08-03: `busi` is the hat, the
  snbusi   1   Japanese 帽子. `busi` is real modern Truku — 7 occurrences in the
               parquets, already dark at rank 1. It still cannot be the root
               here, because `seen` widens and `lex` never does, on purpose:
               a corpus is not a root inventory. There is no positive hand-root
               table in this codebase, only refusal lists, and inventing one to
               win 2 occurrences is not a trade this batch will make.

               Also ruled: Tgdaya `bunuh` 帽子 is NOT the source. Truku `bunuh`
               is 小腹 with a 26-word family (`psbunuh` 小腹很大, `mtgbunuh`
               露出小腹) and a 輪軸 sense besides. Same string, two dialects,
               unrelated words — the reason a cognate may explain a word and
               never spell one, as batch 169 said of `tabul`.

+2 occurrences. 97.4337% -> 97.4382% (43,322 / 1,107 / 32).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# The respelled perfective, dark off the listed slot `tbsan` via the SYN line.
GAIN = {"tnbsan": 2}

# His spelling must be gone; the syncope is the whole point.
GONE = ["tnbusan"]

# The minimal pair that refutes the row: two roots, both listed, both right.
PIN_PAIR = {"tbusan": 1, "tbsan_check": 0}
PIN_ROOTS = {"tbus": 2, "tbusi": 2, "bluhing_check": 0}

# Blocked at the analyser, not by a gloss. If any of these goes dark without
# `roots()` being taught to see through a root-internal syncope (knsbusan) or
# without a root inventory that admits corpus-only loans (mbusi/snbusi), then
# something has been let in by the back door.
PIN_BLOCKED = {"knsbusan": 3, "mbusi": 1, "snbusi": 1}

# The sugar family that knsbusan cannot reach, dark on its own account.
PIN_SUGAR = {"sibus": 4, "msibus": 5, "ssibus": 2, "psbusi": 1}

# The hat: real modern Truku, and still not usable as a root.
PIN_HAT = {"busi": 1}

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
        if not n:
            continue
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
    gone = pg.evaluate(SPANS, sorted(GONE))
    pair = pg.evaluate(SPANS, sorted(PIN_PAIR))
    root = pg.evaluate(SPANS, sorted(PIN_ROOTS))
    blkd = pg.evaluate(SPANS, sorted(PIN_BLOCKED))
    sug = pg.evaluate(SPANS, sorted(PIN_SUGAR))
    hat = pg.evaluate(SPANS, sorted(PIN_HAT))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(pair, PIN_PAIR, "dark", "PAIR")
check(root, PIN_ROOTS, "dark", "ROOT")
check(blkd, PIN_BLOCKED, "pale", "BLOCKED")
check(sug, PIN_SUGAR, "dark", "SUGAR")
check(hat, PIN_HAT, "dark", "HAT")
for w in GONE:
    if gone.get(w):
        fail.append("GONE %s: still rendered, %s" % (w, gone[w]))

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43322:
    fail.append("census: dark fell to %d, below this batch's 43,322" % tally["dark"])
if pct < 97.438:
    fail.append("census: dark fell back below 97.4382%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN    %d occ on `tnbsan`, off the listed slot `tbsan`"
      % sum(GAIN.values()))
print("BLOCKED %d occ still pale: 3 need root-internal syncope, 2 need a root "
      "inventory that admits a corpus-only loan" % sum(PIN_BLOCKED.values()))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
