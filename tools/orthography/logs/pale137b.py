# -*- coding: utf-8 -*-
"""How much of the pale mass is a spelling we never actually changed?

The colour is a claim about a RESPELLING: dark means a modern source confirms the
value we print, pale means it does not. But if the value we print is his own word
with nothing done to it, there is no respelling to confirm or doubt -- the reader
is looking at Pecoraro, and the pale wash says "we are unsure of this" about a
string we did not touch.

So: for every pale type on screen, find the token(s) that produced it and ask how
far the value moved. `identical` = same letters as his token once his diacritics
and elision marks are dropped (norm()); `case only`; `near-universal only` = the
conversions the project treats as automatic (o>u, x>h, ai>ay, ao>aw, final e>i)
and nothing else; `real change` = anything more.

If the first three are a large share, the ratio is not measuring what it claims.
"""
import io, json, os, re, sys, collections, unicodedata
sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ORTH = os.path.dirname(HERE)


def norm(w):
    w = (w or "").replace("ç", "x").replace("Ç", "X")
    w = unicodedata.normalize("NFD", w)
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    w = w.lower().replace("ł", "l").replace("ʔ", "")
    for ch in ("'", "’", "ʼ", "-"):
        w = w.replace(ch, "")
    return re.sub(r"[^a-z]", "", w)


def universal(n):
    """His token after only the conversions the project calls near-universal."""
    w = n.replace("o", "u").replace("x", "h")
    for src, dst in (("ai", "ay"), ("ae", "ay"), ("ao", "aw")):
        if w.endswith(src):
            w = w[: -len(src)] + dst
            break
    else:
        if w.endswith("e"):
            w = w[:-1] + "i"
    return w


pale = json.load(io.open(os.path.join(HERE, "pale137.json"), encoding="utf-8"))
mp = json.load(io.open(os.path.join(ORTH, "modern_map.json"),
                       encoding="utf-8"))["map"]

# modern value -> the tokens of his that produce it
src = collections.defaultdict(list)
for t, rec in mp.items():
    src[rec["modern"].lower()].append((t, rec["tier"]))

buckets = collections.Counter()
occ = collections.Counter()
show = collections.defaultdict(list)
for v, n in sorted(pale.items(), key=lambda kv: -kv[1]):
    toks = src.get(v, [])
    if not toks:
        k, tier = "not in map", "?"
        best = ""
    else:
        # If ANY of his tokens reaches this value untouched, the value is his.
        tier = "/".join(sorted({t[1] for t in toks}))
        k = "real change"
        best = toks[0][0]
        for t, _ in toks:
            nt = norm(t)
            if nt == v:
                k, best = "identical", t
                break
            if universal(nt) == v and k != "identical":
                k, best = "near-universal only", t
    buckets[k] += 1
    occ[k] += n
    if len(show[k]) < 18:
        show[k].append((n, v, best, tier))

tot = sum(pale.values())
print("pale types %d   occurrences %d\n" % (len(pale), tot))
print("%-20s %6s %8s %8s" % ("how far it moved", "types", "occ", "share"))
for k, v in occ.most_common():
    print("%-20s %6d %8d   %5.1f%%" % (k, buckets[k], v, 100.0 * v / tot))
print()
for k in ("identical", "near-universal only", "real change", "not in map"):
    if not show[k]:
        continue
    print("--- %s ---" % k)
    for n, v, t, tier in show[k]:
        print("   %-16s %4d   from %-16s tier %s" % (v, n, t, tier))
    print()
