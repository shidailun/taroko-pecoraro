# -*- coding: utf-8 -*-
"""[batch 223] The card furniture, worked for the first time -- three rulings.

Batch 222 discovered that every ranking instrument this project owns is
`.truku`-scoped, because they were all written to serve the pair metric. His
HEADWORDS, SUB-FORM names and PARADIGM slots render in `.hw` / `.sub-form` /
`.paradigm` and sit in no `.truku` box, so roughly half the pallor in the book
had never been ranked by anything. `logs/furniture.py` ranks it. This log freezes
what batch 223 spent from that seam.

**No pairs, and none were available.** All three values are furniture: not one of
them occurs in an example sentence, so the metric stands where batch 220 left it,
at 5,331 of 5,429. That is the expected outcome, not a disappointment -- a
headword is not a denominator row. What the seam buys is coherence: three of his
paradigms were rendering one suffix two different ways.

### 1. `pt"tui -> pteetui` -- batch 219's shape, in a MANUAL pin

His PT"TO card is 豎立－使立起 and its paradigm is
`° Mpt"to, pt"to, pt"tui, pt"toan, pt"toon.` -- one stem, one elision mark, five
slots. Four of them expand the `"` to `ee` and one did not:

    mpt"to  -> empteetu    pt"to   -> pteetu     pt"tui -> pttui   PALE
    pt"toan -> pteetuan    pt"toon -> pteetuun

The same `"` in the same position in the same stem cannot read two ways. That is
batch 219 exactly (`tglgli -> tgrgri` beside `tgrgrigun`), including its coda:
this was a MANUAL pin, so batch 201's contradiction test has to run over
`manual_map.json` and not only over char-rule output. Eight other hand pins on
this stem all expand it -- `t"to -> teetu`, `st"to -> steetu`, `smt"to ->
smteetu`, `knt"to -> knteetu`, `pnt"toan -> pnteetuan`, `sttuun -> steetuun`,
`knsttuan -> knsteetuan`, `pt"to -> pteetu`.

`pteetui` is NOT listed and is not claimed to be. It verifies at **code 2**, a
regular inflection of the listed `pteetu` 立碑 -- the same rung its siblings
`pteetuun` and `empteetu` already ride, and the gloss test passes on 立 against
his 豎立－使立起.

**The positive half, which is what makes this a correction and not a tidy-up:**
the value it replaces decomposes onto the WRONG card. `ttui` is itself a listed
root glossed 切、剁, so `pttui` reads as p- + cut -- the meaning of his OTHER
card, T"TO 切割. That also settles the neighbour, in the opposite direction:
`t"tuan -> ttuan` is dark at code 2 off that same `ttui` 切, and his `T"tuan` is
glossed 切成的塊－切割的情況. It is CORRECT and must not be "made consistent"
with `teetu`. Decide slot by slot when a homophone exists.

### 2. `tqq"lang -> tqqrang` -- a half-ruling, caught from the other end

Batch 201 ruled `qqrang` and `mqqrang` (HAND_RULED, with a paragraph) on his
QQ'LANG 顫抖 card, riding batch 191's `kkrang`/`mkkrang` because his own gloss
line ends 參見 KK'LANG. The t- slot of the card he cross-references was ruled in
the same sweep -- "`kkrang` and `mkkrang`, so `tkkrang`" is written at
inflection.py:1670, under the heading THE SIBLING SEAM. The t- slot of THIS card
was not. Six of seven forms across the two cards carried `r`; `tqq'lang` alone
kept the `l`.

And the record says it was `tqqrang` first. `logs/b57.py:116` carries the entry
with its reason beside it:

    "tqq'lang": "tqqlang",           # qq'lang>qqlang;  was TQQRANG

Batch 57 changed it to track the head, which then read `qqlang`. Batch 201 moved
that head to `qqrang` and left this slot behind. Restoring it does not overrule
batch 57 -- it finishes the supersession batch 57's own comment predicts. This is
a hand ruling resting on the same hand ruling `qqrang` rests on, and it is
written up in `HAND_RULED` beside them, because an unargued entry there is the
metric deciding the spelling.

### 3. `kl"ulus -> kreurus` -- batch 200's parenthetical, passing its caveat

His KLUULUS 分散的－四散的 card is tagged `(KL'ULUS ? - R. = ULUS ?)`, and his
ULUS card names the same lexeme the same way: "C'est sans doute la R. de KL'ULUS
(=disperser)". One word, two of his spellings, and the map sent them to two
values of which exactly one was dark -- `kluulus -> kreurus` against
`kl'ulus -> klulus` PALE. Batch 200's shape.

Batch 200's caveat is the part that must be checked and it passes: the dark side
is not dark on a homograph. `kreurus` verifies at code 3, vouched by its own
paradigm, and the paradigm's glossed member `mkreurus` 散落的 answers his
`Mkluulus` 分散－散布各處 on 散. A consistency fix, not a new attestation claim.

### 4. `xoil -> huwir` -- the last headword parenthetical in the book

Found by a new instrument, `.scratch`-side: run batch 201's char-rule
contradiction test per CARD over the whole book, flagging cards where his own `l`
renders BOTH `l` and `r` and the minority side is pale. Two hits, both the same
card. Then the general form of it -- every headword of the shape `X (Y)` /
`X (Y ?)` / `X (vl. Y)` where the two sides map to different values of which
exactly ONE is dark -- returns exactly ONE row in 1,967 entries. Batch 200 worked
the sub-form parentheticals; this is the last of them at headword level.

His XOIL (XOWIL ?) is 舀小米酒的杓子, a bamboo ladle for millet beer, French
`Louche pour puiser la bierre de millet`. `xowil` is generated to `huwir` by the
char rules operating cleanly on his own second spelling -- x->h, o->u, l->r --
and `huwir` is listed 湯匙. `xoil` was a tier-M IDENTITY pin: batch 216's one map
entry that ages, a recorded search that FAILED, sitting beside a form of the same
headword that has since been ruled.

**The gloss overlap is ZERO and that is not a refusal here.** 杓子 and 湯匙 share
no character, which is why no character-overlap instrument ever surfaced this
card. Batch 205's LAMIL is the precedent for reading past that (腳掌 vs 拖鞋), and
batch 204's different-root test is what settles it: the register's ladle family
is `isux` 飯瓢, `sahug` 水瓢(舀水用), `wihi` 水瓢、湯匙, `hahug` 舀 -- and not one
of them is reachable from XOIL or XOWIL by his correspondences. There is no rival
root that spells his word, and the only word his own letters produce is `huwir`,
an implement for scooping. Following the dark side asserts nothing `xowil` had
not already asserted about the same lexeme.

The two halves are asserted below: his two spellings must render ONE word, and
`xowil` must remain the SOLE key emitting `huwir` -- which is how "not dark on a
homograph" was checked.

### REFUSED -- `poxel -> puxir`

Same seam, same page shape, and it is not the same question. His KPOXEL 重聽－
耳聾 is tagged `(R. ? - R. = POXEL ?)`. That is not a variant spelling of the
headword the way `KL'ULUS` is; it is a bare ROOT he posits and marks with his own
question mark, and KPOXEL is not POXEL. The head itself is already served --
`qpuhir` 耳聾 is listed and dark, with `mqpuhir` 耳聾的 and `pnqpuhir` beside it
-- so there is no inconsistency to fix. The bare root has no modern reflex to
find: `puhir` is not listed, and the analyser reaches it only by peeling a `p`
off a hypothetical `uhir`.

This is a class, not a candidate. The furniture seam is full of these -- `dux`,
`eydang`, `eysa`, `ihur`, `iyak`, `kuy` are all bare roots he posits, several
marked on the page in his own hand (DUX 參見KNDUX; IXOL 不太可能是 MIXOL 的詞根;
IYAQ 這會是 MIYAQ 的詞根嗎？; UKWI 從未單獨出現). Naming the class is not
opening a door to clear it: pale is not a backlog, and a bulk clearance has been
priced and rejected twice.

    python tools/orthography/logs/dom223.py     # site served at :8765
"""
import io
import json
import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SITE = os.path.join(ROOT, "site")
URL = "http://127.0.0.1:8765/?q=%CC%81"
WAIT = 22000

