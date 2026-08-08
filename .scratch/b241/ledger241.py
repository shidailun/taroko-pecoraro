# -*- coding: utf-8 -*-
"""Negative control for batch 241's ten ledger rows and the new `grew` kind.

Same two things are controlled as in `ledger236.py`, and they fail differently:

  * the KEY. A row whose key does not match the line the log actually prints is
    INVISIBLE -- the suite reports `no ledger row` and the failure stands, which
    reads on screen exactly like a row that was never needed. So every line here
    is the one `.scratch/b241/keys.txt` captured from the log itself, verbatim,
    and each must find its row and be excused.

  * the REASON. A supersession must re-assert why the failure is expected, so
    each row is tampered with in every way its kind can be wrong and must
    REFUSE. Batch 234's pairing rule governs the `None` entries: they mark the
    LOG'S OWN PIN, which is source code and not a fact about the book, so moving
    one must NOT refuse -- and a leg that does not refuse is a claim about the
    world, asserted here rather than skipped.

`grew` is `shape` mirrored, so it gets the mirrored controls: a FALL refuses, a
further RISE is excused, and the None entries stay inert. Writing it as a sign
convention inside `shape` would have made the direction implicit in the wording;
it is declared by the row instead, and these legs are what hold that apart.

    python .scratch/b241/ledger241.py
"""
import os
import sys

sys.path.insert(0, os.path.join("tools", "orthography"))
sys.stdout.reconfigure(encoding="utf-8")
import suite as S                                                # noqa: E402

MAP = S.load_map()
META = set(hw for hw, _ in S.meta_rows())

D217 = ("FAIL thiy renders 1 time(s) and NONE is pale. It was refused because "
        "his Txey sits on the XNUK 軟／便宜 card, not on TOXOI; thiyan "
        "和…在一起 is TOXOI's word and following it would cross two cards")
D230 = ("FAIL snuk no longer renders pale; a refused word going dark is a "
        "ruling nobody wrote")
D232 = "FAIL the spellcheck sweep returned 39 shapes, expected 40"
D235A = "FAIL two-type blocked pairs 3, pinned 4"
D235B = ("FAIL a two-type cluster this batch pinned has left the book "
         "(snuk+thiy): batch 230 confirmed all four as refusals, so one "
         "healing is news")
D236 = ("FAIL the two-type seam moved: 3 rows, [('dmtbasyaq', 'dmtsapat'), "
        "('krikut', 'nrikut'), ('tbasyaq', 'tibasyaq')]. Batch 230 confirmed "
        "all four refusals; a NEW row of this shape is a pair the sole-blocker "
        "ranking cannot see.")
D238A = "FAIL VERIFIED keys 6327, pinned 6326"
D238B = ("FAIL pairs moved to 5348 — both rulings are furniture and buy 0 BY "
         "CONSTRUCTION (batch 223); a change here means one of them reached a "
         "`.truku` box and the pricing was wrong")
D239A = "FAIL VERIFIED keys 6327, pinned 6326"
D239B = "FAIL book-wide pale TYPES 135, pinned 137"

LIVE = [
    ('dom217.py', D217), ('dom230.py', D230), ('dom232.py', D232),
    ('dom235.py', D235A), ('dom235.py', D235B), ('dom236.py', D236),
    ('dom238.py', D238A), ('dom238.py', D238B),
    ('dom239.py', D239A), ('dom239.py', D239B),
]
# Which ruling each row is credited to. dom230's is the ODD one: its blocker
# left the book through a transcription correction, so the row is credited to
# the corrected reading `smuk -> smuk` and dies if THAT goes pale, not if
# `txey` moves.
CREDIT = dict((line, ('smuk', 'smuk') if line is D230 else ('txey', 'thiy'))
              for _log, line in LIVE)

bad = 0


def check(tag, log, line, want_ok, mapover=None, verdrop=None):
    """want_ok True = the ledger must excuse it; False = it must refuse."""
    global bad
    M = dict(MAP)
    if mapover:
        M.update(mapover)
    real = S.load_ver
    if verdrop:
        v = dict(real())
        for k in verdrop:
            v.pop(k, None)
        S.load_ver = lambda _v=v: _v
    try:
        rec, why = S.adjudicate(log, line, M, META)
    finally:
        S.load_ver = real
    ok = (rec is not None) and (why == "")
    good = (ok == want_ok)
    bad = bad or (0 if good else 1)
    note = "excused" if ok else ("REFUSED: " + (why or "no ledger row"))
    print("  %-4s %-52s %s" % ("ok" if good else "BAD", tag, note[:74]))


