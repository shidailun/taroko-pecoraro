# -*- coding: utf-8 -*-
"""Batch 119: the BALI 買/賣 family — two level-1 claims naming the wrong word.

Batch 118 moved only paint. This one moves the map, and it is the class
CLAUDE.md has been circling since batch 15: **a brown claim that names an
existing modern word, the wrong one.** Green says "guessed"; brown says
"verified"; these said the latter about a different word entirely.

His **BALI (R) 買；賣** carries the paradigm `Mali, bali, bligi, bligan, bligun`
— and he **writes the g** in every suffixed slot, so his own root is /balig/ and
the bare forms are the ones that dropped it. Five sub-forms: Mali 買、賣（動詞形）,
Mbali 買者；賣者, Bligan 販賣的地點、時間、物品, Nali 買進或賣出的貨物,
Smbali 做買賣；經商.

The modern lexicon has **both stems**, and the split matches his exactly:
`marig` 買 for his Mali/Nali, `mbarig` 買 for his Mbali/Kmbali/Smbali. The
suffixed slots were already right at level 1 — `bligan/bligi/bligun` →
`brigan/brigi/brigun` — because his g was there for the map to read. Everything
that had lost the g was wrong:

    bali   -> barig      was `bali` 子彈, BROWN level 1
    mali   -> marig      was `mali` 加多, BROWN level 1
    nali   -> narig      was `nali`, pale
    mbali  -> mbarig     was `embari`, pale 5\xd7
    kmbali -> kmbarig    was `kmbari`, pale 3\xd7
    smbali -> smbarig    was `smbari`, pale 1\xd7

**The mechanism is now understood, and it is the id tier.** The auto-generated
map prefers an attested IDENTITY over a character rule, so any of his words
spelled like an unrelated modern word is silently verified at level 1 and never
looks green again. `bali` 子彈 and `mali` 加多 are both real modern words; that
is precisely why they survived. This is the MUBUH class, and it is the strongest
motive yet for the `claimaudit.py` sweep CLAUDE.md has had on the list since
batch 16 — two of them in one family, found by working the pale tail rather than
by looking for them.

**`mali` is a homograph across two of his families, and `modernize()` cannot
resolve it.** It takes ONE WORD with NO entry context (app.js:170, and the
comment at :234 says so), and `T.key("Ma\u0142i")` folds the barred l, so his
notation gives no escape either. Twelve spans in modern mode:

    10 are 買 — AYANG, BARIG \xd74, BMBANG, HAPUY, LUHAY, QPAH, S
     1 is his UMAL 增加－添加 paradigm line `Mumal, umal, mali (=Ma\u0142i), ...`,
       where the OLD value `mali` 加多 was correct
     1 is the separate headword MALI, tagged `name (f)`

So the trade was taken knowingly: 10 right and 2 wrong, against the 2 right and
10 wrong the page shipped before. Both losses are recorded here rather than
quietly absorbed. The name is not a new defect — CLAUDE.md's tier N already
rules that **a name whose token is also another entry's headword or sub-form is
excluded**, because one bare token cannot render two ways and the word carrying
the gloss wins; 30 of 270 name tokens are in that class already (KULAS→KURAS,
LABAI→RABAY).

**`bali` did NOT vanish from the page, and that is correct.** His **BALE** is a
separate entry, the Japanese loan 步槍子彈, and tier J maps it `bale` → `bali`
with its l intact — the tier's own note says "`bali` 子彈 keeps it, and l\u2192r is
guesswork on a word that was never Truku to begin with". Batch 119 never touched
that key, so BALI still renders twice: on BALE's own card and in L'OQ's sentence
「這孩子瘋了！他拿（槍的）子彈來玩爆破取樂」, which is about a bullet. The wrong
claim was his BALI borrowing the loan's spelling, not the loan.

**`barit` was checked as a suspect and came back confirmed** — the useful half
of the result. His BALIT is tagged `animal` and glossed 石貂 (stone marten),
while modern `barit` is glossed only 人名（男;女）, which looks like the same
wrong-word shape. It is not: the derived forms are `tmbbarit` 獵臭鼠 and
`tmnbarit` 曾捕獵臭鼠, so `barit` IS the animal and the personal name is a use of
it. That is the TUIL pattern in CLAUDE.md verbatim — "the omnibus even glosses
bare `tuwil` 人名（男）, which is his own note that it nicknames tall thin young
men". **A bare gloss reading 人名 is not evidence the word is only a name; ask
the paradigm.** `gbali` was exonerated the same way: its single occurrence is in
the GABAL 拔出 paradigm, so 拔掉 is right and it stays where it is.

92.21% -> 92.23% of displayed word occurrences verified. The gain is small
because two of the six were already dark — those twelve spans change their
STRING, not their colour, which no percentage can show. Both modes move +11,
symmetrically this time (batch 118's asymmetry came from two keys sharing one
value; here the paradigm-line collapse of `mali`/`Ma\u0142i` was already in force
before the change, so it cancels).
"""
import collections, io, json, re
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
LEVELS = dict((n, sorted(k for k in V if V[k] == n)) for n in range(1, 8))

