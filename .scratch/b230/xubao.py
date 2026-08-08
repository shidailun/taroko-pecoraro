# -*- coding: utf-8 -*-
"""XUBAO: is the u/i vowel a correspondence he has elsewhere, and is XUBAO even
his string? Batch 68 held this card because 'no bare form is attested'."""
import io
import json
import re
import sys
import collections

sys.stdout.reconfigure(encoding="utf-8")
O = "tools/orthography/"
ent = io.open("site/entries.js", encoding="utf-8").read()
E = json.loads(ent[ent.index("["):ent.rindex("]") + 1])
t = io.open("site/modern_map.js", encoding="utf-8").read()
_a = t.index("window.MODERN_MAP = {")
MM = dict(re.findall(r'^"(.+?)":"(.+?)",?$', t[_a:t.index("\n};", _a) + 2], re.M))
MJ = json.load(io.open(O + "modern_map.json", encoding="utf-8"))["map"]
AM = set(json.load(io.open(O + "attested_modern.json", encoding="utf-8")))

TOK = re.compile(r"[A-Za-zÇçÀ-ſ'’ʼ\"]+")
cnt = collections.Counter()


def walk(n):
    for k in ("hw", "form", "t", "paradigm"):
        v = n.get(k)
        for s in ([v] if isinstance(v, str) else (v or []) if isinstance(v, list) else []):
            for w in TOK.findall(s or ""):
                cnt[w.lower().replace("’", "'").replace("ʼ", "'")] += 1
    for x in (n.get("examples") or []):
        walk(x)
    for s in (n.get("subs") or []):
        walk(s)


for e in E:
    walk(e)

print("his book:  " + "  ".join(
    "%s x%d" % (w, cnt[w]) for w in sorted(cnt) if re.match(r"^x[n]?[uio]bao", w)))
print("map entries for those:")
for w in sorted(cnt):
    if re.match(r"^x[n]?[uio]bao|^xbag", w):
        m = MJ.get(w) or {}
        print("   %-10s -> %-10s tier %-3s %s   AM=%s"
              % (w, MM.get(w, "GREEN"), m.get("tier", ""), m.get("man", ""),
                 MM.get(w) in AM))

# his u  <->  modern i : count it over the whole map, first-syllable only
ui = same = 0
ex = []
for k, v in sorted(MM.items()):
    if len(k) < 3 or len(v) < 3:
        continue
    a = re.sub(r"['’ʼ\"]", "", k)
    if len(a) != len(v):
        continue
    diff = [i for i in range(len(a)) if a[i] != v[i]]
    if len(diff) == 1:
        i = diff[0]
        if a[i] == "u" and v[i] == "i":
            ui += 1
            if len(ex) < 8:
                ex.append("%s>%s" % (k, v))
        elif a[i] == "u" and v[i] == "u":
            same += 1
print("\nmap pairs differing in exactly one letter where his u -> modern i: %d" % ui)
print("   " + "  ".join(ex))
