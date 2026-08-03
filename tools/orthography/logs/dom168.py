# -*- coding: utf-8 -*-
"""Batch 168: BIRI -> `bili`, ruled by a speaker over the map's own statistics.

**Sheet 1 row 2 asked whether `biri` and `tbiran` come from `bir` 車聲（擬聲詞）.**
They do not — `bir` is the noise an engine makes and it is the only `bir-` in the
wordlist. Reading the cards turned the row into a different question, and the
answer had already been written down once, in batch 69, the other way.

**p. 41 carries TWO cards spelled BIRI, and the OCR is faithful to both**
(scans/full/page_041.png, verified 2026-08-03):

    BIRI (R.?) = Dernier.  § Biri bi ka yako = Je suis vraiment le dernier.
    BIRI (R.?) = Mouillé tout outre - trempé.  § ... Biri kana lukus mo da!

Two slots each, four occurrences. `(R.?)` is his own doubt marker on the root —
he was not sure either card had one.

**The wet card is `bili` 很濕 and nothing else.** The wordlist has the whole
paradigm — `blbili` 都淋濕, `dbili` 淋濕者, `empsbili` 會淋濕, `gmnbili` 曾淋濕,
`gbili` 用來避淋濕 — and `Biri kana lukus mo da` is `bili kana lukus mu` said in
1977. The spoken corpus has `bili` ten times.

**Against that stood a statistic, and the statistic lost.** His <l> is ambiguous
— 1,151 of them become modern <r>, 1,275 stay <l> — but his <r> had never once
crossed: 0 cases of his <r> -> modern <l> in 5,514 respellings, against 71 where
his <r> stays <r>. `bili` is the first crossing in the whole map. That is real
evidence and it is not decisive against a speaker reading his own example
sentence; it is recorded here so the next crossing is not waved through on the
strength of this one.

**The cost, stated plainly: two of these four occurrences are knowingly wrong.**
The map is keyed on the raw token, so one key spells both cards, and `Dernier`
is not `bili`. Batch 69 held the tie for exactly this reason ("do not make the
losing side wrong"); the ruling of 2026-08-03 overrides it and accepts 2 false
darks to place 2 true ones. `hili` 最小的、老么 remains the only candidate ever
found for the Dernier card and it is out of reach of `biri`. This is the second
recorded case of the class, after p. 222's two `Mpolo` subs, and both are in
`audit_rare.py`'s docstring because the census cannot see either.

**`tbilan` is untouched.** He glosses it `？？` himself; the only evidence is
`Lukus tbilan` 節慶服飾－盛裝 and `snais so lukus tbilan` on the SAIS card
(p. 256). It is transparently an LF in `-an`, but with the root unknown the
<l> is a coin flip — his <l> goes both ways — so `tbiran` stands as a proposal,
pale, and the sheet keeps asking. `pniri` 挑織布紋的衣服 is the modern festival
garment and is not phonetically reachable from `tbilan`.

+4 occurrences. 97.4247% -> 97.4337% (43,320 / 1,109 / 32).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# Four occurrences, two cards, one key. Two of them are the Dernier card.
GAIN = {"bili": 4}

# His spelling must be gone from the modern page entirely.
GONE = ["biri"]

# Held: the root is unknown, so the <l> cannot be ruled. If this ever goes dark
# without a root being named, something has guessed.
PIN_TBILAN = {"tbiran": 4}

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
    gone = pg.evaluate(SPANS, sorted(GONE))
    tbil = pg.evaluate(SPANS, sorted(PIN_TBILAN))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(tbil, PIN_TBILAN, "pale", "HELD")
for w in GONE:
    if gone.get(w):
        fail.append("GONE %s: still rendered, %s" % (w, gone[w]))

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43320:
    fail.append("census: dark fell to %d, below this batch's 43,320" % tally["dark"])
if pct < 97.433:
    fail.append("census: dark fell back below 97.4337%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d occ on `bili`; 2 of them are the Dernier card and are wrong"
      % sum(GAIN.values()))
print("HELD %d occ still pale on `tbiran`, root unknown" % sum(PIN_TBILAN.values()))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
