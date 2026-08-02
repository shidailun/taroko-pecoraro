# -*- coding: utf-8 -*-
"""Batch 160: the typewriter's blind spot, and the batch that passes 97%.

**Most of this batch is not a spelling map entry at all.** It is a transcription
repair, and the difference is the whole point — a map entry would leave
"original spelling" mode showing a word Pecoraro never printed.

His 1977 typescript prints an `m` that the digitization read as `n`; the proof
is his own French, which the same pass also mangled (`nonbreuses`, `Conbien`,
`janais`). The productive sweep is "the token is nothing in modern Truku but
becomes a real word when one `n` is read as `m`" — and the sweep as previously
run carried an index guard of `i >= 2`, which hid positions 0 and 1. That is
where the remaining ones were. `knnalu` had already been repaired to `knmalu` at
position 2; `nnalu`, one letter earlier in the same entry, had never been seen.

**His French is what licenses each one, because a word-initial `n-` is a real
Truku prefix and looks identical.** The discriminator is on the page:

  Nngangax  "A partir du fait d'être muet"    — n- ON ngangah.  CORRECT AS
                                                PRINTED, and refused here.
  Nnalu     "A partir du bien … Il était bien  — n- on `malu`, so the SECOND
             autrefois"                          letter is the misread m.
                                                `nmalu` 原本是好的.

Same formula, opposite verdicts. Repaired, each confirmed by his French:

  Nnalu   4×  "De bien qu'il était hier"          -> nmalu   原本是好的
  Nniyax  4×  "C'est bien toi qui es venu"        -> mniyah  已經來了
  Nllawa  2×  "il n'est pas permis de chahuter"   -> mrrawa  玩耍
  Naxon   2×  "de l'eau pour boire"               -> mahun   要喝的
  naso    2×  "le millet" / "que du millet"       -> masu    小米

**`naso` is three tokens and only two are millet.** The third is "Distribue cet
argent en trois parts égales", his 分配 root — so the repair is anchored on its
two sentences and not on the word, and the third stays pale. Refusing a blanket
convert is the standing rule of this class: Truku's `<n>` perfective and `<m>`
actor-focus infixes share a slot, so `snpu`/`smpu` and `tnaga`/`tmaga` are real
pairs and the whole C-n- class is off limits. `mnalu`, `snkrawah`, `qnbsranan`
and `tnaga` were all offered by the sweep and all refused on that ground.

**The map layer adds five, and one of them is his own cross-reference.** WINUK
carries the note 無疑是 XWINUK 的縮略形式；參 XWINUK, and X is his h — he is not
corrected, he is taken at his word. The other four are the final-g class already
recorded for 路 `elug` and 餵養 `tabug`, each confirmed by HIS Chinese rather
than by shape: `snpu`=`snpug` 數過 (ini k'la snpu 沒辦法數了), `msnulu`=`msnulug`
恰好 (就在那一刻), `lubu`=`lubug` and `lmubu`=`lmubug` under his LUBU 樂器.

**`psilin` was the sixth and is refused, for a mechanical reason worth keeping.**
His Psilin sits under his own headword SILING, so the ng is his and the entry
corrects itself. But a key `psilin`->`psiling` reads to the cross-entry root
projection as "append g", and it re-applied that to his RAW `psiling` (3×) and
`mpsiling`, putting `psilingg` and `empsilingg` on the page. It bought 1 dark and
cost 4. **A respelling that is right about the word can still be wrong about the
machine** — and the census is what caught it, not the argument.

`tabu` 5× and `tksaw` 5× stay pale and are pinned below. `tabu` is blocked by
homography: there are TWO TABU entries, 餵養 and a hardwood, and this map is
keyed on tokens. `tksaw` is blocked because his own `Xksao` already owns
`hksaw`, so sending `Tksao` there would erase a distinction he drew.

+9 map occurrences / +14 transcription occurrences. Census after: modern dark
43,133 / pale 1,297 / green 32 = **97.0109%** (from 96.9615%), 1,967 cards, 0
page errors. **This is the batch that passes 97%.**
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# The map layer: his own cross-reference, plus the final-g class.
GAIN = {"hwinuk": 6, "snpug": 2, "msnulug": 2, "lubug": 1, "lmubug": 1}

# The transcription layer. These are absolute page totals, not deltas — each
# repaired token merged into a span that already existed, which is itself the
# evidence that the repair spells it the way the rest of the book already does.
REPAIR = {"nmalu": 4, "mniyah": 35, "mrrawa": 5, "mahun": 14, "masu": 39}

# The refusals, and every one of them is load-bearing.
#   tabu   homograph — 餵養 and a hardwood share the token
#   tksaw  his Xksao already owns `hksaw`
#   nasu   the one `naso` of three that means 分配, not millet
#   psilin the root projection would double the g on his raw `psiling`
PIN = {"tabu": 5, "tksaw": 5, "nasu": 1, "psilin": 1}

# His misread spellings must render nowhere, and neither may the double-g the
# refused `psilin` key produced.
GONE = ["nnalu", "nniyah", "nrrawa", "nahun", "winuk", "snpu", "msnulu",
        "lubu", "lmubu", "psilingg", "empsilingg"]

# The raw `psiling` family, restored by dropping that key. If these ever go
# pale again, the projection is doubling the g once more.
KEPT = {"psiling": 3, "empsiling": 1, "msiling": 2}

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
    repair = pg.evaluate(SPANS, sorted(REPAIR))
    pin = pg.evaluate(SPANS, sorted(PIN))
    gone = pg.evaluate(SPANS, sorted(GONE))
    kept = pg.evaluate(SPANS, sorted(KEPT))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(repair, REPAIR, "dark", "REPAIR")
check(pin, PIN, "pale", "PIN")
check(kept, KEPT, "dark", "KEPT")
for w in GONE:
    if gone.get(w):
        fail.append("GONE %s: still renders, %s" % (w, gone[w]))

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43133:
    fail.append("census: dark fell to %d, below this batch's 43,133" % tally["dark"])
if pct < 97.0:
    fail.append("census: dark fell back below 97%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN   %d values / %d occ — his XWINUK cross-reference + the final-g class"
      % (len(GAIN), sum(GAIN.values())))
print("REPAIR %d values / %d occ — typewriter m read as n, French-confirmed"
      % (len(REPAIR), sum(REPAIR.values())))
print("PIN    %d refused (%d occ) — homograph, his own distinction, 分配, projection"
      % (len(PIN), sum(PIN.values())))
print("GONE   %d spellings render nowhere" % len(GONE))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
