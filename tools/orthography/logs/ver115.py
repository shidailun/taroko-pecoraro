# -*- coding: utf-8 -*-
"""Batch 115: SISTER SLOTS (level 5), and the Q'QOL family, which was on the
wrong stem entirely.

`lmuan` is the case, and it is the one shape the first four rules cannot state.
It is the -an slot of his LAMU 收集 paradigm — his own line reads
°Lmamu, lamu, lmui, lmuan, lmuon — and the wordlist lists `lmui` and `lmuun`,
the -i and -un slots of that same stem, but not it. `regular()` reaches it,
because `lmu` IS listed, and then refuses on the gloss: the listed `lmu` is
碎粒 a crumb, a homonym, and the two sisters that would settle it carry no gloss
at all. That is not bad luck with this word — **most of a paradigm is
glossless**, which is why levels 2, 3 and 4 all stall here.

So the claim level 5 makes is about morphology and not about meaning: a stem the
wordlist writes with two different paradigm suffixes takes the third. Two
supporters wearing DIFFERENT suffixes under the SAME prefix, because same-suffix
pairs are substring coincidences waiting to happen.

There is no gloss gate, because there is usually no gloss to read. The guard is
at the other end, and it is his: **the value must be a word he printed in a °
paradigm line.** That is his own statement that it is an inflectional slot
rather than a word in its own right, and it is what keeps the nouns out. Priced
ungated the rule found 49 values; the gate refuses 11, and every one of the 11
is either a noun or a different root:

  sapi     his 小鋤頭, a small hoe, decomposing as `sap`+`-i` beside the attested
           `sapan` and `sapaw` 舖床 — a hoe verified as the imperative of
           spreading a bed. His SAPE is a headword and stands in nobody's
           paradigm.
  ptasaw   his 使沉澱澄清, against the paradigm of `ptas` 寫;紋面.
  srciqun, psmkun, spngaw, syukay, tblai, hrwaan, krhun, ddaan, pkngalan

The gate is not sufficient by itself — a slot of his can be a homonym of a slot
of theirs — so `qurun`/`quran` were refused by hand (HAND_NOT_SISTERED). Their
sisters `quri` 有關 and `quray` are the paradigm of a word about being ABOUT
something, and reading that refusal turned up the real defect: **his Q'QOL
挖鑿（泥土、木頭、石頭）－雕刻 is modern `gqur`, with a g**, and the whole family had
been mapped onto the wrong stem. His own line is °Q'mqol, q'qol, qqoli, qqolan,
qqolun; modern has `gqur` 刻成槽形, `gmqur` 開鑿;雕刻, `gqran` 雕過, `gqrun` 用…鑿,
`gqri` 請…刻, `gnqur` 挖洞過 — slot for slot, all attested. `qnqolan` takes
`gnqur` rather than a composed *`gnqran`, which the n-gram inventory forbids
(`gnqr`, `nqra`).

Two more remaps came out of the same reading. **`knk'laan`/`knklaan` → `kngkla`**
(13 occurrences, the largest open item): his own AN entry glosses it outright,
"Mk'la = Savoir; Knklaan = Connaissance … Mk'la=知道;Knklaan=知識", and `kngkla`
is the only modern word glossed 知識. Two of the 13 are a homograph — his KALA
sub-form 攀登 and XMUK's "betak knklaan xedao", the sun's climbing — but both of
his keys serve both senses, so no key split is possible and the reading that
serves 11 slots wins, exactly as for IYAX, LAWA, NGALI, ULAE, K'LAE, DIYAN and
QALO. And **`dmqpah` → `dmqeepah` 農民們** (7), his 工人們: the short form is 0×,
and batch 40 already established that modern writes both `qpah` and `qmeepah`.

Assertions are over spans and the card section is scoped to the card, which it
finds by MODERN headword — his Q'QOL card now prints GQUR.
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
    ("LAMU", "LMUAN", "LAMU"),          # the case that names the rule
    ("GQUR", "GQUR", "Q'QOL"),          # the family that was on the wrong stem
    ("GQUR", "GMQUR", "Q'QOL"),
    ("GQUR", "GQRAN", "Q'QOL"),
    ("GQUR", "GQRUN", "Q'QOL"),
    ("GQUR", "GQRI", "Q'QOL"),
    ("GQUR", "GNQUR", "Q'QOL"),
    ("AN", "KNGKLA", "AN"),             # 知識, the largest open item
    ("KALA", "KNGKLA", "KALA"),         # and its climbing homograph
    ("GASUT", "DMQEEPAH", "GASUT"),
    ("QLAHANG", "QLHANGAN", "KLAXANG"),
    ("SAPAW", "SPAGAN", "SAPAO"),
    ("UNUH", "NUHUN", "ONOÇ"),
    ("KUWAX", "KWAXAN", "KYUWAX"),
    ("GIYING", "GIMAN", "GIIN"),
    ("KEUDUS", "PKDUSAN", "KUDUS"),
    ("HGLUQ", "HGLQI", "XG'LOQ"),
    ("LIING", "LINGAN", "LIING"),
    ("SALU", "SLUI", "SALU"),
    ("QADA", "QDAUN", "QADA"),
    ("TUCING", "TCINGI", "TÖTING"),
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
      "vouched root, %d sister slots"
      % (len(LISTED), len(INFL), len(VOUCHED), len(VROOT), len(SISTR)))

print("\n--- the totals, measured not computed")
check(M["counts"]["w-mod"] == 40906, "w-mod 40906 (got %d)" % M["counts"]["w-mod"])
check(M["counts"]["w-unv"] == 3543, "w-unv 3543 (got %d)" % M["counts"]["w-unv"])
check(M["counts"]["w-raw"] == 26, "w-raw 26 (got %d)" % M["counts"]["w-raw"])
tot = sum(M["counts"].values())
check(tot == 44475, "44475 words on screen (got %d)" % tot)
rate = 100.0 * M["counts"]["w-mod"] / tot
check(abs(rate - 91.98) < 0.01, "91.98%% of occurrences verified (got %.2f%%)" % rate)

print("\n--- the 36 sister slots are deep brown wherever they reach the page")
check(len(SISTR) == 36, "36 values at level 5 (got %d)" % len(SISTR))
seen = [v for v in SISTR if ALL.get(v, 0)]
wrong = [v for v in seen if M["unv"].get(v, 0)]
check(len(seen) >= 34, "%d of them reach the page" % len(seen))
check(not wrong, "none is painted pale (%s)" % (wrong[:8] or "none"))
occ = sum(M["mod"].get(v, 0) for v in seen)
check(occ >= 45, "they carry %d occurrences of deep brown" % occ)

print("\n--- every one of them is a slot HE printed in a ° paradigm line")
print("    (the gate; the 11 below are what it refuses)")
for v, why in [
        ("sapi", "his 小鋤頭 a hoe, sistered by sapan/sapaw 舖床 — a headword"),
        ("ptasaw", "his 使沉澱澄清, against the paradigm of ptas 寫;紋面"),
        ("srciqun", "not in any ° line of his"),
        ("psmkun", "not in any ° line of his"),
        ("spngaw", "not in any ° line of his"),
        ("syukay", "not in any ° line of his"),
        ("tblai", "not in any ° line of his"),
        ("hrwaan", "not in any ° line of his"),
        ("krhun", "not in any ° line of his"),
        ("ddaan", "not in any ° line of his"),
        ("pkngalan", "not in any ° line of his")]:
    check(v not in V, "%-9s is absent from verified.js — %s" % (v, why))
    check(M["unv"].get(v, 0) > 0 and not M["mod"].get(v, 0),
          "%-9s still pale (%d occurrences)" % (v, M["unv"].get(v, 0)))

print("\n--- a hand-read sample of what the rule vouched for")
for v, why in [("lmuan", "his LAMU -an slot; lmui and lmuun are listed"),
               ("qlhangan", "beside qlhangi 注意；當心 and qlhangun"),
               ("spagan", "the SAPAW bedding paradigm, beside spagi/spagun"),
               ("nuhun", "his 吸奶, beside nuhan and nuhi"),
               ("kwaxan", "his 退避, beside kwaxi 要挪開 and kwaxun"),
               ("giman", "his 尋找, beside gimi and gimun"),
               ("pkdusan", "his 使活著, off the KEUDUS 生命 stem"),
               ("hglqi", "the HGLIQ 撕裂 paradigm, four sisters listed"),
               ("lingan", "his LIING 藏 -an slot; his own lingun is attested"),
               ("slui", "his SALU 做, beside sluan and sluun 要被製作"),
               ("qdaun", "his QADA 丟, beside qdaan and qdaani 丟棄"),
               ("tcingi", "beside tcingan 打鐵店 and tcingun")]:
    check(M["mod"].get(v, 0) > 0 and not M["unv"].get(v, 0),
          "%-9s deep brown -- %s" % (v, why))

print("\n--- the Q'QOL family is off `quri` and onto `gqur`, and stays there")
for v in ["gqur", "gmqur", "gqran", "gqrun", "gqri", "gnqur"]:
    check(V.get(v) == 1, "%-7s is LISTED, not merely inflected (level %s)"
          % (v, V.get(v)))
    check(M["mod"].get(v, 0) > 0, "%-7s deep brown, %d occurrences"
          % (v, M["mod"].get(v, 0)))
for gone, why in [("qmur", "his Q'mqol was claiming it; gmqur 開鑿;雕刻"),
                  ("qurun", "was the -un slot of quri 有關, a different word"),
                  ("quran", "the same"),
                  ("qnquran", "his Qnqolan; gnqran is unwritable (gnqr, nqra)"),
                  ("dmqpah", "0x; his 工人們 is dmqeepah 農民們"),
                  ("knklaan", "his 知識 is kngkla")]:
    check(not ALL.get(gone, 0), "%-8s is rendered nowhere — %s" % (gone, why))

print("\n--- `quri` itself is untouched; the family it belongs to keeps it")
for v in ["quri", "mquri", "pquri", "nquri", "tquri", "spquri"]:
    check(M["mod"].get(v, 0) > 0 and not M["unv"].get(v, 0),
          "%-7s deep brown, %d occurrences" % (v, M["mod"].get(v, 0)))
# `mtquri` is 0x and unverified, and was so before this batch — it is the one
# member of the family the wordlist does not write, and pale is its right state.
check(M["unv"].get("mtquri", 0) == 1 and not M["mod"].get("mtquri", 0),
      "mtquri  still pale, as it was — 0x, and the batch did not touch it")

print("\n--- QOLO 圓的 is a DIFFERENT entry and `qqolo` did not follow the dig root")
check(M["unv"].get("qquru", 0) == 1,
      "qqolo still renders QQURU, still pale — his 很圓, not his 挖鑿")
for v in ["quru", "mquru", "pquru"]:
    check(ALL.get(v, 0) > 0, "%-6s still on the QOLO card (%d)" % (v, ALL.get(v, 0)))
# and the remap did not leak: the six new values total exactly the occurrences
# his six keys had, all of them on the one card the CARDS block scopes.
GQ = sum(ALL.get(v, 0) for v in
         ["gqur", "gmqur", "gqran", "gqrun", "gqri", "gnqur"])
check(GQ == 12, "the six gqur slots carry 12 occurrences between them, which is "
                "what his six keys had (got %d)" % GQ)

print("\n--- the earlier levels are unharmed")
lwrong = [v for v in LISTED if M["unv"].get(v, 0)]
iwrong = [v for v in INFL if M["unv"].get(v, 0)]
vwrong = [v for v in VOUCHED if M["unv"].get(v, 0)]
rwrong = [v for v in VROOT if M["unv"].get(v, 0)]
check(len(LISTED) == 3881, "3881 listed (got %d)" % len(LISTED))
check(len(INFL) == 588, "588 regularly inflected (got %d)" % len(INFL))
check(len(VOUCHED) == 53, "53 vouched by their own paradigm (got %d)" % len(VOUCHED))
check(len(VROOT) == 65, "65 off a vouched root (got %d)" % len(VROOT))
check(not lwrong, "no listed value went pale (%s)" % (lwrong[:8] or "none"))
check(not iwrong, "no inflected value went pale (%s)" % (iwrong[:8] or "none"))
check(not vwrong, "no vouched value went pale (%s)" % (vwrong[:8] or "none"))
check(not rwrong, "no vouched-root value went pale (%s)" % (rwrong[:8] or "none"))

print("\n--- batch 114's refusals are still refused")
for v in ["nnalu", "empnalu", "nilaq", "ngklaan", "sktama", "sblangan"]:
    check(v not in V, "%-9s is absent from verified.js" % v)
    check(M["unv"].get(v, 0) > 0 and not M["mod"].get(v, 0),
          "%-9s still pale (%d occurrences)" % (v, M["unv"].get(v, 0)))

print("\n--- the names did NOT turn dark, which is how this rule fails")
for n in ["sibal", "liwis", "mikat", "ingay", "lauken", "tatu", "talan",
          "banan", "sikat", "imin", "timin", "tain", "pilin"]:
    got = M["unv"].get(n, 0)
    check(got > 0 and not M["mod"].get(n, 0),
          "%-9s still pale (%d occurrences)" % (n, got))
    check(n not in V, "%-9s is absent from verified.js altogether" % n)

print("\n--- per card, scoped to the card")
for r in cardres:
    if r.get("missing"):
        check(False, "%s (%s): no card" % (r["hw"], r["his"]))
        continue
    where = ("deep brown" if r["want"] in r["mod"] else
             "PALE" if r["want"] in r["unv"] else
             "GREEN" if r["want"] in r["raw"] else "ABSENT")
    check(where == "deep brown", "%-8s (%-6s) %-9s %s"
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
