# -*- coding: utf-8 -*-
"""[batch 233] Every parenthetical in every tag, split by batch 223's tag-shape
rule. A VARIANT names another spelling of the headword; a ROOT is one he posits
and marks R. Verdict counts only."""
import sys, io, json, re, importlib.util, collections
sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location("d", "tools/orthography/logs/dom232.py")
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
MM = M.modern_map(); AM = M.sources()[0]
src = io.open("site/entries.js", encoding="utf-8").read()
E = json.loads(src[src.index("["):src.rindex("]")+1])
ROOT = re.compile(r"(^|[\s(=-])R\.?(?=$|[\s)?=.-])")     # app.js:1222 verbatim
UPPER = re.compile(r"[A-ZÇ'\"’]{3,}")
def key(w):
    return re.sub("[’ʼ\"ʔ]", "'", w.lower()).replace("ł", "l")
def modern(w):
    return MM.get(key(w)) or M.char_rules(key(w))
def colour(w):
    v = modern(w)
    return "dark" if v in AM else ("pale" if key(w) in MM else "green")
cls = collections.Counter(); variants = []
for e in E:
    tag = e.get("tag") or ""
    hw = e.get("hw") or ""
    for seg in re.findall(r"\(([^()]*)\)", tag):
        toks = [t for t in UPPER.findall(seg) if t not in ("R", "VR")]
        if not toks:
            cls["no Truku word"] += 1; continue
        if ROOT.search(seg):
            cls["posited root (R. = X)"] += 1; continue
        cls["variant of the head"] += 1
        for t in toks:
            if key(t) == key(hw):
                continue
            variants.append((hw, seg.strip(), t, modern(hw), modern(t),
                             colour(hw), colour(t)))
print("parentheticals:", dict(cls))
print("\n-- variant-shape parentheticals whose two sides differ in COLOUR")
n = 0
for hw, seg, t, mh, mt, ch, ct in variants:
    if ch != ct:
        n += 1
        print("%-12s (%-16s %-10s->%-10s %-5s | head %-10s %s"
              % (hw, seg[:16] + ")", t, mt, ct, mh, ch))
print("rows:", n, "of", len(variants), "variant tokens")
