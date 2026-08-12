# -*- coding: utf-8 -*-
"""What is on the live blocker list, and what has this informant already been
asked about it?

Three files meet here: `.scratch/b245/blocked.json` (the DOM, just harvested),
`.scratch/b243/published_qset.json` (the 46 rows the b243 sheet actually
published, keyed a1..a46 -> HIS token, HTML-escaped) and
`.scratch/b242/answers.json` (what came back). Prints a table, no card bodies.
"""
import html
import io
import json
import os
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.abspath(".")


def jload(p):
    return json.loads(io.open(os.path.join(H, p), encoding="utf-8").read())


rows = jload(".scratch/b245/blocked.json")
qset = jload(".scratch/b243/published_qset.json")
ASKED = set(html.unescape(v).lower() for v in qset.values())
try:
    ans = jload(".scratch/b242/answers.json")
except Exception as e:                                     # noqa: BLE001
    ans = {}
    print("answers.json unreadable: %s" % e)

pairs = Counter()
sole = Counter()
his = defaultdict(set)
for r in rows:
    for p in r["pale"]:
        pairs[p] += 1
        if len(r["pale"]) == 1:
            sole[p] += 1
    # his own token behind each pale value, span-position paired
    if r.get("aligned"):
        for (m, _c), (o, _c2) in zip(r["spans"], r["his"]):
            if m.lower() in r["pale"]:
                his[m.lower()].add(o.strip())

print("live blockers: %d pairs over %d pale types" % (len(rows), len(pairs)))
print("%-14s %5s %5s  %-22s %s" % ("value", "pairs", "sole", "his token(s)",
                                   "asked?"))
for v, n in sorted(pairs.items(), key=lambda kv: (-kv[1], kv[0])):
    hs = sorted(his.get(v, []))
    mark = "yes" if any(h.lower() in ASKED for h in hs) else "NO"
    print("%-14s %5d %5d  %-22s %s" % (v, n, sole[v], ",".join(hs)[:22], mark))

seen = set()
for v in pairs:
    for h in his.get(v, []):
        seen.add(h.lower())
print("\nhis tokens on live blockers: %d | of them already asked: %d | new: %d"
      % (len(seen), len(seen & ASKED), len(seen - ASKED)))
print("asked in b243 and NO LONGER blocking: %d"
      % len(ASKED - seen))
print("answers.json keys: %d" % len(ans))
