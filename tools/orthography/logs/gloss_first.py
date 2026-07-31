"""GLOSS-FIRST. The inverse of green_rule3, and the instrument this review has
been missing for seventy batches.

Every sweep so far has gone shape-first: take his token, generate strings that
look like it, keep the ones that are attested, then read the gloss to decide.
That can only find a word whose SHAPE is reachable, and it fails exactly where
his transcription is worst -- the m read as n, the run-together words, the
letters he had no key for. It also cannot be told to look for a meaning.

This goes the other way. For each green token, take the Chinese gloss of the
slot it stands in, pull out every 2-4 character run, and ask the modern
dictionary which words are glossed with that meaning. Then -- and only then --
score the candidates by how far his spelling is from theirs. The shape is used
to RANK, never to generate, so a candidate can survive a spelling his rules do
not cover, which is precisely the case a shape sweep must miss.

The gloss of a green token is imprecise -- it is the gloss of the whole slot,
not of that one word, and for a headword slot it is the gloss of the card. That
imprecision is the point: a sentence gloss contains the meaning of its verb
somewhere, and the ranking sorts out where.

Scoring: character overlap of the normalised forms (a cheap proxy for
reachability, deliberately looser than the rule table) plus a bonus when the
first letters agree, since his initial consonant is the letter he was most
likely to get right. Spoken frequency breaks ties.

Usage: python gloss_first.py [MINSLOT] [TOPN]
"""
import io, sys, json, pickle, re, collections
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

# gloss substring -> modern words carrying it
BYGLOSS = collections.defaultdict(set)
for w, gs in OMNI.items():
    for g in gs:
        for run in re.findall(r"[\u4e00-\u9fff]+", g):
            for n in (4, 3, 2):
                for i in range(len(run) - n + 1):
                    BYGLOSS[run[i:i + n]].add(w)

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("['\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


# his spelling folded toward theirs, loosely -- this is a RANKING aid, not a rule
SM = {"x": "h", "o": "u", "l": "r", "e": "i", "k": "q", "d": "j", "t": "c"}


def fold(w):
    w = re.sub("['\u2019\u02bc\"\u0294]", "", w.lower())
    return "".join(SM.get(c, c) for c in w)


def sim(a, b):
    fa, fb = fold(a), fold(b)
    ca, cb = collections.Counter(fa), collections.Counter(fb)
    common = sum((ca & cb).values())
    s = 2.0 * common / (len(fa) + len(fb))
    if fa[:1] == fb[:1]:
        s += 0.15
    if fa[-1:] == fb[-1:]:
        s += 0.05
    return s


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

MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 1
TOPN = int(sys.argv[2]) if len(sys.argv) > 2 else 4
greens = sorted({t for t in his if t not in MAP and len(his[t]) >= MIN and len(t) > 2},
                key=lambda t: -len(his[t]))
print("greens at >=%d slots: %d types" % (MIN, len(greens)))
print("gloss index: %d distinct runs\n" % len(BYGLOSS))

for t in greens:
    pool = collections.Counter()
    for hw, kind, g in his[t]:
        for run in re.findall(r"[\u4e00-\u9fff]+", g or ""):
            for n in (4, 3, 2):
                for i in range(len(run) - n + 1):
                    sub = run[i:i + n]
                    if len(BYGLOSS.get(sub, ())) > 60:     # 的/了-style noise
                        continue
                    for w in BYGLOSS[sub]:
                        pool[w] = max(pool[w], n)
    if not pool:
        continue
    ranked = sorted(((sim(t, w), n, SPK.get(w, 0), w) for w, n in pool.items()),
                    reverse=True)[:TOPN]
    if ranked[0][0] < 0.55:
        continue
    hw, kind, g = his[t][0]
    print("%2dx %-14s [%-11s] %s" % (len(his[t]), t, hw[:11], (g or "")[:52]))
    for s, n, spk, w in ranked:
        print("      %.2f g%d %-14s spk %-5d %s"
              % (s, n, w, spk, " | ".join(dict.fromkeys(OMNI[w]))[:44]))
