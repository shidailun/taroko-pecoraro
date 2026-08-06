# -*- coding: utf-8 -*-
"""[batch 228] The analyser's reduplication blindness, priced and then not widened.

His SMUK card, p. 289 (printed 268), sub-form Psmuk:

    Pnsmuk ko daxa ktinox lex xxtlan mo bgixol
    = J'ai cloue deux planches pour en faire une protection (pour arreter le
      vent) contre le vent.
    = 我釘了兩塊木板做擋風的屏障（擋住風）。

`xxtlan` was the SOLE blocker of that pair. `blockers.py` filed it under
`no root`, the class its own preamble calls "not reachable by any argument we
hold" -- 65 types, 74 pairs, never worked. That verdict is an artefact:
`inf.roots()` has no reduplication rule, so EVERY doubled onset reports level 0
whatever the word is. Strip the doubling by hand, as the standing rule says, and
`hhtran` lands on `htran` 阻擋 -- listed, glossed, in the bible.

### The gloss agrees verbatim, which is the test attestation cannot replace

His French is "une protection (pour **arreter** le vent)" and his Chinese is
擋住風. The register's `htran` is 阻擋. Not a shape hit with a plausible gloss --
the same word, in three languages, on both sides.

### Every part is attested; only their crossing is unlisted

    root, bare stem, 8 forms    htra 別阻擋   htran 阻擋   htranay   htrani 去阻擋
                                htraw   htray   htri 要…阻止   htrun 要阻擋…
    hh- instrumental, 120       hhangut 用來煮   hhaqul 用來…搬運   hhabuk 給…用腰帶
    hh- AND -an, 6 stems        hhraan 使長出   hhnian 被…施術   hhlmadan   hhiqan
                                hhmaan   hhuyan

His `xxtlan mo bgixol` is that derivation exactly: "my thing-for-blocking the
wind". Batch 224's slot test is what the third row answers -- `hh-` co-occurring
with `-an` is a real slot spelled for other stems, not a shape invented to tidy
his page. `hhtran` itself is in no wordlist, which is why the value was pale and
why this is `HAND_RULED` and not an attestation claim.

### No rival parse, and no rival root

`tran` is not a register word in ANY shape, so `hhtran` can only be read as
`h-` + `htran`, the ordinary copy of the root's initial consonant. Batch 204's
different-root test finds nothing to respell toward: 屏障 and 遮擋 return zero
register words, and the other 阻擋 root -- `baat`, whose own instrumental `bbaat`
用…阻擋 is listed -- is unreachable from his letters by any correspondence he uses.

### The scan was read, because the token occurs once

Batch 213: a token appearing exactly once in a book that repeats itself is a
candidate for the scan. Page 289 at 5x shows two distinct `x` glyphs, matching
the `x` of `ktinox` and `lex` on the same line. Faithful; `entries.js` untouched.
The map was untouched too -- `charRules("xxtlan")` gives `hhtran` unaided, x>h
and l>r, no letter added or dropped. This batch changed a COLOUR, as batch 224's
`graka` did.

### NOT a widening -- the seam was priced from the DOM first

Teaching `roots()` reduplication was the obvious move and is refused. Of 154 pale
types the entire doubled-onset seam is THREE, and only this one blocks a pair:

    redup+base   3 types   3 spans   1 sole pair    <- ggar, ssapat are furniture
    redup        3 types   3 spans   2 sole pairs   <- no base reached at all
    other      148 types 230 spans  87 sole pairs

One pair does not buy a change to the analyser that could de-verify anywhere.
Batch 217's warning, confirmed by measurement instead of assumed. **The negative
result is the finding**: don't re-open this by widening `roots()`.

    pairs 5331/5429 = 98.1949%  ->  5332/5429 = 98.2133%   (+1)
    pale  236 -> 235 spans, 154 -> 153 types (book-wide)
    sole-blocked pairs 92 -> 91

    python tools/orthography/logs/dom228.py      # site served at :8765
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

FLOOR = 5332
DENOM = 5429
AUDIO_IDS = 5134

RULED = "hhtran"
HIS = "xxtlan"
BASE_WORD = "htran"
BASE_GLOSS = "阻擋"
# his sentence, verbatim: the scan was read at 5x and entries.js is untouched
SENTENCE = "Pnsmuk ko daxa ktinox lex xxtlan mo bgixol"
# the three populations the ruling rests on. Floors, never equality (batch 209).
STEM_FORMS = ("htra", "htran", "htranay", "htrani", "htraw", "htray",
              "htri", "htrun")
HH_FLOOR = 120                  # register words with the hh- instrumental prefix
HH_AN_FLOOR = 6                 # ... of which the -an slot is also spelled
# the negative half: a rival parse or a rival root re-opens the whole argument
NO_RIVAL_PARSE = re.compile(r"^tran")
RIVAL_CHARS = ("屏障", "遮擋")
OTHER_ROOT = "bbaat"            # the other 阻擋 root's instrumental, unreachable
# the seam, priced. A widening is refused; these two must stay furniture.
FURNITURE = ("ggar", "ssapat")

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  let tot = 0, ok = 0;
  const seen = {}, unv = {}, inTruku = {}, sole = {};
  document.querySelectorAll('#results > article.entry').forEach(c => {
    c.querySelectorAll('.truku').forEach(b => {
      const sp = [...b.querySelectorAll(SEL)];
      if (!sp.length) return;
      tot++;
      if (sp.every(s => s.classList.contains('w-mod'))) ok++;
      else {
        const bad = [...new Set(sp.filter(s => !s.classList.contains('w-mod'))
                       .map(s => (s.textContent||'').trim().toLowerCase()))];
        if (bad.length === 1) sole[bad[0]] = (sole[bad[0]] || 0) + 1;
      }
    });
    c.querySelectorAll(SEL).forEach(s => {
      const t = (s.textContent || '').trim().toLowerCase();
      seen[t] = (seen[t] || 0) + 1;
      if (s.classList.contains('w-unv')) unv[t] = (unv[t] || 0) + 1;
      if (s.closest('.truku')) inTruku[t] = (inTruku[t] || 0) + 1;
    });
  });
  return {tot: tot, ok: ok, seen: seen, unv: unv, inTruku: inTruku,
          sole: sole}; }"""


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
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def verified():
    t = io.open(os.path.join(SITE, "verified.js"), encoding="utf-8").read()
    return dict((m.group(1), int(m.group(2)))
                for m in re.finditer(r'^  "(.+?)": (\d+),?$', t, re.M))


