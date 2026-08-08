# -*- coding: utf-8 -*-
"""Every source's word on a candidate: the family, not a single gloss row
(batch 200/221). Counts too, for the >= 2 bar."""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORTH = os.path.join(ROOT, "tools", "orthography")

FILES = ["attested_gloss.json", "bible_gloss.json", "parquet_gloss.json",
         "edictionary_trv.json", "spoken_truku.json"]
SRC = {}
for f in FILES:
    p = os.path.join(ORTH, f)
    if os.path.exists(p):
        try:
            SRC[f.split("_")[0].split(".")[0]] = json.load(io.open(p, encoding="utf-8"))
        except Exception as e:
            print("skip %s (%s)" % (f, e))
AM = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"), encoding="utf-8")))


def show(w):
    print("  %-14s listed=%s" % (w, w in AM))
    for name, d in SRC.items():
        if not isinstance(d, dict) or w not in d:
            continue
        v = d[w]
        if isinstance(v, list):
            v = "/".join(str(x) for x in v)
        print("      %-12s %s" % (name, str(v)[:58]))


for w in sys.argv[1:]:
    show(w)