def short(log, line):
    return "%s %s" % (log.replace(".py", ""), line[5:40].strip())


print("1. the ten live lines must all find their row and be excused")
for log, line in LIVE:
    check(short(log, line), log, line, True)

print("\n2. a key that does not match is INVISIBLE -- the failure mode")
check("dom217 gloss re-typed", 'dom217.py', D217.replace("軟／便宜", "軟/便宜"),
      False)
check("dom230 wording drifted", 'dom230.py', D230.replace("nobody", "no one"),
      False)
check("dom236 a cluster changes -> new key, reported", 'dom236.py',
      D236.replace("'krikut'", "'zzzkut'"), False)

print("\n3. shape: a measured count that RISES is news")
check("two-type pairs rise to 5", 'dom235.py',
      "FAIL two-type blocked pairs 5, pinned 4", False)
check("pale TYPES rise to 140", 'dom239.py',
      "FAIL book-wide pale TYPES 140, pinned 137", False)
check("spellcheck returns MORE shapes", 'dom232.py',
      "FAIL the spellcheck sweep returned 41 shapes, expected 40", False)
check("the seam gains a row", 'dom236.py', D236.replace(": 3 rows", ": 4 rows"),
      False)

print("\n4. ...and a count that falls FURTHER is the project working")
check("two-type pairs fall to 0", 'dom235.py',
      "FAIL two-type blocked pairs 0, pinned 4", True)
check("pale TYPES fall to 120", 'dom239.py',
      "FAIL book-wide pale TYPES 120, pinned 137", True)

print("\n5. grew: a FALL is news -- the mirrored leg")
check("verified LOSES a key (dom238)", 'dom238.py',
      "FAIL VERIFIED keys 6326, pinned 6326", False)
check("verified LOSES a key (dom239)", 'dom239.py',
      "FAIL VERIFIED keys 6300, pinned 6326", False)
check("the metric FALLS", 'dom238.py', D238B.replace("to 5348", "to 5340"),
      False)

print("\n6. ...and a further RISE is the project working")
check("verified grows to 6400", 'dom238.py',
      "FAIL VERIFIED keys 6400, pinned 6326", True)
check("the metric rises to 5360", 'dom238.py',
      D238B.replace("to 5348", "to 5360"), True)

print("\n7. the PAIRED legs: a None entry is the log's own pin, not a fact")
check("dom235 re-pins its own 4 to 9", 'dom235.py',
      "FAIL two-type blocked pairs 3, pinned 9", True)
check("dom239 re-pins its own 137 to 200", 'dom239.py',
      "FAIL book-wide pale TYPES 135, pinned 200", True)
check("dom238 re-pins VER_KEYS to 6000", 'dom238.py',
      "FAIL VERIFIED keys 6327, pinned 6000", True)
check("dom235B cites a different batch", 'dom235.py',
      D235B.replace("batch 230", "batch 999"), True)
check("dom238B cites a different batch", 'dom238.py',
      D238B.replace("batch 223", "batch 999"), True)
check("dom236 cites a different batch", 'dom236.py',
      D236.replace("Batch 230", "Batch 999"), True)

print("\n8. the wording moving breaks the number alignment")
check("a third number appears (shape)", 'dom235.py',
      "FAIL two-type blocked pairs 3, pinned 4, over 2 cards", False)
check("a number vanishes (grew)", 'dom238.py',
      "FAIL VERIFIED keys 6327, pinned six thousand", False)

print("\n9. every row dies if the ruling leaves the map")
for log, line in LIVE:
    tok, val = CREDIT[line]
    check(short(log, line) + " map drift", log, line, False,
          mapover={tok: "zzz"})

print("\n10. ...or if the ruled value stops being verified")
for log, line in LIVE:
    tok, val = CREDIT[line]
    check(short(log, line) + " unverified", log, line, False, verdrop=[val])

print("\n11. PAIRED: moving the OTHER ruling must not excuse or refuse it")
#  dom230's row is credited to `smuk`, every other row to `txey`. If the two
#  were confused, one of these legs would refuse -- which is the check that the
#  credit column above is doing any work at all.
check("dom230 survives txey moving", 'dom230.py', D230, True,
      mapover={"txey": "zzz"})
check("dom217 survives smuk moving", 'dom217.py', D217, True,
      mapover={"smuk": "zzz"})

print("\n%s" % ("all controls behaved" if not bad
                else "*** A CONTROL MISBEHAVED ***"))
sys.exit(bad)
