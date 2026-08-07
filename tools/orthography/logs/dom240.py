# -*- coding: utf-8 -*-
"""batch 240 — the collision class, swept whole and closed at zero.

Batch 239 found one freeze by hand: his QBOLONG 蚱蜢 and his KBOLONG 收割 both
landed on `qburung` 收割, so the grasshopper card rendered dark and wrong. That
is a SHAPE, not an incident, and the shape had never been swept. `collide240.py`
sweeps it: two of his single-word cards on one map value, the register glossing
that value, the gloss agreeing with one card and sharing nothing with the other.

**0 pairs.** The metric HOLDS. Nothing was ruled. The sweep flags 41 rows over
1,967 entries and every one falls in a class already closed in writing:

  20  the SAME headword carded twice — batch 205 refuses the remap (a
      token-keyed map cannot split two senses of one string, and a remap paints
      his correct sentences wrong), and batch 222 measured that whole queue at
      **0 pale**, so it moves the metric by zero in any case.
  15  his OWN cross-reference or variant note — 參見, 見, 「會不會是…的變體」,
      「syn. = SAKOL」, 「更正確的寫法」. He says on the page that the two cards
      are one word; there is no disagreement to adjudicate.
   4  tier-J loans, and they are CORRECT — his BALAS 礫石 (バラス), KASI 餅乾
      (菓子), XANA 花, XAYA 汽車 (ハイヤー) against native `balas`, `kasi`,
      `hana`, `haya`. Batch 204: a modern homophone is not a freeze.
   2  leftovers, both refused below.

So batch 239's was the only freeze of its shape in the book. That is a NEGATIVE
RESULT and it is kept as one — `collide240.py` has the standing of
`freezesweep.py`, `tail221.py` and `premise231.py`; don't rebuild it.

1. The two leftovers, refused by naming the form whose OWN gloss carries his
   character (batch 221)
------------------------------------------------------------------------------
**`tucing`** — his TOTING 鐵鎚 beside his TÖTING 掉落. `wordKey()` folds only
`’ ʼ " ʔ → '` and `ł → l` (batch 219), so the diaeresis survives and the map
COULD send the two heads to different values. It must not: bare `tucing` is
glossed 掉下來, which is the TÖTING sense, AND `tmucing` 敲打、鎚 is built on
that same root and carries his hammer. The negative half stated as a property of
the carriers rather than as a list (batch 229): `tmucing` is the register's
**sole** carrier of 鎚/槌 anywhere, so there is no rival root to respell toward.
Both senses are the register's own; the collision is the language's.

**`qnilaw`** — his KNILAO / QNILAO 豬食. Bare `qnilaw` is glossed 煮爛的食物 and
the register's only two carriers of 豬食 are `tmqnilaw` 煮豬食的人 and
`smqnilaw` 很需要豬食, both spelling that stem whole. Same shape, same verdict.

2. The instrument is controlled from the DATA side, in both directions
------------------------------------------------------------------------------
An empty sweep and a broken sweep have the same output (batch 232), so pinning
`found == 0` proves nothing about the instrument. Both legs run here, offline,
on every suite pass:

* **positive** — drop batch 239's `qbolong → qbolong` identity pin and the char
  rules put his QBOLONG back on `qburung`. The sweep recovers it unaided, as a
  42nd row and a THIRD unclassified leftover.
* **blinded** — hand it an empty register and it recovers nothing at all: 0
  flagged, every collision reported as unjudgeable rather than banked as
  agreement (batch 200).

The control found a defect in the sweep itself, which is the whole reason for
running one. `build_stoplist()` fell back to `ranked[:30], 30` when it could not
reproduce the characters it was asked for — and it WAS falling back, because 我
ranks 368th of 2,780 in the register's glosses and 你 300th, so the line
"depth 30 (reproduces every named noise character)" was false. Two fixes: the
failure now returns depth **0** rather than a plausible number (batch 233's rule
one level down — never let a fallback be mistaken for a derivation), and NAMED
is restricted to the noise characters the project named over REGISTER glosses,
which resolves honestly at 37. 我/你 come from 我的 / 你們的, which are SENTENCE
glosses of batch 221's, and requiring them here would set the cut past 300.

And the stoplist turns out to be **inert in this instrument**: 41 rows at depth
10, at 30 and at 37 alike, because the rarity gate (carriers <= 120) is strictly
stronger — anything in the top 37 by document frequency has hundreds of carriers
and is gone already. Batch 232 requires the amount to be measured rather than
assumed, and here the amount is zero. It is kept, and pinned as inert, so that a
change making it load-bearing is visible.

3. What this log fires on
------------------------------------------------------------------------------
`NEW, unclassified` is the news. A row reaching LEFTOVER that is not one of the
two refused above is a collision no standing refusal covers — a freeze arriving
from a map change elsewhere, painting one of his cards dark and wrong. The class
counts are pinned beside it so that a re-triage is forced rather than assumed
when the shape of the 41 moves.

This log needs no browser: the collision is decided by `entries.js`, the map and
the register, and batch 222's measurement already says the whole twice-carded
queue is 0 pale — so nothing here can move a colour the DOM would show.

    python tools/orthography/logs/dom240.py
"""
import collections
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import collide240 as C                                          # noqa: E402

