# -*- coding: utf-8 -*-
"""Batch 114: level 2 composed over level 3 — a regular inflection of a root the
wordlist only vouches for through its OWN inflections.

Batch 112 verified a word the wordlist does not list when it is a regular
inflection of a root the wordlist does list. Batch 113 verified a ROOT the
wordlist does not list bare when it lists two or more of that root's paradigm
slots. This is the two composed, and neither rule could reach it alone:
`regular()` demands `c in self.lex` for the root, and `vouched()` only ever
returns the citation form itself.

`pspuhun` is the shape. `spuh` is never listed bare, but `spuhun`, `spuhan`,
`spuhi`, `snpuhan`, `pspuhan` 醫院 and `pnspuhan` 被治療過 are, and his gloss for
the value is 使人施行醫治 — the -un sister of a slot the wordlist does list, off a
root it does not. `natas` (n- on `atas`, which batch 113 vouched through `matas`
寫字) and `prijil` (p- on `rijil`, through `mrijil` 使彎曲) are the same.

The evidence chain is one step longer than either rule alone: neither the value
nor its root is listed, and the gloss agreement has to be taken against a
SUPPORTER, because an unlisted root has no gloss of its own to agree with. So
the gate is tighter at the other end — **his Chinese must be a gloss he attached
to the word AS a word**, a headword, sub-form or paradigm gloss, never one
belonging to an example sentence. A sentence gloss describes a whole clause and
shares a character with almost anything: it is what let `sktama` 已故的父親 agree
with `kmtama` 信奉上帝 on the 信 of an unrelated sentence, when the real
morphology is `sk-` 'the late' on `tama` 父. The slot-only gate kills `sktama`
and `sblangan` by itself, and both are asserted pale below.

Three values survive every gate and are still wrong, because the defect is in
the ROOT rather than in the gloss, and no gate reaches it:

  nnalu / empnalu   his 好、良善（過去式）. `nalu` is a phantom: `nmalu` is the
                    preterite of `malu` 好 and `snalu` the perfective of `smalu`
                    做 — two different words that strip to the same four letters,
                    so guard 1's "two distinct affix pairs" was satisfied by
                    conflating two roots. A paradigm-coherence guard was written
                    and abandoned: it killed 44 good claims with them, because
                    most supporters carry no gloss at all, so supporter-to-
                    supporter character overlap measures gloss density and not
                    coherence.
  nilaq             his entry is the edible tree mushroom, and it agreed with
                    `mnilaq` 起屑 to flake only on the 起 of 令人想起海藻.

They are hand-excluded (`HAND_NOT_ROOTED`). A fourth, `ngklaan`, needed no hand
list: 已 joined `STOP`, since it is the perfective marker and nothing else, so
his （已完成的）攀登 was agreeing with `gnkla` 已知道的 — climbing against knowing,
two words with no sense in common at all.

Assertions are over spans, and the card section is scoped to the card and finds
its cards by their MODERN headword, because that is what modern mode renders:
his SAPOX card prints SAPUH and his TÖTING card TUCING.
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
    ("SAPUH", "PSPUHUN", "SAPOX"),      # the case that names the rule
    ("PATAS", "NATAS", "PATAS"),        # n- on batch 113's vouched `atas`
    ("RIJIL", "PRIJIL", "LIDIL"),       # p- on batch 113's vouched `rijil`
    ("TUCING", "PTCINGAN", "TÖTING"),
    ("QARAS", "PSQRASAN", "QALAS"),
    ("HRAPAS", "PHRPASI", "XLAPAS"),
    ("BLAIQ", "EMBLIQAN", "BLAEQ"),     # the commonest of them, 7 occurrences
    ("RAHUL", "PGRAHUL", "LAXOL"),
    ("RAMAL", "MSRAMAL", "LAMAL"),
    ("PAKUX", "EMPAKUX", "PAKOX"),
    ("BARAW", "MKBARAW", "BALAO"),
    ("ELUG", "MEELUG", '"LU'),
]

CARD_PROBE = """(cases) => {
  const out = [];
  const cards = Array.from(document.querySelectorAll('article.entry'));
  for (const [hw, want, his] of cases) {
    // his headword can head TWO cards, so take the one carrying the word and
    // only then ask what colour it is.
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
      "vouched root" % (len(LISTED), len(INFL), len(VOUCHED), len(VROOT)))

print("\n--- the totals, measured not computed")
check(M["counts"]["w-mod"] == 40824, "w-mod 40824 (got %d)" % M["counts"]["w-mod"])
check(M["counts"]["w-unv"] == 3625, "w-unv 3625 (got %d)" % M["counts"]["w-unv"])
check(M["counts"]["w-raw"] == 26, "w-raw 26 (got %d)" % M["counts"]["w-raw"])
tot = sum(M["counts"].values())
check(tot == 44475, "44475 words on screen (got %d)" % tot)
rate = 100.0 * M["counts"]["w-mod"] / tot
check(abs(rate - 91.79) < 0.01, "91.79%% of occurrences verified (got %.2f%%)" % rate)

print("\n--- the 65 level-4 values are deep brown wherever they reach the page")
seen = [v for v in VROOT if ALL.get(v, 0)]
wrong = [v for v in seen if M["unv"].get(v, 0)]
check(len(VROOT) == 65, "65 values at level 4 (got %d)" % len(VROOT))
check(len(seen) >= 60, "%d of them reach the page" % len(seen))
check(not wrong, "none is painted pale (%s)" % (wrong[:8] or "none"))
occ = sum(M["mod"].get(v, 0) for v in seen)
check(occ >= 115, "they carry %d occurrences of deep brown" % occ)

print("\n--- the four the gates refused, and why each was refused")
for v, why in [
        ("nnalu", "phantom root: nmalu 好 and snalu 做 are two different words"),
        ("empnalu", "the same phantom root"),
        ("nilaq", "the tree mushroom, agreeing with mnilaq 起屑 on 想起 only"),
        ("ngklaan", "已 is the perfective marker: （已完成的）攀登 vs gnkla 已知道的"),
        ("sktama", "sk- 'the late' + tama 父; its 信 came from a sentence gloss"),
        ("sblangan", "his 矛 against the 光著身 root, agreeing on 著")]:
    check(v not in V, "%-9s is absent from verified.js — %s" % (v, why))
    check(M["unv"].get(v, 0) > 0 and not M["mod"].get(v, 0),
          "%-9s still pale (%d occurrences)" % (v, M["unv"].get(v, 0)))

print("\n--- a hand-read sample of what the rule vouched for")
for v, why in [("pspuhun", "spuh unlisted; spuhun, spuhan, spuhi, snpuhan, pspuhan 醫院"),
               ("pspuhi", "the imperative of the same"),
               ("natas", "n- on atas, vouched in 113 by matas 寫字"),
               ("prijil", "p- on rijil, vouched by mrijil 使彎曲"),
               ("emprijil", "the future of the same"),
               ("ptcingan", "tcing, through tmucing / ptcingun 釘"),
               ("psqrasan", "qras 臉, through qmras / sqrasan"),
               ("phrpasi", "hrapas 玩, through phrpasun"),
               ("embliqan", "the commonest of them, 7 occurrences"),
               ("pgrahul", "grahul, through the RAHUL family"),
               ("msramal", "sramal, beside psramal 準備 70x"),
               ("empakux", "pakux, his 打呵欠")]:
    check(M["mod"].get(v, 0) > 0 and not M["unv"].get(v, 0),
          "%-9s deep brown -- %s" % (v, why))

print("\n--- the names did NOT turn dark, which is how this rule fails")
for n in ["sibal", "liwis", "mikat", "ingay", "lauken", "tatu", "talan",
          "banan", "sikat", "imin", "timin", "tain", "pilin"]:
    got = M["unv"].get(n, 0)
    check(got > 0 and not M["mod"].get(n, 0),
          "%-9s still pale (%d occurrences)" % (n, got))
    check(n not in V, "%-9s is absent from verified.js altogether" % n)

print("\n--- batch 113's six boilerplate demotions are still pale")
for v in ["snkmalu", "stmaqun", "psrusuq", "mkasi", "spkmalu", "spangun"]:
    check(M["unv"].get(v, 0) > 0 and not M["mod"].get(v, 0),
          "%-9s pale (%d occurrences)" % (v, M["unv"].get(v, 0)))
    check(v not in V, "%-9s is absent from verified.js" % v)

print("\n--- the three earlier levels are unharmed")
lwrong = [v for v in LISTED if M["unv"].get(v, 0)]
iwrong = [v for v in INFL if M["unv"].get(v, 0)]
vwrong = [v for v in VOUCHED if M["unv"].get(v, 0)]
check(len(LISTED) == 3876, "3876 listed (got %d)" % len(LISTED))
check(len(INFL) == 588, "588 regularly inflected (got %d)" % len(INFL))
check(len(VOUCHED) == 53, "53 vouched by their own paradigm (got %d)" % len(VOUCHED))
check(not lwrong, "no listed value went pale (%s)" % (lwrong[:8] or "none"))
check(not iwrong, "no inflected value went pale (%s)" % (iwrong[:8] or "none"))
check(not vwrong, "no vouched value went pale (%s)" % (vwrong[:8] or "none"))
check("biyu" not in ALL, "113's guard 4 holds: BIYU is rendered nowhere")

print("\n--- per card, scoped to the card")
for r in cardres:
    if r.get("missing"):
        check(False, "%s (%s): no card" % (r["hw"], r["his"]))
        continue
    where = ("deep brown" if r["want"] in r["mod"] else
             "PALE" if r["want"] in r["unv"] else
             "GREEN" if r["want"] in r["raw"] else "ABSENT")
    check(where == "deep brown", "%-7s (%-6s) %-9s %s"
          % (r["hw"], r["his"], r["want"], where))

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
