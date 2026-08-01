# -*- coding: utf-8 -*-
"""Batch 118: level 7, the root's root — and when a pronoun is evidence.

Rules 2-6 all stop at the FIRST listed root and ask its gloss. Most of a
paradigm is glossless, so that question comes back empty even when the root is
exactly right: `qnqgu` is q-`-n-` on `qqgu`, which `regular()` reaches through
the infix branch and then abandons, because `qqgu` is a corpus token nobody
glossed. Batch 117 examined that family, could not verify it, and said so.

But a glossless root is usually one obvious step from a glossed one, and it is
the same regular morphology `roots()` already knows. `chained()` takes that
second step, two ways:

  the reduplication  `qqgu` is CV- on `qgu` 公雞叫聲, `sskuxul` on `skuxul` 喜歡,
  `kkhnuk` on `khnuk` 要軟. CLAUDE.md's tier D already says a CV- reduplication
  makes no new lexeme, so the base's gloss IS the reduplicate's gloss. `PRE` has
  no doubling entry and should never get one — a doubled initial is not a
  prefix — so nothing else in the file can reach these.

  the second step  the root is itself a regular inflection: `swiwil` off
  `wiwil` 垂, `psriyux` off `riyux` 換, `psupu` off `upu` 共, `puyas` off `uyas`
  唱歌. Five of the ten are `ms-` reciprocals sitting on an `s-` form, which is
  ordinary Truku morphology twice over.

`pkkhnuk` is the case that shows the fallback earns its keep even when the root
IS glossed. `kkhnuk` is listed, and glossed only 使...便宜 — the price sense —
while his Pkkhnuk is 為了使（某物）更鬆軟、更嫩. The base `khnuk` 要軟;要便宜
carries both senses, so the base recovers a sense the reduplicate's own listing
dropped. A reduplicate's entry can be narrower than its base's; the rule reads
through it.

**Two steps of inference is one more than levels 4 and 6 take, so it carries
their gate: his Chinese must be Chinese he attached to the word AS a word.**
That gate is not decoration here — it is the whole rule. Ungated, `chained()`
finds 16 shapes / 33 occurrences. The gate refuses six, and those six are
**every illicit spelling in the set** (`nniyah`, `nslikaw`, `spsqrinut`) plus
`msneanak` and `ssdhaun`. What it admits is 10 types / 23 occurrences, and all
ten are licit. A gate measured by what it lets through, not by what it turns
down — and this one sorts the set exactly along the line the n-gram inventory
draws, without ever being shown it.

**THE FINDING: a pronoun is junk agreement when the claim is WHICH pronoun, and
evidence when the claim is a derivation OF the pronoun.** `msdeita` survives the
gate on 我們, and batch 116 refused `nta` twice on that same character. The
distinction has to be stated or the rule looks like the mistake:

  `nta` vs `nita` both mean 我們的. The character is shared by the candidate and
  its rival, so it cannot choose between them, and agreeing on it is agreeing on
  nothing.

  `msdeita` is his Msdita 善於交際的——友好的——與我們來往的, off `deita` 我們. The
  claim is that a non-pronoun word derives from the pronoun, and **his own gloss
  says so in words**: 與我們來往的, "one who associates with us".

And the modern dictionary settles it from the other side, which is where this
should have been settled all along. Its whole sociable/associate vocabulary is
`msixal` 來往, `mssixal` 互相來往, `sixal`, `mrrawiq` 互相來往, `ggdangi`
相互來往, `mneggaluk`; 交際, 合群 and 友好 return nothing at all. **Not one
candidate is shaped remotely like Msdita**, so there is no rival word for it to
be. Meanwhile `msd-` + a listed root is a pattern with 33 siblings — `msdalih`
off `dalih`, `msdara` off `dara`, `msdrudan` off `rudan`. Shape and sense point
the same way.

The page confirms the morphology independently, because the reader puts a
derived form on its base's card: PKKHNUK lands on HNUK beside KHNUK, MSDEITA on
ITA beside DEITA, MSSKUXUL on KUXUL beside SKUXUL, MSWIWIL on SWIWIL, and
QNQGU/QNQGUAN on QQGU.

`mswiwil` is a debt paid. `syncopated()`'s own docstring lists it among six
correct claims that rule had to leave pale, reaching it as `m` + `suwiwil` 吊掛,
which shares no character with his 懸垂的－搖晃的. Level 7 gets there by a
different road — `swiwil`, then `wiwil` 垂, which is in 懸垂的.

What level 7 still cannot reach is the rest of batch 117's QQOGO family.
`psqgu` is p-s- on `qgu` and `regular()` has always reached it; it is pale
because **he glossed his PSQGO 「？？」**, so there is no Chinese on either side
of the comparison. No gloss rule can ever verify a word its author marked
unknown, and that is the right outcome.

The map is untouched this batch. Every value on screen is the same string it was
at 705f144; only the paint moved. 92.16% -> 92.21%.
"""
import collections, io, re
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
fail = []


