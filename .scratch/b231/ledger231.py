# -*- coding: utf-8 -*-
"""Negative control for batch 231's LEDGER row, and for the widening of the
`ruled` handler that row needed.

The row supersedes dom219's written refusal of `isuka`, and the ruling that
overturns it emits a TWO-WORD map value -- his typewriter joined a pronoun to a
case marker. `attested()` splits on the space and takes the min over the parts,
so a membership test on the whole string alone would explain away a value that
renders PALE because one half of it is unverified. The handler now asserts the
whole key and every part; this file tampers with each.

A ledger that cannot fail is a list of excuses (batch 209).

    python .scratch/b231/ledger231.py
"""
import importlib.util
import sys

sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location("suite", "tools/orthography/suite.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

REAL = S.load_map()
VER = S.load_ver()
META = set(hw for hw, _ in S.meta_rows())
REAL_VER = S.load_ver

LOG = "dom219.py"
LINE = ("FAIL isuka no longer renders anywhere. It was refused because "
        "蓋住 is spuy, 覆蓋 is bbungan; different roots -- if the map changed, "
        "the refusal needs re-arguing, not deleting.")
OLD = ("dom216.py", "FAIL mtrgri no longer renders anywhere on the page. It "
       "was refused because tlgl and trgr are both empty in "
       "attested_modern.json -- if the transcription or the map changed, the "
       "refusal needs re-arguing, not deleting.")

bad = 0


def check(name, must_refuse, log, line, mp, ver=None):
    global bad
    S.load_ver = (lambda: ver) if ver is not None else REAL_VER
    try:
        rec, why = S.adjudicate(log, line, mp, META)
    finally:
        S.load_ver = REAL_VER
    good = bool(why) == must_refuse
    if not good:
        bad = 1
    print("%-4s %-56s %s" % ("ok" if good else "BAD", name,
                             (why or "explained")[:88]))


def less(d, *keys):
    d = dict(d)
    for k in keys:
        d.pop(k, None)
    return d


# --- the row is in the ledger at all, and keyed on the line dom219 really emits
inled = (LOG, LINE) in S.LEDGER
print("%-4s %-56s %s" % ("ok" if inled else "BAD", "the row is keyed on dom219's own FAIL line",
                         S.LEDGER.get((LOG, LINE))))
bad = bad or (0 if inled else 1)

# --- positive control
check("real map + real verified -- must be EXPLAINED", False, LOG, LINE, REAL)

# --- the ruling itself
check("ruling drifts to a third spelling", True, LOG, LINE,
      dict(REAL, isoka="isu kaa"))
check("ruling reverted to his own letters", True, LOG, LINE,
      dict(REAL, isoka="isuka"))
check("ruling re-joined into one word", True, LOG, LINE,
      dict(REAL, isoka="isuka"))
check("map entry deleted outright", True, LOG, LINE, less(REAL, "isoka"))

# --- the row cannot be borrowed
check("the same line from a log that never pinned it", True, "dom99.py", LINE,
      REAL)
check("the same shape about a different word", True, LOG,
      LINE.replace("isuka", "xisuka"), REAL)

# --- THE WIDENING. A two-word value pales if either half does.
check("the WHOLE key left verified.js", True, LOG, LINE, REAL,
      ver=less(VER, "isu ka"))
check("the part `isu` left verified.js", True, LOG, LINE, REAL,
      ver=less(VER, "isu"))
check("the part `ka` left verified.js", True, LOG, LINE, REAL,
      ver=less(VER, "ka"))
check("both parts present, whole present -- EXPLAINED", False, LOG, LINE, REAL,
      ver=dict(VER))

# --- the widening must not have broken the single-word rows it shares
check("a one-word ruled row still explains itself", False, OLD[0], OLD[1], REAL)
check("...and still refuses when its value goes unverified", True, OLD[0],
      OLD[1], REAL, ver=less(VER, "mtrgrig"))

# --- the three `map` rows for the KASAYANG ruling landing in the HOLD logs
KAS = "BROWN kasayang kasayang missing on [SLIYU]"
for log in ("dom57.py", "dom63.py", "dom67.py"):
    check("%s kasayang -- real map, EXPLAINED" % log[:6], False, log, KAS, REAL)
    check("%s kasayang -- ruling drifts" % log[:6], True, log, KAS,
          dict(REAL, kasayang="ka sayangg"))
    check("%s kasayang -- reverted to his own letters" % log[:6], True, log,
          KAS, dict(REAL, kasayang="kasayang"))
    check("%s kasayang -- map entry deleted" % log[:6], True, log, KAS,
          less(REAL, "kasayang"))
check("kasayang row cannot be borrowed by another log", True, "dom99.py", KAS,
      REAL)
check("kasayang row cannot be borrowed by another card", True, "dom57.py",
      KAS.replace("[SLIYU]", "[ZSLIYU]"), REAL)

# --- [batch 226/231] the three absorbed rows: kept in LEDGER, subtracted from
# the HEALED report, and still able to refuse if the failure ever comes back.
for k, tok, val in ((("dom57.py", "BROWN msnoxel msnoxel missing on [SNOXEL]"),
                     "msnoxel", "msneuhir"),
                    (("dom63.py", "BROWN pstui pstui missing on [SPONG]"),
                     "pstui", "pstutuy"),
                    (("dom66.py", "BROWN msnoxel msnoxel missing on [TAKOL]"),
                     "msnoxel", "msneuhir")):
    good = k in S.LEDGER and k in S.ABSORBED
    if not good:
        bad = 1
    print("%-4s %-56s ledger=%s absorbed=%s"
          % ("ok" if good else "BAD", "%s %s kept AND absorbed" % (k[0][:6], tok),
             k in S.LEDGER, k in S.ABSORBED))
    check("   ...and still refuses a reverted map", True, k[0], k[1],
          dict(REAL, **{tok: tok}))

print("\n%s" % ("all controls behaved" if not bad else "SOMETHING BEHAVED BADLY"))
sys.exit(bad)
