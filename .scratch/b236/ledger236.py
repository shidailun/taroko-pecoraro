# -*- coding: utf-8 -*-
"""Negative control for batch 236's seven ledger rows and the new `shape` kind.

Two things are being controlled, and they fail in different ways:

  * the KEY. A row whose key does not match the line the log actually prints
    is invisible -- the suite reports `no ledger row` and the failure stands.
    So the seven lines are fed in VERBATIM (dom221's reconstructed from its
    own source at :222, the rest as the suite printed them) and every one must
    find its row and be excused.

  * the REASON. A supersession must re-assert why the failure is expected, so
    each row is then tampered with in every way its kind can be wrong, and
    must REFUSE. Batch 234's pairing rule applies to the `None` ceilings: they
    mark the log's own PIN, which is source code and not a fact about the
    book, so moving one must NOT refuse -- and a leg that does not refuse is a
    claim about the world, so it is asserted explicitly rather than skipped.

    python .scratch/b236/ledger236.py
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.join("tools", "orthography"))
sys.stdout.reconfigure(encoding="utf-8")
import suite as S

MAP = S.load_map()
META = set(hw for hw, _ in S.meta_rows())

D221 = ('FAIL teumuk no longer renders anywhere. It was refused because '
        '首領 is bukung and thowlang, neither within reach of teumuk by '
        'any correspondence in the map -- if the map changed, the refusal '
        'needs re-arguing, not deleting.')
LIVE = [
    ('dom221.py', D221),
    ('dom232.py', 'FAIL FLOOR 5346 pairs, got 5347'),
    ('dom232.py', 'FAIL sole-blocked 79/67 pairs/types, got 78/66'),
    ('dom232.py', 'FAIL the sentence sweep returned 12 proposals, expected 13'),
    ('dom234.py', 'FAIL sole-blocker types 66, pinned 67'),
    ('dom235.py', 'FAIL sole-blocker types 66, pinned 67'),
    ('dom235.py', 'FAIL sole-blocked pairs 78, pinned 79'),
]

bad = 0


def check(tag, log, line, want_ok, mapover=None, verdrop=None):
    """want_ok True = the ledger must excuse it; False = it must refuse."""
    global bad
    M = dict(MAP)
    if mapover:
        M.update(mapover)
    real = S.load_ver
    if verdrop:
        v = set(real())
        v -= set(verdrop)
        S.load_ver = lambda _v=v: _v
    try:
        rec, why = S.adjudicate(log, line, M, META)
    finally:
        S.load_ver = real
    ok = (rec is not None) and (why == "")
    good = (ok == want_ok)
    bad = bad or (0 if good else 1)
    note = "excused" if ok else ("REFUSED: " + (why or "no ledger row"))
    print("  %-4s %-46s %s" % ("ok" if good else "BAD", tag, note[:78]))


print("1. the seven live lines must all find their row and be excused")
for log, line in LIVE:
    check(log.replace(".py", ""), log, line, True)

print("\n2. a key that does not match must be invisible (the failure mode)")
check("dom221 wording drifted", 'dom221.py', D221.replace("首領", "首长"), False)

print("\n3. shape: a measured count that RISES is news")
check("sole-blocked pairs rise", 'dom232.py',
      'FAIL sole-blocked 79/67 pairs/types, got 79/66', False)
check("sole-blocker types rise", 'dom234.py',
      'FAIL sole-blocker types 67, pinned 67', False)
check("sweep returns MORE", 'dom232.py',
      'FAIL the sentence sweep returned 14 proposals, expected 13', False)

print("\n4. ...and a count that falls FURTHER is the project working")
check("pairs fall further", 'dom235.py',
      'FAIL sole-blocked pairs 71, pinned 79', True)

print("\n5. the PAIRED legs: a None ceiling is the log's own pin, not a fact")
check("dom234 re-pins to 66", 'dom234.py',
      'FAIL sole-blocker types 66, pinned 66', True)
check("dom235 re-pins to 80", 'dom235.py',
      'FAIL sole-blocked pairs 78, pinned 80', True)

print("\n6. shape: the log's wording moving breaks the number alignment")
check("a third number appears", 'dom232.py',
      'FAIL sole-blocked 79/67 pairs/types, got 78/66/2', False)

print("\n7. every row dies if its RULING leaves the map")
for log, line in LIVE:
    check(log.replace(".py", "") + " map drift", log, line, False,
          mapover={"teumuk": "teumuk"})

print("\n8. ...or if the ruled value stops being verified")
for log, line in LIVE:
    want = (log == 'dom232.py' and line.startswith('FAIL FLOOR'))
    check(log.replace(".py", "") + " towmuk unverified", log, line, want,
          verdrop=["towmuk"])

print("\n9. floor: a NEW fall below batch 236's own floor")
check("metric falls to 5340", 'dom232.py', 'FAIL FLOOR 5346 pairs, got 5340',
      False)

print("\n%s" % ("all controls behaved" if not bad
                else "*** A CONTROL MISBEHAVED ***"))
sys.exit(bad)