def check(cond, msg):
    if not cond:
        fail.append(msg)
    print(("  ok   " if cond else "  FAIL ") + msg)


V = dict((m.group(1), int(m.group(2))) for m in re.finditer(
    r'^  "(.*)": (\d),$', io.open(H + "site/verified.js", encoding="utf-8").read(),
    re.M))
LISTED = sorted(k for k in V if V[k] == 1)
INFL = sorted(k for k in V if V[k] == 2)
VOUCHED = sorted(k for k in V if V[k] == 3)
VROOT = sorted(k for k in V if V[k] == 4)
SISTR = sorted(k for k in V if V[k] == 5)
SYNCP = sorted(k for k in V if V[k] == 6)
CHAIN = sorted(k for k in V if V[k] == 7)

MAN = io.open(H + "tools/orthography/manual_map.json", encoding="utf-8").read()
MAP = io.open(H + "site/modern_map.js", encoding="utf-8").read()
INF = io.open(H + "tools/orthography/inflection.py", encoding="utf-8").read()
BV = io.open(H + "tools/orthography/build_verified.py", encoding="utf-8").read()

# the ten, with the occurrence count each must contribute in modern mode
WON = [("qnqgu", 5), ("pkkhnuk", 3), ("mswiwil", 3), ("msskuxul", 3),
       ("qnqguan", 2), ("msnama", 2), ("msdeita", 2), ("pnsupu", 1),
       ("empsriyux", 1), ("emppuyas", 1)]
# what the slot gate refuses — every illicit shape the ungated rule would take,
# plus two whose only Chinese is an example sentence
GATED = ["nniyah", "nslikaw", "spsqrinut", "msneanak", "ssdhaun"]

PROBE = """() => {
  const out = {mod: {}, unv: {}, raw: {}, counts: {}};
  for (const c of ['w-mod','w-unv','w-raw']) {
    const b = out[c.slice(2)];
    const ns = document.querySelectorAll('span.'+c);
    out.counts[c] = ns.length;
    for (const n of ns) {
      const t = n.textContent.trim().toLowerCase();
      b[t] = (b[t] || 0) + 1;
    }
  }
  out.par = Array.from(document.querySelectorAll('.paradigm'))
                 .map(e => e.textContent.trim());
  out.cards = document.querySelectorAll('article.entry').length;
  return out;
}"""

# (modern headword of the card, the word, what it must be)
CARDS = [
    ("QQGU", "QNQGU", "deep brown"),      # was PALE at ver117 — the flip
    ("QQGU", "QNQGUAN", "deep brown"),
    ("QQGU", "QQGU", "deep brown"),       # the level-1 head, unmoved
    ("PSQGU", "PSQGU", "PALE"),           # he glossed it 「？？」
    ("HNUK", "PKKHNUK", "deep brown"),    # beside its base on the same card
    ("HNUK", "KHNUK", "deep brown"),
    ("ITA", "MSDEITA", "deep brown"),     # the pronoun case
    ("ITA", "DEITA", "deep brown"),
    ("KUXUL", "MSSKUXUL", "deep brown"),
    ("KUXUL", "SKUXUL", "deep brown"),
    ("SWIWIL", "MSWIWIL", "deep brown"),  # the debt syncopated() left
    ("NAMA", "MSNAMA", "deep brown"),
    ("SUPU", "PNSUPU", "deep brown"),
    ("SRIYUX", "EMPSRIYUX", "deep brown"),
    ("UYAS", "EMPPUYAS", "deep brown"),
    ("TEUQU", "TEUQU", "deep brown"),     # batch 117 still standing
    ("TEUQU", "PTEUQU", "deep brown"),
    ("TEUQU", "PTEUQAN", "deep brown"),
    ("TEUQU", "TEUQAN", "PALE"),          # still the two ends of one event
    ("TEUQU", "PTEUQI", "PALE"),
    ("SNUQU", "SNUQU", "PALE"),           # still held
]

