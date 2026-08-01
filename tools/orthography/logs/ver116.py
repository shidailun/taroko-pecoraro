# -*- coding: utf-8 -*-
"""Batch 116: the SYNCOPE branch (level 6), and the KAGOX/QAGOX minimal pair.

`regular()` peels affixes off the front and the back, and the only vowel it can
delete is the one `-un`/`-an` swallows at the END. So a root that loses its own
FIRST vowel under affixation is invisible to it — and Truku writes no schwa, so
that is what a great many roots do. CLAUDE.md has recorded the correspondence
since the generator was written: GAMIL 根 is the root, but "where it took root"
is `Tgmilan`, never *Tgamilan.

His TONGOX 品嚐 is the case that names the rule. `tunguh` is listed; his own
paradigm line reads °Tmongox, tongox, tngoxe, tngoxan, tngoxon; and the modern
wordlist writes those slots on the syncopated stem — `ptnguhi` 給…品嚐 is in it,
which is `p` + `tnguh` + `i`. Rule 2 sees `tnguhan` and finds no root at all.

Level 6 re-inserts one vowel between the first two consonants of the stem, and
takes the reading only where the result is a listed word. Inserting a letter he
did not write is a weaker inference than peeling off one he did, so the branch
pays for it with the gate `vouched_root()` already carries: **the agreeing gloss
must be Chinese he attached to the word AS A WORD** — headword, sub-form or
paradigm slot — never an example sentence. That is the whole difference between
a claim and a coincidence here, because these roots are the commonest words in
the book and a clause gloss shares a character with almost anything.

30 values, and the gate is what keeps `nta` out for the second time this
session: `nita` 我們的 is a listed word, `nta` decomposes onto it perfectly, and
the only 我們 in reach is his example sentence 我們去治療眼睛吧. His own slot
gloss says 邀請前往, which is not a pronoun. Same shape for `empnmu` on `namu`
你們的 (his slot is 將化為塵土), `psyangi` on `sayang` 今天；現在 (his slot is
使變肥), `pslgui` on `lagu` 空手 (his slot is 弄直－矯正), `psttuy` on `tutuy`.

**What the gate costs, stated as plainly as what it buys.** Five correct
readings have no slot gloss to offer and are refused: `hlingan` off `huling` 狗,
where his own Chinese is the metalanguage line 「XEULING的斜格形式」 and the 狗
is in 把骨頭給你的狗吧; `mritan` off `mirit` 山羊, identically; `pttuyun` off
`tutuy` 起來 and `shngi` off `hungi` 健忘, which have no slot gloss at all; and
`mswiwil` off `suwiwil` 吊掛. Most of a paradigm is glossless — that is why
levels 2, 3 and 4 all stall — so a rule this speculative has to fail closed.

**A refusal is not a cost until its level is checked**, and three of the twelve
turn out to cost nothing at all, because a rule that ran earlier and asked a
different question is already holding them brown: `shngi` at level 3 by
`vouched()`, `pslgui` and `psryui` at level 4 by `vouched_root()`. So four
correct readings actually stay pale, not five, and of the six the gate is right
to refuse only five ever reached the page unverified. Measuring a gate by what it
turns down over-counts the damage every time; measure it by what goes pale.

Three gate repairs shipped with it, each measured at zero cost to any value
already verified:

  人名 into BOILER.  `tuqul` is glossed 人名（男）and nothing else, and it was
        verifying `emptquli` on the shared 名. Excising the run rather than
        stopping the character is what makes it safe: `suyang` is
        人名（男）; 美麗, and the excision leaves the 美麗 standing.
  用來 into BOILER.  It says how a word is deployed, not what it means. `ruyu`
        水蟲用來當魚餌的 — a water insect USED AS fish bait — was verifying his
        `psryui` 使突出 on the 來. 369 modern glosses carry the run; his own
        用來品嚐的東西 still says 品嚐, which is the gloss it must not break.
  沒 into STOP, beside the 不 that has been there from the start: it is a
        negation and carries no more sense than one. `tatuk` 什麼都沒有 was
        verifying his `ttuki` 敲打 on the 沒 of 我沒碰撞瓶子.

**A fourth repair was proposed, measured, and DISCARDED — that is the finding
of the batch.** `_chars()` stop-filters single characters but not bigrams, and
that asymmetry looks like an oversight. Priced, it destroys eight correct
claims: 我們 (`nyami`=`yami`, `nyamu`=`yamu`), 你的 (`mnisu`=`nisu`), 有時
(`nsuwil`=`suwil` 有時候), 使用 (`pjiyun`=`jiyun`) and 不會 (`meaji`=`eaji`)
are **real lexemes built out of function characters**. STOP is a statement about
a character standing alone, and it does not carry to a bigram. The asymmetry is
correct as it stands, and those eight are asserted below.

The other half of the batch is a **k/q minimal pair the map had collapsed onto
one word**. His KAGOX 邀請 and QAGOX 抓癢 both spell their root `gox`, and both
families were sitting on `kaguh` 抓癢. Modern separates them: 邀請 is `keaguh`
(`kmeaguh`, `kneaguh`, `kmneaguh` all listed) and 抓癢 is `kaguh` — and the tell
is morphological rather than orthographic. **`aguh`'s vowel never drops and
`kaguh`'s always does**: the invite family writes `keaguhan`, `keaguhi`,
`keaguhun` with the vowel intact, while the itch family syncopates to `kguhan`,
`kguhi`, `kguhun` — which is why two of QAGOX's slots are level 6 and none of
KAGOX's is. Six keys by hand; the wrong `kneguhan` leaves the map entirely.

Assertions are over spans, the card section is scoped to the card, and the card
is found by its MODERN headword.
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
  return out;
}"""

