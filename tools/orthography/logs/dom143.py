# -*- coding: utf-8 -*-
"""Batch 143: seven prefixes his book uses and PRE had never heard of.

313 pale values find no root at all, and for some of them the reason is not
that the root is missing but that the PREFIX is — `roots()` can only peel what
`PRE` lists, so `empaqsiya` was an unanalysable eight-letter string while
`qsiya` 水 sat one row away. Seven were priced one at a time and then together:

    empa  pkp  spk  sps  npk  dmp  emb      ADDED 14, REMOVED 0, RELEVELLED 3

`psp` was priced the same way and gave 0, so it is not in the list — a prefix
earns its row by taking a word, not by looking plausible.

**empa- is "will become X"**, the clearest of the seven and the reason the
group is defensible on meaning and not just on arithmetic:

    empaqsiya   化成水            `qsiya`    水
    empasnaw    成為丈夫          `snaw`     丈夫
    empaayug    將變成溪流        `ayug`     溪
    empanalu    (好)              `nmalu`    好
    empaqmpahan                   `qmpahan`  工作的地

and the rest:

    dmpuyas     歌者              `uyas`     歌
    embsqrul                      `sqrul`    燒焦
    npkrbagan   夏天將至          `rbagan`   夏天
    pkpakux     翻過來            `makux`    翻
    spkmalu                       `malu`     好
    spkungat    使消失            `ungat`
    spspgan                       `snpgan`   算
    spsqrinut   使變窮            `qrinut`   窮

**`pkpakux` is `pkp`+`akux`, not the 老鼠 `pakux`.** The two readings are one
letter-string apart and only one of them is 翻. This matters because batch 142
pinned `mkpakaw` in HAND_NOT_REGULAR for landing on the wrong side of exactly
that kind of split; nothing here touches it, and the check below proves it.

`sgasut` came in on level 3 rather than through a new prefix — the widened
`PRE` grew `derived('sgasut')`'s supporter set past the two-affix guard, so
`vouched()` could speak. `gasut` is 工作範圍（工作的起點及終點）, the run of a
job from its start to its end, against his 照計畫、照正常程序進行——規劃安排.

Three values were already verified and moved level: `embliqan` 5→2,
`empaabalay` 5→4, `spssagun` 4→2 — each now reached by a shorter argument than
the one that had been carrying it. They were dark before and are dark after,
which is what RELEVEL below asserts.

Census after: modern dark 42,191 / pale 2,242 / green 32 = **94.8859%** (from
94.8319%), original 42,664 / 2,266 / 32 = 94.8890%, 1,967 cards, 0 page errors
in both modes.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# the 14 the widened PRE takes, with the pale occurrences each had
GAIN = {
    "dmpuyas": 1, "embsqrul": 1, "empaayug": 2, "empanalu": 4,
    "empaqmpahan": 1, "empaqsiya": 1, "empasnaw": 2, "npkrbagan": 2,
    "pkpakux": 3, "sgasut": 1, "spkmalu": 1, "spkungat": 3, "spspgan": 1,
    "spsqrinut": 1,
}

# already dark, moved level only. If a future batch narrows PRE these are the
# first to fall back, and a fall shows up here as pale rather than silently.
RELEVEL = {"embliqan": 7, "empaabalay": 2, "spssagun": 2}

# batch 142's pin, one letter from `pkpakux` and on the wrong root. Nothing in
# this batch may reach it.
PIN = {"mkpakaw": 4}

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
    rele = pg.evaluate(SPANS, sorted(RELEVEL))
    pin = pg.evaluate(SPANS, sorted(PIN))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(rele, RELEVEL, "dark", "RELEVEL")
check(pin, PIN, "pale", "PIN")

tot = sum(tally.values())
if tally["dark"] < 42191:
    fail.append("census: dark fell to %d, below this batch's 42,191" % tally["dark"])

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], 100.0 * tally["dark"] / tot))
print("GAIN %d values / %d occurrences now dark" % (len(GAIN), sum(GAIN.values())))
print("RELEVEL %d still dark   PIN %d still pale (mkpakaw, batch 142)"
      % (len(RELEVEL), len(PIN)))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