FLOOR = 5331
DENOM = 5429
AUDIO_IDS = 5134

# what the batch wrote: his key -> the value it must now emit
RULED = {"pt'tui": "pteetui", "tqq'lang": "tqqrang", "kl'ulus": "kreurus",
         "xoil": "huwir"}

# the values those keys used to emit. None of them may render anywhere: each was
# replaced outright, so a reappearance means the map was reverted or a second key
# still points at it. `xoil` was a tier-M IDENTITY pin, so the retired value is
# his own spelling.
RETIRED = ("pttui", "tqqlang", "klulus", "xoil")

# his two spellings of ONE headword must render ONE word. This is the whole
# content of the XOIL ruling; if they diverge again the consistency fix is gone.
ONE_WORD = ("xoil", "xowil")

# ...and `huwir` must not be serving anyone ELSE. The ruling followed the dark
# side of his parenthetical, which batch 200 permits only where the dark side is
# not dark on a homograph. `xowil` is the sole key emitting it; a third key
# arriving means that check has to be redone before this ruling stands.
SOLE_SOURCE = "huwir"

# the siblings each ruling was reasoned FROM. If one of these goes pale the
# argument is gone, and the ruling above it has to be re-argued, not kept.
SUPPORT = {
    # PT"TO -- the four slots that expand his elision mark
    "empteetu": "pt\"to card, m- slot",
    "pteetu": "pt\"to card, bare slot (listed, 立碑)",
    "pteetuan": "pt\"to card, -an slot",
    "pteetuun": "pt\"to card, -un slot",
    # QQ'LANG and the card he cross-references with 參見 KK'LANG
    "qqrang": "batch 201 HAND_RULED",
    "mqqrang": "batch 201 HAND_RULED",
    "kkrang": "batch 191",
    "mkkrang": "batch 191",
    "tkkrang": "the SAME t- slot, ruled at inflection.py:1670",
    # KLUULUS
    "kreurus": "his KLUULUS head, code 3",
    "mkreurus": "listed 散落的, what vouches kreurus",
    # XOIL -- the dark side of his own headword parenthetical
    "huwir": "his XOWIL, listed 湯匙",
}

