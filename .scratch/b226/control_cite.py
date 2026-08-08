# -*- coding: utf-8 -*-
"""Negative control for suite.py's new `cite` kind and for ABSORBED.

A ledger that cannot fail is a list of excuses (batch 209), so every half of
the new row is tampered with in turn and required to REFUSE. ABSORBED is
controlled too: it silences the HEALED report, and the one thing it must never
do is silence an explanation -- every key in it has to still be in LEDGER.
"""
import importlib.util
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = importlib.util.spec_from_file_location(
    "suite", os.path.join(ROOT, "tools", "orthography", "suite.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

LINE = "BROWN lidil        rijig        missing on [LIDIL]  green there: []"
LOG = "dom66.py"
REAL_CITE = m.load_cite
MAP = m.load_map()
META = m.meta_rows() if callable(getattr(m, "meta_rows", None)) else set()

results = []


def run(name, expect_ok, mp=None, cite=None, line=LINE, log=LOG):
    if cite is not None:
        m.load_cite = lambda: cite
    rec, err = m.adjudicate(log, line, mp if mp is not None else MAP, META)
    m.load_cite = REAL_CITE
    ok = (err == "") if expect_ok else bool(err)
    got = "explained" if err == "" else "refused (%s)" % err[:58]
    print("%-46s -> %s%s" % (name, got, "" if ok else "   <<< BAD"))
    results.append(ok)


# 1 -- untouched: the row must explain the failure
run("UNTOUCHED (positive control)", True)

# 2 -- the running-text half moves: the map no longer spells the handle
run("map drifts lidil -> rijil (senses re-merged)", False,
    mp=dict(MAP, lidil="rijil"))

# 3 -- the citation half is deleted from app.js
run("CITE_SPELL loses lidil", False, cite={k: v for k, v in REAL_CITE().items()
                                           if k != "lidil"})

# 4 -- the citation half is pointed at the running value: no seam left
run("CITE_SPELL['lidil'] becomes rijig", False,
    cite=dict(REAL_CITE(), lidil="rijig"))

# 5 -- an unrelated failure line must NOT be explained by this row
rec, err = m.adjudicate(LOG, "BROWN lidil rijig missing on [PALEX]", MAP, META)
ok = rec is None and err == "no ledger row"
print("%-46s -> %s%s" % ("a different card is not this row",
                         "no ledger row" if ok else "WRONGLY MATCHED",
                         "" if ok else "   <<< BAD"))
results.append(ok)

# 6 -- ABSORBED silences the HEALED report, never an explanation
orphan = sorted(k for k in m.ABSORBED if k not in m.LEDGER)
ok = not orphan
print("%-46s -> %s%s" % ("every ABSORBED key still has a LEDGER row",
                         "yes" if ok else "MISSING %s" % orphan,
                         "" if ok else "   <<< BAD"))
results.append(ok)

# 7 -- and it must still adjudicate one if it comes back
rec, err = m.adjudicate("dom65.py", "BROWN mqlaq mqraq missing on [QLAQ]",
                        MAP, META)
ok = rec is not None and err == ""
print("%-46s -> %s%s" % ("an ABSORBED failure returning is explained",
                         "explained" if ok else "UNEXPLAINED (%s)" % err[:40],
                         "" if ok else "   <<< BAD"))
results.append(ok)

print("\n%d of %d control cases behaved correctly" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
