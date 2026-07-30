"""Curated keys that match no token in entries.js -- and what they were aiming at.

The builder prints these as DEAD once per build and I had never read the line. A
dead key is not harmless: it is a word somebody adjudicated, wrote down, and still
sees green on the page, with manual_map.json recording the work as done. For each
one, find the live key by matching on the mark-free, diacritic-free shape.
"""
import json, io, sys, re, collections
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography")
import build_modern_map as B

H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"
tokens = B.load_corpus()[0]
manual = json.load(io.open(H + "manual_map.json", encoding="utf-8"))
llm = json.load(io.open(H + "llm_map.json", encoding="utf-8"))

# bare shape -> the keys the census actually holds
by_shape = collections.defaultdict(list)
for t in tokens:
    by_shape[B.norm(t)].append(t)

for name, tbl in (("manual", manual), ("llm", llm)):
    dead = [k for k, v in sorted(tbl.items())
            if v and not k.startswith("_") and k not in tokens]
    print("== %s: %d dead of %d" % (name, len(dead), len(tbl)))
    for k in dead:
        cand = [c for c in by_shape.get(B.norm(k), []) if c != k]
        print("  %-14s -> %-14s  live: %s"
              % (k, tbl[k], ", ".join("%s (%dx)" % (c, tokens[c])
                                      for c in sorted(cand)) or "NONE"))
