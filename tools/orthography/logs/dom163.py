# -*- coding: utf-8 -*-
"""Batch 163: two guards asked what they were actually guarding.

**(a) `outvoted()` — the freeze gates SPELLING, and this rule asks about
MEANING.** `self.frozen` is the name freeze. It exists so l→r cannot rename a
man (batch 21's `Sapah Sibar`), and tier N in `build_modern_map.py` is what
enforces that on the page. Nothing in `outvoted()` can respell anybody: the root
is being asked what it MEANS, and the answer only ever decides a colour. So a
frozen root whose citation gloss reads *only* 人名 is now admitted — because
"this is a name" is not a sense a derived form inherits, which makes it the one
citation gloss a paradigm cannot be outvoted *by*.

`banah` is the textbook case: cited 人名（男）, with 27 derived forms glossed 紅
(`embanah` 紅色的, `kbanah` 染紅, `knbanah`, `gmbanah`) against his `mabanah`
將要變紅. `tasaw` is cited 人名（男）with `mtasaw` / `pgtasaw` / `sgtasaw` all on
清, giving his `ptasaw`. Same distinction as batch 156's `lex` (may be printed)
against `voices` (may be heard), one level further out.

The root floor drops 4→3 in the same rule, and for the reason batch 146 gave
`vouched()`: elsewhere the floor guards a root found INSIDE a longer string,
while here over-generation is already refused by the two-distinct-affix and
supporter bars. It buys `pix`, whose *citation* gloss is **山羊的叫聲** — a
goat's bleat — outvoted by `mapix` 壓在其上－按壓, `empapix` 被壓垮的 and the
supporters `pixi` / `mnpix` / `pixan`, every one of them 壓. That is the rule
doing precisely what batch 152 built it to do, on a gloss no synonym table would
ever have reached.

**(b) `no_chinese()` — ambiguity means two ROOTS, not two spellings.** The rule
refuses when more than one root candidate survives, because with no Chinese of
his there is nothing to break a tie. But the wordlist files a paradigm's cells as
separate headwords, so `pnsblaqan` reaches `blaq`, `blaqa`, `blaqan`, `blaqi`,
`sblaqa`, `sblaqan` and `sblaqi` — one lexeme found seven times over. Whichever
is picked the answer is the same word, and the guard was refusing to break a tie
that does not exist.

`root_groups()` partitions candidates by containment, before or after one
paradigm suffix is peeled off either side (a suffix difference is a SLOT
difference, not a root difference), and the rule now needs exactly one GROUP.
Containment alone gave 44 types; suffix-aware collapse gives 57.

**The load-bearing half is the eleven that still refuse.** `kngusan` sits between
`kgus` and `ngus`, `stmaqun` between `taqi` and `tmaq` — two roots apiece, which
is what the guard was written for, and they are asserted pale below alongside
nine more. If genuine ambiguity ever stops refusing, this collapse has been read
as a licence to widen.

**Seven hand pins, each read against the sentence he prints it in** — the same
method as batch 145's six, and the same failure: one candidate, and it is the
wrong word.

| value | his entry | wrong root |
|---|---|---|
| `mslangan` | BMBANG 鐵皮－鐵桶 (rust on tin) | `langu` 湖 |
| `snpsaran` | PUSAL 更新／XAL 唯一 | `sari` 芋頭 |
| `snpsarun` | PUSAL 成雙－加倍 | `sari` 芋頭 |
| `sbuwai` | TK'MU 把書交給 | `buwa` 氣泡 |
| `shnkan` | LATAT `sapah shnkan` = 監獄 | `hnka` 便宜 |
| `psnluun` | SN'LO 傳達／傳遍各處 | `luun` 將會省著用 |
| `tmukan` | TUYOQ 唾液－吐口水 | `tuki` 抵銷／點鐘；小時 |

`mslangan` is `empslangan`'s own sibling, pinned by batch 145. **`tmukan` is the
price of the widening and is named as such**: it is the only one of the seven the
group collapse reached rather than the old one-candidate guard, and `tuki` is
exactly the Japanese 時計 loan-homograph tier J was built around — "the more often
it turns up, the more confident the wrong answer looked". His sentence is
他們全都朝他的臉吐了口水.

**Two kept after the same scrutiny**, and they are in GAIN: `nhnaan` ← `hnaa`
stands in 澆我們種的花, newly-planted, and `hana` 剛剛 IS that lexeme; `mnkbubu` ←
`kbubu` is his own bracketed variant `mnqbobo (mnkbobo ?)` in 戴著帽子就進了我家,
the hat word `qbubu`.

**One arrival flagged rather than defended.** `pnsblaqan`'s root `blaq` is
glossed 松鼠;老鼠;…碎粒, which is a homograph — the source is his BLAEQ 幸福 /
`bilaq` 小 family, and batch 142 already verified `psblaqan`/`psblaqi` off `bilaq`
小. The morphology lands on a real listed paradigm either way, so the value
stands; the odd gloss is recorded here rather than left to look like evidence.

+53 values / 60 occurrences, 0 de-verified, **0 new pale types**. DOM census
97.0986% → **97.2335%** (43,231 dark / 1,198 pale / 32 green), 1,967 cards,
0 page errors.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# (a) outvoted(): the four the freeze and the floor were withholding.
GAIN_OUTVOTED = {"mabanah": 2, "ptasaw": 2, "mapix": 2, "empapix": 2}

# (b) no_chinese(): the collapse, one lexeme instead of seven analyses.
GAIN_COLLAPSE = {
    "empbais": 1, "empdahung": 1, "empskribut": 1, "hnjyalan": 1,
    "kmptucing": 1, "kmrisuh": 1, "kmsalu": 1, "kmstrung": 1, "kmtgsa": 1,
    "mkbkuy": 1, "mkdngu": 1, "mnkbubu": 1, "mntatuk": 1, "mscimu": 1,
    "mtquri": 1, "nhnaan": 1, "nknnaqih": 1, "npdhuq": 1, "nsrahuq": 1,
    "ntrilan": 1, "pbiqun": 1, "pdangun": 1, "pgskaun": 1, "pkblangun": 1,
    "pkdagun": 1, "pkdnguun": 1, "pnbrihan": 1, "pnkpais": 1, "pnkparu": 1,
    "pnllayan": 1, "pnlnglung": 1, "pnsblaqan": 1, "pnsblayan": 1,
    "pnsgagan": 1, "pnstutuy": 2, "pnsuwiq": 1, "pnteuqan": 2, "pntkumax": 1,
    "pplhlah": 1, "psrisuh": 1, "psthiyaqun": 1, "pstlngun": 1, "pstrilun": 1,
    "ptduwaun": 1, "skcilux": 1, "smnrahuq": 1, "sntlngan": 2, "squwaqi": 1,
    "tnquri": 1,
}

GAIN = dict(GAIN_OUTVOTED)
GAIN.update(GAIN_COLLAPSE)

# The guard still refusing, which is the batch's own claim. Two DIFFERENT roots
# apiece — `kngusan` [kgus, ngus], `stmaqun` [taqi, tmaq] — so the collapse must
# not reach them. If these go dark, ambiguity has stopped meaning ambiguity.
AMBIGUOUS = {
    "kngusan": 2, "stmaqun": 2, "ptbnuun": 2, "ppdsun": 1, "gmnaliq": 1,
    "kmkmalu": 1, "empsneanak": 1, "knkmuyuh": 1, "nkmuyuh": 1,
    "psmkun": 1,
}
# `sneelug` was in this list and is retired from it, batch 166. It was pale
# here for the right reason under the wrong spelling: its two roots were
# `seelug` and `neelug`, both road words, and it was never a road word at all.
# His `Sn"lu` is the preterite of SALU 'to make' and now renders `snalu`
# 用...做的, listed. The ambiguity was real; the word was not.

# The seven read against his own sentences and pinned in HAND_NOT_NC.
PIN = {
    "mslangan": 1, "snpsaran": 2, "snpsarun": 1, "sbuwai": 1, "shnkan": 1,
    "psnluun": 1, "tmukan": 1,
}

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
    amb = pg.evaluate(SPANS, sorted(AMBIGUOUS))
    pin = pg.evaluate(SPANS, sorted(PIN))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(amb, AMBIGUOUS, "pale", "AMBIGUOUS")
check(pin, PIN, "pale", "PIN")

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43231:
    fail.append("census: dark fell to %d, below this batch's 43,231" % tally["dark"])
if pct < 97.0986:
    fail.append("census: dark fell back below batch 162's 97.0986%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occ  (outvoted %d, collapse %d)"
      % (len(GAIN), sum(GAIN.values()), len(GAIN_OUTVOTED), len(GAIN_COLLAPSE)))
print("AMBIGUOUS %d values / %d occ still pale — two roots is still a tie"
      % (len(AMBIGUOUS), sum(AMBIGUOUS.values())))
print("PIN %d values / %d occ still pale — one candidate, wrong word"
      % (len(PIN), sum(PIN.values())))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
