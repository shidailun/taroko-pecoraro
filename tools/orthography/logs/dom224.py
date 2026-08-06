# -*- coding: utf-8 -*-
"""[batch 224] Two cards from the furniture seam: one ruling, one refusal.

`logs/furniture.py` ranks what batch 222 found unranked, and its last column is
batch 199's cheap question: how many slots on this card are already DARK? Exactly
two furniture-pale values sit on a card with 3+ dark slots and have **no prior
mention anywhere in the record** -- not in `batch-log.md`, not in any `dom*.py`.
This log works both, and they came out opposite ways. That is the point of asking
a card rather than a metric: the shape "pale slot beside dark ones" is a
QUESTION, and a question is allowed to be answered no.

### 1. `graka` RULED -- the ladder refused it on a homograph inside the ANALYSER

His GLAQA ( = R. ? ) is 觀察—窺探—監視 / *Observer - espionner - surveiller
(péjoratif)*, and its one sub-form `Gmlaqa` ("d° forme verbale") has rendered
`gmraka` DARK, code 1, since long before this batch. So the project has already
accepted which modern root this card is. The head sat pale beside it.

`roots('graka')` returns exactly one analysis:

    ('raka', 'g', '', 'g')

It peels the `g` as a prefix and lands on `raka` -- which IS listed, and is
glossed **人名（男）**, a male personal name. The gloss test then scores a name
against his 觀察／窺探／監視, shares nothing, and refuses. That is correct
behaviour on the candidate it was handed, and the wrong candidate. Batch 201's
homograph freeze arriving through the analyser instead of through the map.

**The positive half, on the form whose OWN gloss carries the character**
(batch 221): `grkaan` is listed and glossed **監視;埋伏**. 監視 is the third word
of his own gloss, character for character, on the `-an` form of this very stem.
Three further listed forms spell the stem whole:

    empgraka  要埋伏        spgraka  讓…去埋伏        gmraka  (his own Gmlaqa)

`emp-` and `sp-` prefix `graka`, not `raka`. That is what makes the `g` part of
the root and the peel wrong -- the whole argument in one observation.

The different-root test (batch 204) finds no rival: the register's other 監視
words are `tmndeeda` and `gdrqani`/`gdrqanay`, different roots reachable from his
`glaqa` by no correspondence he uses, so there is nothing to respell toward. The
map is UNTOUCHED -- `glaqa -> graka` was already there. This batch changed a
colour, not a spelling, and claims only that the stem is spelled `graka`.

### 2. `psnnai` REFUSED -- and the scan says the string is his

His NAMA (R) 預備好的 card is the biggest all-but-one-dark card in the seam: 13
dark slots, one pale. The pale one is the `-i` slot of `Psnama`, and he wrote it
with HIS OWN question mark:

    °Mpsnama, psnama, psnnai (?), psnmaan, psnmaon.

Every other slot keeps the `m`. So the first question is batch 213's -- is the
string even his? Page 196 (book page 176), the paradigm line, cropped at 8× with
`psnmaan` from the SAME LINE as the known `m`: the glyph in `psnmaan` has three
legs and both glyphs in `psnnai` have two. **The page reads `psnnai`.** No
transcription fix; `entries.js` is untouched, and the `(?)` is his own doubt
about his own form, not ours about the reading.

The register is then silent, in batch 220's exact shape. The syncopated stem has
**zero** forms in it -- no `psnm-` anything -- so his `psnmaan` and `psnmaun` are
already inferences (codes 7 and 9), and `psnmai`, `psnamai` and `nmai` are all
unlisted too. The `-i` slot is precisely where batch 217 refused to widen
`roots()`' vowel restoration, because that vowel is what separates two roots.
Evidence where there is evidence, inference where there is none: inventing
`psnmai` to tidy his paradigm would be the metric deciding the spelling.

Asserted in both halves. If any form of that syncopated stem ever enters the
register, that is the news that re-opens this.

### Cost

**Zero pairs, by construction, and this log asserts it** (batch 223). `GLAQA`
occurs exactly once in 1,967 entries, as its own headword; no example sentence
uses it. `psnnai` is a paradigm slot. Neither value has a single occurrence
inside a `.truku` box, so the metric could not have moved either way.

    python tools/orthography/logs/dom224.py      # site served at :8765
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
ORTH = os.path.join(ROOT, "tools", "orthography")
URL = "http://127.0.0.1:8765/?q=%CC%81"
WAIT = 22000

FLOOR = 5331
DENOM = 5429
AUDIO_IDS = 5134

# the ruling. The MAP is untouched -- this pair was already being emitted -- so
# what this batch changed is the second half: the value is now verified.
RULED_KEY = "glaqa"
RULED_VAL = "graka"

# the register forms the ruling rests on, each with the reason it counts. A
# ruling that rests on a gloss must name the form whose OWN gloss carries the
# character (batch 221), so `grkaan` is checked for 監視 specifically and not
# merely for being listed.
SUPPORT_LISTED = {
    "grkaan": "the -an slot; glossed 監視;埋伏 -- his own third word",
    "empgraka": "要埋伏; emp- prefixes the stem WHOLE",
    "spgraka": "讓…去埋伏; sp- prefixes the stem WHOLE",
    "gmraka": "his own sub-form Gmlaqa, dark since before this batch",
}
SUPPORT_GLOSS = ("grkaan", "監視")

# his Gmlaqa must stay dark: it is what carries the identification of the card
# with this root, and without it the head has nothing to be the head OF.
SUPPORT_DARK = "gmraka"

# the trap. `raka` is listed and glossed as a male personal name, and that is the
# ONLY thing `roots('graka')` can reach. If that gloss ever changes, the story
# this log tells about why the ladder refused the head stops being true.
TRAP = "raka"
TRAP_GLOSS = "人名"

# the refusal, in both halves (batch 221)
REFUSED = "psnnai"
# his own line, scan-confirmed at 8x. If this string changes, someone has
# "corrected" a reading the page really carries and the refusal needs re-arguing.
REFUSED_LINE = "psnnai (?)"
# the positive half: the register spells NO form of this syncopated stem
REFUSED_SILENT_PREFIX = "psnm"
# the negative half, as a regex over the whole register rather than a list -- any
# of these arriving is the news that re-opens the refusal
REFUSED_NEGATIVE = re.compile(r"^(psnn?ai|psn?mai|psnamai|nmai)$")

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
    // the PALLOR census is book-wide (batch 222): this batch works the
    // furniture, and a `.truku`-scoped walk cannot see a headword at all
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


def register():
    """The attested type set and its glosses, as the ladder itself reads them."""
    am = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"),
                               encoding="utf-8")))
    ag = json.load(io.open(os.path.join(ORTH, "attested_gloss.json"),
                           encoding="utf-8"))
    return am, ag


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
    am, ag = register()
    fails = []

    print("PAIRS %d / %d = %.4f%%" % (r["ok"], r["tot"],
                                      100.0 * r["ok"] / r["tot"]))
    print("PALE span types %d, pale spans %d (book-wide)"
          % (len(unv), sum(unv.values())))

    # 1 -- the metric. Both items are furniture, so it cannot have moved.
    if r["tot"] != DENOM:
        fails.append(
            "denominator %d, expected %d. A changed denominator means example "
            "rows entered or left, and the FLOOR below is not comparable."
            % (r["tot"], DENOM))
    if r["ok"] < FLOOR:
        fails.append(
            "FLOOR %d: pairs fell to %d. Batch 224 ruled one FURNITURE value "
            "and refused another; neither occurs in an example sentence, so it "
            "could not have moved this. A fall means something else did."
            % (FLOOR, r["ok"]))

    # 2 -- the ruling stands in BOTH tables. The map was already emitting this
    # pair, so a map drift here means someone respelled the card without
    # reading why the colour changed instead.
    if MM.get(RULED_KEY) != RULED_VAL:
        fails.append(
            "map %r now emits %r, not %r. This batch changed a COLOUR, not a "
            "spelling -- the map entry predates it. A new value here needs the "
            "gloss argument redone against the new spelling."
            % (RULED_KEY, MM.get(RULED_KEY), RULED_VAL))
    if RULED_VAL not in V:
        fails.append(
            "%r is not in verified.js, so it renders PALE again. That is the "
            "whole of what batch 224 bought on this card; if the hand ruling "
            "was dropped, the analyser's `raka` peel is deciding the colour."
            % RULED_VAL)
    if RULED_VAL in unv:
        fails.append(
            "%r renders PALE in %d span(s). It was ruled dark; %s"
            % (RULED_VAL, unv[RULED_VAL], SUPPORT_LISTED["grkaan"]))
    if not seen.get(RULED_VAL):
        fails.append(
            "%r renders NOWHERE on the page. It is his GLAQA headword and must "
            "render exactly once; an absence means the card stopped rendering, "
            "not that the ruling is safe." % RULED_VAL)

    # 3 -- FURNITURE: it buys 0 pairs BY CONSTRUCTION, so assert that (batch
    # 223), or a later batch reads the flat metric as a failed seam.
    for w in (RULED_VAL, REFUSED):
        if inTruku.get(w):
            fails.append(
                "%r now occurs in %d `.truku` span(s). It was ruled/refused as "
                "FURNITURE -- zero sentence occurrences -- and that assertion "
                "is what tells the next batch the flat metric is expected."
                % (w, inTruku[w]))

    # 4 -- the register forms the ruling rests on
    for w, why in sorted(SUPPORT_LISTED.items()):
        if w not in am:
            fails.append(
                "%r is no longer in attested_modern.json (%s). The ruling on "
                "%r rests on four listed forms spelling the stem; losing one "
                "means re-counting them before this stands."
                % (w, why, RULED_VAL))
    w, ch = SUPPORT_GLOSS
    if ch not in "".join(ag.get(w) or []):
        fails.append(
            "%r no longer carries %r in its own gloss (now %r). That character "
            "IS the gloss test for this ruling -- it is the third word of his "
            "own 觀察—窺探—監視 -- and without it the ruling rests on shape."
            % (w, ch, ag.get(w)))
    if SUPPORT_DARK in unv or SUPPORT_DARK not in V:
        fails.append(
            "%r is no longer dark. It is his own sub-form Gmlaqa and is what "
            "identifies this card with this root; the head cannot be ruled off "
            "a family the page no longer shows." % SUPPORT_DARK)

    # 5 -- the trap that refused it. Re-assert the REASON, not the outcome.
    if TRAP_GLOSS not in "".join(ag.get(TRAP) or []):
        fails.append(
            "%r is no longer glossed %r (now %r). The account of WHY the "
            "ladder refused %r -- it peels the g and lands on a male personal "
            "name -- depends on that gloss."
            % (TRAP, TRAP_GLOSS, ag.get(TRAP), RULED_VAL))

    # 6 -- the refusal, in both halves
    if REFUSED in V or REFUSED not in unv:
        fails.append(
            "FAIL %s is no longer pale. It was refused because the register "
            "spells no form of the syncopated stem at all and the scan "
            "confirms the string is his -- if either changed, the refusal "
            "needs re-arguing, not overturning in silence." % REFUSED)
    if REFUSED_LINE not in entries_text():
        fails.append(
            "FAIL the paradigm line no longer reads %r. Page 196 was cropped at "
            "8x against the m of psnmaan on the SAME LINE: two legs against "
            "three. The page carries this string, and his (?) is his own doubt."
            % REFUSED_LINE)
    stem = sorted(w for w in am if w.startswith(REFUSED_SILENT_PREFIX))
    if stem:
        fails.append(
            "FAIL the register now spells %d form(s) of the syncopated stem "
            "(%s). Silence about the slot is the POSITIVE half of this "
            "refusal; a form arriving is exactly the news that re-opens it."
            % (len(stem), ", ".join(stem[:6])))
    arrived = sorted(w for w in am if REFUSED_NEGATIVE.match(w))
    if arrived:
        fails.append(
            "FAIL the register now lists %s. The refusal said no -i form of "
            "this root is spelled anywhere; re-open it rather than carrying "
            "this log." % ", ".join(arrived))

    # 7 -- standing invariants. No audio work is permitted until there is a
    # voice, so the id set must be exactly where it was.
    ids = audio_ids()
    if len(ids) != AUDIO_IDS:
        fails.append(
            "audio ids %d, expected %d. An id is a URL: a re-minted id unhooks "
            "a clip already recorded. Nothing in a spelling batch may move "
            "this." % (len(ids), AUDIO_IDS))

    for f in fails:
        print("FAIL " + f if not f.startswith("FAIL") else f)
    print("%d assertions failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
