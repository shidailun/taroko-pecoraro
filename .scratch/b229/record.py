# -*- coding: utf-8 -*-
"""Batch 221's cheapest cut, over the `other` bucket of the no-root class.

For every blocker type, grep the batch log, the notes and every dom*.py for a
prior mention. A type with a prior mention is already ruled or refused in
writing (batch 221: twelve of sixteen were); the ones with NO mention at all
are the batch. Costs one command.

The blocker is a map VALUE, not his token (batch 219), so reverse it first:
every map key sending to it, plus every raw token whose charRules() output is
it. Grep on the value AND on his tokens.

Summary lines only -- no card bodies.
"""
import collections
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORTH = os.path.join(ROOT, "tools", "orthography")
sys.path.insert(0, ORTH)

MD = io.open(os.path.join(ORTH, "logs", "blockers.md"), encoding="utf-8").read()
sec = MD[MD.index("## no root"):]
rows = [(w, int(n)) for w, n in re.findall(r"(\S+) \((\d+)\)", sec)]

V = "aeiou"


def shape(w):
    if len(w) <= 4:
        return "short"
    if w[0] not in V and w[1] == w[0]:
        return "redup"
    if w[0] not in V and len(w) > 3:
        for i in (2, 3):
            if i < len(w) and w[i] == w[0] and w[1] in V:
                return "redup"
    if w[0] in V and w[1] == w[0]:
        return "redup"
    return "other"


TARGET = [(w, n) for w, n in rows if shape(w) in ("other", "short")]
print("other+short: %d types  %d pairs" % (len(TARGET), sum(n for _, n in TARGET)))

# --- reverse the map values to his tokens -------------------------------------
t = io.open(os.path.join(ROOT, "site", "modern_map.js"), encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {")
MM = dict(re.findall(r'^"(.+?)":"(.+?)",?$', t[a:t.index("\n};", a) + 2], re.M))
REV = collections.defaultdict(set)
for k, v in MM.items():
    REV[v].add(k)


def char_rules(w):
    return w.replace("o", "u").replace("l", "r").replace("x", "h")


ent = io.open(os.path.join(ROOT, "site", "entries.js"), encoding="utf-8").read()
ent = json.loads(ent[ent.index("["):ent.rindex("]") + 1])
TOKENS = set()


def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("hw", "t", "form", "paradigm", "crossRef"):
                if isinstance(v, str):
                    TOKENS.update(re.findall(r"[^\s,.;:!?()\[\]«»\"]+", v.lower()))
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)


walk(ent)
for tok in TOKENS:
    REV[char_rules(tok)].add(tok)

# --- the record ---------------------------------------------------------------
FILES = sorted(glob.glob(os.path.join(ROOT, ".claude", "notes", "*.md"))) + \
        sorted(glob.glob(os.path.join(ORTH, "logs", "dom*.py"))) + \
        sorted(glob.glob(os.path.join(ORTH, "logs", "b*.py"))) + \
        [os.path.join(ORTH, "inflection.py"), os.path.join(ROOT, "CLAUDE.md")]
BLOB = {}
for p in FILES:
    try:
        BLOB[os.path.basename(p)] = io.open(p, encoding="utf-8", errors="ignore").read().lower()
    except Exception:
        pass

seen, virgin = [], []
for w, n in sorted(TARGET, key=lambda r: -r[1]):
    keys = sorted(REV.get(w, set()) | {w})
    where = set()
    for name, b in BLOB.items():
        for k in keys:
            if re.search(r"\b%s\b" % re.escape(k), b):
                where.add(name)
                break
    (seen if where else virgin).append((w, n, keys, sorted(where)))

print("with a prior mention: %d types  %d pairs"
      % (len(seen), sum(r[1] for r in seen)))
print("NO mention anywhere : %d types  %d pairs"
      % (len(virgin), sum(r[1] for r in virgin)))
print("\n-- unworked, by pairs --")
for w, n, keys, _ in virgin[:24]:
    print("  %-14s %d pair  his: %s" % (w, n, " ".join(keys[:5])[:56]))
