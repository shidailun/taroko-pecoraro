# -*- coding: utf-8 -*-
"""Batch 113: a root nobody wrote down bare, vouched by its own inflections.

Batch 112 verified a value the wordlist does not list when it is a regular
inflection of a root the wordlist DOES list -- a listing gap seen from the
citation form. This is the same gap seen from the other side: the wordlist has
no entry for the bare root, but it has two or more of that root's own paradigm
slots, and one of them agrees with his Chinese. `hing` is the case that names
the rule -- his own headword note reads (=PXENG及其衍生形式的詞根), the root of
PXENG, and `mhing` 熄火, `phing`, `emphing`, `pphing` are all listed.

Four guards keep it from vouching for a word that is not there:

  1  two DISTINCT (prefix, suffix) pairs, so one word cannot vouch for itself;
  2  the vouching supporter's modern gloss must share a character with his;
  3  frozen names and loans are excluded outright;
  4  the value's own final vowel needs a witness -- either a supporter carries
     the value WHOLE (`mkmpeysa` for `kmpeysa`), or that vowel is itself a
     paradigm suffix (`paqi` beside `paqan`/`paqun`/`paqaw`). Without guard 4,
     `biyu` was vouched by `biyaw` 109x, `sbiyaw` 281x and `pbiyi` -- which are
     the paradigm of `biyaw` 快, a DIFFERENT word. Supporters reached by the
     -un/-an branch have dropped the value's last vowel, so they witness the
     stem and are silent about the citation form.

`biyu` was a map defect as well as a vouching one, and the repair is asserted
below: his `biyo` occurs once, in QAGOX's 你的傷口很快就會痊癒, so it is 快 --
`biyaw`, not `biyu` (0x anywhere). manual_map.json now says so.

Assertions are over spans. The card section is scoped to the card, and finds
its cards by their MODERN headword, because that is what modern mode renders:
his XENG card prints HING and his QAGOX card prints KAGUH. A finder keyed on
his spelling matches nothing at all.
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
LISTED = sorted(k for k in V if V[k] == 1)
INFL = sorted(k for k in V if V[k] == 2)
VOUCHED = sorted(k for k in V if V[k] == 3)

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
    ("KAGUH", "BIYAW", "QAGOX"),      # the biyo repair, in his own sentence
    ("HING", "HING", "XENG"),         # the root his PXENG note names
    ("BUYU", "BUYU", "BUYO"),
    ("DHA", "TDHA", "DAXA"),          # his 分成兩半 beside tmdha 分成二份
    ("RAMAL", "PSRMALI", "LAMAL"),
    ("QNLQAH", "QNLQAH", "KNKAX"),
    ("LBU", "SLBU", "L'BU"),
    ("BRU", "TNBRU", 'B"LO'),
    ("PATAS", "ATAS", "PATAS"),       # his note: 這會是 Patas 的詞根嗎
    ("SIPAQ", "PAQI", "SIPAQ"),
    ("LUTUT", "LTUDI", "LUTUT"),
    ("RIJIL", "RIJIL", "LIDIL"),
]

CARD_PROBE = """(cases) => {
  const out = [];
  const cards = Array.from(document.querySelectorAll('article.entry'));
  for (const [hw, want, his] of cases) {
    // his headword can head TWO cards (KAGUH is both 邀請 and 抓), so take the
    // one carrying the word and only then ask what colour it is.
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
print("verified.js: %d listed, %d regularly inflected, %d vouched"
      % (len(LISTED), len(INFL), len(VOUCHED)))

print("\n--- the totals, measured not computed")
check(M["counts"]["w-mod"] == 40704, "w-mod 40704 (got %d)" % M["counts"]["w-mod"])
check(M["counts"]["w-unv"] == 3745, "w-unv 3745 (got %d)" % M["counts"]["w-unv"])
check(M["counts"]["w-raw"] == 26, "w-raw 26 (got %d)" % M["counts"]["w-raw"])
tot = sum(M["counts"].values())
check(tot == 44475, "44475 words on screen (got %d)" % tot)
rate = 100.0 * M["counts"]["w-mod"] / tot
check(abs(rate - 91.52) < 0.01, "91.52%% of occurrences verified (got %.2f%%)" % rate)

print("\n--- the 53 vouched values are deep brown wherever they reach the page")
seen = [v for v in VOUCHED if ALL.get(v, 0)]
wrong = [v for v in seen if M["unv"].get(v, 0)]
check(len(VOUCHED) == 53, "53 values at level 3 (got %d)" % len(VOUCHED))
check(len(seen) >= 45, "%d of them reach the page" % len(seen))
check(not wrong, "none is painted pale (%s)" % (wrong[:8] or "none"))
occ = sum(M["mod"].get(v, 0) for v in seen)
check(occ >= 90, "they carry %d occurrences of deep brown" % occ)

print("\n--- guard 4: biyu is gone from the map and from the page")
check("biyu" not in ALL, "BIYU is rendered nowhere (%d spans)" % ALL.get("biyu", 0))
check("biyu" not in V, "biyu is absent from verified.js")
check(M["mod"].get("biyaw", 0) > 0, "biyaw is deep brown (%d occurrences)"
      % M["mod"].get("biyaw", 0))
# modern_map.js holds TWO objects; index on the one that is the map.
_mm = io.open(H + "site/modern_map.js", encoding="utf-8").read()
_a = _mm.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MMAP = json.loads(_mm[_a:_mm.index("\n};", _a) + 2])
check(MMAP.get("biyo") == "biyaw", "the map sends biyo to biyaw (got %r)"
      % MMAP.get("biyo"))

print("\n--- a hand-read sample of what the rule vouched for")
for v, why in [("hing", "his note: =PXENG及其衍生形式的詞根; mhing 熄火, phing"),
               ("atas", "his note: 這會是 Patas 的詞根嗎; matas 寫字, pnatas"),
               ("tdha", "his 分成兩半; tmdha 分成二份"),
               ("tbalung", "his own gloss: Balong＝蛋；Tbalong＝下蛋"),
               ("paqi", "imperative beside paqan / paqun / paqaw"),
               ("ltudi", "imperative beside ltudan"),
               ("kmpeysa", "carried whole by mkmpeysa, which licenses kmpeysun"),
               ("qnaya", "carried whole by qmnaya"),
               ("tnbru", "carried whole by tmnbru"),
               ("rijil", "the commonest of them, 6 occurrences")]:
    check(M["mod"].get(v, 0) > 0 and not M["unv"].get(v, 0),
          "%-9s deep brown -- %s" % (v, why))

print("\n--- the names did NOT turn dark, which is how this rule fails")
for n in ["sibal", "liwis", "mikat", "ingay", "lauken", "tatu", "talan",
          "banan", "sikat", "imin", "timin", "tain", "pilin"]:
    got = M["unv"].get(n, 0)
    check(got > 0 and not M["mod"].get(n, 0),
          "%-9s still pale (%d occurrences)" % (n, got))
    check(n not in V, "%-9s is absent from verified.js altogether" % n)

print("\n--- the boilerplate excision demoted six false claims, and they stayed pale")
# Both wordlists talk ABOUT words, so 的詞根/動詞形/同上 -- and 子, a classifier
# that confirms anything against anything -- are excised before the glosses are
# compared. Five of the six losses are brown that should never have been brown.
for v in ["snkmalu", "stmaqun", "psrusuq", "mkasi", "spkmalu", "spangun"]:
    check(M["unv"].get(v, 0) > 0 and not M["mod"].get(v, 0),
          "%-9s pale (%d occurrences)" % (v, M["unv"].get(v, 0)))
    check(v not in V, "%-9s is absent from verified.js" % v)

print("\n--- the listed and inflected halves are unharmed")
lwrong = [v for v in LISTED if M["unv"].get(v, 0)]
iwrong = [v for v in INFL if M["unv"].get(v, 0)]
check(len(LISTED) == 3876, "3876 listed (got %d)" % len(LISTED))
check(len(INFL) == 588, "588 regularly inflected (got %d)" % len(INFL))
check(not lwrong, "no listed value went pale (%s)" % (lwrong[:8] or "none"))
check(not iwrong, "no inflected value went pale (%s)" % (iwrong[:8] or "none"))

print("\n--- per card, scoped to the card")
for r in cardres:
    if r.get("missing"):
        check(False, "%s (%s): no card" % (r["hw"], r["his"]))
        continue
    where = ("deep brown" if r["want"] in r["mod"] else
             "PALE" if r["want"] in r["unv"] else
             "GREEN" if r["want"] in r["raw"] else "ABSENT")
    check(where == "deep brown", "%-6s (%-6s) %-7s %s"
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
