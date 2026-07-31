"""The derived table applied as REWRITES, so the multi-character rules can fire.

green_rule2 expanded per character, which can express x>h but not ye>i, 'lo>ru,
lye>ri or dya>ji -- and those are not marginal: 'lo>ru is counted 26 times in the
shipped pairs, ye>i 35, '>ee 40. A per-character table simply cannot see them, so
every green whose spelling turns on one was unreachable no matter how many
single-letter rules I added.

So: derive the rule table from the human-checked pairs (as derive_rules.py does),
keep every rule counted at least MINCOUNT, and search from each green by applying
one rule at a time -- breadth-first, bounded by depth and by set size. A landing
counts only if it is attested. Depth is the honest knob here: depth 1 is "one
correspondence away", depth 5 is "his spelling and theirs differ in five places",
which real pairs do (s'lno>srngaw needs four). The cost is that deep landings are
weak evidence, so the depth is printed beside every hit and the sentence still
decides.

Positional rules are anchored: a rule counted only word-finally is applied only
word-finally. That matters -- the velar he drops is a word-end rule and would
generate nonsense as a general one.

Usage: python green_rule3.py [MINSLOT] [DEPTH] [MINCOUNT]
"""
import io, sys, json, pickle, re, collections, difflib
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
MAP = {k: v["modern"] for k, v in MM.items()}
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")
HUMAN = {"M", "J", "N", "C-review", "A"}


def key(w):
    return re.sub("['\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


def norm(w):
    return re.sub(r"[^a-z']", "", w.lower())


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
his = collections.defaultdict(list)
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh"), "hw")]
    slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh") or ent.get("zh"), "sub")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
    for f, g, kind in slots:
        for w in TOK.findall(f or ""):
            his[key(w)].append((hw, kind, g))

# ---- derive the table from the human-checked pairs, exactly as derive_rules does
counts = collections.Counter()
for k, v in MM.items():
    if v["tier"] not in HUMAN or not v["modern"]:
        continue
    a, b = norm(k), norm(v["modern"])
    if not a or not b or a == b:
        continue
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        pos = "init" if i1 == 0 else ("fin" if i2 >= len(a) else "med")
        if tag == "replace" and (i2 - i1) == (j2 - j1):
            for n in range(i2 - i1):
                p = ("init" if i1 + n == 0 else
                     ("fin" if i1 + n == len(a) - 1 else "med"))
                counts[(a[i1 + n], b[j1 + n], p)] += 1
        elif tag == "replace":
            counts[(a[i1:i2], b[j1:j2], pos)] += 1
        elif tag == "insert":
            counts[("", b[j1:j2], pos)] += 1
        else:
            counts[(a[i1:i2], "", pos)] += 1

MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 1
DEPTH = int(sys.argv[2]) if len(sys.argv) > 2 else 4
MINCOUNT = int(sys.argv[3]) if len(sys.argv) > 3 else 8
RULES = [(a, b, p, n) for (a, b, p), n in counts.items() if n >= MINCOUNT]
RULES.sort(key=lambda r: -r[3])
print("rules derived at count >= %d: %d   (depth %d)" % (MINCOUNT, len(RULES), DEPTH))
print("   " + "  ".join("%s>%s/%s:%d" % r for r in RULES[:18]))

CAP = 40000


def step(s):
    """Every string one derived rule away from s."""
    out = set()
    for a, b, p, _ in RULES:
        if a == "":                       # insertion
            spots = ([0] if p == "init" else
                     [len(s)] if p == "fin" else range(1, len(s)))
            for i in spots:
                out.add(s[:i] + b + s[i:])
            continue
        start = 0
        while True:
            i = s.find(a, start)
            if i < 0:
                break
            start = i + 1
            if p == "init" and i != 0:
                continue
            if p == "fin" and i + len(a) != len(s):
                continue
            out.add(s[:i] + b + s[i + len(a):])
    return out


def search(tok):
    seen = {tok: 0}
    frontier = {tok}
    for d in range(1, DEPTH + 1):
        nxt = set()
        for s in frontier:
            for t in step(s):
                if t not in seen:
                    seen[t] = d
                    nxt.add(t)
        frontier = nxt
        if len(seen) > CAP:
            return seen, True
    return seen, False


greens = sorted({t for t in his if t not in MAP and len(his[t]) >= MIN and len(t) > 2},
                key=lambda t: -len(his[t]))
print("greens at >=%d slots: %d types\n" % (MIN, len(greens)))

hits, blown = [], 0
for t in greens:
    seen, over = search(t)
    if over:
        blown += 1
    found = [(SPK.get(c, 0), c, d) for c, d in seen.items()
             if c != t and (c in OMNI or SPK.get(c, 0) >= 1)]
    if found:
        hits.append((len(his[t]), t, sorted(found, key=lambda f: (f[2], -f[0]))))

print("blew the cap: %d      greens with an attested landing: %d\n" % (blown, len(hits)))
for n, t, found in sorted(hits, reverse=True):
    hw, kind, g = his[t][0]
    print("%2dx %-14s [%-11s] %s" % (n, t, hw[:11], (g or "")[:56]))
    for s, c, d in found[:5]:
        print("      d%d %-14s spk %-5d %s"
              % (d, c, s, " | ".join(dict.fromkeys(OMNI.get(c, ["(unglossed)"])))[:46]))
