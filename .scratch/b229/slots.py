# -*- coding: utf-8 -*-
"""One card's slots: his form -> what the map emits -> is that value attested.

The colour question is settled from verified.js + the map chain, and the DOM is
the authority (standing rule) -- this is the table-side view, used only to see
which siblings SPELL a letter. Names only, never a card body.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORTH = os.path.join(ROOT, "tools", "orthography")

AM = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"), encoding="utf-8")))
AG = json.load(io.open(os.path.join(ORTH, "attested_gloss.json"), encoding="utf-8"))
t = io.open(os.path.join(ROOT, "site", "modern_map.js"), encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {")
MM = dict(re.findall(r'^"(.+?)":"(.+?)",?$', t[a:t.index("\n};", a) + 2], re.M))
vt = io.open(os.path.join(ROOT, "site", "verified.js"), encoding="utf-8").read()
V = dict((m.group(1), m.group(2)) for m in re.finditer(r'^  "(.+?)": (\d+),?$', vt, re.M))
ent = io.open(os.path.join(ROOT, "site", "entries.js"), encoding="utf-8").read()
ENT = json.loads(ent[ent.index("["):ent.rindex("]") + 1])


def char_rules(w):
    return w.replace("o", "u").replace("l", "r").replace("x", "h")


def wordkey(w):
    return re.sub(r'[’ʼ"ʔ]', "'", w.lower()).replace("ł", "l")


def render(tok):
    k = wordkey(tok)
    v = MM.get(k)
    return (v, "map") if v else (char_rules(k), "char")


def gl(w):
    g = AG.get(w) or []
    g = g if isinstance(g, list) else [g]
    return "/".join(g)[:34]


PAT = sys.argv[1]
for e in ENT:
    if not re.search(PAT, e.get("hw") or "", re.I):
        continue
    print("\n== %s  %s | %s" % (e.get("hw"), (e.get("fr") or "")[:34],
                                (e.get("zh") or "")[:20]))
    forms = [(e.get("hw"), "HEAD")]
    for s in e.get("subs") or []:
        forms.append((s.get("form"), "sub"))
        if s.get("paradigm"):
            for p in re.split(r"[\s,;/]+", s["paradigm"]):
                if p:
                    forms.append((p, "para"))
    if e.get("paradigm"):
        for p in re.split(r"[\s,;/]+", e["paradigm"]):
            if p:
                forms.append((p, "para"))
    seen = set()
    for f, kind in forms:
        if not f or f.lower() in seen:
            continue
        seen.add(f.lower())
        v, how = render(f)
        code = V.get(v)
        print("  %-14s %-5s -> %-14s %-4s %s %s"
              % (f, kind, v, how, "code%s" % code if code else "PALE", gl(v)))
