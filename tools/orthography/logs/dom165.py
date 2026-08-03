# -*- coding: utf-8 -*-
"""Batch 165: two sources of evidence no rung had ever read, and a coin flip.

**The build was not reproducible, and had not been for some time.**
`root_groups()` partitions candidate roots GREEDILY — each candidate joins the
first group it touches — so its answer depends on the order it walks them, and
it walked a SET sorted by length alone. Every tie among equal-length candidates
was therefore broken by Python's per-process hash order. `mngahan` reaches
`mngaha`, `mngahi`, `ngahan`, `ngaha`, `ngahi`, `ngaho`, `ngahu`: six of them
tied at two lengths, falling into one group or two depending on the run, so
no_chinese()'s one-group gate passed or failed and the word came out verified
in three builds out of four. Found by rebuilding twice with no change at all
and diffing the output. dom164 asserts `mngahan` GAINED — that assertion has
been a coin flip since it was written, and every one of no_chinese()'s 195
values was exposed to the same instability. The sort key is now `(len, x)`.
A greedy algorithm over an unordered input is not a rule; it is a sample.

**(a) His own paradigm, where the wordlist has none.** `unglossed_root()` asks
a listed-but-unglossed root's modern paradigm what the root means. For eleven
types the paradigm is glossless too, end to end — the wordlist is not
disagreeing with him, it is silent — and `_agrees` returns None for want of
anything whatever to read. So ask HIS paradigm. The wordlist lists `ngangah`
and glosses neither it nor any of its three slots; Pecoraro wrote four separate
cards on it — 表現得像啞巴、像白痴, 白痴——笨蛋——傻子——啞巴, 從（原本）啞、痴的
狀態而來 — and they agree with each other across entries he typed at different
times. Four independent statements about one root are a gloss for it.

Two guards. The agreement must be a BIGRAM: two glosses of his share 的 and 使
and 人 by the nature of his prose, and a one-character match between two
entries by the same hand at the same desk is not corroboration. And it takes
TWO supporters, because one cross-referencing card is a restatement —
`pnkltudan` and `pkltudan` carry the same sentence and would vouch for each
other in a circle. Where the paradigm SPEAKS and disagrees the value stays pale
and that is the larger half of the bucket: `msilung` against `silung` 海,
`snulu` against `sulu` 屁股.

**(b) He names the word himself.** Some glosses are not meanings but pointers.
`rnjingan`'s entire gloss is （ldingan 的過去式）, `ktbnaw`'s is MTBNAO 的否定形,
`baisan`'s is Bais 的斜格形式 — grammar and a name, no semantic content at all,
so `_agrees` has nothing to weigh rather than something to reject. But a
pointer is BETTER evidence than a gloss: every other rule in the file infers a
root by peeling affixes and then argues the inference; here he states it.

The pointer must land on a root the morphology independently found. A third
shape was written, measured at ten types, and deliberately removed: letting the
pointer SUPPLY the root where the affix rules find none, paying for it with a
gloss agreement. Every one of the ten is wrong the same way. His 參見 and 較常說
are see-also notes — `loai` 外部 carries 較常說：NGANGOT, and `nilaq` a mushroom
cross-references another mushroom — so the pointer names a synonym, the gloss
agrees because synonyms mean the same thing, and out comes `loai`'s spelling
certified by a modern word that is not `loai`. That is the SISUN error with a
citation attached to it.

**A pointer inside a question is not a citation.** He marks his own uncertainty
with ？ and is scrupulous about it, so the punctuation is evidence and it is
his. `tbowyak` is （詞根 BOYAQ？）＝痛得打滾 — he is ASKING whether the root is
BOYAQ, and `bowyak` is 山豬 a wild boar, spelled the same and meaning nothing
like rolling on the ground in pain. `empsibus` is （Pksibus?）加糖 while its own
sibling `pksibus` carries 參見 Psibus with no question mark; the two together
draw the line exactly where he drew it.

**The suite caught this batch, and it caught it on a tripwire set in advance.**
(a) verified `psiisi`, `psiisan`, `psiisun` and dom153 went red. Batch 153
respelled his SISI/SISAN/SISUN to `siisi`/`siisan`/`siisun` on a Truku
speaker's ruling and let the unlisted causatives go honestly pale — then wrote
the trap down: "if these ever go dark without a speaker or a listing behind
them, the respelling has been allowed to carry verification with it, which it
must never do." That is precisely what happened. This rung asks whether his own
cards agree about a listed root; `siisan` is listed only because we put it
there, so what agreed with itself was our own respelling. Six occurrences
refused, in HAND_NOT_FAMILY. A log that only ever confirms the batch that wrote
it is decoration; this one cost 6 occurrences and was worth more than that.

11 values, 22 occurrences, 0 de-verified, 0 new pale types.
DOM 97.3415% -> 97.3910% (43,301 / 1,128 / 32).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# (a) his own cards on a root the wordlist lists and nobody glossed.
GAIN_FAM = {
    "mnngangah": 2, "pngangah": 1, "pnngangah": 3,     # 啞巴／白痴／傻子
    "nnuhan": 2, "pnuhi": 2, "pnuhun": 1,              # 吸奶－吸吮乳房
}

# (b) the root he names is the root the affix rules found.
GAIN_XREF = {
    "baisan": 2,      # Bais 的斜格形式          -> bais 伴侶
    "ktbnaw": 2,      # MTBNAO 的否定形          -> tbnaw
    "pksibus": 1,     # 參見 Psibus              -> sibus
    "rnjingan": 3,    # （ldingan 的過去式）      -> rjingan
    "tqudak": 3,      # 參見 QODAP               -> qudak
}

GAIN = dict(GAIN_FAM)
GAIN.update(GAIN_XREF)

# The removed third shape. Each of these reaches a listed modern word ONLY
# through a pointer that names a synonym rather than a form, and each would
# have been coloured by a word that is not it: `loai`/`lowai` 外部 by `ngangut`
# 外面 (his own note: 較常說 NGANGOT), `nilaq` by another mushroom `qihung`,
# `bsekan` by `pskan` — 參見 PSKAN, and no affix relation between them at all.
PIN_SYNONYM = {"loai": 3, "lowai": 1, "nilaq": 1, "bsekan": 1, "kiima": 2,
               "qtaqi": 2, "qnbsranan": 2, "dup": 7}
# `dd` and `kn` are his AFFIX cards — entries about a prefix, whose romanized
# tokens are his EXAMPLES of it at work. An affix card is not a lexeme.
PIN_AFFIXCARD = {"dd": 1, "kn": 1}
# The question mark, and the two standing refusals a pointer can now reach.
PIN_QUESTION = {"tbowyak": 1, "empsibus": 1}
PIN_STANDING = {"mnalu": 5, "pauxun": 2}
# (a) must not fire where the paradigm speaks and disagrees.
PIN_SPEAKS = {"msilung": 2, "snulu": 1}
# The regression suite paid for itself. (a) fired on his sew causatives and
# batch 153 caught it: `siisan` is in the wordlist only because WE respelled his
# SISAN there on a speaker's ruling, so his own cards agreeing about that root
# is our respelling agreeing with itself. dom153 wrote the tripwire in advance —
# "if these ever go dark without a speaker or a listing behind them, the
# respelling has been allowed to carry verification with it" — and this is it.
PIN_TRIPWIRE = {"psiisan": 3, "psiisi": 1, "psiisun": 2}
# Batch 164's, still held.
PIN_164 = {"smhngi": 1, "stmaqun": 2, "tnaga": 2}

PIN = {}
for d in (PIN_SYNONYM, PIN_AFFIXCARD, PIN_QUESTION, PIN_STANDING,
          PIN_SPEAKS, PIN_TRIPWIRE, PIN_164):
    PIN.update(d)

# The reproducibility claim. `mngahan` is verified in EVERY build now, not in
# three of four; dom164 asserts it dark and this asserts why that is safe.
PIN_STABLE = {"mngahan": 1}

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
    stable = pg.evaluate(SPANS, sorted(PIN_STABLE))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(pin, PIN, "pale", "PIN")
check(stable, PIN_STABLE, "dark", "STABLE")

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43301:
    fail.append("census: dark fell to %d, below this batch's 43,301" % tally["dark"])
if pct < 97.390:
    fail.append("census: dark fell back below 97.3910%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occ  (his paradigm %d, he names it %d)"
      % (len(GAIN), sum(GAIN.values()), sum(GAIN_FAM.values()),
         sum(GAIN_XREF.values())))
print("PIN %d values / %d occ still pale" % (len(PIN), sum(PIN.values())))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