def register():
    L = lambda n: json.load(io.open(os.path.join(ORTH, n), encoding="utf-8"))
    return set(L("attested_modern.json")), L("attested_gloss.json")


def gloss(AG, w):
    g = AG.get(w) or []
    return g if isinstance(g, list) else [g]


def char_rules(w):
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
    seen, unv, itk, sole = d["seen"], d["unv"], d["inTruku"], d["sole"]
    print("pairs %d/%d = %.4f%%" % (ok, tot, 100.0 * ok / tot))
    print("pale span types %d   pale spans %d   sole-blocked pairs %d"
          % (len(unv), sum(unv.values()), sum(sole.values())))

    # --- 1. the metric. This batch BOUGHT a pair, so the floor moved up
    if tot != DENOM:
        fail("DENOM %d got %d" % (DENOM, tot))
    if ok < FLOOR:
        fail("FLOOR %d got %d" % (FLOOR, ok))

    MM, V = modern_map(), verified()
    AM, AG = register()

    # --- 2. the ruling landed: dark on the page, in verified.js, in a SENTENCE.
    # Unlike batch 227 this is NOT furniture -- it must be inside a .truku box,
    # or it bought nothing and the +1 came from somewhere else.
    if unv.get(RULED):
        fail("%s renders pale %d times; the ruling is not in effect"
             % (RULED, unv[RULED]))
    if seen.get(RULED, 0) == 0:
        fail("%s renders nowhere at all" % RULED)
    if RULED not in V:
        fail("%s left verified.js; HAND_RULED is where the ruling lives" % RULED)
    if itk.get(RULED, 0) < 1:
        fail("%s is in no .truku box -- it cannot have bought the pair" % RULED)
    if sole.get(RULED):
        fail("%s still sole-blocks %d pairs" % (RULED, sole[RULED]))

    # --- 3. the spelling itself. The map entry is inert by construction here:
    # charRules gives the same string unaided, so the value cannot drift without
    # BOTH the map and the char rules changing. Assert both.
    if MM.get(HIS) != RULED:
        fail("MAP %s -> %s got %s" % (HIS, RULED, MM.get(HIS)))
    if char_rules(HIS) != RULED:
        fail("char_rules(%s) should give %s unaided, got %s"
             % (HIS, RULED, char_rules(HIS)))

    # --- 4. his sentence, unchanged. The scan was read; entries.js is untouched
    if SENTENCE not in entries_text():
        fail("his Psmuk sentence has changed; the scan reading was: %s" % SENTENCE)

    # --- 5. the positive half: the root, its gloss, and the two populations
    if BASE_WORD not in AM or not any(BASE_GLOSS in x for x in gloss(AG, BASE_WORD)):
        fail("%s no longer carries %s -- the gloss test that ruled this is gone"
             % (BASE_WORD, BASE_GLOSS))
    missing = [w for w in STEM_FORMS if w not in AM]
    if missing:
        fail("the bare stem has lost forms: %s (the ruling cited all 8)" % missing)
    hh = [w for w in AM if w.startswith("hh")]
    if len(hh) < HH_FLOOR:
        fail("hh- population %d, floor %d -- the instrumental prefix argument "
             "was made on 120 words" % (len(hh), HH_FLOOR))
    hh_an = [w for w in hh if w.endswith("an")]
    if len(hh_an) < HH_AN_FLOOR:
        fail("hh-...-an slot spelled for %d stems, floor %d -- batch 224's slot "
             "test is what makes this shape a real slot" % (len(hh_an), HH_AN_FLOOR))
    if OTHER_ROOT not in AM:
        fail("%s has left the register; the different-root half needs re-arguing"
             % OTHER_ROOT)

    # --- 6. the negative half. A rival parse or a rival root re-opens the ruling
    rival = sorted(w for w in AM if NO_RIVAL_PARSE.match(w))
    if rival:
        fail("NEGATIVE a rival parse is now listed: %s -- `hhtran` could be "
             "hh- + that, and the h- + htran reading is no longer forced" % rival)
    for ch in RIVAL_CHARS:
        hit = sorted(w for w in AM if any(ch in g for g in gloss(AG, w)))
        if hit:
            fail("NEGATIVE %s is now carried by %s -- a rival root for his "
                 "meaning re-opens batch 204's test" % (ch, hit[:4]))

    # --- 7. the widening stays refused, and the seam stays small. If either of
    # these two ever blocks a pair, the price of teaching roots() reduplication
    # changes and the refusal above has to be re-argued.
    for w in FURNITURE:
        if sole.get(w) or itk.get(w):
            fail("%s now blocks %s pairs / sits in %s .truku boxes -- the seam "
                 "was priced at 1 pair and the widening refused on that"
                 % (w, sole.get(w, 0), itk.get(w, 0)))

    # --- 8. audio. Blocked pending a voice; an id is a URL (batch 219)
    n = len(audio_ids())
    if n != AUDIO_IDS:
        fail("AUDIO ids %d, pinned at %d" % (n, AUDIO_IDS))

    print("\n%d assertions failed" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
