"""Green tokens whose OWN CARD already tells us the modern root.

sl'dan is the shape. Its card S'LUT ships ms'lut>msdlut, ps'lut>psdlut and
s'lut>sdlut -- all three tier M, all human-checked -- and leaves the fourth key
green, when the omnibus holds sltan 被黏著, which is that root's -an form and his
gloss word for word. Nobody had to look anything up: the card had already decided.

That is the self-contradiction signature (pax/pnax, skawas/sxkawas,
mnswai/mnsuwai) pointed at greens instead of at wrong browns. So for every green
token: gather the shipped values of the OTHER keys on the same cards, reduce each
to a root by stripping the affixes Truku actually uses, and hunt the omnibus for a
word built on that root that is close to what charRules prints for his token.

The candidate is then a form of a root his own card has already accepted, which is
much stronger evidence than a string neighbour or a shared gloss bigram -- both of
which the last two sweeps showed to be mostly coincidence.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
MAP = {k: v["modern"] for k, v in MM.items()}
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)

MARKS = "['\u2019\u02bc\"\u0294]"
SM = {"x": "h", "o": "u", "l": "r"}


def cr(w):
    w = re.sub(MARKS, "", w).replace("\u0142", "l")
    w = re.sub(r"a[oO]$", "aw", w)
    return "".join(SM.get(c, c) for c in w)


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


# the affixes that actually appear on Truku verbs, longest first so mneg- is
# stripped before m-. Roots are what is left; a root under three letters is
# discarded because it matches everything.
PRE = ["empeg", "mneg", "pneg", "empe", "gmn", "smn", "tmn", "pnk", "psk", "snk",
       "emp", "mne", "pne", "kn", "sn", "tn", "pn", "mn", "gm", "sm", "tm", "km",
       "pk", "sk", "mk", "mq", "ms", "mt", "pt", "st", "gn", "ss", "pp", "dd",
       "m", "p", "s", "t", "k", "g", "d", "q", "n", "b", "h", "e"]
SUF = ["anay", "aneu", "un", "an", "ay", "ai", "aw", "i", "u", "a"]


def roots(v):
    """Every plausible root of a shipped value, best (longest) first."""
    out = {v}
    for p in PRE:
        if v.startswith(p) and len(v) - len(p) >= 3:
            out.add(v[len(p):])
    for r in list(out):
        for s in SUF:
            if r.endswith(s) and len(r) - len(s) >= 3:
                out.add(r[:-len(s)])
    # infixed <m>/<n> actor focus: smiling -> siling, tmaga -> taga
    for r in list(out):
        if len(r) > 3 and r[1] in "mn":
            out.add(r[0] + r[2:])
    return {r for r in out if len(r) >= 3}


TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub(MARKS, "'", w).replace("\u0142", "l").lower()


def clean(g):
    return re.sub(r"\s+", " ", g or "").strip()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])

# card -> the keys on it (headword, paradigm and sub forms only: an example
# sentence's other words belong to other cards, not to this one)
his = collections.defaultdict(list)
cardkeys = []
for ent in E:
    hw = ent.get("hw") or ""
    heads = [(ent.get("hw"), ent.get("zh"), "hw"),
             (ent.get("paradigm"), ent.get("zh"), "par")]
    heads += [(s.get("form"), s.get("zh") or ent.get("zh"), "sub")
              for s in ent.get("subs", [])]
    ks = []
    for f, g, kind in heads:
        for w in TOK.findall(f or ""):
            his[key(w)].append((clean(g), hw, kind))
            ks.append(key(w))
    for x in ent.get("examples", []):
        for w in TOK.findall(x.get("t") or ""):
            his[key(w)].append((clean(x.get("zh")), hw, "ex"))
    for s in ent.get("subs", []):
        for x in s.get("examples", []):
            for w in TOK.findall(x.get("t") or ""):
                his[key(w)].append((clean(x.get("zh")), hw, "ex"))
    cardkeys.append((hw, ks))

# green key -> the shipped values of its card-mates
mates = collections.defaultdict(set)
for hw, ks in cardkeys:
    vals = {MAP[k].lower() for k in ks if k in MAP}
    for k in ks:
        if k not in MAP and k not in LEX:
            mates[k] |= vals

BYROOT = collections.defaultdict(set)
for w in OMNI:
    for i in range(len(w) - 2):
        BYROOT[w[i:i + 4] if len(w) - i >= 4 else w[i:]].add(w)

MINSLOT = int(sys.argv[1]) if len(sys.argv) > 1 else 1
LO = int(sys.argv[2]) if len(sys.argv) > 2 else 0
HI = int(sys.argv[3]) if len(sys.argv) > 3 else 30
rows = []
for k, vals in mates.items():
    slots = his[k]
    if len(slots) < MINSLOT:
        continue
    target = cr(k)
    if len(target) < 4:
        continue
    rr = set()
    for v in vals:
        rr |= roots(v)
    cand = {}
    for r in rr:
        pool = BYROOT.get(r[:4]) if len(r) >= 4 else None
        for w in (pool or ()):
            if r not in w or w in vals:
                continue
            d = lev(target, w)
            if d > 3:
                continue
            if SPK.get(w, 0) < 1:
                continue
            if d < cand.get(w, (99,))[0]:
                cand[w] = (d, r)
    if not cand:
        continue
    best = sorted(cand.items(), key=lambda kv: (kv[1][0], -SPK.get(kv[0], 0)))
    rows.append((len(slots), k, target, best[:4], slots[0][1],
                 "; ".join(dict.fromkeys(g for g, _, kd in slots if kd != "ex" and g))[:58],
                 sorted(vals)[:5]))

rows.sort(key=lambda r: -r[0])
print("%d green tokens with a candidate built on a root their OWN CARD already "
      "ships (>=%d slots)\n" % (len(rows), MINSLOT))
for n, k, target, best, hw, gl, vals in rows[LO:HI]:
    print("%3dx [%-13s] %-13s prints %-13s %s" % (n, hw[:13], k, target.upper(), gl))
    print("      card ships %s" % ", ".join(vals))
    for w, (d, r) in best:
        print("      d%-2d %-13s spk %-5d root %-9s %s"
              % (d, w, SPK.get(w, 0), r, " | ".join(dict.fromkeys(OMNI[w]))[:44]))
