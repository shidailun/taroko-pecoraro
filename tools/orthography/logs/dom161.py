# -*- coding: utf-8 -*-
"""Batch 161: eighteen more typewriter repairs, and the audio slug that nearly ate them.

Batch 160 opened positions 0 and 1 of the m-read-as-n sweep. This batch works the
rest of that list — 45 candidates, of which **18 pass and 27 are refused**. The
ratio is the point: the sweep proposes, his French disposes.

Every one of the 18 is a single occurrence in the book, and every one merged into
a dark span that already existed. **That merge is itself the evidence**: the rest
of the dictionary already spells the word with the m.

  nlmilit  "toutes tes chèvres se sont sauvées"     -> mrmirit
  nlidil   "ta tête est de travers !"               -> mrijil   使彎曲
  nawit    "je suis fatigué"                        -> meuwit   很累
  neidang  "mon fils dévoyé (perdu)"                -> meydang  迷路
  nmulun   "un médicament à sucer"                  -> mmulun   含在嘴裏
  nuxeng   "mon nez est complètement bouché"        -> muhing   鼻子
  nlut     HIS OWN "(m'lut ?)" — "faisant pression" -> mrut     按住
  ntluula  "venu se montrer", his own VR. TLUULA    -> mtreura  明顯
  n'kai    "je n'ai que les travaux de la maison"   -> mkay     整理家事
  nlata    "Aller soldat."                          -> mrata    軍人
  notong   "on ne peut pas allumer tes allumettes"  -> mutung   點火
  ntqeli   "tapisser le pourtour de ta chambre"     -> mtqiri   周圍
  ntaga    "je t'attendrai le temps qu'il faudra"   -> mtaga    等候
  Nndaxa   "deux trois fois"                        -> mndha    二次
  n'ulat   "attraper une crampe"                    -> meurat   抽筋
  nmxa     "ton père qui va partir"                 -> mmha     要去
  nglaxol  "viennent s'attrouper"                   -> mgrahul  聚集
  nqalox   "ou blanc, ou noir, ou rouge"            -> mqalux   黑色的

**`nlut` is the best of them, because he flagged it himself.** His text reads
`Asi nlut (m'lut ?) xeaan` — the question mark is his. The book had already
noticed and could not resolve it; `mrut` 按住 against his "en faisant pression
sur lui" resolves it.

**Tense in his French is what separates a misread m from a real `n-` prefix.**
`ntaga` is the clean case: "je t'attendrai" is FUTURE, and `n-` is past, so the
letter cannot be an `n`. The same test refuses `Nngangax` — "A partir du fait
d'être muet", a genuine `n-` on `ngangah`, correct as printed.

**The 27 refusals, by kind:**
  * C-n- infix — `snkrawah`, `tnaga`, `qnbsranan`, `sneelug`, `tnquri`,
    `sneuwit`, `snka`, `snnru`. `<n>` perfective and `<m>` actor-focus share a
    slot, so these are real pairs and the whole class is off limits.
  * genuine `n-` prefix — `nngangah`, on his own "A partir du fait d'être".
  * false friends — `nilaq` is his 可食用的菇類, a mushroom, against `milaq`
    碎粒 crumbs; `narung` is "a obtenu le prix" against `marung`, a man's name.
  * homograph — `mnalu` is FIVE occurrences and would be the biggest gain here,
    and it is refused: his MALU prints Mnalu "s'entr'aimer" and his NALU prints
    Mnalu "qui tient la place", the same raw string in two entries. Repairing
    one would respell the other. Same blocker as `tabu` and `bir`.
  * unglossed target — `ntlawa`, `nruq`, `nay`, `nhnaan`, `nsntug`, `nsleelug`,
    `niyak`, `snuk`. A word with no Chinese cannot confirm anything.

**The audio slug.** The first run of this patch replaced 51 strings where 36
were expected, and the extra 15 were inside `"a"` fields — which are AUDIO
FILENAME SLUGS, e.g. `ex_qpaxan_so_manu_ka_ntqeli_tqean_so`. Renaming those in
the JSON renames nothing on disk; it just unhooks the recording, silently, with
the page still rendering perfectly. It was caught only because the replacement
COUNT was asserted per token rather than the patch being trusted. The patcher
now masks every `"a"` value before substituting and restores it after, and
batch 160 was re-checked against the same fault and is clean.

**A count assertion is not bureaucracy; it is the only thing standing between a
spelling repair and a dead audio link.**

+18 occurrences, 0 de-verified. Census after: modern dark 43,150 / pale 1,279 /
green 32 = **97.0513%** (from 97.0109%), 1,967 cards, 0 page errors.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# Absolute page totals, not deltas — each repaired token joined a span that was
# already there.
GAIN = {"mrmirit": 4, "mrijil": 3, "meuwit": 13, "meydang": 10, "mmulun": 1,
        "muhing": 14, "mrut": 5, "mtreura": 3, "mkay": 3, "mrata": 4,
        "mutung": 3, "mtqiri": 15, "mtaga": 6, "mndha": 4, "meurat": 2,
        "mmha": 3, "mgrahul": 7, "mqalux": 10}

GONE = ["nrmirit", "nrijil", "neuwit", "neydang", "nmulun", "nuhing", "nrut",
        "ntreura", "nkay", "nrata", "nutung", "ntqiri", "ntaga", "nndha",
        "neurat", "nmha", "ngrahul", "nqalux"]

# The refusals. `mnalu` at 5 would have been the largest single gain in the
# batch; it is the homograph, and it stays pale.
PIN = {"mnalu": 5, "snkrawah": 5, "nngangah": 2, "tnaga": 2, "nilaq": 1,
       "narung": 1}

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
    gone = pg.evaluate(SPANS, sorted(GONE))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(pin, PIN, "pale", "PIN")
for w in GONE:
    if gone.get(w):
        fail.append("GONE %s: his misread spelling still renders, %s" % (w, gone[w]))

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43150:
    fail.append("census: dark fell to %d, below this batch's 43,150" % tally["dark"])
if pct < 97.0:
    fail.append("census: dark fell back below 97%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d repairs, each merged into an existing dark span (%d occ total)"
      % (len(GAIN), sum(GAIN.values())))
print("GONE %d misread spellings render nowhere" % len(GONE))
print("PIN  %d refused (%d occ) — infix, real n-, false friends, homograph"
      % (len(PIN), sum(PIN.values())))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