CARD_PROBE = """(cases) => {
  const out = [];
  const cards = Array.from(document.querySelectorAll('article.entry'));
  for (const [hw, want, expect] of cases) {
    const named = cards.filter(c => {
      const h = c.querySelector('.hw');
      return h && h.textContent.trim().toUpperCase().split(/[^A-Z']+/)[0] === hw;
    });
    const card = named.find(c => c.textContent.toUpperCase().indexOf(want) >= 0)
                 || named[0];
    if (!card) { out.push({hw, want, expect, missing: true}); continue; }
    const grab = cls => Array.from(card.querySelectorAll('span.' + cls))
                             .map(e => e.textContent.trim().toUpperCase());
    out.push({hw, want, expect, mod: grab('w-mod'), unv: grab('w-unv'),
              raw: grab('w-raw'),
              par: Array.from(card.querySelectorAll('.paradigm'))
                        .map(e => e.textContent.trim())});
  }
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    res, cardres = {}, {}
    for mode in ("modern", "original"):
        ctx = b.new_context()
        ctx.add_init_script(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','%s')" % mode)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL)
        pg.wait_for_timeout(9000)
        res[mode] = pg.evaluate(PROBE)
        res[mode]["errs"] = errs
        cardres[mode] = pg.evaluate(CARD_PROBE, CARDS)
        ctx.close()
    b.close()

M, O = res["modern"], res["original"]
ALL = collections.Counter()
for k in ("mod", "unv", "raw"):
    ALL.update(M[k])

print("modern", M["counts"], "original", O["counts"])
print("verified.js: %d listed, %d regularly inflected, %d vouched, %d off a "
      "vouched root, %d sister slots, %d syncopated roots, %d chained roots"
      % (len(LISTED), len(INFL), len(VOUCHED), len(VROOT), len(SISTR),
         len(SYNCP), len(CHAIN)))

print("\n-- the totals, both modes")
tm = sum(M["counts"].values())
to = sum(O["counts"].values())
check(M["cards"] == 1967 and O["cards"] == 1967,
      "1967 cards in both modes")
check(M["counts"] == {"w-mod": 41010, "w-unv": 3439, "w-raw": 26},
      "modern: w-mod 41010 / w-unv 3439 / w-raw 26  (was 40987/3462/26)")
check(tm == 44475 and abs(100.0 * 41010 / tm - 92.21) < 0.005,
      "44,475 displayed words, 92.21%% verified  (was 92.16%%)")
check(O["counts"] == {"w-mod": 41444, "w-unv": 3492, "w-raw": 26},
      "original: w-mod 41444 / w-unv 3492 / w-raw 26  (was 41420/3516/26)")
check(to == 44962, "44,962 displayed words in Pecoraro mode")
check(not M["errs"] and not O["errs"],
      "no page errors in either mode: %s" % ((M["errs"] + O["errs"]) or "none"))

print("\n-- the modern mode gains 23 and Pecoraro mode 24, and the odd one out "
      "is predictable")
check(41010 - 40987 == 23 and 3462 - 3439 == 23,
      "modern +23 dark / -23 pale, which is exactly the ten values' occurrences")
check(sum(n for _, n in WON) == 23,
      "the ten sum to 23 occurrences")
check(41444 - 41420 == 24 and 3516 - 3492 == 24,
      "Pecoraro mode moves 24, one more — `knqogo` and `qnqogo` BOTH map to "
      "`qnqgu`, so collapsed() shows one span in modern and two in his")
check('"knqogo":"qnqgu"' in MAP and '"qnqogo":"qnqgu"' in MAP,
      "and both those keys are in modern_map.js, which is why")

print("\n-- level 7 exists, and holds exactly ten keys")
check("def chained" in INF, "inflection.py defines chained()")
check("if inf.chained(p):\n            return 0.03125" in BV,
      "build_verified.py asks it after syncopated(), so 7 is the last resort")
check(BV.count("0.03125") == 4 and "0.03125: 7" in BV,
      "and emits it as level 7")
check(CHAIN == sorted(v for v, _ in WON),
      "level 7 = %s" % ", ".join(sorted(v for v, _ in WON)))
for v, n in WON:
    check(M["mod"].get(v) == n and v not in M["unv"],
          "`%s` is deep brown %d\xd7 and appears pale nowhere" % (v, n))

print("\n-- the slot gate is the rule, and it sorts the set along the licit line")
for v in GATED:
    check(v not in V,
          "`%s` is NOT verified: its only Chinese is an example sentence, and "
          "the gate refuses those" % v)
check(all(v not in V for v in ("nniyah", "nslikaw", "spsqrinut")),
      "all three ILLICIT shapes the ungated rule would have taken are refused, "
      "though chained() never asks T.licit() — 16 types/33 occ ungated, "
      "10 types/23 occ gated, and the ten are licit")
check("slots_only=True" in INF.split("def chained")[1],
      "chained() takes _his(v, slots_only=True), the same gate as 4 and 6")
check("if v in self.frozen" in INF.split("def chained")[1],
      "and replicates regular()'s frozen check (CLAUDE.md ddd)")

print("\n-- every earlier level is byte-identical to batch 117")
check(len(LISTED) == 3883, "3883 listed (level 1), unmoved")
check(len(INFL) == 596, "596 regularly inflected (level 2), unmoved")
check(len(VOUCHED) == 53, "53 vouched (level 3), unmoved")
check(len(VROOT) == 65, "65 off a vouched root (level 4), unmoved")
check(len(SISTR) == 36, "36 sister slots (level 5), unmoved")
check(len(SYNCP) == 30, "30 syncopated roots (level 6), unmoved")
check(len(CHAIN) == 10, "10 chained roots (level 7), new")
check(len(V) == 4673, "4673 verified values in all")

print("\n-- the map did not move; only the paint did")
check('"snoqo": "snuqu"' in MAN,
      "`snoqo` still maps to `snuqu` — level 7 offers it nothing, since the "
      "candidate `sneuqu` contradicts his 頑皮－開心果－愛開玩笑的人")
check("sneuqu" not in MAN and not ALL.get("sneuqu", 0),
      "`sneuqu` appears neither in the map nor on the page")
for v in ("teuqu", "pteuqu", "spteuqu", "pteuqan", "pteuqun", "empqneuqu"):
    check(v in V and M["mod"].get(v),
          "batch 117's `%s` is still deep brown" % v)
for v in ("tuuqu", "ptquwan", "ptquwi", "tquwan"):
    check(not ALL.get(v) and v not in V,
          "and the `tquw-` spelling `%s` still renders nowhere" % v)

print("\n-- what level 7 cannot reach, and should not")
check(M["unv"].get("psqgu") == 2 and "psqgu" not in V,
      "`psqgu` is still pale 2\xd7: regular() reaches `qgu` and always could, "
      "but he glossed his PSQGO \u300c\uff1f\uff1f\u300d, so there is no "
      "Chinese on his side to compare")
for v in ("teuqan", "pnteuqan", "tneuqan", "pteuqi"):
    check(v not in V, "`%s` stays pale — the two ends of one event share no "
                      "character, and level 7 changes nothing about that" % v)
check("qnqgu" in V and "psqgu" not in V,
      "so the QQOGO family ends the batch 7 dark of 9, not 9 of 9")

print("\n-- the page puts each new dark word on its base's card")
for r in cardres["modern"]:
    lab = "%s / %s" % (r["hw"], r["want"])
    if r.get("missing"):
        check(False, lab + ": card not found")
        continue
    if r["expect"] == "deep brown":
        check(r["want"] in r["mod"] and r["want"] not in r["unv"],
              "%-22s deep brown on its own card" % lab)
    else:
        check(r["want"] in r["unv"] and r["want"] not in r["mod"],
              "%-22s PALE on its own card" % lab)
kux = [r for r in cardres["modern"] if r["hw"] == "KUXUL"][0]
check("MSSKUXUL" in kux["mod"] and "SKUXUL" in kux["mod"],
      "KUXUL carries both the reduplicate and its base, both deep brown — the "
      "reader shows the derivation the rule claims")
ita = [r for r in cardres["modern"] if r["hw"] == "ITA"][0]
check("MSDEITA" in ita["mod"] and "DEITA" in ita["mod"],
      "and ITA carries `msdeita` beside `deita` 我們, which is the claim")

print("\n-- green did not move")
check(M["counts"]["w-raw"] == 26 and O["counts"]["w-raw"] == 26,
      "26 green occurrences in both modes, unchanged since batch 116")
check(len(M["raw"]) == 22, "22 green types, unchanged")

print("\n%d failures" % len(fail))
for f in fail:
    print("  FAIL " + f)
