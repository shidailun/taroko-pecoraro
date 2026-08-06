# -*- coding: utf-8 -*-
"""[batch 225] The last member of one root still standing on a dog's name.

His KUBWI card is *Ombrager - étouffer (la végétation)* / 遮蔽－（植物）悶死、
壓過, tagged `(KBUI ?) (R. = BUYO ?)`. He names his own root: BUYO. And on the
BUYO card, five slots over, sits the same lexeme carded a second time --
`Pkbuyo` 使荒蕪——遮蔭——悶住（使窒息）, his own paradigm `°Pkbuyo, .?. ,
pkbuyan, pkbuyun`.

The BUYO card has been ruled twice already:

    batch 49   Pkbuyo 使荒蕪－遮蔭 -> pkbuyu          (b49.py:28, manual_map:1064)
    batch 201  Kmubui (kmbui ?)  -> kmbuyu BOTH     (HAND_RULED, inflection:2121)

and `loose179.py:86` records the second one, including the rendering consequence
that recurs below. So seven of the ten spellings this root reaches were already
on the `buyu`/`kbuy-` stem before this batch:

    BUYO -> buyu 3     Pkbuyo -> pkbuyu 2     pkbuyan 2     pkbuyun 2
    Kmubui, kmbui -> kmbuyu 1                 his own `kbuyun` in a sentence, 6

The three that were not are the whole of the OTHER card:

    KUBWI  -> kubuy    DARK 1   tier B      <- a projection, and a dog's name
    KBUI   -> kbui     PALE     tier M      <- identity: "no modern form found"
    Knubwi -> knubuy   PALE     tier P      <- projected OFF the dog's name

That is batch 223's sibling seam (`inflection.py:1670`) spanning two CARDS
instead of two slots. Batch 49 ruled the stem on one card, batch 201 ruled
another slot of it, and the head on the second card kept a tier-B shape
projection nobody had asked the gloss about.

### The freeze

`kubuy` IS listed. Its only gloss, in `attested_gloss.json` and nowhere else, is
**狗名** -- a dog's name. Bible gloss: absent. Parquet: one occurrence, under the
universal `>= 2` bar. Zero character overlap with his 遮蔽／悶死／壓過. So the
span was DARK AND WRONG in batch 201's exact sense, and invisible to every
colour metric because the span was already dark.

**A name gloss does not by itself convict, and that was tested first.** Over all
1,967 entries, 41 dark map values are glossed ONLY as a name in the register
while their card's Chinese shares no character with it -- `harung` 松樹,
`sudu` 雜草, `waray` 線, `pajiq` 蔬菜, `putuh` 截斷, `urung` 角. Truku personal
names ARE ordinary words and `attested_gloss.json` often carries only the name
row; four of the eight sampled have a second source giving the everyday meaning
(bible `pajiq` 蔬菜；青菜, `urung` 角, `putuh` 斷絕; parquet `sudu` 垃圾,
`waray` 麵). The class is a NEGATIVE RESULT -- do not sweep it. What separates
`kubuy` from all 41 is that it has no second source at all AND its own root is
already spelled seven other ways in the same book.

### The positive half, on the form whose own gloss carries it (batch 221)

`kbuyu` is LISTED, glossed 都是草叢. Zero character overlap with his gloss too --
which is why no overlap instrument ever surfaced this card, exactly as in batch
223's XOIL. The argument is not overlap; it is that the project's OWN ladder has
already matched his gloss to this root, mechanically, on his other card:

    inf.regular('pkbuyu') == ('kbuyu', 'p', '', 'p', '荒蕪=草叢')

That fifth element is the gloss evidence, and it is what makes his `Pkbuyo` dark
today. His 使荒蕪 is `kbuyu`'s 草叢 by the project's own test, and his KUBWI
gloss 遮蔽－悶死、壓過 is the same lexeme's -- he wrote the two cards for one
word. `kmbuyu` (his `Kmubui`) is the AF of the same root, hand-ruled in batch
201, and its perfective `kmnbuyu` 看成…草 is listed.

**And the correspondence was already ruled, inside this same root.** His `-UI` /
`-WI` answering modern `-UYU` is not proposed here: batch 201 sent BOTH his
`Kmubui` and his `kmbui` to `kmbuyu`, on the sibling sub-form of the card his own
tag names as the root. `kubwi -> kbuyu` and `kbui -> kbuyu` are the same
alternation applied to the head. Batch 215's test — did he have a spelling for
this shape, and did he use it elsewhere — answers yes, in his own hand, twice.

The different-root test (batch 204) does not refuse: the register's 遮蔽／覆蓋
family is 63 words strong (`bubung`, `hlakuk`, `haur`, `gumuk`, `sasaw`, `pix`
...) and not one is reachable from his spelling by any correspondence he uses --
but they are all a DIFFERENT root, whereas `kbuyu` is the root HE NAMES.

### `collapsed()` drops the bracket, and that is the precedent too

With `kbui` sending to `kbuyu` as well, the card's tag no longer renders
`(KBUI ?)` -- `collapsed()` (app.js:484) drops a bracket that would read
"Kbuyu (kbuyu?)", a variant note distinguishing a word from itself. That is not
a side effect of this batch; `loose179.py:86` records the identical thing
happening to `Kmubui (kmbui ?)` in batch 201. **The app itself now says the two
spellings are one word**, which is what his `(KBUI ?)` claims. One span leaves
the book: 6,485 -> 6,484 span types.

### `knbuyu` REFUSED -- pale before, pale after (batch 215 shape, batch 220 rule)

`Knubwi` is "同上之動詞形", the -n- infix on his head, and the map sent it to
`knubuy` -- which decomposes off the dog name (`roots('knubuy')` is
`('kubuy','','','infix')`). Batch 223's rule: ask what the value you are
REPLACING decomposes to. So it is repinned onto the stem, `knbuyu`, and it is
NOT a claim: `regular()` and `no_chinese()` both return None, it does not enter
`verified.js`, and it renders PALE before and after.

**Assert the negative half.** The register spells the kn- form of this root
exactly one way -- `knbbuyu` 長滿草叢 -- and it is REDUPLICATED, which his
`Knubwi` is not. There is no `knbuyu` and no unreduplicated kn- form anywhere.
Inventing one to tidy the paradigm would be the metric deciding the spelling.
If an unreduplicated form ever enters the register, that is the news that
re-opens this.

### The pairs

**Zero, by construction, and it is asserted below.** His headword, his tag and
his sub-form name are in `.hw` / `.sub-form`, in no `.truku` box, so a value
ruled there cannot move the denominator (batch 223). The card's one sentence
runs `... kbuyun na kana ka oqon so`, whose every span was already dark --
including his own `kbuyun`, which is what proves the stem is his.

    metric   5331 / 5429 = 98.1949%   unchanged
    pallor   154 -> 153 span types, 236 -> 235 spans (book-wide, batch 222)

    python tools/orthography/logs/dom225.py      # site served at :8765
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SITE = os.path.join(ROOT, "site")
ORTH = os.path.join(ROOT, "tools", "orthography")
BASE = "http://127.0.0.1:8765/"

FLOOR = 5331
DENOM = 5429
AUDIO_IDS = 5134

# the ruling: his three keys, all onto the stem he names as his own root
RULED = {"kubwi": "kbuyu", "kbui": "kbuyu", "knubwi": "knbuyu"}
STEM = "kbuyu"
STEM_GLOSS = "草叢"
# the freeze that was removed: no map key may send to it again
FREEZE = "kubuy"
FREEZE_GLOSS = "狗名"
# the family that was already on the stem before this batch
SUPPORT_DARK = ("buyu", "pkbuyu", "kmbuyu", "kbuyun")
# the refusal: pale before, pale after, and the register's silence
REFUSED = "knbuyu"
REFUSED_LISTED_KN = "knbbuyu"
# an UNreduplicated kn- form of this root arriving is what re-opens it
REFUSED_NEGATIVE = re.compile(r"^kn(?:u)?buy(?:u|un|an)?$")

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
    // the PALLOR census is book-wide (batch 222): this batch works a HEADWORD,
    // a TAG and a SUB-FORM NAME, none of which is inside any `.truku` box
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
    L = lambda n: json.load(io.open(os.path.join(ORTH, n), encoding="utf-8"))
    return set(L("attested_modern.json")), L("attested_gloss.json")


def measure():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(BASE)
        pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
        pg.goto(BASE + "?q=%CC%81")
        pg.wait_for_timeout(22000)
        d = pg.evaluate(JS)
        b.close()
    return d


def main():
    bad = []

    def fail(msg):
        bad.append(msg)
        print("FAIL " + msg)

    d = measure()
    tot, ok = d["tot"], d["ok"]
    seen, unv, itk = d["seen"], d["unv"], d["inTruku"]
    print("pairs %d/%d = %.4f%%" % (ok, tot, 100.0 * ok / tot))
    print("pale span types %d   pale spans %d   span types %d"
          % (len(unv), sum(unv.values()), len(seen)))

    # --- 1. the metric. A furniture batch must not move it in either direction
    if tot != DENOM:
        fail("DENOM %d got %d" % (DENOM, tot))
    if ok < FLOOR:
        fail("FLOOR %d got %d" % (FLOOR, ok))
    if ok != FLOOR:
        print("NOTE pair count %d is above the pinned floor %d" % (ok, FLOOR))

    MM, V = modern_map(), verified()

    # --- 2. the ruling is in the map, and the freeze is gone from ALL of it
    for k, v in sorted(RULED.items()):
        if MM.get(k) != v:
            fail("MAP %s -> %s got %s" % (k, v, MM.get(k)))
    back = sorted(k for k, v in MM.items() if v == FREEZE)
    if back:
        fail("FREEZE %s reinstated as the value of %s" % (FREEZE, back))

    # --- 3. the stem is verified and renders DARK, and it renders at ALL
    if STEM not in V:
        fail("BROWN %s absent from verified.js" % STEM)
    if not seen.get(STEM):
        fail("BROWN %s renders nowhere" % STEM)
    if unv.get(STEM):
        fail("BROWN %s pale on %d spans" % (STEM, unv[STEM]))
    # collapsed() drops the "(KBUI ?)" bracket, so the head renders it ONCE
    if seen.get(STEM) != 1:
        fail("COLLAPSE %s renders %d times, expected 1 (app.js:484 drops the "
             "bracket that would read \"Kbuyu (kbuyu?)\")" % (STEM, seen.get(STEM)))

    # --- 4. FURNITURE: this batch buys 0 pairs BY CONSTRUCTION (batch 223)
    for w in sorted(set(RULED.values())):
        if itk.get(w):
            fail("FURNITURE %s inside a .truku box on %d spans -- this ruling "
                 "was priced at 0 pairs" % (w, itk[w]))

    # --- 5. the support. The family this batch made the head agree with
    am, ag = register()
    if STEM not in am:
        fail("SUPPORT %s no longer listed" % STEM)
    if STEM_GLOSS not in "".join(ag.get(STEM) or []):
        fail("SUPPORT %s lost %s from its gloss (%s)"
             % (STEM, STEM_GLOSS, "".join(ag.get(STEM) or []) or "-"))
    for w in SUPPORT_DARK:
        if w not in V:
            fail("SUPPORT %s absent from verified.js" % w)
        if unv.get(w):
            fail("SUPPORT %s went pale on %d spans" % (w, unv[w]))
    # the ladder's own gloss match is the positive half -- re-derive it
    sys.path.insert(0, ORTH)
    import inflection as I
    inf = I.Inflection(am, MM)
    r = inf.regular("pkbuyu")
    if not r or r[0] != STEM:
        fail("SUPPORT regular('pkbuyu') no longer derives off %s: %s" % (STEM, r))

    # --- 6. the trap. WHY the map was wrong, re-asserted (batch 221)
    g = "".join(ag.get(FREEZE) or [])
    if FREEZE not in am:
        fail("TRAP %s no longer listed -- the account of the freeze has changed"
             % FREEZE)
    if FREEZE_GLOSS not in g:
        fail("TRAP %s no longer glossed %s (%s) -- re-argue the freeze"
             % (FREEZE, FREEZE_GLOSS, g or "-"))
    if re.search(r"[遮蔽悶壓]", g):
        fail("TRAP %s gained his meaning (%s) -- this re-opens the ruling"
             % (FREEZE, g))

    # --- 7. the refusal, in both halves (batch 220)
    if REFUSED in V:
        fail("REFUSED %s entered verified.js -- it was pinned as a consistency "
             "fix, NOT a claim; pale before, pale after" % REFUSED)
    if not unv.get(REFUSED):
        fail("REFUSED %s no longer renders pale (seen %d)"
             % (REFUSED, seen.get(REFUSED, 0)))
    if REFUSED_LISTED_KN not in am:
        fail("REFUSED the register lost %s, the ONLY kn- form of this root"
             % REFUSED_LISTED_KN)
    arrived = sorted(w for w in am if REFUSED_NEGATIVE.match(w))
    if arrived:
        fail("REFUSED an unreduplicated kn- form arrived in the register: %s "
             "-- that is the news that re-opens this refusal" % arrived)

    # --- 8. audio. Nothing is voiced until the text is at 100 and there is a
    # voice; an id is a URL and a re-minted one unhooks a paid-for clip.
    n = len(audio_ids())
    if n != AUDIO_IDS:
        fail("AUDIO %d ids, expected %d" % (n, AUDIO_IDS))

    print("%d assertions failed" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
