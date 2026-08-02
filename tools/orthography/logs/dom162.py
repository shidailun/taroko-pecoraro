# -*- coding: utf-8 -*-
"""Batch 162: the second witness was always sitting there.

Two veins were opened and refuted before this one, and both refutations are
worth more than the batch:

**The entry-mate rung, refuted by measurement.** 326 pale occurrences are words
his own dictionary lists as SUBS of an already-verified headword — `Empskeagul`
is glossed 同上（d°），未來式, literally "same as above, future tense". That
looks like the dictionary vouching structurally for a form the gloss-agreement
rungs cannot hear. It is not. Of those 326, the number that are BOTH in the
modern lexicon AND analyse as an affixation of their own verified parent is
**zero**. They are not pale because a gloss test rejects them; they are pale
because no modern source attests them at all. A rung that verified them would
make a dark span mean "he said so", which is the one thing it has never meant.

**The edit-distance-1 sweep, refuted by its own shape.** Batch 161 finished the
n→m class. Tallying every single-letter substitution that lands a pale type on
a lexicon word gives a FLAT distribution — u→a 47 occ, n→m 33, a→u 25, l→h 22 —
with no dominant class and a top entry made of false friends (`rngut` féconder
against `rngat` crier). A flat tally is what a mined-out seam looks like.

**What was actually left.** `PQ_MIN = 2` discards every type the ILRDF parquets
saw exactly once, because an ASR hapax is as likely a mis-hearing as a word.
That is right in bulk — but it discards them UNREAD, and 15 of them are words
on this page. Which means each already has a second witness: **Pecoraro typed
it in 1977.** A 2020s acoustic model mis-hearing cannot land on a string a
French priest typed fifty years earlier by accident; the two witnesses have no
path to each other. The gate is not loosened here, it is ANSWERED, per word.

  mlilug    起義軍佔領霧社          ~ his Mlilu 移動－活動 (LILU)
  tntmaan   口傳／經文 of old       ~ his Tntmaan 曾經坐過 (TTAMA)
  brnahan   其他的創作              ~ his Blnaxan 後退 (BLENAX)
  mskrut    duma mskrut ni duma mslhkah 時鬆時緊 — paired against mslhkah
  pnlwaan   呼喚而出                ~ his "tu m'as fait appeler a midi"
  pniq      駐紮一支分遺隊          ~ his Pnyeq 使留下－使存在
  ppkmalu   醫病趕鬼                ~ his "te remettre la tete en place"
  mknsat    派出所上班              ~ his Mkensat 當警察
  dnrunan   老師交代的功課          ~ his "ce qu'ils ont demande"
  pgmaxun   族語融合                ~ his "melanger du sucre a cette farine"
  pkhwayun  優待入山工作人員        ~ his Pkxwayun
  mnlamu    plealay strung mnlamu   ~ his "autrefois je recueillais l'argent"
  emptaril  準備登陸攻擊            ~ his Ptaril 使越到對岸 (TALIL)

**The coincidence argument has exactly one failure mode, and it is length.** At
two or three letters chance can reach a real string, so the short ones are
refused even where the sense fits — and `rih` is the case that proves the rule
costs something real. Six occurrences, the largest single gain left on the
page, and his 幾乎－接近－有點像 fits the parquet's `qhuqil kana rih saw psahug
dhyaan` — "killed them all, almost as a punishment to them" — rather well. It
stays pale. Batch 146 pinned it because a three-letter root needs his
word-level Chinese and not a sentence gloss, and batch 159 showed the honest
way out: `nta` was the fourth pinned member and went dark because **a person
spoke for it**, not because a gate moved. One ASR token is not a person.

`kn` is refused twice over: two letters, and its single parquet occurrence is
inside `Fu-kn-su`, the romanized Japanese 撫墾署 split on its hyphens. The gate
was earning its keep on that one all along.

Like every corpus source here this widens `seen` and never `lex`, and like
every corpus source it vouches for a SPELLING and not for his gloss — `brnahan`
is admitted as modern Truku orthography while his 後退 reading of it stays his
own business.

+21 occurrences, 0 de-verified, 0 new pale types. Census after: modern dark
43,171 / pale 1,258 / green 32 = **97.0986%** (from 97.0513%), 1,967 cards,
0 page errors.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

GAIN = {"mlilug": 3, "tntmaan": 3, "brnahan": 2, "mskrut": 2, "pnlwaan": 2,
        "pniq": 2, "ppkmalu": 1, "mknsat": 1, "dnrunan": 1, "pgmaxun": 1,
        "pkhwayun": 1, "mnlamu": 1, "emptaril": 1}

# The two the length rule refuses. `rih` is the expensive one and that is the
# point of asserting it here.
PIN = {"rih": 6, "kn": 1}

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
    tally = pg.evaluate("""() => { const r = {dark: 0, pale: 0, green: 0};
      for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw'))
        r[n.className.indexOf('w-mod') >= 0 ? 'dark'
          : n.className.indexOf('w-unv') >= 0 ? 'pale' : 'green'] += 1;
      return r; }""")
    gain = pg.evaluate(SPANS, sorted(GAIN))
    pin = pg.evaluate(SPANS, sorted(PIN))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(pin, PIN, "pale", "PIN")

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43171:
    fail.append("census: dark fell to %d, below this batch's 43,171" % tally["dark"])
if pct < 97.09:
    fail.append("census: dark fell back below 97.09%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d hapaxes admitted one at a time (%d occ)"
      % (len(GAIN), sum(GAIN.values())))
print("PIN  rih 6 + kn 1 stay pale — two and three letters is where the "
      "coincidence argument stops working")
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