MAN = json.load(io.open(H + "tools/orthography/manual_map.json", encoding="utf-8"))
# site/modern_map.js holds TWO objects and is minified — index, don't json.loads
# the file, and don't grep for a space after the colon.
_t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
_a = _t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(_t[_a:_t.index("\n};", _a) + 2])

# key -> value, all six, and every one of them absent from manual_map.json
# before this batch (i.e. they were auto-generated claims)
NEW = [("bali", "barig"), ("mali", "marig"), ("nali", "narig"),
       ("mbali", "mbarig"), ("kmbali", "kmbarig"), ("smbali", "smbarig")]
# the pale values this retires, with the occurrences each was carrying
GONE_PALE = [("embari", 5), ("kmbari", 3), ("nali", 2), ("smbari", 1)]
# values that must now render NOWHERE in either colour
BANNED = ["mali", "nali", "embari", "kmbari", "smbari"]

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
  out.cards = document.querySelectorAll('article.entry').length;
  return out;
}"""

# (modern headword of the card, the word, what it must be)
CARDS = [
    # his BALI, the whole family on one card
    ("BARIG", "BARIG", "deep brown"),      # the head, was `bali` 子彈
    ("BARIG", "MARIG", "deep brown"),      # was `mali` 加多
    ("BARIG", "MBARIG", "deep brown"),     # was pale `embari`
    ("BARIG", "NARIG", "deep brown"),      # was pale `nali`
    ("BARIG", "KMBARIG", "deep brown"),    # was pale `kmbari`
    ("BARIG", "SMBARIG", "deep brown"),    # was pale `smbari`
    ("BARIG", "BRIGAN", "deep brown"),     # already right — his own g
    ("BARIG", "BRIGI", "deep brown"),
    ("BARIG", "BRIGUN", "deep brown"),
    # the mbarig stem away from its own card
    ("SIBUS", "MBARIG", "deep brown"),
    ("SIBUS", "KMBARIG", "deep brown"),
    ("TBNAW", "MBARIG", "deep brown"),
    ("DJIMA", "KMBARIG", "deep brown"),
    # the marig stem away from its own card — all 買
    ("AYANG", "MARIG", "deep brown"),
    ("BMBANG", "MARIG", "deep brown"),
    ("HAPUY", "MARIG", "deep brown"),
    ("LUHAY", "MARIG", "deep brown"),
    ("QPAH", "MARIG", "deep brown"),
    # the two knowingly-wrong spans, asserted so they cannot drift unnoticed
    ("UMAL", "MARIG", "deep brown"),       # his 增加－添加 line; `mali` was right
    ("MARIG", "MARIG", "deep brown"),      # the `name (f)` headword MALI
    # the Japanese loan, untouched
    ("BALI", "BALI", "deep brown"),        # his BALE 步槍子彈
    ("RUQ", "BALI", "deep brown"),         # L'OQ's bullet sentence
    # exonerated, not fixed
    ("BARIT", "BARIT", "deep brown"),      # 石貂, proved by tmbbarit 獵臭鼠
    ("GABAL", "GBALI", "deep brown"),      # GABAL 拔出's own paradigm
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
              raw: grab('w-raw')});
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
print("verified.js: %s"
      % "  ".join("%d@%d" % (len(LEVELS[n]), n) for n in range(1, 8)))

print("\n-- the totals, both modes")
tm = sum(M["counts"].values())
to = sum(O["counts"].values())
check(M["cards"] == 1967 and O["cards"] == 1967, "1967 cards in both modes")
check(M["counts"] == {"w-mod": 41021, "w-unv": 3428, "w-raw": 26},
      "modern: w-mod 41021 / w-unv 3428 / w-raw 26  (was 41010/3439/26)")
check(tm == 44475 and abs(100.0 * 41021 / tm - 92.23) < 0.005,
      "44,475 displayed words, 92.23%% verified  (was 92.21%%)")
check(O["counts"] == {"w-mod": 41455, "w-unv": 3481, "w-raw": 26},
      "original: w-mod 41455 / w-unv 3481 / w-raw 26  (was 41444/3492/26)")
check(to == 44962, "44,962 displayed words in Pecoraro mode")
check(not M["errs"] and not O["errs"],
      "no page errors in either mode: %s" % ((M["errs"] + O["errs"]) or "none"))

print("\n-- both modes move +11, and 11 is the four pale values' occurrences")
check(41021 - 41010 == 11 and 3439 - 3428 == 11,
      "modern +11 dark / -11 pale")
check(41455 - 41444 == 11 and 3492 - 3481 == 11,
      "Pecoraro mode moves 11 as well — symmetric, unlike batch 118, because "
      "the `mali`/`Ma\u0142i` paradigm-line collapse was already in force before "
      "the change and so cancels on both sides")
check(sum(n for _, n in GONE_PALE) == 11,
      "the four retired pale values sum to 11: %s"
      % ", ".join("%s %d" % (v, n) for v, n in GONE_PALE))
check(tm == 44475, "and the total is unchanged, so nothing was added or lost — "
                   "12 further spans changed their STRING at constant colour, "
                   "which no percentage can show")

print("\n-- the six keys, all of them absent from manual_map.json before this")
for k, v in NEW:
    check(MAN.get(k) == v, "manual_map.json: %-8s -> %s" % (k, v))
    check(MAP.get(k) == v, "modern_map.js:  %-8s -> %s  (the hand key won)" % (k, v))
check(len(MAN) == 1722, "manual_map.json holds 1722 keys (was 1716)")

print("\n-- the wrong words are gone from the page entirely")
for v in BANNED:
    check(not ALL.get(v),
          "`%s` renders nowhere in any colour" % v)
check("mali" not in V and "mali" not in set(MAP.values()),
      "`mali` 加多 is no longer a value of any key, so it left verified.js too")
check(MAP.get("bale") == "bali" and V.get("bali") == 1,
      "but `bale` -> `bali` is untouched: his BALE is the Japanese loan "
      "\u6b65\u69cd\u5b50\u5f48, and tier J keeps its l on purpose")
check(ALL.get("bali") == 2,
      "so BALI still renders exactly 2\xd7 \u2014 BALE's own card and L'OQ's "
      "bullet sentence")

print("\n-- level 1 gains 5, not 6, and the arithmetic says which")
check(len(LEVELS[1]) == 3888, "3888 listed (level 1), was 3883")
check(all(V.get(v) == 1 for _, v in NEW),
      "all six new values are themselves listed modern words: %s"
      % ", ".join(v for _, v in NEW))
check(len(LEVELS[1]) == 3883 + 6 - 1,
      "+6 new values, -1 for `mali`, which no key claims any more = +5")
check(len(V) == 4678, "4678 verified values in all (was 4673)")

print("\n-- levels 2-7 are byte-identical to batch 118")
for n, want in ((2, 596), (3, 53), (4, 65), (5, 36), (6, 30), (7, 10)):
    check(len(LEVELS[n]) == want, "level %d unmoved at %d" % (n, want))
check(sorted(LEVELS[7]) == sorted(
      ["emppuyas", "empsriyux", "msdeita", "msnama", "msskuxul", "mswiwil",
       "pkkhnuk", "pnsupu", "qnqgu", "qnqguan"]),
      "and batch 118's ten chained roots are exactly the ten still there")

print("\n-- his own g is why the suffixed slots were right all along")
for v, n in (("brigan", 20), ("brigi", 2), ("brigun", 7)):
    check(M["mod"].get(v) == n and v not in M["unv"],
          "`%s` deep brown %d\xd7 \u2014 he wrote the g in `bligan/bligi/bligun`, "
          "so the map could read the root" % (v, n))

print("\n-- the family per card")
for r in cardres["modern"]:
    lab = "%s / %s" % (r["hw"], r["want"])
    if r.get("missing"):
        check(False, lab + ": card not found")
        continue
    if r["expect"] == "deep brown":
        check(r["want"] in r["mod"] and r["want"] not in r["unv"]
              and r["want"] not in r["raw"],
              "%-22s deep brown on its own card" % lab)
    else:
        check(r["want"] in r["unv"] and r["want"] not in r["mod"],
              "%-22s PALE on its own card" % lab)
bar = [r for r in cardres["modern"] if r["hw"] == "BARIG"][0]
check(bar["mod"].count("MARIG") == 4 and bar["mod"].count("MBARIG") == 3,
      "BARIG's own card carries MARIG \xd74 and MBARIG \xd73 \u2014 the two stems "
      "his Mali/Nali vs Mbali/Kmbali/Smbali split asks for, side by side")
check(not bar["unv"] and not bar["raw"],
      "and nothing on that card is pale or green any more: %s"
      % ((bar["unv"] + bar["raw"]) or "clean"))

print("\n-- the two spans this batch knowingly gets wrong, named out loud")
check(ALL.get("marig") == 12,
      "MARIG renders 12\xd7: 10 of them 買 and correct, 1 on UMAL and 1 on the "
      "MALI name card")
uma = [r for r in cardres["modern"] if r["hw"] == "UMAL"][0]
check(uma["mod"].count("MARIG") == 1 and "MALI" not in uma["mod"],
      "UMAL \u589e\u52a0\uff0d\u6dfb\u52a0 shows MARIG once where `mali` "
      "\u52a0\u591a was right \u2014 modernize() takes one word with no entry "
      "context (app.js:170), so a homograph across two of his families cannot "
      "be resolved; 10 right against 2 wrong beats the 2 against 10 it replaced")
nam = [r for r in cardres["modern"] if r["hw"] == "MARIG"][0]
check(nam["mod"].count("MARIG") == 1,
      "and his `name (f)` headword MALI renders MARIG \u2014 the documented "
      "tier-N exclusion, not a new defect: a name whose token is also another "
      "entry's sub-form keeps the word's spelling (KULAS\u2192KURAS, "
      "LABAI\u2192RABAY), because one bare token cannot render two ways")

print("\n-- exonerated rather than fixed")
check(MAP.get("balit") == "barit" and V.get("barit") == 1,
      "`balit` -> `barit` stands: his 石貂 against a bare gloss of 人名（男;女）"
      " looked like the same wrong-word shape, but `tmbbarit` 獵臭鼠 and "
      "`tmnbarit` 曾捕獵臭鼠 prove the animal is the word \u2014 the TUIL pattern")
check(ALL.get("gbali") == 1,
      "`gbali` renders once, in GABAL 拔出's own paradigm, so 拔掉 is right")

print("\n-- green did not move")
check(M["counts"]["w-raw"] == 26 and O["counts"]["w-raw"] == 26,
      "26 green occurrences in both modes, unchanged since batch 118")
check(not any(ALL.get(v) for v in
              ("barig", "marig", "narig", "mbarig", "kmbarig", "smbarig")
              if v in M["raw"]),
      "and no member of the family is green")

print("\n%d failures" % len(fail))
for f in fail:
    print("  " + f)
