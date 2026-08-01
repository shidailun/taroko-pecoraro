# -*- coding: utf-8 -*-
"""The tie-break with the frozen populations taken back out.

Giving a contested token to the entry that heads it is right for TAMA 父親 and
wrong for MISO 味噌: his loan headwords are spelled like ordinary Truku words
(miso is also 'your'), which is the whole reason tier J is a pre-pass. So the
tie-break declines to fire for a loan or a name, exactly as tier W declines.
"""
import collections, io, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")

H = "C:/dev/formosan/seediq/taroko-pecoraro/"
TOK = re.compile(r"[A-Za-zÀ-ÿłŁʔ'’\"]+")
FROZEN = re.compile(r"emprunt|\(J|name\s*\(")
s = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])


def wkey(w):
    return w.lower().replace('"', "'").replace("\u2019", "'").replace("\u0142", "l")


def keys(t, out):
    for m in TOK.finditer(t or ""):
        k = wkey(m.group(0))
        if len(k) > 1:
            out[k] = 1
    return out


SENT, own, head = [], [], []
for i, e in enumerate(E):
    o = keys(e.get("paradigm"), keys(e.get("hw"), {}))
    h = set()
    if not FROZEN.search(e.get("tag") or ""):
        h = set(keys(e.get("hw"), {}))
    head.append(h)
    for x in e.get("examples", []):
        if x.get("t"):
            SENT.append((i, x["t"]))
    for sb in e.get("subs", []):
        keys(sb.get("form"), o)
        keys(sb.get("paradigm"), o)
        for x in sb.get("examples", []):
            if x.get("t"):
                SENT.append((i, x["t"]))
    own.append(o)

owners, heads = collections.defaultdict(set), collections.defaultdict(set)
for i, o in enumerate(own):
    for w in o:
        owners[w].add(i)
    for w in head[i]:
        heads[w].add(i)

idx = collections.defaultdict(set)
for n, (i, t) in enumerate(SENT):
    for w in keys(t, {}):
        idx[w].add(n)

mine = collections.defaultdict(set)
for n, (i, _) in enumerate(SENT):
    mine[i].add(n)

sizes = []
for i, e in enumerate(E):
    hit = set()
    for w in own[i]:
        if owners[w] == {i} or heads.get(w) == {i}:
            hit |= idx.get(w, set())
    sizes.append((len(hit - mine[i]), e.get("hw")))

n = [x for x, _ in sizes]
print("entries with a list: %d of %d   rows %d   max %d"
      % (sum(1 for x in n if x), len(n), sum(n), max(n)))
for c in (10, 40, 100, 500):
    print("  > %3d rows: %4d entries" % (c, sum(1 for x in n if x > c)))
print("\nlongest")
for c, hw in sorted(sizes, reverse=True)[:16]:
    print("  %5d  %s" % (c, hw))
print("\nMISO / KENSAT after the guard:")
for c, hw in sizes:
    if hw in ("MISO", "KENSAT", "TAMA", "MOBOX"):
        print("  %5d  %s" % (c, hw))
