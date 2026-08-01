# -*- coding: utf-8 -*-
"""Does the positional read survive counting CELLS instead of tokens?

His ° line is a comma-separated list of slots, and a bracket inside one is his
second spelling of THAT slot -- `plqe (pl'qe)` is one slot written twice, not
two slots. Counting tokens therefore breaks the positional read on every line
carrying a variant, which is most of the ones currently unlabelled. `.?.` is a
slot he left blank and still holds its place.

Before widening the rule, re-measure the invariant parslot3.py measured on
tokens: of the 5-CELL lines, does cell 4 end in -an and cell 5 in -un/-on?
"""
import io, json, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")

H = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
s = io.open(os.path.join(H, "site", "entries.js"), encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])

TOK = re.compile(r"[A-Za-z'’ʼʔ\"çÇłöÖäÄ]+")
GAP = re.compile(r"\.\s*\?\s*\.")

def key(m):
    return re.sub(r"[’ʼʔ\"]", "'", m).lower().strip("'")

def cells(text):
    out, depth, pos = [], 0, 0
    for m in TOK.finditer(text or ""):
        pre = (text or "")[pos:m.start()]
        pos = m.end()
        for c in pre:
            if c in "([":
                depth += 1
            elif c in ")]" and depth:
                depth -= 1
        if GAP.search(pre):
            out.append([])
        k = key(m.group(0))
        if len(k) < 2 or not re.search(r"[a-z]", k):
            continue
        if depth > 0 and out:
            out[-1].append(k)
        else:
            out.append([k])
    return out

lines = []
for i, e in enumerate(E):
    if e.get("paradigm"):
        lines.append((e["hw"], e["paradigm"]))
    for sb in e.get("subs") or []:
        if sb.get("paradigm"):
            lines.append((sb.get("form"), sb["paradigm"]))

tk = collections.Counter(len([k for k in TOK.findall(l) if len(key(k)) >= 2]) for _, l in lines)
cn = collections.Counter(len(cells(l)) for _, l in lines)
print("° lines: %d" % len(lines))
print("by TOKEN count: %s" % ", ".join("%d->%d" % (k, tk[k]) for k in sorted(tk)))
print("by CELL  count: %s" % ", ".join("%d->%d" % (k, cn[k]) for k in sorted(cn)))
print()

five = [(h, l, cells(l)) for h, l in lines if len(cells(l)) == 5]
print("five-cell lines: %d  (was %d by token)" % (len(five), tk[5]))
p = [collections.Counter() for _ in range(5)]
test = [lambda w: True, lambda w: True,
        lambda w: re.search(r"[ie]$", w),
        lambda w: w.endswith("an"),
        lambda w: re.search(r"[uo]n$", w)]
bad = []
for h, l, c in five:
    ok = True
    for j in (2, 3, 4):
        if not c[j]:            # a blank he marked; it holds its place, claims nothing
            p[j]["(blank)"] += 1
            continue
        good = test[j](c[j][0])
        p[j]["ok" if good else "other"] += 1
        if not good:
            ok = False
    if not ok:
        bad.append((h, l))
for j, name in ((2, "cell 3 ends -i/-e   "), (3, "cell 4 ends -an     "), (4, "cell 5 ends -un/-on ")):
    print("   %s %s" % (name, dict(p[j])))
print("\nlines with a cell that does not fit: %d" % len(bad))
for h, l in bad[:25]:
    print("   %-20s %s" % (h, l.strip()[:78]))
