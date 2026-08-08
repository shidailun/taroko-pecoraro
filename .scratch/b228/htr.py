# -*- coding: utf-8 -*-
"""Every register word on a root, with its gloss and its sources. Summary only."""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORTH = os.path.join(ROOT, "tools", "orthography")
PAT = re.compile(sys.argv[1] if len(sys.argv) > 1 else "htr")

L = lambda n: json.load(io.open(os.path.join(ORTH, n), encoding="utf-8"))
AM = set(L("attested_modern.json"))
AG = L("attested_gloss.json")
SRC = {}
for n in ("bible_gloss.json", "parquet_gloss.json", "edictionary_trv.json"):
    p = os.path.join(ORTH, n)
    SRC[n[:3]] = L(n) if os.path.exists(p) else {}

hits = sorted(w for w in AM if PAT.search(w))
print("%d register words match /%s/" % (len(hits), PAT.pattern))
for w in hits:
    g = AG.get(w) or []
    g = g if isinstance(g, list) else [g]
    s = "".join(k[0] for k in sorted(SRC) if w in SRC[k])
    print("  %-14s %-3s %s" % (w, s or "-", "／".join(g)[:64]))