# `ttuan` is the neighbour this batch refused to touch. It is dark off `ttui`
# 切、剁, which is his T"TO 切割 card's own meaning -- the correct value, and the
# reason `pttui` was wrong ON THE PT"TO CARD. If it ever goes pale, the
# slot-by-slot reasoning that separated the two cards needs re-deriving.
NEIGHBOUR = "ttuan"

# the refusal, asserted in both halves (batch 221)
REFUSED = "puxir"
REFUSED_TAG = "(R. ? - R. = POXEL ?)"
REFUSED_POSITIVE = ("qpuhir", "mqpuhir")   # the head IS served, so nothing to fix
REFUSED_NEGATIVE = re.compile(r'"(puhir|puxil)"')  # a listed bare root re-opens it

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  let tot = 0, ok = 0;
  const seen = {}, unv = {}, inTruku = {};
  document.querySelectorAll('#results > article.entry').forEach(c => {
    // the PAIR metric is `.truku`-scoped, and must stay that way (batch 208)
    c.querySelectorAll('.truku').forEach(b => {
      const sp = [...b.querySelectorAll(SEL)];
      if (!sp.length) return;
      tot++;
      if (sp.every(s => s.classList.contains('w-mod'))) ok++;
    });
    // the PALLOR census is book-wide, because this batch works the furniture --
    // a `.truku`-scoped walk cannot see a headword or a paradigm slot at all
    // (batch 222, which reported six rendered values as rendering NOWHERE)
    c.querySelectorAll(SEL).forEach(s => {
      const t = (s.textContent || '').trim().toLowerCase();
      seen[t] = (seen[t] || 0) + 1;
      if (s.classList.contains('w-unv')) unv[t] = (unv[t] || 0) + 1;
      if (s.closest('.truku')) inTruku[t] = (inTruku[t] || 0) + 1;
    });
  });
  return {tot: tot, ok: ok, seen: seen, unv: unv, inTruku: inTruku}; }"""


def entries_text():
    return io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()


def audio_ids():
    s = entries_text()
    E = json.loads(s[s.index("["):s.rindex("]") + 1])
    out = set()

    def walk(e):
        for x in (e.get("examples") or []):
            if x.get("a"):
                out.add(x["a"])
        for sb in (e.get("subs") or []):
            walk(sb)
    for e in E:
        walk(e)
    return out


def modern_map():
    """His key -> modern value. NO leading indent in modern_map.js (batch 207)."""
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    b = t.index("\n};", a) + 2
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$', t[a:b], re.M))


def verified():
    """Value -> code. TWO leading spaces in verified.js (batch 207)."""
    t = io.open(os.path.join(SITE, "verified.js"), encoding="utf-8").read()
    return dict((m.group(1), int(m.group(2)))
                for m in re.finditer(r'^  "(.+?)": (\d+),?$', t, re.M))


def register_text():
    p = os.path.join(os.path.dirname(HERE), "attested_modern.json")
    return io.open(p, encoding="utf-8").read()


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("http://127.0.0.1:8765/")
        pg.evaluate(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
        pg.goto(URL)
        pg.wait_for_timeout(WAIT)
        r = pg.evaluate(JS)
        b.close()

    seen, unv, inTruku = r["seen"], r["unv"], r["inTruku"]
    MM, V = modern_map(), verified()
    fails = []

    print("PAIRS %d / %d = %.4f%%" % (r["ok"], r["tot"],
                                      100.0 * r["ok"] / r["tot"]))

    # 1 -- the metric floor. Batch 223 spent nothing, so this must not move.
    if r["tot"] != DENOM:
        fails.append(
            "denominator %d, expected %d. The metric is deliverable sentence "
            "pairs over a fixed set of example rows; a changed denominator "
            "means rows entered or left and the FLOOR below is not comparable."
            % (r["tot"], DENOM))
    if r["ok"] < FLOOR:
        fails.append(
            "FLOOR %d: pairs fell to %d. Batch 223 ruled three FURNITURE "
            "values -- none of them occurs in an example sentence -- so it "
            "could not have moved this either way. A fall means something "
            "else did." % (FLOOR, r["ok"]))

    # 2 -- the three rulings still stand in the map, and still render dark
    for k, v in sorted(RULED.items()):
        if MM.get(k) != v:
            fails.append(
                "map %r now emits %r, not %r. The ruling is in the map or it "
                "is nowhere; re-read dom223's reasoning before letting a third "
                "spelling stand." % (k, MM.get(k), v))
        if v not in seen:
            fails.append(
                "%s renders nowhere. It was measured DARK on his card when "
                "batch 223 ruled it; a value that stops rendering means the "
                "card changed shape and this measurement no longer describes "
                "it." % v)
        elif unv.get(v):
            fails.append(
                "%s renders PALE %dx. The whole point of the ruling was that "
                "it darkens -- pale means the verification behind it lapsed, "
                "not that the spelling is wrong." % (v, unv[v]))

    # 3 -- and they are FURNITURE. If one turns up inside a `.truku` box the
    # "0 pairs was the expected outcome" claim above is no longer true, and the
    # seam has to be re-priced as a pair seam.
    for v in sorted(RULED.values()):
        if inTruku.get(v):
            fails.append(
                "%s now renders inside a `.truku` box %dx. Batch 223 recorded "
                "these as furniture-only and therefore worth 0 pairs; if it is "
                "in a sentence, re-price the furniture seam."
                % (v, inTruku[v]))

    # 4 -- the replaced values are gone
    for v in RETIRED:
        if v in seen:
            fails.append(
                "the retired value %s renders %dx again. Batch 223 replaced it "
                "outright, so either the map was reverted or a second key "
                "still points at it." % (v, seen[v]))

    # 5 -- every sibling the rulings were reasoned FROM is still dark
    for w, why in sorted(SUPPORT.items()):
        if w not in seen:
            fails.append(
                "the supporting form %s (%s) renders nowhere; the argument for "
                "the ruling beside it cannot be checked." % (w, why))
        elif unv.get(w):
            fails.append(
                "the supporting form %s (%s) is PALE %dx. A ruling reasoned "
                "from a sibling dies when the sibling does -- re-argue it, do "
                "not keep it." % (w, why, unv[w]))

    # 6 -- the neighbour this batch deliberately did NOT touch
    if unv.get(NEIGHBOUR) or NEIGHBOUR not in seen:
        fails.append(
            "%s is no longer dark. It is his T\"tuan 切成的塊 rendering off "
            "`ttui` 切、剁 -- the CORRECT value, and the evidence that `pttui` "
            "was wrong on the PT\"TO card. Losing it collapses the "
            "slot-by-slot distinction between his two cards." % NEIGHBOUR)

    # 7 -- the refusal, in both halves (batch 221)
    if unv.get(REFUSED) is None:
        fails.append(
            "%s no longer renders PALE. It was refused as a bare root he "
            "POSITS (his tag %r), not a variant spelling -- if something "
            "darkened it, that ruling was made without citing this refusal."
            % (REFUSED, REFUSED_TAG))
    if REFUSED_TAG not in entries_text():
        fails.append(
            "the tag %r is gone from entries.js. It is the whole basis of the "
            "refusal: `(R. ? - R. = POXEL ?)` posits a root, where KLUULUS's "
            "`(KL'ULUS ? ...)` names a variant. If the tag changed, the two "
            "cases may no longer be different." % REFUSED_TAG)
    for w in REFUSED_POSITIVE:
        if unv.get(w) or w not in seen:
            fails.append(
                "the positive half of the POXEL refusal failed: %s is not "
                "dark. The refusal says the head is ALREADY served so there is "
                "no inconsistency to fix; if it is not served, re-open it." % w)
    m = REFUSED_NEGATIVE.search(register_text())
    if m:
        fails.append(
            "the negative half of the POXEL refusal failed: the register now "
            "lists %r. The refusal rests on the bare root having no modern "
            "reflex -- one appearing is exactly the news that re-opens it."
            % m.group(1))

    # 7b -- the XOIL ruling, in the two halves that license it
    a, b = ONE_WORD
    if MM.get(a) != MM.get(b):
        fails.append(
            "his two spellings of one headword diverged again: %s -> %r but "
            "%s -> %r. XOIL (XOWIL ?) is one word by his own tag, and making "
            "them render one word IS the ruling (batch 200)."
            % (a, MM.get(a), b, MM.get(b)))
    src = sorted(k for k, v in MM.items() if v == SOLE_SOURCE and k not in ONE_WORD)
    if src:
        fails.append(
            "%s is now emitted by %s as well. The XOIL ruling followed the "
            "DARK side of his parenthetical, which batch 200 permits only "
            "where that side is not dark on a homograph -- `xowil` being the "
            "sole source is how that was checked. Redo it." % (SOLE_SOURCE, src))

    # 8 -- standing invariants. A spelling batch writes no data file.
    for v in sorted(RULED.values()):
        if v not in V:
            fails.append(
                "%s is absent from verified.js, so darkClass pales it however "
                "well argued it is (batch 215). Check build_verified.py ran."
                % v)
    n = len(audio_ids())
    if n != AUDIO_IDS:
        fails.append(
            "attached audio ids: %d, expected %d. An id is a URL and batch 223 "
            "touched no data file -- three map entries cannot move this."
            % (n, AUDIO_IDS))

    for f in fails:
        print("FAIL " + f)
    print("\n%d assertions failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
