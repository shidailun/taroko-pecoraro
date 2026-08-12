# -*- coding: utf-8 -*-
"""Live figure sheet. Summary lines only -- no leaderboards."""
import io
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(
    __file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "orthography"))
import suite as S                                                # noqa: E402
import inflection as INF                                         # noqa: E402


def rd(*p):
    return io.open(os.path.join(ROOT, *p), encoding="utf-8").read()


MAP = S.load_map()
print("MAP keys                %d" % len(MAP))
print("MAP identity values     %d" % sum(1 for k, v in MAP.items() if k == v))
print("MAP two-word values     %d" % sum(1 for v in MAP.values() if " " in v))

v = rd("site", "verified.js")
codes = Counter(int(c) for c in re.findall(r'":\s*(\d+)', v))
print("VERIFIED keys           %d" % sum(codes.values()))
print("VERIFIED by code        %s" % dict(sorted(codes.items())))

e = rd("site", "entries.js")
data = json.loads(e[e.index("["):e.rindex("]") + 1])
subs = sum(len(x.get("subs", [])) for x in data)
ex = sum(len(x.get("examples", [])) for x in data) + sum(
    len(s.get("examples", [])) for x in data for s in x.get("subs", []))
ids = len(re.findall(r'"id":', e))
print("ENTRIES                 %d roots, %d subs, %d examples" %
      (len(data), subs, ex))
print("ENTRIES audio ids       %d" % ids)
print("ENTRIES (R)-tagged      %d" % sum(1 for x in data
                                         if "R" in (x.get("tag") or "")))

for nm in ("HAND_SPOKEN", "HAND_RULED", "HAND_NAMES", "HAND_LOANS",
           "HAND_ONOM", "HAND_SPECIES", "HAND_AFFIX"):
    t = getattr(INF, nm, None)
    if t is not None:
        print("%-23s %d" % (nm, len(t)))
for f in ("name_population.json", "loan_population.json", "manual_map.json",
          "lexical_map.json"):
    p = os.path.join(ROOT, "tools", "orthography", f)
    if os.path.exists(p):
        d = json.loads(io.open(p, encoding="utf-8").read())
        n = len(d) if isinstance(d, (dict, list)) else 0
        cm = sum(1 for k in d if str(k).startswith("_")) if isinstance(
            d, dict) else 0
        print("%-23s %d keys (%d comments)" % (f, n, cm))