# (modern headword of the card, the word that must be deep brown, his headword)
CARDS = [
    ("KEAGUH", "KEAGUH", "KAGOX"),        # the invite family, off the itch word
    ("KEAGUH", "KMEAGUH", "KAGOX"),
    ("KEAGUH", "KEAGUHAN", "KAGOX"),
    ("KEAGUH", "KEAGUHI", "KAGOX"),
    ("KEAGUH", "KEAGUHUN", "KAGOX"),
    ("KEAGUH", "KNEAGUHAN", "KAGOX"),
    ("KAGUH", "KAGUH", "QAGOX"),          # the itch family, unmoved
    ("KAGUH", "KMAGUH", "QAGOX"),
    ("KAGUH", "KGUHAN", "QAGOX"),
    ("KAGUH", "KGUHI", "QAGOX"),          # and its two syncopated slots
    ("KAGUH", "KGUHUN", "QAGOX"),
    ("TUNGUH", "TNGUHAN", "TONGOX"),      # the case that names the rule
    ("TUNGUH", "TNGUHI", "TONGOX"),
    ("SIQA", "SQAAN", "SIQA"),            # 7 occurrences, the batch's largest
    ("SQAAN", "SQAAN", "SQAAN"),
    ("TUYUQ", "TYUQAN", "TUYOQ"),
    ("SDAHAR", "SDHARAN", "SDAXAL"),
    ("DARA", "SDRAAN", "DALA"),
    ("KUKUL", "SKKULI", "KUKUL"),
    ("SIKUL", "SSKULAN", "SIKUL"),
    ("SWIWIL", "PSWWILAN", "SWIWIL"),
    ("SWIWIL", "PSWWILI", "SWIWIL"),
    ("KIYUX", "PKYUXAN", "KIYUX"),
    ("KIYUX", "PKYUXI", "KIYUX"),
    ("NAMA", "PSNMAAN", "NAMA"),
    ("SMIYAH", "PSMYAHAN", "SMIYAX"),
    ("QURI", "PQRIUN", "QOLE"),
]

