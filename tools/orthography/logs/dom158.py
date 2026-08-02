# -*- coding: utf-8 -*-
"""Batch 158: word-final P/K. He documents the alternation; so does the wordlist.

Pecoraro states this rule himself, in three entries, and it is the only sound
correspondence in the book he bothers to write out in prose:

    DUK   「請注意詞尾輔音P與K之間常見的變換；派生詞保留P，而詞基往往作K」
    NDUP  「NDUK 的變體（詞尾的 P 實現為 K）」
    GALUK 「見 GALUP。(註:…相當多的詞基實際上容許 P 與 K 互換)」

**The modern wordlist obeys it, slot for slot.** The blow root is the proof, and
it is the whole argument for the shape of this batch:

    base      iyuk 吹;吹氣      miyuk 吹          — K
    derived   yupi 吹洞簫       yupan 要…吹       yupun 吹      — P

Five listed words, one root, both consonants, split exactly where he says they
split. That is not a spelling drift between 1977 and now; it is a live
alternation in the language, and he described it correctly.

**So this is a rule about BASES, and it must never become a rule about the
letter.** A blanket p→k would have taken `yupi`/`yupan`/`yupun` — three listed,
glossed, dark words — and rewritten them into forms the wordlist does not have.
The gate is the one `regular()` already uses: respell only where the K-twin is
**LISTED** and its gloss agrees with his. Five values pass, and all five verify
at **rank 1**, the strongest rung there is — these are not inferences, they are
words the modern wordlist prints.

    iyup  → iyuk   吹;吹氣    his 吹。（註：引申為「熄滅」。）參見 YUP。
    qmrap → qmrak  已抓        his 抓住——捕捉。
    trap  → trak   毛巾、頭巾   his 太魯閣族特有的頭帶，寬 4 至 6 公分…
    qnrap → qnrak  抓（已抓到）
    mdup  → mduk   關(門、窗)  his 處於關閉狀態的。

**Batch 29 refused `mdup` and this batch overturns it.** Its stated reason was
that "modern has no p-final form of the root at all… so rewriting his variant to
the k-form is a lexical substitution". The measurement was right — `-dup$` is
**0 words in 40,760**, re-measured here — but it argues the other way. A
substitution is when his WORD is gone and a different word carries the sense
(`q'nao` → `qusul`, garlic). Here the root, the prefix and the sense are
identical and one consonant differs, a consonant he documents as alternating and
whose k-form the wordlist glosses 關(門、窗) against his 處於關閉狀態的.
`-duk$` holds 96 words. The p-spelling names nothing.

Batch 19 had already decided this exact question the other way, in the GALUP
family — six p-forms taken to k on the strength of him writing both spellings
under one gloss — so the two rulings contradicted each other for 139 batches.
**The tie-breaker is not which batch was later; it is that the evidence in 19 was
his own doubled spelling and the evidence in 29 was an inference about what a
zero count means.** CLAUDE.md's batch-29 paragraph is corrected in place.

**`dup` itself does not move, and that is the gate holding rather than mercy.**
Bare `duk` is not listed — modern writes `eduk` 門扇 — so the K-twin fails the
test and his 7 occurrences stay pale. `dupan` 獵場 is the OTHER DUP root, real,
p-final and dark; both are asserted below. Seven occurrences left on the table is
what a gate costs when it is real.

Three of the five come from raw tokens spelled with **l** — `kmlap`, `knlap`,
`t'lap`/`tlap` — so an existing rule already folds their l→r and this batch
changes only the final letter. All six keys are written on his **RAW** tokens, in
front of normalisation [batch 155].

+5 values / 8 occurrences, 0 de-verified. Census after: modern dark 43,076 /
pale 1,356 / green 32 = **96.8784%** (from 96.8605%), 1,967 cards, 0 page errors.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# The five, at their modern spelling. `mduk` counts 2: his MDUK card already had
# one, and his `mdup` is the second.
GAIN = {"iyuk": 3, "qmrak": 2, "mduk": 2, "trak": 1, "qnrak": 1}

# The load-bearing assertion. These are the derived slots of the SAME root,
# listed and glossed by the modern wordlist **with his p**, and they are what a
# rule about the letter rather than about the base would destroy. If they ever
# turn pale or change spelling, the gate has been read as a licence to fold
# every final p in the dictionary.
CLASS = {"yupan": 5, "yupi": 5, "yupun": 2, "miyuk": 2, "yuki": 1}

# The gate holding. `dup`'s K-twin is unlisted (modern writes `eduk`), so it is
# refused and stays pale at 7 — and `dupan` 獵場 is a different root that was
# never this batch's business.
PIN = {"dup": 7}
KEEP = {"dupan": 4, "eduk": 7}

# His spellings must not render at all. This is the batch-155 assertion: a
# manual_map key that silently matches nothing leaves the census identical.
GONE = ["iyup", "qmrap", "trap", "qnrap", "mdup"]

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
    cls = pg.evaluate(SPANS, sorted(CLASS))
    pin = pg.evaluate(SPANS, sorted(PIN))
    keep = pg.evaluate(SPANS, sorted(KEEP))
    gone = pg.evaluate(SPANS, sorted(GONE))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(cls, CLASS, "dark", "CLASS")
check(pin, PIN, "pale", "PIN")
check(keep, KEEP, "dark", "KEEP")
for w in GONE:
    if gone.get(w):
        fail.append("GONE %s: his spelling still renders, %s" % (w, gone[w]))

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43076:
    fail.append("census: dark fell to %d, below this batch's 43,076" % tally["dark"])
if pct < 96.6667:
    fail.append("census: dark fell back below 96.6667%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN  %d values / %d occ dark, 8 of them new — his final P where the "
      "wordlist lists a K base (mduk's card already had one)"
      % (len(GAIN), sum(GAIN.values())))
print("CLASS %d values / %d occ — the SAME root's derived slots, listed with his P"
      % (len(CLASS), sum(CLASS.values())))
print("PIN   dup still pale at %d — bare `duk` is unlisted, so the gate refuses it"
      % PIN["dup"])
print("GONE  %d of his spellings render nowhere" % len(GONE))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
