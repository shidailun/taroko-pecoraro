# -*- coding: utf-8 -*-
"""What would the ILRDF parquet corpus buy, at which believability bar?

`load_spoken()` in build_modern_map.py reads ILRDF_texts.xlsx — 272,150 tokens.
The parquet datasets those transcripts came from hold 361,630, and 2,172 of their
types are ones attested_modern.json has never seen. This scores every currently
PALE page value under three policies, counting PAGE OCCURRENCES, not types, and
including the knock-on: a new root makes its regular inflections verifiable too.
"""
import io, json, os, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..")))
from inflection import Inflection

ORTH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = os.path.normpath(os.path.join(ORTH, "..", "..", "site"))

lex0 = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"), encoding="utf-8")))
pq = json.load(io.open(os.path.join(ORTH, "parquet_truku_freq.json"), encoding="utf-8"))
pale = json.load(io.open(os.path.join(ORTH, "logs", "pale136.json"), encoding="utf-8"))

import re
m = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
a = m.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
mp = json.loads(m[a:m.index("\n};", a) + 2])

TESTS = [("regular", "regular"), ("vouched", "vouched"),
         ("vouched_root", "vouched_root"), ("sistered", "sistered"),
         ("syncopated", "syncopated"), ("chained", "chained")]


def verified(inf, lex, v):
    parts = v.split()
    if not parts:
        return False
    for p in parts:
        if p in lex:
            continue
        if any(getattr(inf, fn)(p) for _, fn in TESTS):
            continue
        return False
    return True


for bar in (None, 1, 2, 3):
    if bar is None:
        lex = lex0
        label = "baseline (no parquet)"
    else:
        add = {w for w, c in pq.items() if c >= bar and w not in lex0}
        lex = lex0 | add
        label = "parquet freq >= %d  (+%d types)" % (bar, len(add))
    inf = Inflection(lex, mp)
    gained = [(v, n) for v, n in pale.items() if verified(inf, lex, v)]
    print("%-34s  pale types cleared %4d   page occurrences %5d"
          % (label, len(gained), sum(n for _, n in gained)))
    if bar == 1:
        one = dict(gained)
    if bar == 2:
        two = dict(gained)

print("\n-- what freq>=1 buys over freq>=2 (the ASR-hapax question)")
extra = {v: n for v, n in one.items() if v not in two}
print("   %d more types, %d more page occurrences" % (len(extra), sum(extra.values())))
for v, n in sorted(extra.items(), key=lambda kv: -kv[1])[:20]:
    print("      page %4d  corpus %s  %s" % (n, pq.get(v, "via inflection"), v))

print("\n-- biggest wins at freq>=2")
for v, n in sorted(two.items(), key=lambda kv: -kv[1])[:25]:
    print("      page %4d  corpus %-4s %s" % (n, pq.get(v, "infl"), v))
