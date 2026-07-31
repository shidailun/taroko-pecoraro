"""green_rule with the correspondence table DERIVED rather than recalled.

derive_rules.py aligned the 1788 human-checked pairs already in the map and
counted what his spelling actually does. Most of it I had; these I did not, and
each is commoner in the checked pairs than rules I was already generating on:

    e -> i    115   (med 74, fin 41)      k -> q     59   and q -> k  13
    d -> j     46                         t -> c     28
    a -> e     29                         p -> k fin 10
    ' -> e/ee/h/u  131                    ye -> i    35   dya -> ji  9
    +e  113   +g fin 54   +y  42   +w 28  +u 16      +a  19

The insertions are why substitution-only expansion missed things: the modern word
often carries a vowel his transcription has no letter for at all. So this runs in
two passes. Pass 1 is the old one, substitutions only, and its hits are strong.
Pass 2 takes tokens pass 1 could not place and allows ONE further edit -- a single
inserted letter from the derived set, or one deleted medial vowel -- and requires
the landing to be a SPOKEN word, since one free edit is enough slack to reach a
lot of unattested strings by accident.

A pass-2 hit is a lead, not a finding. Same rule as glaqung: attestation plus a
regular correspondence is not enough by itself, the sentence decides.

Usage: python green_rule2.py [MINSLOT] [PASS: 1|2|12]
"""
import io, sys, json, pickle, re, collections, itertools
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
MARKS = "['\u2019\u02bc\"\u0294]"


def key(w):
    return re.sub(MARKS, "'", w).replace("\u0142", "l").lower()


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

ALT = {
    "x": ["h", "x"],
    "l": ["r", "l"],
    "o": ["u", "o", "w"],
    "n": ["n", "ng"],
    "y": ["y", "i"],
    "e": ["e", "i", ""],
    "a": ["a", "e"],
    "k": ["k", "q"],
    "q": ["q", "k"],
    "d": ["d", "j"],
    "t": ["t", "c"],
    "'": ["", "e", "u", "h"],
    "c": ["c", "s"],
}
INS = "eguywahiq"      # the derived insertion set, commonest first
CAP = 20000


def expand(tok):
    pools = [ALT.get(ch, [ch]) for ch in tok]
    n = 1
    for p in pools:
        n *= len(p)
    if n > CAP:
        return None
    out = set()
    for combo in itertools.product(*pools):
        s = "".join(combo)
        out.add(s)
        out.add(s + "g")          # the final velar he drops
        out.add(s + "q")
        if s.endswith("u"):
            out.add(s[:-1] + "aw")
    return out


MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 1
WHICH = sys.argv[2] if len(sys.argv) > 2 else "12"
greens = sorted({t for t in his if t not in MAP and len(his[t]) >= MIN and len(t) > 2},
                key=lambda t: -len(his[t]))
print("greens at >=%d slots: %d types" % (MIN, len(greens)))


def report(hits, title):
    print("\n======== %s: %d greens placed\n" % (title, len(hits)))
    for n, t, found in sorted(hits, reverse=True):
        hw, kind, g = his[t][0]
        print("%2dx %-14s [%-11s] %s" % (n, t, hw[:11], (g or "")[:56]))
        for s, c, how in found[:6]:
            print("        %-14s spk %-5d %-9s %s"
                  % (c, s, how, " | ".join(dict.fromkeys(OMNI[c]))[:48]))


p1, p2, skipped, base = [], [], [], {}
for t in greens:
    cands = expand(t)
    if cands is None:
        skipped.append(t)
        continue
    base[t] = cands
    found = [(SPK.get(c, 0), c, "sub") for c in cands if c in OMNI and c != t]
    if found:
        p1.append((len(his[t]), t, sorted(found, reverse=True)))

print("skipped (too many expansions): %d  %s" % (len(skipped), skipped[:8]))
if "1" in WHICH:
    report(p1, "PASS 1 -- substitutions only")

if "2" in WHICH:
    placed = {t for _, t, _ in p1}
    VOW = set("aeiou'")
    for t in greens:
        if t in placed or t not in base:
            continue
        found = {}
        for s in base[t]:
            for i in range(len(s) + 1):
                for ch in INS:
                    c = s[:i] + ch + s[i:]
                    if SPK.get(c, 0) >= 1 and c != t:
                        found.setdefault(c, "+" + ch)
            for i in range(1, len(s) - 1):
                if s[i] in VOW:
                    c = s[:i] + s[i + 1:]
                    if SPK.get(c, 0) >= 1 and c != t:
                        found.setdefault(c, "-" + s[i])
        if found:
            p2.append((len(his[t]), t,
                       sorted(((SPK.get(c, 0), c, h) for c, h in found.items()), reverse=True)))
    report(p2, "PASS 2 -- one further edit, spoken landings only")
