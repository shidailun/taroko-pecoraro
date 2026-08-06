# -*- coding: utf-8 -*-
"""[batch 227] The dark sibling batch 221 said his SA'MUL card did not have.

His SA'MUL card is *Tenir (un bébé) dans ses bras* / 把（嬰兒）抱在懷裡－抱著
孩子, tagged `(S'MUL ?) (R)`, with one sub-form `Sn'mul (sma'mul)` 同上之動詞形.

Batch 221 worked the PALE side of this card for pairs and refused it in writing
(`dom221.py:132-133`):

    "smmul": his SA'MUL 抱在懷裡 is carried by kmeabuh, verbatim, off abuh;
             the nearest samul-shaped words are smulus 拉著 and smuling 汙辱
    "snmul": same card as smmul, and the whole card is pale head included --
             there is no dark sibling to reason from

**That refusal stands, and nothing here overturns it.** What this batch changes
is the one clause in it that was not true. The card was not pale throughout: his
own bracketed variant rendered DARK, on a word from a different card entirely.

    SA'MUL   -> samul    PALE   tier M   elision dropped, `l` kept
    S'MUL    -> smur     DARK   tier B   <- 濕冷
    Sn'mul   -> snmul    PALE   tier P   elision dropped, `l` kept
    sma'mul  -> smamul   PALE   tier P   elision dropped, `l` kept

### Three independent arguments, and they agree

**1. The tier and the bar.** `s'mul -> smur` is tier **B**, a shape projection
that was never asked for a gloss -- the same tier batch 218 reverted for `mqlaq`
and batch 225 for `kubuy`. `smur` is glossed 濕冷 in `attested_gloss.json` and
appears in NO other source: bible 0, parquet 0, edictionary 0, so it stands
under the universal `>= 2` bar. 濕冷 shares no character with 把（嬰兒）抱在懷裡
－抱著孩子. Dark AND wrong, in batch 201's exact sense.

**2. His tag shape.** `(S'MUL ?)` names another SPELLING of the headword, not a
posited root, so batch 200's parenthetical rule applies and batch 223's tag-shape
test lets it in. But batch 200 refused 7 of its own 17 for exactly this reason:
*the dark side still has to pass the gloss test*, and following a dark value that
is dark on a homograph spreads the freeze. This is the MIRROR shape -- his HEAD
is the pale one -- so the fix runs the other way: the dark side comes down to
where the head already is.

**3. A char-rule contradiction inside one root (batch 201).** `l -> r` fires on
this one slot of a card whose other three slots all keep the `l`. Batch 201's
rule says that is a bug, not a variant, and the siblings decide it. They are
unanimous: `samul`, `snmul`, `smamul`.

### The positive half, and the negative half

The register carries his meaning on a DIFFERENT root, so batch 204 says there is
nothing to respell toward and the pallor is correct: **39 words are glossed 抱**
and every one of them is `abuh`/`eabuh` (`kmeabuh` 帶種子袋;挖成窪地;抱在懷裡 is
his gloss verbatim), plus `duuy` 持, `jijil`, `qrapu` 擁抱, `hiyug`. Nothing
shaped like his. So there is no rival value for `s'mul`, and the entry is pinned
to his own letters instead: `smul`, unattested, PALE.

**The pin is load-bearing** exactly as batch 218's `mqlaq -> mqlaq` was:
`charRules("s'mul")` spells `smur` on its own, so DELETING the entry would put
the freeze's own string back on the page as a green span. Pale is the honest
colour -- we know his family's convention for the shape and have no attestation
for it.

Negative half, asserted below as a regex over the register: if any word of this
shape ever turns up glossed 抱, that is the news that re-opens both this and
batch 221's refusal of `snmul`.

### The pairs

**Zero, by construction, and asserted.** `s'mul` occurs exactly once in the whole
book -- in his TAG on SA'MUL -- and a tag is in no `.truku` box (batch 223), so
this cannot move the denominator. Priced from the DOM, not from the table
(batch 218): `smur` rendered 1 span, `inTruku` 0.

`snmul` keeps its one `.truku` occurrence, in `Msnulu bi mstlong xea ludan ka
sn'mul madas laqe na` on his SNULU card, where it is the SOLE blocker. That pair
stays lost, and batch 221 is why.

    metric   5331 / 5429 = 98.1949%   unchanged
    pallor   153 -> 154 span types, 235 -> 236 spans (book-wide, batch 222)
             a freeze removal can only ever LOOK like a regression

    python tools/orthography/logs/dom227.py      # site served at :8765
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

# the ruling: his bracketed variant comes down onto his own letters
RULED = {"s'mul": "smul"}
# the freeze that was removed: no map key may send to it again
FREEZE = "smur"
FREEZE_GLOSS = "濕冷"
# the card, after: four spellings of one root, all pale, all keeping the `l`
CARD = ("smul", "samul", "snmul", "smamul")
# batch 221's refusal, which this batch does NOT overturn
REFUSED = "snmul"
REFUSED_INTRUKU = 1          # the SNULU sentence it still blocks, sole blocker
# his meaning, on the different root that carries it (batch 204/221)
OTHER_ROOT = "kmeabuh"
OTHER_CHAR = "抱"
# a word of HIS shape turning up glossed 抱 re-opens both refusals
NEGATIVE = re.compile(r"^s(?:m?a|n|ma)?mul$")

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
    // the PALLOR census is book-wide (batch 222): this batch works a TAG
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


def sources():
    """The second-source test: the `>= 2` bar that convicted kubuy in 225."""
    out = {}
    for n in ("bible_gloss.json", "parquet_gloss.json", "edictionary_trv.json"):
        p = os.path.join(ORTH, n)
        out[n] = json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return out


def char_rules(w):
    """app.js's fallback, on the folded key. It spells the freeze unaided."""
    k = re.sub("[’ʼ\"ʔ']", "", w.lower()).replace("ł", "l")
    return "".join({"x": "h", "o": "u", "l": "r"}.get(c, c) for c in k)


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
    AM, AG = register()

    # --- 2. the ruling is in the map, and the freeze is gone from ALL of it
    for k, v in sorted(RULED.items()):
        if MM.get(k) != v:
            fail("MAP %s -> %s got %s" % (k, v, MM.get(k)))
    back = sorted(k for k, v in MM.items() if v == FREEZE)
    if back:
        fail("FREEZE %s reinstated as the value of %s" % (FREEZE, back))
    if FREEZE in V:
        fail("FREEZE %s is back in verified.js, so some key still emits it"
             % FREEZE)

    # --- 3. the pin is LOAD-BEARING: charRules spells the freeze on its own,
    # so deleting the entry would put the freeze's string back as a green span
    if char_rules("s'mul") != FREEZE:
        fail("char_rules(s'mul) should still spell %s, got %s"
             % (FREEZE, char_rules("s'mul")))

    # --- 4. the card is coherent: four spellings of one root, every one pale,
    # every one keeping his `l`. A value going dark here is a NEW claim and
    # wants its own batch; a value going green means the pin was deleted.
    for w in CARD:
        if w.endswith("r") or "mur" in w:
            fail("CARD %s has taken the char rule's `r`" % w)
        if w in V:
            fail("CARD %s entered verified.js -- the consistency fix has "
                 "become a claim" % w)
        if seen.get(w, 0) == 0:
            fail("CARD %s renders nowhere; the map entry is not firing" % w)
        elif unv.get(w, 0) != seen.get(w, 0):
            fail("CARD %s renders %d spans of which only %d are pale"
                 % (w, seen.get(w, 0), unv.get(w, 0)))

    # --- 5. FURNITURE: 0 pairs by construction (batch 223). His tag is in no
    # `.truku` box, so this ruling CANNOT have moved the denominator.
    if itk.get("smul", 0) != 0:
        fail("FURNITURE smul is inside a .truku box %d times -- this batch "
             "claimed 0 pairs by construction" % itk["smul"])

    # --- 6. the freeze account. `smur` is still a real word with a gloss that
    # is still nothing to do with his card, and still has no second source.
    g = AG.get(FREEZE) or []
    g = g if isinstance(g, list) else [g]
    if FREEZE not in AM:
        fail("%s has left the register; the account of WHY it was a freeze "
             "no longer holds" % FREEZE)
    if not any(FREEZE_GLOSS in x for x in g):
        fail("%s no longer carries %s; re-argue the freeze" % (FREEZE, FREEZE_GLOSS))
    if any(OTHER_CHAR in x for x in g):
        fail("%s has gained %s -- it may be his word after all" % (FREEZE, OTHER_CHAR))
    second = sorted(n for n, s in sources().items() if FREEZE in s)
    if second:
        fail("%s now has a second source (%s): it clears the >= 2 bar and the "
             "conviction has to be re-argued" % (FREEZE, second))

    # --- 7. batch 221's refusal is NOT overturned, in both halves
    if REFUSED in V:
        fail("REFUSED %s entered verified.js; batch 221 refused it in writing "
             "(dom221.py:133) and no new evidence was offered" % REFUSED)
    if itk.get(REFUSED, 0) != REFUSED_INTRUKU:
        fail("REFUSED %s now has %s .truku occurrences, pinned at %d"
             % (REFUSED, itk.get(REFUSED, 0), REFUSED_INTRUKU))
    og = AG.get(OTHER_ROOT) or []
    og = og if isinstance(og, list) else [og]
    if OTHER_ROOT not in AM or not any(OTHER_CHAR in x for x in og):
        fail("the positive half is gone: %s no longer carries %s, so the "
             "different-root refusal needs re-arguing" % (OTHER_ROOT, OTHER_CHAR))
    # the NEGATIVE half, as a regex over the whole register (batch 221)
    arrived = sorted(w for w in AM if NEGATIVE.match(w))
    if arrived:
        fail("NEGATIVE a word of his shape is now listed: %s -- this re-opens "
             "batch 221's refusal and this batch's pin" % arrived)

    # --- 8. audio. Blocked pending a voice; an id is a URL (batch 219)
    n = len(audio_ids())
    if n != AUDIO_IDS:
        fail("AUDIO ids %d, pinned at %d -- nothing in a spelling batch may "
             "touch the audio wiring" % (n, AUDIO_IDS))

    print("\n%d assertions failed" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
