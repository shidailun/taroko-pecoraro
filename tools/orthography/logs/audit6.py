"""audit5 pointed at the GREENS. This one reduces the unknown count.

Batches 64, 65 and 66 all corrected words that already claimed to be verified;
green held at 272 types / 399 occurrences through all three. Green means
UNVERIFIED -- no curated table has a key, so charRules prints a mechanical
respelling and nobody has ever checked it against the modern dictionary.

Same question as audit5, asked of a token with no entry at all: HIS gloss is
known, so hunt the omnibus for a word that is within a length-scaled edit
distance of what charRules would print AND whose gloss shares a two-character
Chinese word with his. Rank by how many slots the token fills, so the sweep goes
in order of frequency.

The sibling filter that cleaned up audit5 does not apply here -- there is no
shipped value for a candidate to be a morphological relative OF. What replaces it
is the charRules baseline: print what the reader currently shows, so a candidate
that merely reproduces it is visibly not news, and one that differs is a claim
about a word charRules got wrong.
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


TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")
CJK = re.compile(r"[\u4e00-\u9fff]+")
STOP = set("\u7684\u4e86\u662f\u5728\u6709\u4eba\u4e0d\u4e00\u500b\u6211\u4f60"
           "\u4ed6\u5011\u9019\u90a3\u4e4b\u548c\u8207\u6216\u4e5f\u5c31\u628a"
           "\u5230\u53bb\u4f86\u505a\u7269\u4e8b\u6642\u5730\u65b9\u5f0f\u8005"
           "\u4f7f\u88ab\u6240\u53ca\u7b49\u5176\u800c\u4ee5\u70ba\u4e2d\u4e0a"
           "\u4e0b\u5927\u5c0f\u5df2\u8981\u6703\u80fd\u53ef\u5f97\u5f88\u592a")


def bigrams(text):
    out = set()
    for run in CJK.findall(text or ""):
        for i in range(len(run) - 1):
            b = run[i:i + 2]
            if b[0] not in STOP or b[1] not in STOP:
                out.add(b)
    return out


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


def clean(g):
    g = re.sub(r"\uff08\u8a3b[^\uff09]*\uff09?", "", g or "")
    return re.sub(r"\s+", " ", re.sub(r"\u53c3\u898b.*$", "", g)).strip()


def key(w):
    return re.sub(MARKS, "'", w).replace("\u0142", "l").lower()


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
hits = []
for k, slots in his.items():
    if k in MAP or k in LEX:          # GREENS only: nothing in any curated table
        continue
    if len(slots) < MINSLOT:
        continue
    hisb = set()
    for g, _, kind in slots:
        if kind != "ex":
            hisb |= bigrams(g)
    if not hisb:
        continue
    target = cr(k)
    cap = max(1, min(2, len(target) // 3))
    best = []
    for L in range(len(target) - 2, len(target) + 3):
        for w in BYLEN.get(L, ()):
            wb = set()
            for g in OMNI[w]:
                wb |= bigrams(g)
            shared = hisb & wb
            if not shared:
                continue
            if lev(target, w, cap) > cap:
                continue
            best.append((SPK.get(w, 0), w, shared))
    if not best:
        continue
    best.sort(reverse=True)
    hits.append((len(slots), k, target, best[:3], slots[0][1],
                 "; ".join(dict.fromkeys(g for g, _, kd in slots if kd != "ex"))[:64]))

hits.sort(key=lambda r: -r[0])
print("%d GREEN tokens where the omnibus holds a word matching his gloss "
      "(>=%d slots)\n" % (len(hits), MINSLOT))
LO = int(sys.argv[2]) if len(sys.argv) > 2 else 0
HI = int(sys.argv[3]) if len(sys.argv) > 3 else 30
for n, k, target, best, hw, hg in hits[LO:HI]:
    print("%3dx [%-14s] %-15s  reader now prints %s" % (n, hw[:14], k, target))
    print("      his %s" % hg)
    for s, w, sh in best:
        print("      CAND %-13s spk %-5d %-30s  shares %s"
              % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:30], "".join(sorted(sh))[:20]))
