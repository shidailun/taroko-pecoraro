# -*- coding: utf-8 -*-
"""Negative control for the four LEDGER rows batch 230 added, and for the two
dom58 rows it moved to ABSORBED.

Batch 209's rule: a supersession must RE-ASSERT the reason, not excuse the
failure, and a ledger that cannot fail is a list of excuses. Kind `map` re-reads
modern_map.js, so the tamper is the map: drift the ruling to a third spelling,
revert it, or delete it, and the row must refuse.

Also asserts the ABSORBED pair is subtracted from the HEALED report while
staying IN the ledger (batch 226) — deleting them would destroy the record."""
import importlib.util
import sys

sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location("suite", "tools/orthography/suite.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

REAL = S.load_map()
META = set(hw for hw, _ in S.meta_rows())

NEW = [
    ("dom57.py", "BROWN snoxel snoxel missing on [SNOXEL]", "snoxel", "sneuhir"),
    ("dom57.py", "BROWN msnoxel msnoxel missing on [SNOXEL]", "msnoxel", "msneuhir"),
    ("dom63.py", "BROWN pstui pstui missing on [SPONG]", "pstui", "pstutuy"),
    ("dom66.py", "BROWN msnoxel msnoxel missing on [TAKOL]", "msnoxel", "msneuhir"),
]

bad = 0


def check(name, must_refuse, log, line, mp):
    global bad
    rec, why = S.adjudicate(log, line, mp, META)
    refused = bool(why)
    good = refused == must_refuse
    if not good:
        bad = 1
    print("%-4s %-62s %s" % ("ok" if good else "BAD", name, why or "explained"))


for log, line, tok, val in NEW:
    short = "%s %s" % (log[:6], tok)
    # positive control: the row explains its own failure against the real map
    check("%s -- real map, must be EXPLAINED" % short, False, log, line, dict(REAL))
    # the ruling drifts to a third spelling
    check("%s -- ruling drifts" % short, True, log, line,
          dict(REAL, **{tok: val[:-1] + "x"}))
    # the ruling is reverted to his own letters (the pin's own claim)
    check("%s -- ruling reverted to identity" % short, True, log, line,
          dict(REAL, **{tok: tok}))
    # the map entry is deleted outright
    gone = dict(REAL)
    gone.pop(tok)
    check("%s -- map entry deleted" % short, True, log, line, gone)
    # the same line from a log that never pinned it
    check("%s -- wrong log" % short, True, "dom99.py", line, dict(REAL))
    # the same word, a card the pin never named
    check("%s -- wrong card" % short, True, log,
          line.replace("missing on [", "missing on [Z"), dict(REAL))

# [batch 226] The two dom58 rows: absorbed, but NOT deleted.
for k in (("dom58.py", "BROWN n'gui nguy missing on [SLAP]"),
          ("dom58.py", "BROWN nagui nagui missing on [SLAP]")):
    inled, inabs = k in S.LEDGER, k in S.ABSORBED
    good = inled and inabs
    if not good:
        bad = 1
    print("%-4s %-62s ledger=%s absorbed=%s"
          % ("ok" if good else "BAD", "dom58 %s kept AND absorbed" % k[1].split()[1],
             inled, inabs))
    # and the row still re-asserts its reason if the failure comes back
    rec, why = S.adjudicate(k[0], k[1], dict(REAL, **{k[1].split()[1]: "nguy"}), META)
    good = bool(why)
    if not good:
        bad = 1
    print("%-4s %-62s %s" % ("ok" if good else "BAD",
                             "   ...and still refuses a reverted map", why or "explained"))

print("\nledger control %s" % ("PASSED" if not bad else "FAILED"))
sys.exit(bad)
