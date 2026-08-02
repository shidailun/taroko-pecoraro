# -*- coding: utf-8 -*-
"""Batch 157: LIWAQ. The bar was met, not lowered.

`liwaq` is the last root the speaker shortlist was still holding, and it comes
off it the same way `qdug` did — by asking the Truku Bible instead of a person.

Its 趕 sense fell in batch 154. Its 發亮 sense is these three: `pkliwaq` and
`skliwaq` 使其變得明亮, `spkliwaq` 用來使東西發亮. dom152 filed them as
coincidences of the kind the second-voice bar exists to catch, and dom154 left
them there. **Both files said, in writing, that if these ever went dark without
the supporter requirement being argued down, the bar had been read as a licence
to widen.** It has not been argued down. It has been satisfied:

    pkliwaq   sup = qnliwaq 明亮=閃光 , tqliwaq 明亮=發光
    skliwaq   sup = qnliwaq 明亮=閃光 , tqliwaq 明亮=發光
    spkliwaq  sup = qnliwaq 發亮=閃光 , tqliwaq 發

Two independent voices apiece, on a root the wordlist glosses 化妝 and the
glossary glosses 銀 — makeup and silver, which is what a shine word looks like
when an editor has to pick one noun for it.

**Two small changes, and neither buys anything on its own.**

`tq` joins PRE. It is the exact parallel of `mq`, legal since batch 128 and
yielding `mqliwaq` off this very root, and it exists here only so `tqliwaq`
發光的；閃耀的 can be a supporter in `derived()`. Priced the way PRE's own note
demands — singly and in combination, gain column AND re-cut column: **0 values
re-cut, 0 roots stolen, 0 values verified by it directly.** Compare `sq`, which
that note records as measured and rejected for stealing `sqrasan` off `qras`
快樂. A prefix that moves nothing and reaches one new voice is the cheapest
thing this inventory has ever been asked to hold.

Three members join the shine SYN line, which already held 光線 有光 明亮 照亮
天亮 發亮 and now holds 發光 閃耀 閃光. This is the case SYN was written for:
his 明亮 and the glossary's 發光 name one thing and share no character, so
neither the bigram tier nor the character tier could see between them. Every
new member is two characters, per the table's guard.

**And the other five coincidences do not move.** `ptaril` on the 方 of 地方,
`ppungu`, `ssiyang`, `emptaril`, `emppungu` — one voice on one fragment, still
pale, asserted below. (`emptaril` is dark as of batch 162, on an ILRDF parquet
attestation of the spelling — not on this bar, which never moved and which
`ptaril` still fails.) That is what makes this a satisfied bar rather than a
lowered one, and dom152.py and dom154.py have both been corrected in place to
say so rather than being left to contradict the build.

+3 values / 6 occurrences, 0 de-verified. Census after: modern dark 43,069 /
pale 1,364 / green 32 = **96.8605%** (from 96.8470%), 1,967 cards, 0 page
errors.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

GAIN = {"pkliwaq": 2, "skliwaq": 2, "spkliwaq": 2}

# The bar still doing its job. These five are one supporter on one fragment and
# no prefix or synonym reaches them. If they go dark, the widening this batch
# priced at six occurrences has been let loose on the rest of the dictionary.
COINCIDENCE = {
    "ptaril": 3, "ppungu": 2, "ssiyang": 2, "emppungu": 1,
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
    coin = pg.evaluate(SPANS, sorted(COINCIDENCE))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(coin, COINCIDENCE, "pale", "COINCIDENCE")

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43069:
    fail.append("census: dark fell to %d, below this batch's 43,069" % tally["dark"])
if pct < 96.6667:
    fail.append("census: dark fell back below 96.6667%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occ — the 發亮 sense, two supporters apiece"
      % (len(GAIN), sum(GAIN.values())))
print("COINCIDENCE %d values / %d occ still pale — the bar was met, not lowered"
      % (len(COINCIDENCE), sum(COINCIDENCE.values())))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
