# -*- coding: utf-8 -*-
"""What would his ° LINE buy, as evidence rather than as a page?

sistered() (level 5) asks the modern WORDLIST for two sisters of the same stem
wearing other suffixes. His ° line makes a stronger and different statement: he
himself declares these five tokens are one word's slots. So where a line-mate is
already verified, the line is a witness the verifier has never read.

Priced against the real pale census (pale136.json, DOM-measured), because a
type-level count says nothing about the ratio on screen.
"""
import io, json, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")

L = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(L, ".."))
H = os.path.normpath(os.path.join(D, "..", ".."))
SITE = os.path.join(H, "site")

def read(p):
    return io.open(p, encoding="utf-8").read()

PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')

def table(app, name):
    # The tables carry comments, so parse the pairs rather than the object --
    # same reader build_verified.py uses.
    i = app.index("var %s = {" % name)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))

app = read(os.path.join(SITE, "app.js"))
ov = table(app, "WORD_OVERRIDES")
m = read(os.path.join(SITE, "modern_map.js"))
a = m.index("window.MODERN_MAP = {")
mp = json.loads(m[m.index("{", a):m.index("\n};", a) + 2])
v = read(os.path.join(SITE, "verified.js"))
VER = {k: int(n) for k, n in
       re.findall(r'"((?:[^"\\]|\\.)*)"\s*:\s*(\d+)', v[v.index("{"):])}
pale = json.load(io.open(os.path.join(L, "pale136.json"), encoding="utf-8"))

s = read(os.path.join(SITE, "entries.js"))
E = json.loads(s[s.index("["):s.rindex("]") + 1])

TOK = re.compile(r"[A-Za-z'’ʼʔ\"çÇłöÖäÄ]+")
def keys(t):
    out = []
    for mm in TOK.findall(t or ""):
        k = re.sub(r"[’ʼʔ\"]", "'", mm).lower().strip("'")
        if len(k) >= 2 and re.search(r"[a-z]", k):
            out.append(k)
    return out

def value(k):
    return ov.get(k) or mp.get(k)

lines = []
for e in E:
    for f in [e.get("paradigm")] + [sb.get("paradigm") for sb in e.get("subs") or []]:
        if f:
            lines.append(keys(f))

# A pale value is one a curated table proposes that verified.js does not carry.
def reachable(need):
    out = {}
    for line in lines:
        lvl = [(k, value(k), VER.get(value(k))) for k in line if value(k)]
        dark = [x for x in lvl if x[2] is not None and x[2] <= 2]
        for k, val, lv in lvl:
            if lv is not None:
                continue
            others = [x for x in dark if x[1] != val]
            if len(others) >= need:
                out.setdefault(val, (k, [x[1] for x in others[:3]]))
    return out

# The census denominator is every coloured span, green included -- batch 136
# measured dark 41,854 / pale 2,579 / green 32.
DARK, PALE, GREEN = 41854, 2579, 32
TOT = DARK + PALE + GREEN
print("° lines: %d" % len(lines))
print("baseline   dark %d / %d = %.4f%%" % (DARK, TOT, 100.0 * DARK / TOT))
print("for 95%% we need +%.0f dark occurrences\n" % (0.95 * TOT - DARK))

for need in (1, 2):
    r = reachable(need)
    occ = sum(pale.get(x, 0) for x in r)
    print(">= %d verified line-mates: %d types, %d pale occurrences  ->  %.4f%%"
          % (need, len(r), occ, 100.0 * (DARK + occ) / TOT))

r = reachable(2)
print("\ntop reachable, by pale occurrences:")
for val, (k, sis) in sorted(r.items(), key=lambda kv: -pale.get(kv[0], 0))[:20]:
    print("   %-16s %4d   his %-14s line-mates %s"
          % (val, pale.get(val, 0), k, ", ".join(sis)))
