# -*- coding: utf-8 -*-
"""Batch 147: the Truku Bible readers, and the decoder lexicon that was refused.

Two new bodies of Truku were found on this box and asked the one question `seen`
is allowed to ask — does this exact string occur in real modern Truku?

**Admitted: Kari Pnsdhgan Bgurah / Smudal** (新約選讀 / 舊約選讀), the Truku
scripture readers in bible-app. 56 paragraphs, 15,338 tokens, 2,058 types, 435 of
them new. It enters on the parquets' terms and for the opposite reason: the
parquets are gated at freq>=2 because an ASR hapax is as likely a mis-hearing as
a word, while these are edited and typeset, so a hapax here is a spelling
somebody stood behind. Still a text and not a wordlist — it widens `seen`, never
`lex`, so nothing in it becomes a root the analyser may cut a word onto.

**Two counting traps inside those files, both caught by reading the data.**
The paragraph records carry six parallel VERSIONS — tgdaya, truku, hh, xz, kjv,
gnb — so a walk over every string in the JSON returns 203,648 "Truku" tokens that
are mostly English and Chinese. It offered `put` (79x), `trap`, `nay` and `un` as
Truku words. Only `paragraphs[].text` is Truku, and it is 15,338 tokens: 7.5% of
what the naive walk reported. The other trap is the name — these are 選讀,
selections, not a Bible.

**Refused: the Kaldi decoder lexicon**, kaldi_formosan_250514_Truku/graph/
words.txt. 13,351 types, 2,040 of them new here, and it would have cleared 25
pale words. 1,918 of those 2,040 do not occur in the ILRDF parquets at all,
because it was built from a dirtier transcript set than the cleaned datasets, and
its new types read `alagn`, `alnag` and `aalng` for alang, with `amerika`,
`amerrika` and `amrika` side by side. **A decoding inventory is not an
attestation.** It is REQUIRED to hold every string the acoustic model might emit;
that is its job. Admitting it would have listed `alagn` as modern Truku.

**Already in, and checked rather than assumed.** dict_truku.json in the same
folder is 32,208 glossed Truku headwords and looks like a major find — it is
100.0% inside attested_modern.json already. Its 2,038-entry Bible companion
yielded exactly one new type. And the ILRDF Truku dialogues are all eight
datasets, ingested since batch 136 at 361,630 tokens; there was no ninth.

+11 values / 24 occurrences, 0 de-verified, 26 relevelled (all upward, into
`listed`, as new attestation should relevel). No rule changed, so no renumbering.

Census after: modern dark 42,714 / pale 1,719 / green 32 = **96.0621%** (from
96.0081%), original 43,190 / 1,740 / 32 = 96.0589%, 1,967 cards, 0 page errors in
both modes.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

GAIN = {"emphaal": 3, "mkrawah": 3, "pksyangun": 3, "smqdug": 3, "empsdhug": 2,
        "empshjil": 2, "emptduwa": 2, "krwahi": 2, "smpsaan": 2, "pksgun": 1,
        "ptreura": 1}

# The decoder lexicon's price, asserted unpaid. `tgbilaq`, `tgbhgay` and
# `tgbasi` are in Kaldi's words.txt and in neither the scripture readers nor any
# listed source; `put` and `un` are the English the multi-version walk offered.
# If any of these five ever goes dark, a bad source got in.
#
# `mskingal` WAS a sixth and is not any more. Batch 148's SYN reached it
# legitimately — regular() off `skingal`, agreeing 合而為一=專一 on the 單一 line
# — so it went dark for a reason that has nothing to do with Kaldi, and this
# assertion had been stale for a batch before batch 149 caught it. A pin that
# names one possible cause has to be retired when a second cause turns up;
# leaving it in would have made a real gain read as a contaminated source.
PIN = {"tgbilaq": 2, "tgbhgay": 1, "tgbasi": 1, "put": 1, "un": 2}

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
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 42714:
    fail.append("census: dark fell to %d, below this batch's 42,714" % tally["dark"])
if pct < 96.0:
    fail.append("census: dark fell back below 96%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN %d values / %d occurrences from the scripture readers"
      % (len(GAIN), sum(GAIN.values())))
print("PIN  %d still pale — the Kaldi decoder lexicon's price, unpaid" % len(PIN))
print("failures: %d" % len(fail))
for f in fail:
    print("   " + f)
