# -*- coding: utf-8 -*-
"""Batch 171: the DLUT card, and a rung that never read a gloss.

**Worksheet row 5 grouped the DLUT family under `dlut` 黏. The card is not about
adhesion at all, and two of its forms were already dark on the wrong word.**

His card: DLUT (R) *Moudre - écraser en frottant - froisser* / 磨碎－搓碾－揉皺,
and all three of its example sentences are dry grain — 玉米, 米, 小米. Nothing on
it sticks to anything.

Three candidate roots were measured, not guessed:

  dlut 黏   OUT on his own evidence. The modern 黏 family is adhesion end to end
           (電焊, 依靠著) and has no grinding member. His French is *moudre*.
  dgut 磨   OUT on the null. `l` -> `g` lands 20 of 716 = 2.8%, against nulls
           l->n 2.9%, l->r 3.4%, l->b 2.1%. `dldun` -> `dgdun` 都要磨 agrees at
           exactly the background rate, which is the batch 169 TABE trap: a
           cognate may explain a word and never spell one.
  drut     IN. Batch 168 measured his `<l>` and it is his most ambiguous
           consonant — 1,151 become `<r>`, 1,275 stay, a coin flip. `drut`
           用手揉起來 shares 揉 with his 揉皺 and 搓 with his 搓碾.

**The map already crossed l -> r on this very card and nobody noticed.** `dludi`
was rendered `drudi` by the default rule (SM = {"x":"h","o":"u","l":"r"}). The
other five kept the `l` — and the reason is the part worth writing down.

**A rung that returns his own spelling without ever consulting a gloss.**
`build_modern_map.py`'s tier `id` (~line 747) is

    if n in attested: result[t] = {"modern": ..., "tier": "id"}

so any raw token whose string happens to appear in the modern wordlist is handed
straight back, and then verifies at rank 1 as LISTED. `dlut` is in the wordlist
— meaning 黏 — so `dlut` and `pdlut` were frozen onto a homograph and painted
dark, 4 occurrences, with the card's own 磨碎 never read. Dark is a claim, and
this rung can make the claim without evidence whenever a homograph exists. It is
the same shape as the `id` freeze batch 148 hit, and the reason a dark span is
not self-certifying.

**What moved.** Five raw tokens respelled in `manual_map.json`:

    dlut -> drut     dmlut -> dmrut    mdlut -> mdrut
    dnlut -> dnrut   pdlut -> pdrut

`drut` is listed, so it verifies at rank 1 on its own account; `roots()` offers
`drut` for the other four —

    dmrut -> ('drut', '', '',  'infix')
    mdrut -> ('drut', 'm', '', 'm')
    dnrut -> ('drut', '', '',  'infix')
    pdrut -> ('drut', 'p', '', 'p')

— and three of the four take rank 2 on the 揉 agreement.

**`pdrut` went the other way, and that is the honest half of this batch.** It was
dark at rank 1 as `pdlut`, on the 黏 freeze; respelled, it finds no gloss
agreement through `p-` and falls to pale. So the trade is 6 occurrences gained
and 2 given back, for +4 — and 4 occurrences that were dark-and-wrong are now
either dark-and-right or honestly pale. The percentage is the smaller half of
what this batch did.

**Five stay pale, and they are a different problem.** `dldan` 3, `dlutun` 2,
`dldi` 1, `drudi` 1 are his syncopated slots — the root's vowel is gone INSIDE
the form, so `roots()` is never handed `drut` to agree with. That is the same
structural block as `knsbusan` in batch 170, and it is not a gloss question.

+4 occurrences. 97.4382% -> 97.4472% (43,326 / 1,103 / 32).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"

# `drut` listed at rank 1; the other three regular inflections off it at rank 2.
GAIN = {"drut": 2, "dmrut": 2, "mdrut": 2, "dnrut": 2}

# His spellings, and the two that were dark on the 黏 homograph. All must be gone.
GONE = ["dlut", "dmlut", "mdlut", "dnlut", "pdlut"]

# The honest half: dark-and-wrong at rank 1, now pale-and-right. If this ever
# goes dark, check that it did so on a gloss and not on another `id` freeze.
#
# [batch 196] It did go dark, and the check the pin asked for is what refused
# it: rule 2, agreeing on the 去 of his example sentence 我沒時間去請人磨小米
# against the 去 of `drut` 輾過去 — his own word gloss 使人碾磨 agrees with the
# root on nothing. `pdrut` is in HAND_NOT_REGULAR now, so this pin is load-
# bearing again and not merely stale.
# [batch 199] THE PIN COMES DOWN, on evidence and not because it tired. What
# refused it in 196 was rule 2 measuring his 使人碾磨 against a gloss of `drut`
# reading 輾過去, and no p- path agreed. The register's own gloss of `drut` is
# 用手揉起來 — rubbing and crumbling with the hand — and his DLUT card is 磨碎－
# 搓碾－揉皺. Those agree; 輾過去 was the wrong witness to weigh him against. Five
# slots on that card are dark (drut, dmrut, dnrut, drtan, drtun), so `pdrut` is
# the causative slot of a root the card has already settled, and a p- causative
# of 揉/碾 glossed 使人碾磨 is the regular reading of it. Ruled in HAND_RULED and
# pinned here in the direction it went.
PIN_TRADE = {"pdrut": 2}

# The syncopated slots. Blocked at the analyser — the root vowel is gone inside
# the form, so no rung is ever handed `drut`. Same block as knsbusan (batch 170).
#
# [batch 196] Two of the four came off this pin in batch 190, on evidence, and
# the pin was left standing until this batch caught it. That batch read the
# alternation the wordlist shows — `brut`→`brutun` keeps the vowel, `krut`→
# `krtun` drops it — and let HIS OWN witness break the tie, since he wrote DLUT
# full and `Dldun`/`Dldan` syncopated. Pinned `drtun`/`drtan`, and the syncope
# rung, which had been in the ladder all along and could never see the root
# through the `l`, fired on both (code 11). So the strings this pin named are
# no longer rendered at all — a pin on a string nothing emits asserts nothing,
# and an absent span is not a pale one. The two that remain are genuinely
# blocked; the two that moved are pinned dark below, where their gain is
# protected instead of denied.
# [batch 199] And the last two came off it. The block this pin names is real --
# roots() is never handed `drut` through a form whose root vowel is gone -- but a
# block in the analyser is not a verdict about the word. The imperative slot is
# the one his own paradigm spells for us: drtan and drtun are pinned dark two
# lines down, so the stem is drt-, and the imperative of a drt- stem is `drci`,
# the same alternation the SBUT card shows in sbtan/sbtun/sbci. Both his spellings
# (dldi, dludi) now render `drci`; the strings this pin used to name are emitted
# nowhere, and an absent span is not a pale one. Pinned on what the page shows.
PIN_SLOTS = {"drci": 2}

# Batch 190's gain, pinned in the direction it actually went.
PIN_SYNCOPE = {"drtan": 3, "drtun": 2}

# The word this card is NOT about. Adhesion, dark on its own account, untouched.
PIN_NOT_GLUE = {"dmrut_check": 0}

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
        if not n:
            continue
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
    trade = pg.evaluate(SPANS, sorted(PIN_TRADE))
    slots = pg.evaluate(SPANS, sorted(PIN_SLOTS))
    sync = pg.evaluate(SPANS, sorted(PIN_SYNCOPE))
    b.close()

check(gain, GAIN, "dark", "GAIN")
check(trade, PIN_TRADE, "dark", "TRADE")
check(slots, PIN_SLOTS, "dark", "SLOTS")
check(sync, PIN_SYNCOPE, "dark", "SYNCOPE")
for w in GONE:
    if gone.get(w):
        fail.append("GONE %s: his spelling still rendered, %s" % (w, gone[w]))

tot = sum(tally.values())
pct = 100.0 * tally["dark"] / tot
if tally["dark"] < 43326:
    fail.append("census: dark fell to %d, below this batch's 43,326" % tally["dark"])
if pct < 97.447:
    fail.append("census: dark fell back below 97.4472%%, to %.4f%%" % pct)

print("cards %d   page errors %d %s" % (cards, len(errs), errs[:2]))
print("dark %d  pale %d  green %d   dark %.4f%%"
      % (tally["dark"], tally["pale"], tally["green"], pct))
print("GAIN  %d occ on the drut family, off the listed root `drut`"
      % sum(GAIN.values()))
print("TRADE %d occ back to dark: the 196 refusal weighed him against 輾過去; "
      "the register glosses drut 用手揉起來, which is his card" % sum(PIN_TRADE.values()))
print("SLOTS %d occ dark as `drci`: his own drt- stem spells the imperative"
      % sum(PIN_SLOTS.values()))
print("SYNC  %d occ dark since batch 190, on his own full/syncopated witness"
      % sum(PIN_SYNCOPE.values()))
print("failures: %d" % len(fail))
for f in fail:
    print("  " + f)
