"""Every green token, with every modern word within two edits of what the reader
currently prints for it -- gloss and spoken count shown, no filtering.

audit6 asked the strict question (does an omnibus word MATCH his gloss?) and only
10 of the 272 green types produced any candidate at all. That is either the real
answer -- the modern dictionary does not contain these words -- or an artefact of
requiring a shared two-character word between two dictionaries written a century
apart in different registers. This script removes the gloss test entirely and
prints the neighbourhood, so the decision is made by reading rather than by
string overlap.

Ranked by occurrences, so it goes in order of frequency. A token with NO
neighbour at any distance is the interesting negative result: it means green is
where it is because the word is absent from modern Truku, not because nobody
looked.
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


def lev(a, b, cap=2):
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        if min(cur) > cap:
            return cap + 1
        prev = cur
    return prev[-1]


TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub(MARKS, "'", w).replace("\u0142", "l").lower()


def clean(g):
    return re.sub(r"\s+", " ", g or "").strip()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
his = collections.defaultdict(list)
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh"), "hw"),
             (ent.get("paradigm"), ent.get("zh"), "par")]
    slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh") or ent.get("zh"), "sub")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
    for f, g, kind in slots:
        for w in TOK.findall(f or ""):
            his[key(w)].append((clean(g), hw, kind))

BYLEN = collections.defaultdict(list)
for w in OMNI:
    BYLEN[len(w)].append(w)

MINSLOT = int(sys.argv[1]) if len(sys.argv) > 1 else 2
LO = int(sys.argv[2]) if len(sys.argv) > 2 else 0
HI = int(sys.argv[3]) if len(sys.argv) > 3 else 40
rows = []
for k, slots in his.items():
    if k in MAP or k in LEX or len(slots) < MINSLOT:
        continue
    target = cr(k)
    if len(target) < 3:
        continue
    near = []
    for L in range(len(target) - 2, len(target) + 3):
        for w in BYLEN.get(L, ()):
            d = lev(target, w, 2)
            if d <= 2:
                near.append((d, -SPK.get(w, 0), w))
    near.sort()
    gl = "; ".join(dict.fromkeys(g for g, _, kd in slots if kd != "ex" and g))
    rows.append((len(slots), k, target, near, slots[0][1], gl[:66]))

rows.sort(key=lambda r: -r[0])
none = [r for r in rows if not r[3]]
print("%d green types at >=%d slots; %d have NO modern word within two edits\n"
      % (len(rows), MINSLOT, len(none)))
for n, k, target, near, hw, gl in rows[LO:HI]:
    print("%3dx [%-14s] %-14s prints %-14s %s" % (n, hw[:14], k, target.upper(), gl))
    if not near:
        print("      -- nothing in the modern dictionary within two edits --")
    for d, ns, w in near[:4]:
        print("      d%d %-13s spk %-5d %s" % (d, w, -ns,
              " | ".join(dict.fromkeys(OMNI[w]))[:52]))