ORTH = os.path.dirname(HERE)

# ---- the pins -------------------------------------------------------------
COLLIDING = 211                   # map values serving 2+ of his one-word cards
DEPTH = 37                        # batch 232's derived stoplist, at its depth
STOP_RANGE = (10, 37)             # ...and what it is WORTH: nothing, see below
UNJUDGEABLE = 24                  # the register glosses the value nowhere
FLAGGED = 41
CLASSES = {"same headword carded twice (batch 205/222)": 20,
           "his own cross-ref / variant note": 15,
           "tier-J loan, and correct (batch 204)": 4,
           "LEFTOVER": 2}

# section 1 -- the two refusals
TUCING = ("tucing", "掉下來")      # the SERVED sense: his TÖTING 掉落
HAMMER = ("tmucing", "鎚")         # the form whose own gloss carries his TOTING
HAMMER_CHARS = "鎚槌"              # ...and it is the register's sole carrier
QNILAW = ("qnilaw", "煮爛的食物")
PIGFOOD = ("tmqnilaw", "smqnilaw")
PIGFOOD_CHARS = "豬食"

# section 2 -- the control, which needs batch 239's ruling to still be there
PIN = ("qbolong", "qbolong")
FREEZE = "qburung"
RECOVERS = ["KBOLONG", "QBOLONG"]

fails = []


def ck(cond, msg):
    if not cond:
        fails.append(msg)
    return cond


def carriers(G, chars):
    return sorted(w for w in G
                  if any(c in " ".join(G[w]) for c in chars))


