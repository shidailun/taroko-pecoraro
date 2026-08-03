# -*- coding: utf-8 -*-
"""Batch 169: three refusals, and the most tempting wrong merge on the sheet.

No occurrences move. This log exists because everything it pins is one careless
widening away from going dark on a guess, and the census cannot see any of it.

**Sheet 1 row 3 proposed the root `biyi` for his TABE card. It is wrong.**
`biyi` is 工寮, the field hut, and the modern dictionary writes the hut in full
as `biyi qmpahan` — the hut of the worked land. Its family is `pbiyi` 蓋工寮,
`tmbiyi` 專蓋工寮, `spbiyi` 因…蓋工寮: all building, no ploughing. 15 occurrences
of `biyi` are already dark on that meaning and they are not these. The sheet
reached the string, not the word.

**His TABE and TABUN are one word, and a speaker said so.** p. 274 carries
TABE 犁 with the subs Tbian (Tbiyan) 可耕的－可以犁田的地方, Tnbiyan 犁過的田,
Ptabe, and his own note （註：是否與 TMABUN 有親屬關係？）; four pages on, TABUN
開墾－深掘 with Tmabun, Tnabun, Tnbunan 已開墾的地方. Tgdaya has `tabul` for both
犁 and 開墾 — the ruling of 2026-08-03 — so his guess was right and the two cards
are one root, split by a vowel.

**Which is exactly why nothing may move.** Modern Truku kept only the digging
half: `tabun` 鋤地, `tmabun` 在鋤地, `mtabun` 鋤地的人, `stabun` 為…鋤地, and its
suffixed slot `tbunaw` 被…鋤地. All of his TABUN slots are already dark. The
ploughing half he glosses himself as 同義詞＝SAKOL, and the map long ago wrote
his unsuffixed forms onto `sakur` 犁 — `tabe`>`sakur`, `ptabe`>`psakur`,
`mptabe`>`empsakur` — which is where `sakur` 2 dark comes from. But `sakur` has
no suffixed slot in the wordlist at all (`msakur`, `psakur`, `spsakur`,
`empsakur`, `mnsakur`, `ppsakur` and no more), so his eight suffixed TABE
occurrences have nowhere modern to land and stay pale.

The trap is that they very nearly do. `tnbiyan` 犁過的田 against listed
`tnbunan` 已開墾的地方 is one vowel and one gloss apart, and the two ARE the same
root historically. That is not a licence to respell i as u. Pinned pale below;
if they ever go dark, something has merged the two cards on the strength of the
Tgdaya cognate, and the eight are a guess.

**`tabe` is not a subjunctive.** Asked whether his final -e is the projective
suffix: no. His four word-final vowels split two ways, and the map counts it.
Bare -e is modern -i (~170: `laqe`>`laqi`, `taqe`>`taqi`, `bale`>`bali`) and bare
-o is modern -u (~450: `ako`>`aku`, `bato`>`batu`). The subjunctive pair is the
one that carries an extra letter — -AE > `-ay` (49) and -AO > `-aw` (289).

The paradigm confirms the split, and it is the batch-167 rung that makes the test
sharp. A true `-aw` ALTERNATES before a suffix: SPADAO > `pspadaw`, but
`pspdagan`, `pspdagun`, `pspdagi`. A root-final -e SURVIVES every suffix, in all
four of his -e headwords that have suffixed slots — LAQE = `laqi` 孩子 keeps it in
`Lqean`; TAQE = `taqi` 睡 in `Tqean`, `Tnqean`; LABE = `rabi` 晚上 in `Klbiyun`,
`Pklbiyan`; and TABE in `Tbian (Tbiyan)`, `Tnbiyan`, `Tbiun`. `laqi` and `taqi`
are as uncontroversial as roots get and TABE inflects exactly like them, so the
-e is root material: his headword is `tabi`, and the open question is a speaker's
one about `tabi` beside `tabun`, not a spelling one.

(An earlier pass scored this 0 of 4 the other way. The classifier looked for the
stem vowel without allowing for syncope, `ta-` > `t-`, so it missed the vowel in
every slot that has one. Same class as the `inf.roots()` tuple trap: a heuristic
that silently returns the opposite answer. The four were then read by hand.)

**`tbilan` stays held, and the weaving line is now closed.** Batch 168 left it
pale with the root unknown; the `miri` hypothesis of 2026-08-03 was tested and
fails. `pniri` 挑織布紋的衣服 is semantically perfect for `Lukus tbilan` 節慶服飾,
but the family reduces to `-iri`/`-ri` with no b and no l (`miri` 布紋;挑織,
`pmiri` 編挑織, `priun` 織成布紋繡, `mgpniri`, `empeepniri`), he has no MIRI card,
and `tbilan` appears in no modern corpus in any spelling. His own page proves he
tried: p. 320 reads TBILAN (R. = ??) between TBALAE (R. = BALAE) and TBNAO
(R. = LBNAO + Préfixe T, le L étant escamoté?) — he does T-prefix analysis on
that very page and could not do it here. The one thread not yet pulled is
`hmuril` 鈴鐺（裝飾品）, with `pnril` and `tnrilan` sitting unglossed in the
lexicon.

Census unchanged: 43,320 / 1,109 / 32, dark 97.4337%.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# The eight suffixed TABE slots. `sakur` has no suffixed form in the wordlist,
# so these have nowhere to land. Dark here means a merge onto the TABUN card.
PIN_TABE = {"tnbiyan": 2, "tbiyun": 2, "tbiyi": 1,
            "ptbiyi": 1, "ptbiyan": 1, "ptbiyun": 1}

# The digging half, already dark on listed modern words. This is the side that
# survived into modern Truku, and it is the bait.
PIN_TABUN = {"tabun": 1, "tmabun": 5, "tnabun": 2, "tnbunan": 2}

# The field hut and the worked land: the row's proposed root, on its own meaning.
PIN_HUT = {"biyi": 15, "qmpahan": 58}

# The 犁 word he names himself as 同義詞＝SAKOL, carrying his unsuffixed forms.
PIN_SAKUR = {"sakur": 2}

# Held since batch 168; the `miri` line is closed but the root is still unknown.
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
    tabe = pg.evaluate(SPANS, sorted(PIN_TABE))
    tabun = pg.evaluate(SPANS, sorted(PIN_TABUN))
    hut = pg.evaluate(SPANS, sorted(PIN_HUT))
    sak = pg.evaluate(SPANS, sorted(PIN_SAKUR))
    tbil = pg.evaluate(SPANS, sorted(PIN_TBILAN))
    b.close()

check(tabe, PIN_TABE, "pale", "TABE")
check(tabun, PIN_TABUN, "dark", "TABUN")
check(hut, PIN_HUT, "dark", "HUT")
check(sak, PIN_SAKUR, "dark", "SAKUR")
check(tbil, PIN_TBILAN, "pale", "HELD")

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43320:
    fail.append("census: dark fell to %d, below batch 168's 43,320" % tally["dark"])
if pct < 97.433:
    fail.append("census: dark fell back below 97.4337%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("REFUSED %d occ still pale on the TABE card; `sakur` has no suffixed slot"
      % sum(PIN_TABE.values()))
print("BAIT    %d occ dark on the TABUN card, one vowel away"
      % sum(PIN_TABUN.values()))
print("HELD    %d occ pale on `tbiran`; the `miri` line is closed, root unknown"
      % sum(PIN_TBILAN.values()))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
