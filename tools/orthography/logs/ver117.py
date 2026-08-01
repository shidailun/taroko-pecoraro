# -*- coding: utf-8 -*-
"""Batch 117: the uqu / TOOQO cluster, and which SLOT a word was written in.

His TOOQO 生氣、動怒－被冒犯 is modern `teuqu` 生氣;負氣, and the family was
scattered. The bare form was mapped to `tuuqu`, a spelling that occurs exactly
once in the corpus, while six suffixed slots sat on `tquw-` — `ptquwan`,
`ptquwun`, `ptquwi`, `tquwan` — which is not a stem at all. Every already-curated
member takes `-eu-` (`qneuqu` 錯誤, `mqneuqu`, both listed), so the family had two
stems and one of them was a typo of the other. Eleven keys.

**The n-gram inventory was measured before the six illicit values were replaced,
and it did not veto them.** Across all 38,687 modern types the `euq` population is
about 23 types — `euqu` 20, `euqa` 2, `euq$` 1 — and **`euqi` is 0**, so the two
imperatives take a four-gram the orthography never writes. Four of the six land
licit (`teuqan`, `pteuqan`, `pnteuqan`, `pteuqun`); the two `-i` slots do not.
Shipped anyway, and the reason is the one thing licitness cannot touch: the value
they replace (`ptquwi`) is **also** illicit AND on the wrong root, and
`build_verified.py` never asks `T.licit()` at all. So an illicit value that is not
listed simply stays pale either way. The trade buys the right family at no cost in
claimed verification — which is exactly the case where a shape objection is a
statement about the audit tool rather than about the page.

**The batch's real finding is that a paradigm SLOT decides verifiability.**
`pteuqan` and `pteuqun` verify at level 2; `teuqan` and `pnteuqan` go pale. The
difference is not the morphology — all four are the same regular -an/-un on the
same root — and it is not the spelling. `_his_glosses()` feeds every slot on a
sub-form's ° line **that sub-form's own gloss**, and his `Ptooqo` line reads
`°Ptooqo, ptooqo, ptqoe (pt'qoe), ptqoan, ptqoon` under the gloss 使…生氣, so its
slots inherit 生氣 and agree with modern `pteuqu` 讓（使）人生氣. `Tqoan` and
`Pntqoan` carry only his own Chinese, **冒犯／委屈**, and the modern lexicon glosses
the root **生氣**.

That is the second finding, and it is a limit rather than a bug: his Chinese and
the modern gloss name **the two ends of one event** — the offence received against
the anger felt — with not one character in common. No rule that compares glosses
can see they are one word. Both are correctly spelled; they are simply
unverifiable, and the honest colour for that is pale.

**A rule change was measured and rejected.** `roots()` adds back a swallowed root
vowel only for `sf in ("un","an","ani","anay","aneyi")`; the imperatives `-i`,
`-ay`, `-aw` get no such branch, which is precisely why `pteuqi` is unreachable
even though `pteuqu` is listed. `swallow117.py` widened it and priced the result:
**7 types / 10 occurrences**, three of them illicit (`pteuqi`, `qhdi`, `pnnaki`)
and several resting on a single weak character (`prudaw` on 亂, `phrisi` on 別).
Not worth touching `inflection.py` for.

**QQOGO looked at, and refused with a reason.** His QQOGO 公雞的啼叫 is modern
`qgu` 公雞叫聲 — an exact gloss match with a real family (`msqgu`, `pqguaw`,
`qmqgu`, `qsqgu`) — and `qqogo` → `qqgu` is **already brown at level 1**. The pale
remainder (`qnqgu` 5, `qnqguan` 2, `psqgu` 2) is already correctly spelled and
simply unverifiable: `regular()` reaches it through the `-n-` infix branch onto
`qqgu`, and `qqgu` is a **glossless corpus token**, so there is nothing to agree
with. His own PSQGO is glossed 「？？」. A batch that changes the spelling here
would move nine occurrences from one correct spelling to another and verify
nothing.

`snoqo` HELD. The only shape-consistent candidate is `sneuqu` 不接受人的建議,
which contradicts his 頑皮－開心果－愛開玩笑的人 — and level 1 asks nothing about
gloss, so mapping it would **auto-verify** a claim its own gloss refutes.

One consequence visible on the page: in modern mode the TEUQU paradigm line reads
`° Pteuqu, pteuqu, pteuqi, pteuqan, pteuqun.` — his two spellings of the
imperative, `ptqoe` and `pt'qoe`, now converge on one word, so `collapsed()` drops
the bracket. Pecoraro mode still shows both. Fixing a family can silently merge
two of his spellings on screen, and that is a display change the map diff cannot
predict.
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

MAN = io.open(H + "tools/orthography/manual_map.json", encoding="utf-8").read()

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
    ("TEUQU", "TEUQU", "deep brown"),        # his TOOQO, off the one-off tuuqu
    ("TEUQU", "PTEUQU", "deep brown"),       # his Ptooqo 使…生氣
    ("TEUQU", "SPTEUQU", "deep brown"),      # his Sptooqo 用來冒犯的
    ("TEUQU", "PTEUQAN", "deep brown"),      # the -an slot ON Ptooqo's ° line
    ("TEUQU", "PTEUQUN", "deep brown"),      # the -un slot, same line
    ("TEUQU", "TEUQAN", "PALE"),             # his own slot, glossed 冒犯 only
    ("TEUQU", "PNTEUQAN", "PALE"),           # the same, with the -n- past
    ("TEUQU", "PTEUQI", "PALE"),             # euqi is 0 of a 23-type population
    ("TEUQU", "TNEUQAN", "PALE"),            # the -n- past of Tqoan
    ("QNEUQU", "QNEUQU", "deep brown"),      # the already-listed half, unmoved
    ("QNEUQU", "MQNEUQU", "deep brown"),
    ("QQGU", "QQGU", "deep brown"),          # QQOGO: the head was always brown
    ("QQGU", "QNQGU", "PALE"),               # correctly spelled, unverifiable
    ("QQGU", "QNQGUAN", "PALE"),
    ("PSQGU", "PSQGU", "PALE"),
    ("SNUQU", "SNUQU", "PALE"),              # held: sneuqu contradicts his gloss
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
        pg.goto(URL)
        pg.wait_for_timeout(9000)
        res[mode] = pg.evaluate(PROBE)
        cardres[mode] = pg.evaluate(CARD_PROBE, CARDS)
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
check(M["counts"]["w-mod"] == 40987, "w-mod 40987 (got %d)" % M["counts"]["w-mod"])
check(M["counts"]["w-unv"] == 3462, "w-unv 3462 (got %d)" % M["counts"]["w-unv"])
check(M["counts"]["w-raw"] == 26, "w-raw 26 (got %d)" % M["counts"]["w-raw"])
tot = sum(M["counts"].values())
check(tot == 44475, "44475 words on screen (got %d)" % tot)
rate = 100.0 * M["counts"]["w-mod"] / tot
check(abs(rate - 92.16) < 0.01,
      "92.16%% of occurrences verified, up from 92.12%% (got %.2f%%)" % rate)
# Pecoraro mode carries 487 more words because his spellings do not converge:
# `ptqoe` and `pt'qoe` are two tokens there and one word in modern mode.
check(O["counts"]["w-mod"] == 41420, "original w-mod 41420 (got %d)"
      % O["counts"]["w-mod"])
check(O["counts"]["w-unv"] == 3516, "original w-unv 3516 (got %d)"
      % O["counts"]["w-unv"])
check(O["counts"]["w-raw"] == 26, "original w-raw 26 (got %d)"
      % O["counts"]["w-raw"])
check(M["cards"] == 1967 and O["cards"] == 1967,
      "1967 cards in both modes (got %d / %d)" % (M["cards"], O["cards"]))

print("\n--- the six new values, at the level each one earned")
for v, lv, occ, why in [
        ("teuqu", 1, 6, "his TOOQO — listed; it replaces `tuuqu`, a spelling "
                        "with exactly one corpus occurrence"),
        ("pteuqu", 1, 6, "his Ptooqo 使…生氣 against 讓（使）人生氣 — listed"),
        ("spteuqu", 2, 2, "his Sptooqo 用來冒犯、惹人生氣的 — regular s-p- on it"),
        ("empqneuqu", 2, 2, "his Mpqnoqo, beside the listed qneuqu / mqneuqu 錯誤"),
        ("pteuqan", 2, 4, "the -an slot, verified on the 生氣 its own ° line "
                          "hands down from Ptooqo"),
        ("pteuqun", 2, 2, "the -un slot of the same line, the same way")]:
    check(V.get(v) == lv, "%-10s level %s — %s" % (v, lv, why))
    check(M["mod"].get(v, 0) == occ and not M["unv"].get(v, 0),
          "%-10s deep brown, %d occurrences (got %d mod / %d unv)"
          % (v, occ, M["mod"].get(v, 0), M["unv"].get(v, 0)))
# the sum closes exactly: w-mod rose 40971 -> 40987, and teuqu contributes
# nothing net because the six occurrences it carries were already brown as tuuqu
new = sum(M["mod"].get(v, 0) for v in
          ("pteuqu", "spteuqu", "empqneuqu", "pteuqan", "pteuqun"))
check(new == 16, "the five genuinely new values carry 16 occurrences, which is "
                 "the whole of the +16 in w-mod (got %d)" % new)
check(not ALL.get("tuuqu", 0),
      "tuuqu is rendered nowhere — the one-off spelling is gone from the page")
check("tuuqu" not in V, "tuuqu has left verified.js as well")
check(M["mod"].get("teuqu", 0) == 6,
      "teuqu carries the 6 occurrences tuuqu used to (got %d)"
      % M["mod"].get("teuqu", 0))

print("\n--- the four that stay pale, and WHY each one does")
for v, occ, why in [
        ("teuqan", 3, "his Tqoan is glossed 冒犯／委屈 — the offence RECEIVED — "
                      "while modern teuqu is 生氣, the anger FELT. Same word, "
                      "no shared character, and no rule can see it"),
        ("pnteuqan", 2, "the -n- past of the same slot, and the same gloss"),
        ("pteuqi", 2, "`euqi` is 0 of a 23-type euq population, and roots() "
                      "swallows the root vowel for -un/-an but never for -i"),
        ("tneuqan", 1, "the -n- past of Tqoan; it was `tnquan`, illicit and on "
                       "the wrong stem, and the card probe is what surfaced it")]:
    check(v not in V, "%-10s absent from verified.js — %s" % (v, why))
    check(M["unv"].get(v, 0) == occ and not M["mod"].get(v, 0),
          "%-10s pale, %d occurrences (got %d unv / %d mod)"
          % (v, occ, M["unv"].get(v, 0), M["mod"].get(v, 0)))

print("\n--- the already-listed half of the family is unmoved")
for v, occ in [("qneuqu", 8), ("mqneuqu", 4), ("qnquan", 4)]:
    check(V.get(v) == 1, "%-10s still level 1" % v)
    check(M["mod"].get(v, 0) == occ and not M["unv"].get(v, 0),
          "%-10s deep brown, %d occurrences (got %d)"
          % (v, occ, M["mod"].get(v, 0)))

print("\n--- the six ILLICIT tquw- values are gone from the page entirely")
for gone in ("tquwan", "ptquwan", "ptquwun", "ptquwi", "tnquan", "pntquwan"):
    check(not ALL.get(gone, 0), "%-10s is rendered nowhere" % gone)

print("\n--- QQOGO: examined, and REFUSED with a reason")
check(V.get("qqgu") == 1,
      "qqgu      is level 1 — his QQOGO 公雞的啼叫 is `qgu` 公雞叫聲, an exact "
      "gloss match, and the head has been brown all along")
for v, occ in [("qnqgu", 5), ("qnqguan", 2), ("psqgu", 2)]:
    check(v not in V and M["unv"].get(v, 0) == occ,
          "%-10s pale, %d occurrences — correctly spelled and unverifiable: "
          "regular() reaches it through the -n- infix onto `qqgu`, and `qqgu` "
          "is a glossless corpus token" % (v, occ))
check(M["unv"].get("qnqgu", 0) + M["unv"].get("qnqguan", 0)
      + M["unv"].get("psqgu", 0) == 9,
      "the whole QQOGO remainder is 9 pale occurrences, not 10 — `knqogo` and "
      "`qnqogo` both map to `qnqgu`, so the value's total was being read twice")

print("\n--- snoqo is HELD, and the hold is the assertion")
check('"snoqo": "snuqu"' in MAN,
      "snoqo still maps to `snuqu`, NOT to the family stem — the only "
      "shape-consistent candidate is `sneuqu` 不接受人的建議, which "
      "contradicts his 頑皮－開心果－愛開玩笑的人, and level 1 asks nothing "
      "about gloss, so moving it would AUTO-VERIFY a claim its own gloss "
      "refutes. An illicit value that stays pale is the cheaper error")
check("sneuqu" not in MAN and not ALL.get("sneuqu", 0),
      "sneuqu appears neither in the map nor on the page")
check(M["unv"].get("snuqu", 0) == 2 and "snuqu" not in V,
      "snuqu still pale, 2 occurrences (got %d)" % M["unv"].get("snuqu", 0))

print("\n--- the eleven keys are in manual_map.json and nothing else moved")
for k, v in [("tooqo", "teuqu"), ("ptooqo", "pteuqu"), ("sptooqo", "spteuqu"),
             ("mpqnoqo", "empqneuqu"), ("tqoan", "teuqan"),
             ("ptqoan", "pteuqan"), ("pntqoan", "pnteuqan"),
             ("ptqoon", "pteuqun"), ("ptqoe", "pteuqi"),
             ("pt'qoe", "pteuqi"), ("tnqoan", "tneuqan")]:
    check('"%s": "%s"' % (k, v) in MAN, '%-10s -> %s' % (k, v))

print("\n--- every earlier level is exactly where batch 116 left it")
check(len(LISTED) == 3883,
      "3883 listed — 3882 + teuqu + pteuqu - tuuqu (got %d)" % len(LISTED))
check(len(INFL) == 596,
      "596 regularly inflected — 592 + the four -eu- slots (got %d)" % len(INFL))
check(len(VOUCHED) == 53, "53 vouched, unchanged (got %d)" % len(VOUCHED))
check(len(VROOT) == 65, "65 off a vouched root, unchanged (got %d)" % len(VROOT))
check(len(SISTR) == 36, "36 sister slots, unchanged (got %d)" % len(SISTR))
check(len(SYNCP) == 30, "30 syncopated roots, unchanged (got %d)" % len(SYNCP))
for name, pool in [("listed", LISTED), ("inflected", INFL),
                   ("vouched", VOUCHED), ("vouched-root", VROOT),
                   ("sister", SISTR), ("syncopated", SYNCP)]:
    bad = [v for v in pool if M["unv"].get(v, 0)]
    check(not bad, "no %s value went pale (%s)" % (name, bad[:8] or "none"))

print("\n--- batch 116's own work is still dark")
for v in ("keaguh", "kmeaguh", "keaguhan", "keaguhi", "keaguhun", "kneaguhan",
          "kaguh", "kmaguh", "kguhan", "kguhi", "kguhun", "tnguhan", "tnguhi",
          "sqaan", "tyuqan", "sdharan", "sdraan", "skkuli", "sskulan",
          "pswwilan", "pswwili", "pkyuxan", "pkyuxi", "psnmaan", "psmyahan",
          "pqriun"):
    check(M["mod"].get(v, 0) > 0 and not M["unv"].get(v, 0),
          "%-10s deep brown, %d occurrences" % (v, M["mod"].get(v, 0)))

print("\n--- per card, scoped to the card")
for r in cardres["modern"]:
    if r.get("missing"):
        check(False, "%s: no card for %s" % (r["hw"], r["want"]))
        continue
    where = ("deep brown" if r["want"] in r["mod"] else
             "PALE" if r["want"] in r["unv"] else
             "GREEN" if r["want"] in r["raw"] else "ABSENT")
    check(where == r["expect"], "%-8s card: %-10s %s (wanted %s)"
          % (r["hw"], r["want"], where, r["expect"]))

print("\n--- collapsed() reached the paradigm line, and only in modern mode")
mp = [x for x in M["par"] if "euq" in x.lower()]
op = [x for x in O["par"] if "ptqo" in x.lower()]
check(mp == ["° Pteuqu, pteuqu, pteuqi, pteuqan, pteuqun."],
      "modern line reads '° Pteuqu, pteuqu, pteuqi, pteuqan, pteuqun.' — his "
      "two spellings of the imperative converge on one word, so the bracket "
      "is dropped (got %s)" % (mp or "nothing"))
check(op == ["° Ptooqo, ptooqo, ptqoe (pt'qoe), ptqoan, ptqoon."],
      "Pecoraro mode keeps '° Ptooqo, ptooqo, ptqoe (pt'qoe), ptqoan, ptqoon.' "
      "— there they really are two spellings (got %s)" % (op or "nothing"))

print("\n--- green is exactly where it was")
GREEN22 = set("""curuphun diram dpnah dubut gaugan gryeq kmrnu kruheng meq
mkruheng mngusyeh ndiyan pa paaaq r remarque req ryeq skrt sruweq supyeh
upskra""".split())
check(set(M["raw"]) == GREEN22, "the same 22 green types (%s)"
      % (set(M["raw"]) ^ GREEN22 or "identical"))
check(O["counts"]["w-raw"] == M["counts"]["w-raw"],
      "green identical in both modes")

print("\n%d failures" % len(fail))
for f in fail:
    print("  " + f)
