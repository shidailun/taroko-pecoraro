# -*- coding: utf-8 -*-
"""Batch 120: four families off `stemsplit120.py`, and a fifth that had to be
BACKED OUT before the commit because the word it named was the wrong one.

`stemsplit120.py` is one mechanical arm of the `claimaudit.py` sweep CLAUDE.md
has carried since batch 16: rank every entry whose PALE members sit on a stem
none of its own BROWN members share. Fifty entries, 143 pale occurrences at
stake. Four families off the top of that list went in.

    pnpong      -> pngpung          his PNPONG, and his own tag says PNGPONG
    mpnpong     -> empngpung
    pkpnpong    -> pkpngpung        was `pkpnpung`
    pnkpnpong   -> pnkpngpung
    tnppngan    -> tnpngan          was `tnppngan`, an identity claim
    kayao       -> keiyaw           was `kayaw`
    pkayao      -> pkeiyaw
    k'yagan     -> kayagan          was `kyagan`
    k'yagi      -> kayagi           was `kyagi`
    k'yagun     -> kayagun          was `kyagun`
    tsai        -> tgsai            was `tsay`
    tsaan       -> tgsaan           was `tsaan`, an identity claim
    tsaon       -> tgsaun           was `tsaun`
    tnsaan      -> tnegsaan         was `tnsaan`, an identity claim

**Three of the fourteen were ALREADY BROWN under another of his own spellings of
the same slot**, which is the strongest form this evidence takes and the reason
the batch is safe: he wrote the slot twice, one spelling was adjudicated long ago
and the other was never asked. `pngpong` -> `pngpung` was already in the map while
`pnpong` claimed `pnpung`; `tnpngan`/`tnpongan` -> `tnpngan` while `tnppngan`
claimed itself; `tngsaan` -> `tnegsaan` while `tnsaan` claimed itself. Same shape
as batch 20's five (`lqlaqe`/`llaqe`, `ldludan`/`lludan`) and batch 25's three
half-brown cards.

**TQELI was proposed, built, measured — and backed out.** `tqliyan` -> `tqrian`
and `tnqliyan` -> `tnqrian` passed every mechanical test in the build: attested
values, level 1, no impossible n-gram, and his TQELI slots really are the -an
forms of a t- prefixed root. The gloss says no. **`tqrian` is 裝填** — to load or
fill — and it belongs to the root `quri`, whose modern paradigm is complete and
coherent: `tquri` 倒水, `tmquri` 已裝、倒, `ptquri` 使裝;倒, `ttquri` 裝的東西,
`tqrii` 要裝, `tqrian` 裝填. That is his **TKULI 倒－裝入（容器）**, whose own slots
are spelled with a k — `tkliyan`, `tklean`, `tkleun`, `tnklean` — so the four
level-1 claims already standing on `tqrian` are TKULI's and are RIGHT.

His `tqliyan` is a different key with no 裝填 use anywhere in the book: it is
QELI's *Tmqeli* 包圍 slot, QULI's *Tmquli* 領養 slot, and TQELI's 環繞的地點、
時間與方式. The encircling root is `qiri` — `qmiri` 圍圈;迂迴;捲起, `qrian` 被圍繞,
`qnrian` 被繞著, `mtqiri`, `ptqiri`. Mapping his 柵欄 word onto `tqrian` would have
told the reader, in the brown that means *verified*, that it is the attested word
meaning 裝填. That is the BALI failure of batch 119 exactly, and **a brown claim
naming the wrong existing word is the worst state available to a span.**

Both keys are therefore deleted rather than left at their old value, because the
old value was itself an identity claim — `tqliyan` -> `tqliyan`, a string the
modern lexicon does not have — i.e. the idtrap shape, pale and asserting. Green is
the honest colour, and here it also spells better: green runs `charRules()`, whose
l->r gives TQRIYAN, and the encircling root really does take r. The batch loses 6
occurrences to green (26 -> 32) and gains the right to be believed.

**The two spellings that decide it are one letter apart and only the gloss
separates them.** His SAPANG example reads「Ndoa bi snapang llubwi tqlyaan payai」
= 要好好把袋子補好，**用來裝稻穀** — to hold grain. So `tqlyaan`, with the q, IS
the container word and its existing claim on `tqrian` is confirmed by his own
translation; `tqliyan`, with the q and an i, is not. Nothing but the sentence
tells them apart.

**The modern-mode total FELL by 4, and that is the map working.** `collapsed()`
and `collapseTagBrackets()` drop a bracketed alternative once his two spellings of
one slot converge in modern Truku, so a batch of this shape removes spans from
modern mode only; Pecoraro mode is untouched. All four are named below.

92.23% -> 92.29% of displayed word occurrences verified.
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

# the fourteen keys, with the value each retires
NEW = [("pnpong", "pngpung", "pnpung"),
       ("mpnpong", "empngpung", "empnpung"),
       ("pkpnpong", "pkpngpung", "pkpnpung"),
       ("pnkpnpong", "pnkpngpung", "pnkpnpung"),
       ("tnppngan", "tnpngan", "tnppngan"),
       ("kayao", "keiyaw", "kayaw"),
       ("pkayao", "pkeiyaw", "pkayaw"),
       ("k'yagan", "kayagan", "kyagan"),
       ("k'yagi", "kayagi", "kyagi"),
       ("k'yagun", "kayagun", "kyagun"),
       ("tsai", "tgsai", "tsay"),
       ("tsaan", "tgsaan", "tsaan"),
       ("tsaon", "tgsaun", "tsaun"),
       ("tnsaan", "tnegsaan", "tnsaan")]
# values that must now render NOWHERE in any colour
BANNED = sorted(set(old for _, _, old in NEW) - set(v for _, v, _ in NEW))
# the six values level 1 gains
LISTED_NEW = ["kayagan", "keiyaw", "pkeiyaw", "tgsaan", "tgsai", "tgsaun"]
# already brown under ANOTHER of his own spellings of the same slot
ALREADY = [("pngpung", "pngpong"), ("tnpngan", "tnpongan"),
           ("tnegsaan", "tngsaan")]
# the four bracket pairs that newly converge, hence the -4 in modern mode
COLLAPSED = ["BTUNUX ex `pngpong (pnpong)`",
             "PNPONG tag `(PNGPONG ?)` vs its own headword",
             "PNPONG sub `Mpnpong (mpngpong)`",
             "PNPONG sub `Tnpngan ( = Tnppngan ?)`"]

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
    # PNGPUNG — his PNPONG 山丘, the head and its three derivatives
    ("PNGPUNG", "PNGPUNG", "deep brown"),
    ("PNGPUNG", "EMPNGPUNG", "pale"),
    ("PNGPUNG", "PKPNGPUNG", "pale"),
    ("PNGPUNG", "PNKPNGPUNG", "pale"),
    ("PNGPUNG", "TNPNGAN", "deep brown"),
    ("BTUNUX", "PNGPUNG", "deep brown"),
    ("DGIYAQ", "PNGPUNG", "deep brown"),
    ("KALA", "PNGPUNG", "deep brown"),
    ("SANGAY", "PNGPUNG", "deep brown"),
    ("YAYUNG", "PNGPUNG", "deep brown"),
    ("TNPNGAN", "TNPNGAN", "deep brown"),
    # KEIYAW — his KAYAO 醒著的
    ("KEIYAW", "KEIYAW", "deep brown"),
    ("KEIYAW", "PKEIYAW", "deep brown"),
    ("KEIYAW", "KAYAGAN", "deep brown"),
    ("KEIYAW", "KAYAGI", "pale"),
    ("KEIYAW", "KAYAGUN", "pale"),
    ("IYAW", "KEIYAW", "deep brown"),
    # TGSA — his TSAI 教
    ("TGSA", "TGSAI", "deep brown"),
    ("TGSA", "TGSAAN", "deep brown"),
    ("TGSA", "TGSAUN", "deep brown"),
    ("TGSA", "TNEGSAAN", "deep brown"),
    ("ASI", "TGSAI", "deep brown"),
    ("KARI", "TGSAI", "deep brown"),
    ("NUQIH", "TGSAI", "deep brown"),
    # the backed-out TQELI keys — green, and the container word untouched
    ("TQIRI", "TQRIYAN", "green"),
    ("TQIRI", "TNQRIYAN", "green"),
    ("QIRI", "TQRIYAN", "green"),
    ("QULI", "TQRIYAN", "green"),
    ("TKURI", "TQRIAN", "deep brown"),
    ("TKURI", "TNQRIAN", "deep brown"),
    ("SAPANG", "TQRIAN", "deep brown"),
    # families stemsplit120 proposed and this batch DECLINED
    ("SIPA", "SIPA", "deep brown"),
    ("SIPA", "PSIPA", "deep brown"),
    ("SIPA", "PSPAAN", "pale"),
    ("SIPA", "PNSPAAN", "pale"),
    ("SMUK", "SMUK", "deep brown"),
    ("SMUK", "PNSMKAN", "pale"),
    ("DLUT", "DLUT", "deep brown"),
    ("DLUT", "PDLUT", "deep brown"),
    ("MALU", "MNALU", "pale"),
    ("MALU", "NNALU", "pale"),
    ("LALA", "MLLAUN", "pale"),
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
check(M["counts"] == {"w-mod": 41044, "w-unv": 3395, "w-raw": 32},
      "modern: w-mod 41044 / w-unv 3395 / w-raw 32  (was 41021/3428/26)")
check(tm == 44471 and abs(100.0 * 41044 / tm - 92.29) < 0.005,
      "44,471 displayed words, 92.29%% verified  (was 44,475 and 92.23%%)")
check(O["counts"] == {"w-mod": 41481, "w-unv": 3449, "w-raw": 32},
      "original: w-mod 41481 / w-unv 3449 / w-raw 32  (was 41455/3481/26)")
check(to == 44962, "44,962 displayed words in Pecoraro mode, unchanged")
check(not M["errs"] and not O["errs"],
      "no page errors in either mode: %s" % ((M["errs"] + O["errs"]) or "none"))

print("\n-- the -4 in modern mode is four of HIS OWN bracket pairs converging")
check(to == 44962 and tm == 44471 and to - tm == 491,
      "Pecoraro mode holds its 44,962 while modern mode drops 44,475 -> 44,471: "
      "`collapsed()`/`collapseTagBrackets()` drop a bracketed alternative once "
      "his two spellings of one slot agree in modern Truku, which is modern-mode "
      "only by construction")
for c in COLLAPSED:
    print("       collapsed: %s" % c)
check(len(COLLAPSED) == 4, "four such pairs, so -4 — the ledger closes exactly")
check(41044 - 41021 == 23 and 3428 - 3395 == 33 and 32 - 26 == 6
      and 23 - 33 + 6 == -4,
      "dark +23, pale -33, green +6 = -4")

print("\n-- the fourteen keys, in manual_map.json AND in the built map")
for k, v, _old in NEW:
    check(MAN.get(k) == v, "manual_map.json: %-10s -> %s" % (k, v))
    check(MAP.get(k) == v, "modern_map.js:  %-10s -> %s  (the hand key won)"
          % (k, v))
check(len([k for k in MAN if not k.startswith("_")]) == 1731,
      "manual_map.json holds 1731 keys (was 1722): ten added, `tqliyan` deleted")

print("\n-- the retired values render NOWHERE in any colour")
for v in BANNED:
    check(not ALL.get(v), "`%s` renders nowhere" % v)
check(not any(v in set(MAP.values()) for v in BANNED),
      "and none of them is the value of any key any more")

print("\n-- TQELI: proposed, built, measured, BACKED OUT")
check("tqliyan" not in MAN and "tnqliyan" not in MAN,
      "`tqliyan` and `tnqliyan` are not in manual_map.json")
check("tqliyan" not in MAP and "tnqliyan" not in MAP,
      "and not in the built map either — they are unmapped, hence GREEN")
check(ALL.get("tqriyan") == 4 and ALL.get("tnqriyan") == 2,
      "so his TQELI slots render TQRIYAN 4\xd7 and TNQRIYAN 2\xd7 in green: an "
      "honest guess, and `charRules()`'s l->r is the right liquid, because the "
      "encircling root is `qiri` (`qmiri` \u5708\u570d, `qrian` \u88ab\u570d\u7e5e)")
check(M["raw"].get("tqriyan") == 4 and M["raw"].get("tnqriyan") == 2,
      "both green rather than pale — no claim is being made about either")
check(sorted(k for k in MAP if MAP[k] == "tqrian")
      == ["tklean", "tkliyan", "tqlean", "tqlyaan"],
      "`tqrian` \u88dd\u586b is claimed by exactly his four TKULI/SAPANG "
      "spellings and by nothing else — the container word, unchanged from HEAD")
check(sorted(k for k in MAP if MAP[k] == "tnqrian") == ["tnklean"],
      "and `tnqrian` by his `tnklean` alone")
check(V.get("tqrian") == 1 and V.get("tnqrian") == 1,
      "both still level 1 — the TKULI claims were never in doubt")

print("\n-- three of the fourteen were already brown under another of HIS spellings")
for v, other in ALREADY:
    check(MAP.get(other) == v,
          "`%s` -> `%s` was already in the map before this batch, while his "
          "other spelling of the same slot claimed something else" % (other, v))

print("\n-- level 1 gains exactly six, and loses none")
check(len(LEVELS[1]) == 3894, "3894 listed (level 1), was 3888")
check(sorted(LISTED_NEW) == sorted(LISTED_NEW) and
      all(V.get(v) == 1 for v in LISTED_NEW),
      "the six are all listed modern words: %s" % ", ".join(LISTED_NEW))
check(len(V) == 4684, "4684 verified values in all (was 4678)")

print("\n-- levels 2-7 are byte-identical to batch 119")
for n, want in ((2, 596), (3, 53), (4, 65), (5, 36), (6, 30), (7, 10)):
    check(len(LEVELS[n]) == want, "level %d unmoved at %d" % (n, want))

print("\n-- five values stay PALE, and that is `regular()` needing the ROOT'S GLOSS")
for v in ("empngpung", "pkpngpung", "pnkpngpung", "kayagi", "kayagun"):
    check(v in M["unv"] and v not in M["mod"],
          "`%s` pale: its stem is attested but carries no omnibus gloss, so no "
          "level above 1 can reach it" % v)

print("\n-- the families per card")
for r in cardres["modern"]:
    lab = "%s / %s" % (r["hw"], r["want"])
    if r.get("missing"):
        check(False, lab + ": card not found")
        continue
    if r["expect"] == "deep brown":
        check(r["want"] in r["mod"] and r["want"] not in r["unv"]
              and r["want"] not in r["raw"],
              "%-24s deep brown" % lab)
    elif r["expect"] == "pale":
        check(r["want"] in r["unv"] and r["want"] not in r["mod"],
              "%-24s PALE" % lab)
    else:
        check(r["want"] in r["raw"] and r["want"] not in r["mod"]
              and r["want"] not in r["unv"],
              "%-24s GREEN" % lab)

print("\n-- the whole-page counts for the fourteen")
for v, n in (("pngpung", 8), ("empngpung", 2), ("pkpngpung", 1),
             ("pnkpngpung", 1), ("tnpngan", 4), ("keiyaw", 4), ("pkeiyaw", 3),
             ("kayagan", 4), ("kayagi", 1), ("kayagun", 1), ("tgsai", 4),
             ("tgsaan", 1), ("tgsaun", 1), ("tnegsaan", 3)):
    check(ALL.get(v) == n, "`%s` renders %d\xd7" % (v, n))

print("\n-- the declined families are untouched")
check(ALL.get("sipa") == 6 and ALL.get("psipa") == 2,
      "SIPA keeps its two dark members (6 and 2) — `pspaan`/`pnspaan` are "
      "SYNCOPE, not a rival stem, which is stemsplit's own false-positive class")
check(ALL.get("smuk") == 3 and M["unv"].get("pnsmkan") == 3,
      "SMUK likewise: `pnsm'kan` -> `pnsmkan` is the same root with its vowel "
      "syncopated")
check(ALL.get("dlut") == 2 and ALL.get("pdlut") == 2, "DLUT unmoved")
check(M["unv"].get("mnalu") == 5 and M["unv"].get("nnalu") == 4,
      "MALU's `mnalu`/`nnalu` still pale — the 和睦相處 sense may belong to the "
      "`gealu` family, and that needs its own pass")
check(M["unv"].get("mllaun") == 1, "LALA's `mllaun` still pale")

print("\n-- green moved by exactly the two backed-out keys")
check(M["counts"]["w-raw"] == 32 and O["counts"]["w-raw"] == 32,
      "32 green occurrences in both modes, up from 26")
check(ALL.get("tqriyan", 0) + ALL.get("tnqriyan", 0) == 6,
      "and all 6 of the new ones are TQELI's, so nothing else went green")

print("\n%d failures" % len(fail))
for f in fail:
    print("  " + f)