def main():
    E, MM, G = C.entries(), C.modern_map(), C.register()
    colliding, depth, unjudgeable, rows = C.sweep(E, MM, G)
    cnt, left = C.classify(rows, E)

    print("COLLIDE %d values | depth %d | unjudgeable %d | FLAGGED %d"
          % (colliding, depth, len(unjudgeable), len(rows)))
    ck(colliding == COLLIDING,
       "map values serving 2+ of his single-word cards: %d, pinned %d: the "
       "universe this sweep covers has changed and the 41 need re-triaging"
       % (colliding, COLLIDING))
    ck(depth == DEPTH,
       "the derived stoplist now cuts at %d, pinned %d: batch 232 sets that "
       "depth by what the derivation must reproduce, so a move re-scores every "
       "row" % (depth, DEPTH))
    lo, hi = STOP_RANGE
    inert = {len(C.sweep(E, MM, G, depth=x)[3]) for x in (lo, 30, hi)}
    ck(inert == {FLAGGED},
       "the stoplist has stopped being inert: flagged counts %s across depths "
       "%s, where all three were %d. Batch 232 requires the amount to be "
       "measured; if the cut now moves rows, the rarity gate has stopped "
       "subsuming it and every row needs re-scoring."
       % (sorted(inert), [lo, 30, hi], FLAGGED))
    ck(len(unjudgeable) == UNJUDGEABLE,
       "unjudgeable rows %d, pinned %d: the register has started or stopped "
       "glossing a colliding value" % (len(unjudgeable), UNJUDGEABLE))
    ck(len(rows) == FLAGGED, "FLAGGED %d, pinned %d" % (len(rows), FLAGGED))

    # --- the classification, and the one row that is news -------------------
    for k, n in sorted(CLASSES.items()):
        ck(cnt.get(k, 0) == n, "class %r holds %d rows, pinned %d: the four "
                               "classes are what make this sweep a closed "
                               "negative result, so re-triage before believing "
                               "it" % (k, cnt.get(k, 0), n))
    news = [h for _, h in left if h not in C.KNOWN_LEFTOVERS]
    print("LEFTOVERS %s | NEW %s"
          % (", ".join("/".join(h) for _, h in left), news or "none"))
    ck(not news,
       "FAIL a NEW collision has appeared that none of the four closed classes "
       "accounts for: %s. Two of his cards are on one map value, the register "
       "agrees with one and shares nothing with the other, and no standing "
       "refusal covers it — this is batch 239's shape, which paints a card "
       "dark AND wrong. Read it before pinning it."
       % "; ".join("/".join(h) for h in news))
    ck(sorted(h for _, h in left) == sorted(C.KNOWN_LEFTOVERS),
       "a refused leftover has left the flagged set (%s, pinned %s): the two "
       "refusals below were written against those rows"
       % ([h for _, h in left], C.KNOWN_LEFTOVERS))

    # --- section 1: both refusals, positive half and negative half ----------
    for w, zh in (TUCING, QNILAW):
        ck(any(zh in g for g in G.get(w, [])),
           "FAIL %s lost its %s gloss. The refusal rests on the bare value "
           "carrying the SERVED card's sense; if it has moved, the collision "
           "is no longer between two senses the register owns." % (w, zh))
    w, zh = HAMMER
    ck(any(zh in g for g in G.get(w, [])),
       "FAIL %s lost its %s gloss — the form whose own gloss carries his "
       "TOTING 鐵鎚 (batch 221). Without it the hammer sense has no carrier "
       "on his root and the refusal has to be re-argued." % (w, zh))
    hc = carriers(G, HAMMER_CHARS)
    ck(hc == [w],
       "FAIL the register's carriers of %s are now %s, pinned [%s]. The "
       "negative half of the refusal is that no OTHER root carries his hammer; "
       "a second carrier is a rival root and re-opens the row."
       % (HAMMER_CHARS, hc[:4], w))
    pc = carriers(G, [PIGFOOD_CHARS])
    ck(sorted(pc) == sorted(PIGFOOD),
       "FAIL the register's carriers of %s are now %s, pinned %s. Both pinned "
       "forms spell his stem whole, which is what refuses the KNILAO/QNILAO "
       "row; a carrier off another root re-opens it."
       % (PIGFOOD_CHARS, pc[:4], list(PIGFOOD)))
    ck(all(re.sub(r"^[a-z]m", "", x).startswith(QNILAW[0]) for x in pc),
       "FAIL a %s carrier no longer spells his stem whole: %s"
       % (PIGFOOD_CHARS, pc[:4]))

    # --- section 2: the control, both directions ----------------------------
    k, v = PIN
    ck(MM.get(k) == v,
       "batch 239's %s → %s identity pin is gone (now %s): the positive "
       "control below reconstructs the pre-239 state by DELETING it, so "
       "without the pin the leg no longer tests anything"
       % (k, v, MM.get(k)))
    pre = {a: b for a, b in MM.items() if a != k}
    _, _, _, rows2 = C.sweep(E, pre, G)
    _, left2 = C.classify(rows2, E)
    got = [h for _, h in left2 if h not in C.KNOWN_LEFTOVERS]
    print("CONTROL pre-239 recovers %s | blinded register ..." % (got or "NOTHING"))
    ck(got == [RECOVERS],
       "the positive control FAILED: fed the pre-239 map the sweep recovers %s "
       "instead of %s. It must find the freeze batch 239 found by hand, or a "
       "zero over the book today is a broken sweep and not an empty one "
       "(batch 232)." % (got, [RECOVERS]))
    ck(C.value("QBOLONG", pre) == FREEZE,
       "with the pin deleted his QBOLONG no longer char-rules to %s: the "
       "pre-239 state the control reconstructs was that collision" % FREEZE)

    _, _, unj3, rows3 = C.sweep(E, MM, collections.defaultdict(list))
    print("CONTROL blinded flags %d, unjudgeable %d" % (len(rows3), len(unj3)))
    ck(not rows3,
       "the blinded control FAILED: with an empty register the sweep still "
       "flags %d rows. Agreement is supposed to be scored against the "
       "register's own gloss and nothing else." % len(rows3))
    ck(len(unj3) >= len(rows) + len(unjudgeable),
       "the blinded control did not report its collisions as unjudgeable "
       "(%d): a value with no gloss row must never be scored as disagreement "
       "(batch 200)" % len(unj3))

    for f in fails:
        print("FAIL " + f if not f.startswith("FAIL") else f)
    print("\n%d assertions failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
