# -*- coding: utf-8 -*-
"""Batch 144: pale is not a verdict a person's name can ever shed.

The name path had two gates in series, and only one of them was doing the work
the docstring credited it with. `named` was the NAME POPULATION — tokens his own
`name (m)`/`name (f)` tag declares, plus tier N's "capitalized mid-sentence,
never lowercase anywhere" — intersected with the ILRDF registry. The docstring
defends the intersection with the homograph trap: `aku`, `taya`, `urang`, `tabu`
are somebody's name AND ordinary vocabulary. But those are kept out by the
POPULATION, which never contained them; the registry was answering a second
question, "and is this the modern spelling?", that three whole classes of name
can never be asked:

  Japanese-era loans   `denki` 電気, `banasi` 話, `stbaku` 煙草, `tausen`, `teaji`
  place names          `tagahan` (他從Tagarhan出發), `taulan`, `tyakang`
  Christian names      `jes` (Jes Cristo — Notre Seigneur Jésus-Christ), `maria`,
                       `dcristu`, `yurdan`

No register of Truku given names will ever list one of them, so requiring one
kept them pale forever on a test they cannot pass. Their modern spelling comes
from the same o>u and x>h rules that spell every other word on the page.

So the registry now only REPORTS (140 of the 247 values), and the population is
the gate. HAND_NAMES joins it — names reached only through an example sentence,
which his tagger never saw and tier N never fired on.

**+82 values / 313 occurrences, 0 de-verified, 0 relevelled.** The biggest pale
words on the page were all people: `liwis` 38 (里維斯), `ingay` 24, `lauken` 22,
`tagahan` 13, `pilin` 11, `timin` 11, `akit`/`banan`/`lautan` 10 each.

**What the intersection had been silently filtering out, and now HAND_NOT_NAMES
does by hand** — sixteen values, because at midcap=1 tier N's evidence is a
single capital letter, as likely sentence-initial as a person. Six are FRENCH,
out of his own glosses: "Beau père", "1) Grand père", "= Grandeur - taille",
"Vivant - mobile", "Connaissance (=…)", rougeur. They were then run through the
o>u rules, which is how `cunnaissance` and `ruugeur` got their spelling — the
respelling is itself the proof they are not Truku words. `mpa` is his own PREFIX
card ("Ce préfixe composé MPA"). The rest are ordinary words wearing one
capital: `byeqay` (Byeqai nako munan, a verb starting a sentence), `qlap`
(Qlap ! an imperative after a semicolon), `yianu` (his form label Yiano "Pour
vous"), `pnsdahung` (a nominalized verb, and his own headword sense 造成瘀傷),
and four queried variants in parentheses — `mnttlaqel`, `mpsqlul`, `tbasyaq`,
`tsaleh` ("(= Ts'alex) Misanthrope").

A midcap>=2 floor was measured as the alternative and REFUSED: it is blunt
enough to drop `maria`, and it keeps `mpa` (midcap 4).

Census after: modern dark 42,504 / pale 1,929 / green 32 = **95.5898%** (from
94.8859%), original 42,977 / 1,953 / 32 = 95.5852%, 1,967 cards, 0 page errors
in both modes. **This is the batch that passes 95%.**
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# the names, with the pale occurrences each had. Every one of these is a person,
# a place or a loan, and none of them is a claim about Truku vocabulary.
GAIN = {
    "akit": 10, "apin": 1, "apwi": 4, "arin": 2, "atuh": 7, "atwi": 8,
    "bal": 2, "banan": 10, "banasi": 5, "cristu": 2, "dcristu": 1, "denki": 7,
    "diku": 7, "dluan": 7, "efunang": 6, "eku": 5, "hane": 1, "huyu": 4,
    "ilus": 1, "ingay": 24, "jes": 1, "kikit": 1, "lakah": 1, "laubin": 1,
    "lauken": 22, "laun": 4, "lausin": 1, "lautan": 10, "liwis": 38, "liya": 1,
    "lubaq": 3, "maria": 1, "mici": 2, "miheng": 1, "mityang": 1,
    "mkmurisaka": 6, "moxoi": 1, "murisaka": 5, "nahui": 1, "nati": 3,
    "paidang": 1, "piking": 1, "pilin": 11, "pilyaq": 1, "pirin": 3,
    "putal": 1, "puti": 3, "qemai": 1, "sati": 1, "seguk": 1, "segup": 1,
    "seguq": 1, "sidi": 1, "sidwi": 1, "silin": 2, "sinkai": 1, "sipwi": 2,
    "stbaku": 2, "subil": 1, "syukang": 1, "tagahan": 13, "takux": 1,
    "taulan": 5, "tausen": 4, "tautyeh": 2, "teaji": 1, "temi": 3, "tensu": 1,
    "tenung": 1, "tiing": 2, "tikai": 1, "tilay": 1, "timin": 11, "tiwin": 1,
    "tyakang": 3, "uding": 1, "ukak": 1, "umyaq": 1, "unin": 1, "wating": 1,
    "watyeh": 1, "yurdan": 2,
}

# HAND_NOT_NAMES. The population REACHES all sixteen and this list is the only
# thing keeping them pale. Four have no page occurrence and so cannot be checked
# for colour here — they are asserted absent from verified.js instead, below.
PIN = {"byeqay": 2, "grand": 1, "grandeur": 1, "mnttlaqel": 1, "mpa": 4,
       "mpsqlul": 1, "pnsdahung": 1, "qlap": 1, "tbasyaq": 1, "tsaleh": 1,
       "yianu": 2, "yiyah": 1}
PIN_OFFPAGE = ["beau", "cunnaissance", "ruugeur", "vivant"]

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


import io, re, os
vjs = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                           "..", "..", "site", "verified.js"),
              encoding="utf-8").read()
have = set(re.findall(r'"([^"]+)": \d+', vjs))
for w in PIN_OFFPAGE:
    if w in have:
        fail.append("PIN_OFFPAGE %s: French, must not be in verified.js" % w)

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
if tally["dark"] < 42504:
    fail.append("census: dark fell to %d, below this batch's 42,504" % tally["dark"])
if 100.0 * tally["dark"] / tot < 95.0:
    fail.append("census: dark fell back below 95%")

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], 100.0 * tally["dark"] / tot))
print("GAIN %d names / %d occurrences now dark" % (len(GAIN), sum(GAIN.values())))
print("PIN  %d impostors still pale, %d French off-page absent from verified.js"
      % (len(PIN), len(PIN_OFFPAGE)))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
