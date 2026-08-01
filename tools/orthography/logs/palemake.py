# -*- coding: utf-8 -*-
"""What is the pale 2,579 actually MADE OF?

linemate.py priced one proposal (his ° line as evidence) and got +298. That says
nothing about whether some OTHER rule reaches further. So decompose the measured
pale census instead: for every pale type on screen, which suffix slot is it, and
is its own root already dark?

The user's proposal in his words -- "put the -an -un for that word kgus and
similar in verified" -- is the LF/PF slice of this table, gated on the root
being dark. Report it as its own line.
"""
import io, json, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")

L = os.path.dirname(os.path.abspath(__file__))
H = os.path.normpath(os.path.join(L, "..", "..", ".."))
SITE = os.path.join(H, "site")

def read(p):
    return io.open(p, encoding="utf-8").read()

PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')

def table(app, name):
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

DARK, PALE, GREEN = 41854, 2579, 32
TOT = DARK + PALE + GREEN
print("pale types %d   pale occurrences %d (census %d)"
      % (len(pale), sum(pale.values()), PALE))
print("for 95%% we need +%.0f dark occurrences\n" % (0.95 * TOT - DARK))

# inflection.py's inventory, longest first.
SUF = [("aneyi", "imp"), ("anay", "imp"), ("ani", "imp"),
       ("un", "PF -un"), ("an", "LF -an"),
       ("ay", "imp"), ("aw", "imp"), ("i", "imp")]

def slot(w):
    for sf, name in SUF:
        if w.endswith(sf) and len(w) - len(sf) >= 3:
            return name, w[:-len(sf)]
    return "(other)", None

# -un / -an swallow a root-final vowel, so the root of `kgusan` may be `kgusa`
# just as easily as `kgus`. Try both, plus the m-/-m- actor form, and call the
# root dark if ANY of those readings is verified -- the generous direction, so a
# small number here is a real ceiling and not an artifact of my stemming.
def roots(stem):
    out = {stem}
    for vwl in "aeiou":
        out.add(stem + vwl)
    for s in list(out):
        out.add("m" + s)
        if len(s) > 1:
            out.add(s[0] + "m" + s[1:])
    return out

def dark(w):
    return w in VER

by = collections.Counter()
occ = collections.Counter()
reach_t, reach_o = collections.Counter(), collections.Counter()
examples = collections.defaultdict(list)
for w, n in pale.items():
    name, stem = slot(w)
    by[name] += 1
    occ[name] += n
    if stem and any(dark(r) for r in roots(stem)):
        reach_t[name] += 1
        reach_o[name] += n
        if len(examples[name]) < 6:
            r = sorted(r for r in roots(stem) if dark(r))
            examples[name].append((w, n, r[0]))

print("%-10s %6s %8s   %6s %8s" % ("slot", "types", "occ", "root-dark", "occ"))
seen = set()
for name in [s[1] for s in SUF] + ["(other)"]:
    if not by[name] or name in seen:
        continue
    seen.add(name)
    print("%-10s %6d %8d   %6d %8d"
          % (name, by[name], occ[name], reach_t[name], reach_o[name]))

lf_pf = reach_o["LF -an"] + reach_o["PF -un"]
imp = reach_o["imp"]
print()
print("his proposal, -an/-un off a dark root: %d types, %d occurrences  ->  %.4f%%"
      % (reach_t["LF -an"] + reach_t["PF -un"], lf_pf,
         100.0 * (DARK + lf_pf) / TOT))
print("adding the imperatives too:            %d types, %d occurrences  ->  %.4f%%"
      % (reach_t["LF -an"] + reach_t["PF -un"] + reach_t["imp"], lf_pf + imp,
         100.0 * (DARK + lf_pf + imp) / TOT))
print("every pale word, whatever the slot:    %d types, %d occurrences  ->  %.4f%%"
      % (len(pale), sum(pale.values()), 100.0 * (DARK + sum(pale.values())) / TOT))
print()
for name in ("LF -an", "PF -un"):
    print("%s samples:" % name)
    for w, n, r in examples[name]:
        print("   %-18s %4d   root %s" % (w, n, r))

# The 20 heaviest pale types overall -- whatever moves the ratio is in here.
print("\nheaviest pale types:")
for w, n in sorted(pale.items(), key=lambda kv: -kv[1])[:20]:
    print("   %-18s %4d   %s" % (w, n, slot(w)[0]))
