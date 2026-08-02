# -*- coding: utf-8 -*-
"""Batch 149: a second opinion on what a root means.

Batch 147 found dict_truku_bible.json beside the scripture readers, checked its
SPELLINGS against attested_modern.json, found them already there, and moved on.
It never read the glosses. That was the whole value of the file.

**A text and a glossary are allowed to answer different questions.** 147's rule
was that a corpus may say a string occurs and may never say what it means, which
is why the readers widened `seen` and nothing else. This is the other thing:
2,033 headwords with Chinese and English definitions, edited and published for
this dialect. Meaning is the one question a wordlist is FOR.

**It answers the failure bucket D was full of.** Over and over the refusal was
not that his Chinese disagreed with the root, but that the wordlist gave the root
one sense and it was the wrong one, or gave it a name tag instead of a gloss:

    tama    上帝            ->  父親；天父
    pajiq   人名（女）       ->  蔬菜；青菜
    kari    挖掘            ->  話語；言語
    rusuq   卵子            ->  水滴；淚珠
    putuh   人名（男;女）     ->  失敗；終止；斷絕
    saw     希望，但願/邵族   ->  像；如此；那樣

His SKTAMA 已故的父親 is 11 occurrences on its own and was refused because the
wordlist thinks `tama` means 上帝. It means father; 上帝 is the capitalised
sense, and the glossary prints both in that order.

**Additive, never replacing** — `_gloss()` returns the wordlist's glosses and
then this one, so the rule can only turn a refusal into an agreement. 0 words
were de-verified, which is the property and not a hope.

**Where that property broke, the change was reverted.** Routing `no_chinese()`'s
candidate filter through `_gloss()` looks obviously right — NAMEGL exists to
throw out roots glossed 人名, and `pajiq` is exactly the root it was wrong
about. But that rule refuses on AMBIGUITY, one root candidate or nothing, so a
second gloss source does not only admit candidates, it creates ties: it turned
`mtbrinah`, `mkphing`, `mnksaw`, `tnklai` and six more from dark to pale to buy
7 occurrences. Those ten are asserted DARK below. The second opinion may say
what a root means; it may not make a rule less sure WHICH root it is.

**It cannot reopen the SISUN trap or the `paux` family: it glosses neither
`sisi` nor `paux`.** That is a property of the file rather than a claim about
the rule, and the pins below check it from the DOM.

**Eleven of the 37 reached it through a supporter rather than their own root,
and two of those are worth naming.** `pnnaki` resolves to `nanak` 獨自 — which
is the guess Pecoraro pencilled into his own entry, 「會不會是 Pknanak（？）」.
And the `kray` family is RESOLVED rather than trapped: `tkkray`, `pkrayan` and
`pkrayun` are his 堅固－堅硬, the wordlist's `kray` is 背蔞 a carrying basket, and
what carries them is `knkrayan`/`pskrayun` 堅, an independent source printing the
hard/firm sense as a real modern root. Two homographs, told apart, not merged.

`empkhuway` runs the same check backwards: the wordlist glosses `pkhuway` 要慷慨,
the glossary glosses it 醫治；治癒, and Pecoraro glosses his EMPKHUWAY and
PKHUWAYUN as healing. Two sources that never saw each other agree against the
wordlist.

+37 values / 64 occurrences, 0 de-verified, 32 relevelled. No new level.

Census after: modern dark 42,879 / pale 1,554 / green 32 = **96.4331%** (from
96.2892%), original 43,358 / 1,572 / 32 = 96.4325%, 1,967 cards, 0 page errors in
both modes.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

GAIN = {
    "sktama": 11, "sppajiq": 3, "msaw": 3, "tnqtaan": 2, "tkkray": 2,
    "tgrgrigun": 2, "suusa": 2, "srusuq": 2, "spsrusuq": 2, "smkari": 2,
    "psrusuq": 2, "pkrayun": 2, "nputuh": 2, "mtama": 2, "gnlaan": 2,
    "emppquri": 2, "sspgan": 1, "sptaqi": 1, "spajiq": 1, "rjingi": 1,
    "ptrgrig": 1, "pshgi": 1, "prrawah": 1, "pnsbyaxan": 1, "pnsbrinah": 1,
    "pnnaki": 1, "plnglungun": 1, "pkrayan": 1, "pkhuwayun": 1, "pgkari": 1,
    "ntnegsaan": 1, "mseulah": 1, "mkmppatas": 1, "kdusun": 1, "kdusi": 1,
    "empkhuway": 1, "empakeeman": 1,
}

# The glossary has no entry for `sisi` and none for `paux`, so a second opinion
# on meaning cannot reach either standing refusal. Checked from the DOM rather
# than trusted: if a later batch ever admits a source that DOES gloss them,
# these six go dark and this file says so.
PIN = {"sisun": 5, "kmpaux": 6, "kpaux": 3, "kpauxi": 2, "pauxun": 2,
       "pkpaux": 2, "knslaan": 2}

# The ten that widening no_chinese()'s candidate filter would have cost. They
# are dark today by the wordlist gloss alone; a change that makes that rule less
# sure which root it is takes them away.
DARK = ["dthiyan", "emptquli", "kmpspung", "mkmphing", "mkphing", "mnksaw",
        "mnqqita", "mtbrinah", "pptpusu", "tnklai"]

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
    dark = pg.evaluate(SPANS, sorted(DARK))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(pin, PIN, "pale", "PIN")
for w in DARK:
    seen = dark.get(w) or {}
    if not seen.get("dark") or seen.get("pale"):
        fail.append("DARK %s: no_chinese lost it again, got %s" % (w, seen))

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 42879:
    fail.append("census: dark fell to %d, below this batch's 42,879" % tally["dark"])
if pct < 96.0:
    fail.append("census: dark fell back below 96%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occ from the Bible glossary's glosses"
      % (len(GAIN), sum(GAIN.values())))
print("PIN  %d still pale — it glosses neither `sisi` nor `paux`" % len(PIN))
print("DARK %d still dark — what widening no_chinese() would have cost" % len(DARK))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
