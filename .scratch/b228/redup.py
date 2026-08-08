# -*- coding: utf-8 -*-
"""Which of the 65 `no root` blockers are only there because roots() is blind?

`inf.roots()` has no reduplication rule, so a doubled onset reports level 0
whatever the word is. That is a fact about the ANALYSER, not a verdict about the
word (standing rule). Bucket the class by shape before believing any of it:

  redup   C1C1- or C1VC1V- or VV-  -> roots() structurally cannot analyse it
  short   <= 4 letters             -> nothing to peel
  other   -> the level 0 is a real inventory miss

Then, for the redup bucket only, strip the doubled onset by hand and re-ask.
Summary lines only.
"""
import io
import os
import re
import sys
import collections

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORTH = os.path.join(ROOT, "tools", "orthography")
sys.path.insert(0, ORTH)

MD = io.open(os.path.join(ORTH, "logs", "blockers.md"), encoding="utf-8").read()
sec = MD[MD.index("## no root"):]
rows = re.findall(r"(\S+) \((\d+)\)", sec)
print("no-root class: %d types, %d pairs" % (len(rows), sum(int(n) for _, n in rows)))

V = "aeiou"


def shape(w):
    if len(w) <= 4:
        return "short"
    # C1C1-  (mm-, ss-, qq-, ll- ...)
    if w[0] not in V and w[1] == w[0]:
        return "redup"
    # C1VC1V- / C1VC1- : the onset consonant repeats across the first syllable
    if w[0] not in V and len(w) > 3:
        for i in (2, 3):
            if i < len(w) and w[i] == w[0] and w[1] in V:
                return "redup"
    # VV-
    if w[0] in V and w[1] == w[0]:
        return "redup"
    return "other"


B = collections.defaultdict(list)
for w, n in rows:
    B[shape(w)].append((w, int(n)))
for k in ("redup", "short", "other"):
    print("  %-6s %2d types  %2d pairs" % (k, len(B[k]), sum(n for _, n in B[k])))

# --- the redup bucket: strip the doubled onset by hand and re-ask roots()
try:
    import inflection as inf
except Exception as e:
    print("inflection import failed: %s" % e)
    sys.exit(0)

import json
AG = json.load(io.open(os.path.join(ORTH, "attested_gloss.json"), encoding="utf-8"))
AM = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"), encoding="utf-8")))


def strips(w):
    """Hand-undo the reduplication, several ways; return candidate bases."""
    out = set()
    if len(w) > 2 and w[1] == w[0]:
        out.add(w[1:])                      # mmteru -> mteru
    if len(w) > 3 and w[0] not in V and w[1] in V and len(w) > 2 and w[2] == w[0]:
        out.add(w[2:])                      # bibu- -> bu-
    if len(w) > 4 and w[0] not in V and w[1] in V and w[3:4] == w[0:1]:
        out.add(w[3:])
    if len(w) > 4 and w[:2] == w[2:4]:
        out.add(w[2:])                      # baba- -> ba-
    return {b for b in out if b and any(c in V for c in b)}


print("\nredup bucket, doubled onset stripped by hand:")
hits = 0
for w, n in sorted(B["redup"], key=lambda r: -r[1]):
    cands = []
    for b in sorted(strips(w)):
        if b in AM:
            g = AG.get(b) or []
            g = g if isinstance(g, list) else [g]
            cands.append("%s=%s" % (b, "/".join(g)[:26] or "(no gloss)"))
        else:
            try:
                r = inf.roots(b)
            except Exception:
                r = []
            if r:
                cands.append("%s~%s" % (b, r[0][0]))
    if cands:
        hits += 1
        print("  %-12s %d pair  %s" % (w, n, "  ".join(cands[:3])))
print("%d of %d redup types get a base the analyser could not reach" % (hits, len(B["redup"])))
