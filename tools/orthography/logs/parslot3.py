# -*- coding: utf-8 -*-
"""Is his ° line POSITIONAL?

`Madas, adas, d'si, d'san, d'sun` and `Mapa, apa, pai, paan, paon` are the same
five slots in the same order: AF, citation root, imperative, LF, PF. If that
holds across the book the label comes from the position and the suffix is only
a check -- which is what rescues the 641 syncopated tokens suffix-matching alone
could not reach.
"""
import io, json, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")

H = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
s = io.open(os.path.join(H, "site", "entries.js"), encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])

TOK = re.compile(r"[A-Za-z'’ʼʔ\"çÇłöÖäÄ]+")
def keys(t):
    out = []
    for m in TOK.findall(t or ""):
        k = re.sub(r"[’ʼʔ\"]", "'", m).lower().strip("'")
        if len(k) >= 2 and re.search(r"[a-z]", k):
            out.append(k)
    return out

lines = []
for i, e in enumerate(E):
    if e.get("paradigm"):
        lines.append((i, None, e["paradigm"]))
    for sb in e.get("subs") or []:
        if sb.get("paradigm"):
            lines.append((i, sb.get("form"), sb["paradigm"]))

n = collections.Counter(len(keys(l[2])) for l in lines)
print("° lines: %d" % len(lines))
print("token counts: %s" % ", ".join("%d→%d" % (k, n[k]) for k in sorted(n)))
print()

# For the 5-token lines, does slot 3 look like an imperative, 4 like -an, 5 -un?
five = [l for l in lines if len(keys(l[2])) == 5]
p3 = collections.Counter(); p4 = collections.Counter(); p5 = collections.Counter()
for _, _, l in five:
    t = keys(l)
    p3["-i/-e" if re.search(r"[ie]$", t[2]) else "other"] += 1
    p4["-an" if t[3].endswith("an") else "other"] += 1
    p5["-un/-on" if re.search(r"[uo]n$", t[4]) else "other"] += 1
print("of the %d five-token lines:" % len(five))
print("   slot 3 ends -i/-e      %s" % dict(p3))
print("   slot 4 ends -an        %s" % dict(p4))
print("   slot 5 ends -un/-on    %s" % dict(p5))
print()
print("the exceptions at slot 4/5:")
bad = [l for l in five if not keys(l[2])[3].endswith("an")
       or not re.search(r"[uo]n$", keys(l[2])[4])]
for i, form, l in bad[:20]:
    print("   %-22s %s" % (form or E[i]["hw"], l.strip()[:70]))
print("   ... %d in all" % len(bad))