CARD_PROBE = """(cases) => {
  const out = [];
  const cards = Array.from(document.querySelectorAll('article.entry'));
  for (const [hw, want, his] of cases) {
    const named = cards.filter(c => {
      const h = c.querySelector('.hw');
      return h && h.textContent.trim().toUpperCase().split(/[^A-Z']+/)[0] === hw;
    });
    const card = named.find(c => c.textContent.toUpperCase().indexOf(want) >= 0)
                 || named[0];
    if (!card) { out.push({hw, his, want, missing: true}); continue; }
    const grab = cls => Array.from(card.querySelectorAll('span.' + cls))
                             .map(e => e.textContent.trim().toUpperCase());
    out.push({hw, his, want, mod: grab('w-mod'), unv: grab('w-unv'),
              raw: grab('w-raw')});
  }
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    res, cardres = {}, None
    for mode in ("modern", "original"):
        ctx = b.new_context()
        ctx.add_init_script(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','%s')" % mode)
        pg = ctx.new_page()
        pg.goto(URL)
        pg.wait_for_timeout(9000)
        res[mode] = pg.evaluate(PROBE)
        if mode == "modern":
            cardres = pg.evaluate(CARD_PROBE, CARDS)
        ctx.close()
    b.close()

M, O = res["modern"], res["original"]
ALL = collections.Counter()
for k in ("mod", "unv", "raw"):
    ALL.update(M[k])

print("modern", M["counts"], "original", O["counts"])
print("verified.js: %d listed, %d regularly inflected, %d vouched, %d off a "
      "vouched root, %d sister slots, %d syncopated roots"
      % (len(LISTED), len(INFL), len(VOUCHED), len(VROOT), len(SISTR),
         len(SYNCP)))

print("\n--- the totals, measured not computed")
check(M["counts"]["w-mod"] == 40971, "w-mod 40971 (got %d)" % M["counts"]["w-mod"])
check(M["counts"]["w-unv"] == 3478, "w-unv 3478 (got %d)" % M["counts"]["w-unv"])
check(M["counts"]["w-raw"] == 26, "w-raw 26 (got %d)" % M["counts"]["w-raw"])
tot = sum(M["counts"].values())
check(tot == 44475, "44475 words on screen (got %d)" % tot)
rate = 100.0 * M["counts"]["w-mod"] / tot
check(abs(rate - 92.12) < 0.01,
      "92.12%% of occurrences verified, up from 91.98%% (got %.2f%%)" % rate)

print("\n--- the 30 syncopated roots are deep brown wherever they reach the page")
check(len(SYNCP) == 30, "30 values at level 6 (got %d)" % len(SYNCP))
seen = [v for v in SYNCP if ALL.get(v, 0)]
wrong = [v for v in seen if M["unv"].get(v, 0)]
check(len(seen) == 30, "all 30 reach the page (got %d)" % len(seen))
check(not wrong, "none is painted pale (%s)" % (wrong[:8] or "none"))
occ = sum(M["mod"].get(v, 0) for v in seen)
check(occ == 60, "they carry 60 occurrences of deep brown (got %d)" % occ)
# w-mod rose by 65 and these 30 account for 60 of it. The other 5 are the KAGOX
# remap and they close the sum exactly: `kguhi` and `kguhun` used to be the
# spelling of BOTH families' -i and -un slots, so five of the occurrences the
# batch-115 census counted under them are now spelled the invite way.
check(M["mod"].get("kguhi", 0) + M["mod"].get("keaguhi", 0) == 2,
      "kguhi 1 + keaguhi 1 = the 2 occurrences kguhi carried at batch 115 "
      "(got %d + %d)" % (M["mod"].get("kguhi", 0), M["mod"].get("keaguhi", 0)))
check(M["mod"].get("kguhun", 0) + M["mod"].get("keaguhun", 0) == 6,
      "kguhun 2 + keaguhun 4 = the 6 occurrences kguhun carried at batch 115 "
      "(got %d + %d)" % (M["mod"].get("kguhun", 0),
                         M["mod"].get("keaguhun", 0)))

print("\n--- a hand-read sample: the root, and the character his own slot shares")
for v, why in [
        ("sqaan", "off siqa 害羞 — and his own gloss says 參見 SIQA"),
        ("kguhun", "QAGOX's -un slot; kaguh 抓癢 against his 抓、搔"),
        ("kguhi", "the same paradigm's imperative"),
        ("tnguhan", "off tunguh 品嚐 — the case the rule is named for"),
        ("tnguhi", "his 嚐嚐看！, the imperative of the same"),
        ("tyuqan", "off tuyuq 痰 against his 痰盂－唾沫"),
        ("sdharan", "off dahar 靠著 against his 倚靠－背靠"),
        ("sdraan", "off dara 月經的血 against his 出血（自發的）"),
        ("psnmaan", "off nama 先去預備 — batch 37 exonerated this root, and "
                    "this is the rule finally reaching its slot"),
        ("skkuli", "off kukul 口袋 against his 放進口袋"),
        ("sskulan", "off sikul 推 against his 推擠、擁擠"),
        ("pswwilan", "off wiwil 掛 against his 懸掛－吊起"),
        ("pkyuxan", "off kiyux 很擠 against his 擁擠——非常密集"),
        ("plqihan", "off luqih 受傷 against his 造成傷口"),
        ("phyugan", "off hiyug 站立 against his 使站立－豎立"),
        ("jjili", "off jijil 提 against his 用手、用臂提著"),
        ("ptungun", "off putung 火柴 against his 擦火柴"),
        ("psmyahan", "off miyah 來 against his 為促使到來所付出的活動"),
        ("pqriun", "off qiri 彎向 against his 轉向"),
        ("plqihun", "the -un slot of the same wound root")]:
    check(M["mod"].get(v, 0) > 0 and not M["unv"].get(v, 0),
          "%-9s deep brown, %d occ -- %s" % (v, M["mod"].get(v, 0), why))
    check(V.get(v) == 6, "%-9s is level 6 in verified.js (got %s)" % (v, V.get(v)))

print("\n--- the gloss gate, and the ten readings it refuses OUTRIGHT")
print("    (four of them correct, and that is the price of the other six)")
for v, why in [
        ("nta", "nita 我們的 — his slot says 邀請前往; the 我們 is a sentence"),
        ("empnmu", "namu 你們的 — his slot says 將化為塵土"),
        ("psyangi", "sayang 今天；現在 — his slot says 使變肥－養肥"),
        ("psyangun", "the same, and no root is reachable for it at all"),
        ("psttuy", "tutuy 起來 — he gave that slot no Chinese of its own"),
        ("hlingan", "huling 狗 IS right; his slot is 「XEULING的斜格形式」"),
        ("mritan", "mirit 山羊 IS right; his slot is 「MILIT 的斜格形。」"),
        ("pttuyun", "tutuy 起來 IS right; his slot is glossless"),
        ("mswiwil", "suwiwil 吊掛 IS right; his slot says 懸垂的－搖晃的"),
        ("tnguhun", "the third TONGOX slot — 「同上之動詞形。」 is all "
                    "metalanguage, so BOILER leaves nothing to agree with")]:
    check(v not in V, "%-9s is absent from verified.js — %s" % (v, why))
    if ALL.get(v, 0):
        check(M["unv"].get(v, 0) > 0 and not M["mod"].get(v, 0),
              "%-9s still pale (%d occurrences)" % (v, M["unv"].get(v, 0)))
    else:
        check(not ALL.get(v, 0), "%-9s reaches no card at all" % v)

print("\n--- the three gate repairs, each priced at zero before it went in")
check("emptquli" not in V,
      "emptquli absent — tuqul is 人名（男）and nothing else, so the 名 it "
      "shared was a label rather than a sense")
check(M["unv"].get("emptquli", 0) == 1 and not M["mod"].get("emptquli", 0),
      "emptquli still pale (1 occurrence)")
check("ttuki" not in V,
      "ttuki    absent — tatuk 什麼都沒有 was agreeing with his 敲打 on the 沒 "
      "of 我沒碰撞瓶子, and 沒 is a negation like the 不 already in STOP")
check(M["unv"].get("ttuki", 0) == 2 and not M["mod"].get("ttuki", 0),
      "ttuki    still pale (2 occurrences)")
# `psryui` is the 用來 case, and it is brown for a DIFFERENT reason: level 4
# holds it independently. The excision cost it nothing, which is the measurement.
check(V.get("psryui") == 4,
      "psryui   is level 4, not 6 — the 用來 excision took away the syncope "
      "reading (ruyu 水蟲用來當魚餌的) and vouched_root() still vouches for it")

# And `psryui` is not alone. A refusal is not a COST until its level is checked:
# two more values the gloss gate turned down are brown anyway, held by a rule that
# ran earlier and asked a different question. `pslgui` would have read as a
# syncope of `lagu` 空手 against his 弄直－矯正, and the gate was right to refuse it
# — but vouched_root() had already vouched for it, so nothing changed on the page.
# `shngi` is the opposite shape: its syncope reading (hungi 健忘) is CORRECT and
# the gate refused it only because his slot carries no Chinese to agree with, and
# vouched() holds it at level 3 regardless. So of the twelve readings the gate
# turns down, ten are refusals with nothing behind them and these two cost zero.
check(V.get("pslgui") == 4,
      "pslgui   is level 4 — the gate refused its syncope reading (lagu 空手 "
      "against his 弄直－矯正) and vouched_root() had it already")
check(V.get("shngi") == 3,
      "shngi    is level 3 — the gate refused a CORRECT syncope reading "
      "(hungi 健忘) for want of a gloss, and vouched() had it already")
for v in ("pslgui", "shngi"):
    check(M["mod"].get(v, 0) > 0 and not M["unv"].get(v, 0),
          "%-9s deep brown, %d occ — the refusal cost it nothing"
          % (v, M["mod"].get(v, 0)))

print("\n--- the fourth repair was WRONG, and these eight are why")
print("    (STOP is about a character alone; a bigram of two of them is a word)")
for v, why in [("nyami", "yami 我們"), ("nyamu", "yamu 你們"),
               ("mnisu", "nisu 你的"), ("nsuwil", "suwil 有時候"),
               ("pjiyun", "jiyun 使用"), ("meaji", "eaji 不會"),
               ("knhwayun", "the same class"), ("pdkai", "the same class")]:
    check(V.get(v) == 2, "%-9s still level 2 — %s" % (v, why))
    check(not M["unv"].get(v, 0), "%-9s not painted pale" % v)

print("\n--- the KAGOX / QAGOX minimal pair: two families, two words")
for v, lv, why in [("keaguh", 1, "his KAGOX 邀請, listed"),
                   ("kmeaguh", 1, "listed"),
                   ("kneaguh", 1, "listed"),
                   ("kmneaguh", 1, "listed"),
                   ("keaguhan", 2, "blind, but a regular slot of a listed root"),
                   ("keaguhi", 2, "the same"),
                   ("keaguhun", 2, "the same"),
                   ("kneaguhan", 2, "the same"),
                   ("kaguh", 1, "his QAGOX 抓癢, a different word"),
                   ("kmaguh", 1, "listed"),
                   ("kguhan", 1, "listed"),
                   ("kguhi", 6, "syncopated — the itch root drops its vowel"),
                   ("kguhun", 6, "the same")]:
    check(V.get(v) == lv, "%-10s level %s — %s" % (v, lv, why))
for gone, why in [("kneguhan", "the old value; his Kngoxan is kneaguhan"),
                  ("keguhan", "never a word on either side of the pair")]:
    check(not ALL.get(gone, 0), "%-9s is rendered nowhere — %s" % (gone, why))
# the invite family never syncopates and the itch family always does; if either
# statement were wrong the two would be indistinguishable and the pair collapses
check(all(V.get(v) for v in
          ["keaguhan", "keaguhi", "keaguhun", "kneaguhan"]),
      "every KEAGUH slot keeps the root vowel and is verified")
check(all(V.get(v) for v in ["kguhan", "kguhi", "kguhun"]),
      "every KAGUH slot drops it and is verified")

print("\n--- the earlier levels are unharmed by the three gate repairs")
check(len(LISTED) == 3882, "3882 listed (got %d)" % len(LISTED))
check(len(INFL) == 592, "592 regularly inflected (got %d)" % len(INFL))
check(len(VOUCHED) == 53, "53 vouched by their own paradigm (got %d)" % len(VOUCHED))
check(len(VROOT) == 65, "65 off a vouched root (got %d)" % len(VROOT))
check(len(SISTR) == 36, "36 sister slots, exactly as batch 115 left them (got %d)"
      % len(SISTR))
for name, pool in [("listed", LISTED), ("inflected", INFL),
                   ("vouched", VOUCHED), ("vouched-root", VROOT),
                   ("sister", SISTR), ("syncopated", SYNCP)]:
    bad = [v for v in pool if M["unv"].get(v, 0)]
    check(not bad, "no %s value went pale (%s)" % (name, bad[:8] or "none"))

print("\n--- batch 115's sister slots are still dark")
for v in ["lmuan", "qlhangan", "spagan", "nuhun", "kwaxan", "giman", "hglqi",
          "lingan", "slui", "qdaun", "tcingi"]:
    check(M["mod"].get(v, 0) > 0 and not M["unv"].get(v, 0),
          "%-9s deep brown, %d occurrences" % (v, M["mod"].get(v, 0)))

print("\n--- the names did NOT turn dark, which is how a shape rule fails")
print("    (a branch that forgets regular()'s frozen check reaches these)")
for n in ["sibal", "liwis", "mikat", "ingay", "lauken", "tatu", "talan",
          "banan", "sikat", "imin", "timin", "tain", "pilin"]:
    got = M["unv"].get(n, 0)
    check(got > 0 and not M["mod"].get(n, 0),
          "%-9s still pale (%d occurrences)" % (n, got))
    check(n not in V, "%-9s is absent from verified.js altogether" % n)
# `mknsat` is his KENSAT 警察, tier J: a loan with no Truku root at all, and the
# first sweep of the syncope branch surfaced it before the frozen check went in.
check("mknsat" not in V, "mknsat is absent — a tier-J loan, not a syncopated root")

print("\n--- per card, scoped to the card")
for r in cardres:
    if r.get("missing"):
        check(False, "%s (%s): no card" % (r["hw"], r["his"]))
        continue
    where = ("deep brown" if r["want"] in r["mod"] else
             "PALE" if r["want"] in r["unv"] else
             "GREEN" if r["want"] in r["raw"] else "ABSENT")
    check(where == "deep brown", "%-8s (%-6s) %-10s %s"
          % (r["hw"], r["his"], r["want"], where))
# the itch card must not have picked up the invite spelling, or the pair is
# still collapsed and the k/q distinction has simply moved
for r in cardres:
    if r["hw"] == "KAGUH":
        check(not any(w.startswith("KEAGUH") for w in
                      r["mod"] + r["unv"] + r["raw"]),
              "KAGUH card carries no KEAGUH- form (%s)" % r["want"])

print("\n--- green is exactly where it was")
GREEN22 = set("""curuphun diram dpnah dubut gaugan gryeq kmrnu kruheng meq
mkruheng mngusyeh ndiyan pa paaaq r remarque req ryeq skrt sruweq supyeh
upskra""".split())
check(set(M["raw"]) == GREEN22, "the same 22 green types (%s)"
      % (set(M["raw"]) ^ GREEN22 or "identical"))
check(O["counts"]["w-raw"] == M["counts"]["w-raw"], "green identical in both modes")

print("\n%d failures" % len(fail))
for f in fail:
    print("  " + f)
