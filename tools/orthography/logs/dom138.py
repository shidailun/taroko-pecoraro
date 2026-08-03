# -*- coding: utf-8 -*-
"""Batch 138: the ILRDF name registry, gated to the name population.

    https://indigenous-name.ilrdf.org.tw/#/searchView?zuqunId=13&zuName=太魯閣族

No wordlist has a reason to hold a personal name, which is why tier N was the
one population where every spelling was a guess and every word stayed pale
forever. The Council of Indigenous Peoples has digitized the register — 1,792
Truku names, each with its 男名 / 女名 / 男女共名 type and a recording of a
speaker saying it — so `build_verified.py` now widens `seen` with it, at level 1
(LISTED), exactly as it does with the parquets. Harvested once by
`fetch_ilrdf_names.py`; the output is committed and the build never touches the
network.

**The gate is the whole design, and this file's load-bearing half tests it.**
The registry is matched only against the values the NAME POPULATION puts on
screen — his own `name (m)`/`name (f)` tags (minus the jp names and minus the
tokens that are also some entry's headword) plus whatever tier N admitted,
exported by the map builder as `name_population.json`. Ungated, plain string
matching against 1,792 names also clears 21 pale types that are not names on
this page at all: `tabu` is his 餵養 root, `aku`, `mici`, `taya`, `urang`,
`burung`, `satu`, `bulu` are ordinary words that happen to be spelled like
somebody. A registry of names is evidence about names.

So:

  GAIN — 61 values / 189 occurrences, every one a name, must now be dark
         everywhere they appear.
  KEEP — the 21 registered-but-refused values must still be PALE. If the gate
         ever reads the registry as a wordlist, these are what fall first.
  JP   — `boro`, `mori`, `xalo` are `name (.., jp)`, excluded from the name
         population by design (his Japanese romanization is a different system,
         tier J's question, not tier N's). Still pale.
  MISS — `liwis` 38, `ingay` 24, `lauken` 22, `akit` 10 are the heaviest names
         the register does NOT hold. Still pale, and they are the honest answer:
         the outside source was asked and did not know.
         **SUPERSEDED BY BATCH 144**, which is the answer to "did not know": a
         register of Truku GIVEN names cannot hold a Japanese loan or a place,
         so requiring it was a test they could never pass. The population is now
         the only gate and these four are dark. The assertion below is inverted,
         not deleted. `eku` and `mici` move out of KEEP with them — both are in
         HAND_NAMES, named by hand as this page's people.
  FIX  — nine names the register spells differently, applied to `manual_map.json`
         and asserted here in both directions. The rule is stated in that file's
         `_ilrdf_names` key: his form absent from the register, exactly one
         registered name one letter away, that name's 男名/女名 type agreeing with
         his own tag, and the letter a correspondence this book documents. The
         old spelling must appear nowhere on the page.

`upix` is the one that indicts the tier rather than the map. His token is `opiç`,
and this book's own first rule is that **his ç is modern x** — tier N applied
x→h to it anyway and printed `upih`. The register agrees with his ç, not with
the tier. `maruy` is the documented order working: the name freeze exists to stop
l→r renaming a man, and here the register says the man really is Maruy, so
outside evidence outranks the freeze exactly as attestation does.

Census after: dark 42,099 / pale 2,334 / green 32 = 94.6790%, 1,967 cards, 0
page errors in both modes (`census137.py`, whose baseline predates commit
098b28f — 14 of the occurrences it shows moving are that batch's six affix
letters, not this one's names).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# the 61 values the registry cleared, with the pale occurrences each had
GAIN = {
    "mikat": 33, "sikat": 16, "tatu": 14, "talan": 13, "imin": 12, "tain": 11,
    "utun": 10, "sitang": 7, "aman": 6, "aput": 4, "cibi": 4, "akin": 3,
    "masa": 3, "patung": 3, "kimi": 2, "pinang": 2, "sasak": 2, "akang": 1,
    "amay": 1, "ami": 1, "apit": 1, "asin": 1, "atang": 1, "atu": 1,
    "bakan": 1, "butung": 1, "daway": 1, "duka": 1, "dura": 1, "habaw": 1,
    "ici": 1, "ipin": 1, "iping": 1, "isat": 1, "iyung": 1, "kitan": 1,
    "kutan": 1, "makat": 1, "masay": 1, "masing": 1, "mihang": 1, "muna": 1,
    "nunung": 1, "payan": 1, "pitung": 1, "pusing": 1, "sigi": 1, "simi": 1,
    "siri": 1, "siyal": 1, "tami": 1, "tuli": 1, "tunung": 1, "ubin": 1,
    "udang": 1, "ukah": 1, "umat": 1, "unaw": 2, "yawas": 1, "yukung": 1,
    "yuyu": 1,
}
# `unaw` was 1 here when this batch ran; batch 140 put his UNAQ on the same
# registered name, so it is 2 now. Raised rather than pinned, because the point
# of the assertion is that every occurrence is dark, not that the count froze.

# registered names that are NOT this page's names — the gate must refuse them.
# The gate that refuses them is the NAME POPULATION, which is what batch 144
# kept when it dropped the registry intersection; these are still the homograph
# class and must still be pale.
KEEP = {
    "tabu": 5, "butang": 3, "urang": 2, "satu": 2,
    "nuli": 2, "iyak": 2, "ayuq": 2, "turu": 1, "tapak": 1,
    "sugi": 1, "sabung": 1, "muli": 1, "miru": 1, "kuy": 1, "emi": 1,
    "burung": 1, "bulu": 1, "aku": 1,
}

# his Japanese names
JP = {"boro": 2, "mori": 1, "xalo": 1}

# SUPERSEDED BY BATCH 144. `eku` and `mici` were in KEEP and `liwis`, `ingay`,
# `lauken`, `akit` in MISS, on the same rule from opposite sides: this batch
# admitted a name only if the ILRDF registry listed it. Batch 144 dropped that
# intersection — the registry cannot spell a Japanese loan or a place name, and
# `eku`/`mici` are in HAND_NAMES, i.e. named by hand as this page's people. The
# assertion is kept and inverted rather than deleted, so a revert shows up here.
SUPERSEDED_144 = {"eku": 5, "mici": 2,
                  "liwis": 38, "ingay": 24, "lauken": 22, "akit": 10}

# SUPERSEDED BY BATCH 164, and it left KEEP by a door this batch was not looking
# at. `taya` was held pale here as a name the register does not list; it is dark
# now at rung 6, `no_chinese` — the rung for a word he glosses in French only.
# Batch 164 ruled that an empty candidate list is not a refusal, and `taya` had
# an empty one. Nothing about the NAME question moved: the register still does
# not list it, and if it ever goes dark as a name rather than as a gloss this
# assertion is where that shows up. Inverted, not deleted, exactly as above.
SUPERSEDED_164 = {"taya": 2}

# the register's own spelling, applied — dark now, and his old form gone
# `kumu` is 2 because he writes the name twice, `komu` and `komù`, and only the
# first was the identity claim this batch overturned — the accented twin was
# already on `kumu` through tier R. The two now agree, which is what tier V asks
# of a pair his marks split into different keys.
FIX = {"lubyak": 20, "upix": 7, "pidu": 4, "ihing": 3, "sidu": 1, "pilih": 1,
       "kumu": 2, "maruy": 1, "taylung": 1}
WAS = ["lubyaq", "upih", "pido", "iheng", "sido", "pileh", "komu", "maluy",
       "tailung"]

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
    """Every occurrence of each value must wear `colour`, and the count must
    match what the census measured — a value that half-moved is as wrong as one
    that did not move."""
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
    gain = pg.evaluate(SPANS, sorted(GAIN))
    keep = pg.evaluate(SPANS, sorted(KEEP))
    jp = pg.evaluate(SPANS, sorted(JP))
    sup = pg.evaluate(SPANS, sorted(SUPERSEDED_144))
    s164 = pg.evaluate(SPANS, sorted(SUPERSEDED_164))
    fix = pg.evaluate(SPANS, sorted(FIX))
    was = pg.evaluate(SPANS, sorted(WAS))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(keep, KEEP, "pale", "KEEP")
check(jp, JP, "pale", "JP")
check(sup, SUPERSEDED_144, "dark", "SUPERSEDED_144")
check(s164, SUPERSEDED_164, "dark", "SUPERSEDED_164")
check(fix, FIX, "dark", "FIX")
for w in WAS:
    if was.get(w):
        fail.append("WAS %s: his old spelling still on the page as %s"
                    % (w, was[w]))

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("GAIN %d values / %d occurrences now dark" % (len(GAIN), sum(GAIN.values())))
print("KEEP %d registered values the gate refuses, still pale (%d occ)"
      % (len(KEEP), sum(KEEP.values())))
print("JP   %d japanese names untouched   SUPERSEDED_144 %d now dark by name"
      % (len(JP), len(SUPERSEDED_144)))
print("FIX  %d respelled from the register / %d occurrences dark, %d old "
      "spellings gone from the page" % (len(FIX), sum(FIX.values()), len(WAS)))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
