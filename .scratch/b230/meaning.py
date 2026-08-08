# -*- coding: utf-8 -*-
"""Batch 230's meaning search, with the two misses this batch found fixed:
   (a) read BOTH gloss files -- batch 201 searched attested_gloss only;
   (b) search his gloss CHARACTER BY CHARACTER -- searching the string 嫉妒
       returns only the hkrig family, because the reachable root is glossed 忌妒.
Prints, per query character: how many register words carry it, and which of them
are reachable from his letters under an ESTABLISHED map correspondence."""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
O = "tools/orthography/"
AM = set(json.load(io.open(O + "attested_modern.json", encoding="utf-8")))
AG = json.load(io.open(O + "attested_gloss.json", encoding="utf-8"))
BG = json.load(io.open(O + "bible_gloss.json", encoding="utf-8"))
t = io.open("site/modern_map.js", encoding="utf-8").read()
_a = t.index("window.MODERN_MAP = {")
MM = dict(re.findall(r'^"(.+?)":"(.+?)",?$', t[_a:t.index("\n};", _a) + 2], re.M))

STOP = set("的了是不在有人和一二三個他她我你們也就都很")


def L(x):
    return [] if x is None else (x if isinstance(x, list) else [x])


def gl(w):
    return L(AG.get(w)) + L(BG.get(w))


POOL = sorted(set(AG) | set(BG))


def carriers(ch):
    return [w for w in POOL if any(ch in s for s in gl(w))]


def ed(a, b):
    p = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        c = [i]
        for j, cb in enumerate(b, 1):
            c.append(min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (ca != cb)))
        p = c
    return p[-1]


def main():
    tok, zh = sys.argv[1], sys.argv[2]
    print("=== %s   his: %s" % (tok, zh))
    for ch in sorted(set(zh)):
        if ch in STOP or not ("一" <= ch <= "鿿"):
            continue
        cs = carriers(ch)
        near = sorted(((ed(tok, w), w) for w in cs if w in AM))[:5]
        print("  %s  %3d carriers | nearest reachable: %s"
              % (ch, len(cs), " ".join("%s(%d)" % (w, d) for d, w in near)))


main()
