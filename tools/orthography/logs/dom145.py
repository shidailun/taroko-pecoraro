# -*- coding: utf-8 -*-
"""Batch 145: a sentence gloss is too loose to refuse with, as well as to accept with.

Batch 141 opened the hole where the WORDLIST has no gloss to test against. This
is the other side of the same test, the one where HE has none: 264 pale values /
312 occurrences whose root is listed AND glossed and whose morphology is his own
productive machinery, refused because `regular()` could find no character shared
between the root's gloss and his Chinese — and the only Chinese anywhere near
those words belongs to an EXAMPLE SENTENCE.

**The argument is already in this codebase, run the other way.** `vouched_root`
refuses to ACCEPT a sentence gloss as evidence, and says why: "a sentence gloss
describes a whole clause and shares a character with almost anything" — the
`sktama` 已故的父親 agreeing with `kmtama` 信奉上帝 on an unrelated 信. If a
whole-clause translation is too loose to license an agreement, it is exactly as
loose in the other direction. A translator writing 我們去求爸爸，你同意嗎？owes
no stem in that clause its dictionary meaning, and 133 well-formed inflections
were sitting pale because a free translation declined to contain them.

So the entry condition is `slots_only` — he attached no Chinese to this word as
a word — and inside it there is NO GLOSS TEST AT ALL. The guards carry the whole
weight instead: the root listed in the modern wordlist and glossed there, four
letters (batch 141's floor), its gloss not merely 人名/地名, and **exactly one
root candidate**, since with no gloss there is nothing to break a tie with.

**SISUN cannot arrive.** The rule this book keeps returning to is refused one
step before the morphology is looked at: he glosses SISUN 縫 himself, so the
entry condition throws it out and rule 2 reads and refuses it as it always did.
It is asserted still pale below, because it is the thing this rule would have to
break to be wrong.

**What the guards could not catch, and the hand read did — six of 139.** Each has
exactly one root candidate and that candidate is the wrong word, which is the
SISUN shape with no gloss of his to catch it:

  slungan     `slung` 毛線 wool — his own note names the root: Ma so lmngao
              slongan! 你怎麼對著大海說話呢?(Silong=海). It is the SEA.
  drnai       `drna` 鹿鞭 — the card is DULUN: Dlnai ta tmaan xo? 我們去求爸爸.
  ggitan      `gitu` 枇杷 a loquat — the card is GIGIT: Tayai bi ka g'gitan so!
              你真是纏人!, and he adds 含有…糾纏的意思.
  empslangan  `langu` 湖 a lake — the card is his own headword SLANGAN:
              adi biyao mpslangan ka kia! 很快就會被鏽蝕掉.
  mtgtmaq     `tmaq` 水桶樹 — the card is TMAQ/Tgtmaq and the sentence is
              mxa mtgtmaq d'xgal 全都趴倒在地; the tree is a homograph.
  narung      `arung` 穿山甲 a pangolin — Xea ka mnangal nalong 得獎的是他.

None of the six is a headword or a sub-form, which is why they took finding:
every one appears only inside an example sentence.

The 132 that remain are his paradigm and nothing else — n- preterite (`nsping`
<- `sping` 化妝, `ntakur` <- `takur` 跌倒, `nqraqil` <- `qraqil` 皮, `nruciq` <-
`ruciq` 罪), mn- past, d- plural-human (`drdanan` <- `rdanan` 父母), emp-/mkm-
future and desiderative, p-/ps-/s- causative and instrumental, t-/tt- iterative.

Emitted at a NEW LEVEL 5, between 4 and 6, which renumbers `vouched_root` and
everything under it by one. That is free: app.js's attested() only asks whether
a value is IN `MODERN_VERIFIED`, never what number it carries.

**+132 values / 161 occurrences, 0 de-verified, 0 relevelled** (every one of the
132 added at level 5, and every value that moved moved only by the renumbering).

Census after: modern dark 42,665 / pale 1,768 / green 32 = **95.9519%** (from
95.5898%), original 43,139 / 1,791 / 32 = 95.9455%, 1,967 cards, 0 page errors in
both modes.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

GAIN = {
    "lqlqian": 5, "sntlung": 5, "nsaang": 4, "nstuq": 4, "ntaqi": 4,
    "ddaan": 3, "mlnglung": 3, "empkudaw": 2, "mntjiyal": 2, "nqsahur": 2,
    "nrahuq": 2, "ntgsa": 2, "pnklutut": 2, "snkrbutan": 2, "tthmuku": 2,
    "dahani": 1, "dmpsadu": 1, "dmsapat": 1, "dmtjiyal": 1, "dmusa": 1,
    "dpusu": 1, "drdanan": 1, "dtayal": 1, "dthiyan": 1, "embabaw": 1,
    "empealix": 1, "empkatay": 1, "emppqluli": 1, "emppsdhug": 1,
    "empqapah": 1, "emprinah": 1, "empspala": 1, "empsqrinut": 1,
    "emptquli": 1, "emptseejiq": 1, "kbuyun": 1, "kgriq": 1, "kinai": 1,
    "kkaraw": 1, "kmpspung": 1, "kmttgxal": 1, "knktmai": 1, "knngungu": 1,
    "knngunguan": 1, "knuyuh": 1, "krikit": 1, "ksbilaq": 1, "ksblus": 1,
    "lnnglung": 1, "mapala": 1, "masuyang": 1, "mkbnaqig": 1, "mkmpaux": 1,
    "mkmphing": 1, "mkphing": 1, "mmalax": 1, "mmuda": 1, "mniyak": 1,
    "mnkingal": 1, "mnklabi": 1, "mnksaw": 1, "mnprawah": 1, "mnqlit": 1,
    "mnqqita": 1, "mnsgasut": 1, "mnutux": 1, "msnsinaw": 1, "mtbrinah": 1,
    "nguyan": 1, "nlamu": 1, "npkusa": 1, "npprngaw": 1, "nprbnaw": 1,
    "npungu": 1, "nqatar": 1, "nqraqil": 1, "nrangi": 1, "nrikit": 1,
    "nruciq": 1, "nslupung": 1, "nsping": 1, "nsuwiq": 1, "ntakur": 1,
    "pbgbagi": 1, "peeutuxun": 1, "pkrbungun": 1, "pkriqu": 1, "pnkrikit": 1,
    "pnqbling": 1, "pnsdraan": 1, "pnslutut": 1, "pnsqrinutan": 1, "pnuda": 1,
    "ppeeutux": 1, "ppshada": 1, "pptpusu": 1, "prbungun": 1, "pseeliq": 1,
    "psgun": 1, "pshlisi": 1, "pslhayun": 1, "psrnuun": 1, "psttui": 1,
    "ptpaqi": 1, "ptrmaun": 1, "pttaqi": 1, "ptthiyaq": 1, "qnlit": 1,
    "rnagak": 1, "rnigaw": 1, "rnqdug": 1, "sduray": 1, "smbrih": 1,
    "smnipaq": 1, "sneeliq": 1, "snisu": 1, "spktaqi": 1, "sprisuh": 1,
    "spskryaun": 1, "sruani": 1, "ssapa": 1, "ssdhaun": 1, "ssghuway": 1,
    "tblai": 1, "thgut": 1, "thungan": 1, "tmnucing": 1, "tneuqan": 1,
    "tnklai": 1, "ttasil": 1, "ttrbuq": 1, "ttrilun": 1,
}

# HAND_NOT_NC, and `sisun` with them. The six are pinned by hand; `sisun` is
# pinned by the RULE — the entry condition refuses it because he glossed it —
# and it is here because it is what this rule would have to break to be wrong.
PIN = {"slungan": 2, "drnai": 1, "ggitan": 1, "empslangan": 1, "mtgtmaq": 1,
       "narung": 1, "sisun": 5}

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
if tally["dark"] < 42665:
    fail.append("census: dark fell to %d, below this batch's 42,665" % tally["dark"])
if 100.0 * tally["dark"] / tot < 95.0:
    fail.append("census: dark fell back below 95%")

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], 100.0 * tally["dark"] / tot))
print("GAIN %d values / %d occurrences now dark" % (len(GAIN), sum(GAIN.values())))
print("PIN  %d still pale — 6 by hand, `sisun` by the entry condition"
      % len(PIN))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
