# -*- coding: utf-8 -*-
"""The four no-prior-mention rows: his card compactly, and the register family
around each candidate. Verdict material only -- no full card bodies."""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
O = "tools/orthography/"
AM = set(json.load(io.open(O + "attested_modern.json", encoding="utf-8")))
AG = json.load(io.open(O + "attested_gloss.json", encoding="utf-8"))
BG = json.load(io.open(O + "bible_gloss.json", encoding="utf-8"))
SPK = json.load(io.open(O + "spoken_truku.json", encoding="utf-8"))
ent = io.open("site/entries.js", encoding="utf-8").read()
E = json.loads(ent[ent.index("["):ent.rindex("]") + 1])
t = io.open("site/modern_map.js", encoding="utf-8").read()
_a = t.index("window.MODERN_MAP = {")
MM = dict(re.findall(r'^"(.+?)":"(.+?)",?$', t[_a:t.index("\n};", _a) + 2], re.M))


def L(x):
    return [] if x is None else (x if isinstance(x, list) else [x])


def gl(w):
    return "; ".join(L(AG.get(w)) + L(BG.get(w)))[:52]


def reg(pat):
    for w in sorted(w for w in set(AG) | set(BG) | AM if re.search(pat, w)):
        print("      %-12s spk%-4s %s%s" % (w, SPK.get(w, 0),
                                            "AM " if w in AM else "-- ", gl(w)))


def card(hw):
    for e in E:
        if (e.get("hw") or "").upper().startswith(hw):
            print("  [%s] %s %s | %s" % (e.get("hw"), e.get("tag") or "",
                                         (e.get("zh") or "")[:40],
                                         (e.get("fr") or "")[:44]))
            for x in e.get("examples", []):
                print("     §  %-42s %s" % ((x.get("t") or "")[:42],
                                            (x.get("zh") or x.get("fr") or "")[:34]))
            for s in e.get("subs", []):
                print("     %-16s %-22s %s" % (s.get("form"),
                                               (s.get("zh") or "")[:22],
                                               (s.get("fr") or "")[:30]))
                for x in s.get("examples", []):
                    print("        § %-40s %s" % ((x.get("t") or "")[:40],
                                                  (x.get("zh") or x.get("fr") or "")[:30]))


for hw, pat in [("XUBAO", r"^h[nb]?[ib]bag|^hn?[ib]baw|^hbag"),
                ("SAPAT", r"^m?s?sapa[ntg]"),
                ("MANU", r"^n?m?[sn]?[nm]anu$"),
                ("MOXONG", r"^[rtm]?m?uhu[gn]")]:
    print("======== %s" % hw)
    card(hw)
    print("    -- register:")
    reg(pat)
    print()
