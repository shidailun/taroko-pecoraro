# -*- coding: utf-8 -*-
"""Batch 141: the root is listed, and nobody ever glossed it.

`regular()` asks two questions of a root and needs both — is it listed, and
does its gloss agree with his Chinese — and for **138 types / 223 occurrences**
the first answer is yes and the second cannot be asked at all, because
`attested_gloss.json` holds no gloss for the root. That is a hole in the GLOSS
TABLE, not a verdict on the word, and this project has already convicted that
same hole twice by name: `qriban`, and `ttmaan` in `inflection.py`'s
HAND_NOT_ROOTED note ("what stops regular() reaching it is that `ttmaan`
carries no gloss, which is the listing gap, not a morphology gap"). Most of a
paradigm is glossless; the wordlist glosses a citation form and leaves the
slots bare.

So ask the paradigm instead. `ptbgi` is the shape: `tbgi` is listed and bare,
`tbgan` 養家畜的地方 is listed too, and his gloss for the value is 託人餵養－使人
餵養, agreeing on 養. The root's own inflection says what the root means.

**It cannot reopen the SISUN trap**, which is the first thing to check of any
rule that touches roots. His SISUN decomposes perfectly as `sisi`+`-un` and
`sisi` is 用來濾酒的工具, a rattan wine strainer — so `regular()` READS that
gloss, refuses on it, and the value never arrives here. This level fires only
where `self.gl.get(root)` is empty, i.e. only where there was nothing to read.

The chain is the same length as `vouched_root()`'s — one affix step to a root,
one paradigm step from the root to a supporter that speaks for it — so it
carries that method's guard set verbatim: slot-only Chinese, a four-letter root
floor, the root unfrozen, `derived()` yielding two DISTINCT affixes, and the
whole/VSUF final-vowel witness. Its one respect in which the evidence is
stronger is why it sits a level ABOVE: `vouched_root()`'s root is a hypothesis,
and this one is a word the wordlist prints. Emitted level 4; `vouched_root`
moves to 5, `sistered` 6, `syncopated` 7, `chained` 8, `affix` 9. Renumbering
is free — `app.js` only tests MEMBERSHIP of MODERN_VERIFIED (`hasOwnProperty`),
never the number.

**26 values, read one by one, six pinned.** All six fail the same way and it is
the only way this kind of agreement can fail: the shared character is not a
word but a PARTICLE, and no gate can see that, because a particle is a
character like any other.

  psqpahan  his （主動）地黏貼－使黏附 against `qmpahan` 工作的地, agreeing on 地 —
  psqpahi   the ADVERBIAL 地 against the 地 that means ground. He has two roots
  psqpahun  here and they are not one root: QPAH 工作 and SQPAX 黏貼. Right
            letters, wrong word — SISUN exactly, which is the point.
  mttama    坐著的人／坐下－靠著休息 against `pttama` 守著, on 著, the aspect
  tmtama    marker. All three glosses wear it and none of them means it.
  mrbuq     his 呈凹陷－形成凹穴 against `trbuq` 形容坑洞深, on the 形 of 形容 —
            the head the wordlist writes before a gloss that DESCRIBES, the
            same class as the 用來 already in BOILER. Both readings really are
            hollows, so this one is pinned rather than remapped: the answer is
            right and the argument for it is worthless.

Requiring a two-character RUN instead of a hand list was measured and refused —
it costs 14 of the 26 to save these 6, including `qnriqani` 恨, `trgrig` 舞,
`smbrinah` 回 and the three `pllg-` 動, every one a single character that IS a
word.

Census after: modern dark 42,148 / pale 2,285 / green 32 = **94.7892%** (from
94.7037%), original 42,621 / 2,309 / 32 = 94.7934%, 1,967 cards, 0 page errors
in both modes. +38 occurrences, 0 de-verified — `verified.js` gained exactly
these 20 keys and lost none.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# the 20 the rule takes, with the pale occurrences each had
GAIN = {
    "matrima": 2, "mlxan": 2, "msbrinah": 2, "msparu": 1, "mstama": 3,
    "mtrima": 2, "pjiyan": 1, "pllgan": 1, "pllgi": 1, "pllgun": 2,
    "pntrilun": 3, "pqpahan": 1, "psuqi": 2, "ptbgi": 2, "qnriqani": 2,
    "smbrinah": 3, "spqnaqih": 2, "spqpah": 2, "sruciqun": 2, "trgrig": 2,
}

# the six pinned by hand — the rule REACHES all six, and HAND_NOT_UNGLOSSED is
# the only thing keeping them pale. If that set is ever dropped, this is what
# tells you, and `psqpah*` is the SISUN case wearing a different word's letters.
PIN = {"psqpahan": 1, "psqpahi": 1, "psqpahun": 1,
       "mttama": 3, "tmtama": 2, "mrbuq": 2}

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
if tally["dark"] < 42148:
    fail.append("census: dark fell to %d, below this batch's 42,148" % tally["dark"])

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], 100.0 * tally["dark"] / tot))
print("GAIN %d values / %d occurrences now dark" % (len(GAIN), sum(GAIN.values())))
print("PIN  %d hand-pinned values still pale (%d occ)" % (len(PIN), sum(PIN.values())))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
