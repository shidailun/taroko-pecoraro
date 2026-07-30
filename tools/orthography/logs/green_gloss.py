"""Green tokens, searched by MEANING first and shape second.

audit6 required both at once -- a shared gloss bigram AND an edit distance of two
-- and only 10 of 272 green types produced a candidate. green_near dropped the
gloss test and found the neighbourhoods are string coincidences. Neither is the
question the review keeps coming back to, which is: look his word up in the modern
dictionary BY WHAT IT MEANS, and only then ask whether his spelling could be it.

So: take his Chinese gloss, find every omnibus word whose gloss shares a
two-character word with it, rank by how well attested it is, and print the edit
distance rather than filtering on it. A distance of 4 between a French-era
transcription and a modern orthography is not disqualifying -- ayo/ayug was 2,
ml'bu/mgrbu was 3 -- so the distance is evidence to weigh, not a gate.

Distinctive glosses only. A token glossed 去 or 做 shares a bigram with half the
dictionary and tells us nothing; one glossed 犬齒, 兔唇, 細腰蜂 or 雉雞 names a
thing, and if modern Truku has a word for that thing this will find it.
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

# invert the omnibus: bigram -> words that carry it. Only spoken words, because
# an unattested modern headword is no better evidence than his transcription.
BYBI = collections.defaultdict(set)
for w, gs in OMNI.items():
    if SPK.get(w, 0) < 1:
        continue
    for g in gs:
        for b in bigrams(g):
            BYBI[b].add(w)

# a bigram carried by many words is a register word, not a name for a thing
MAXCARRY = int(sys.argv[4]) if len(sys.argv) > 4 else 40
MINSLOT = int(sys.argv[1]) if len(sys.argv) > 1 else 2
rows = []
for k, slots in his.items():
    if k in MAP or k in LEX or len(slots) < MINSLOT:
        continue
    target = cr(k)
    if len(target) < 3:
        continue
    hisb = set()
    for g, _, kind in slots:
        if kind != "ex":
            hisb |= bigrams(g)
    cand = collections.defaultdict(set)
    for b in hisb:
        ws = BYBI.get(b) or ()
        if len(ws) > MAXCARRY:        # 很多 / 東西 / 一起 -- carries no content
            continue
        for w in ws:
            cand[w].add(b)
    if not cand:
        continue
    best = sorted(cand.items(), key=lambda kv: (-len(kv[1]), -SPK.get(kv[0], 0)))
    rows.append((len(slots), k, target, best[:5], slots[0][1],
                 "; ".join(dict.fromkeys(g for g, _, kd in slots if kd != "ex" and g))[:60]))

rows.sort(key=lambda r: -r[0])
LO = int(sys.argv[2]) if len(sys.argv) > 2 else 0
HI = int(sys.argv[3]) if len(sys.argv) > 3 else 30
print("%d green types with a distinctive-gloss match in spoken modern Truku "
      "(>=%d slots, bigram carried by <=%d words)\n" % (len(rows), MINSLOT, MAXCARRY))
for n, k, target, best, hw, gl in rows[LO:HI]:
    print("%3dx [%-14s] %-14s prints %-13s %s" % (n, hw[:14], k, target.upper(), gl))
    for w, bs in best:
        print("      d%-2d %-13s spk %-5d %-34s %s"
              % (lev(target, w), w, SPK.get(w, 0),
                 " | ".join(dict.fromkeys(OMNI[w]))[:34], "".join(sorted(bs))[:16]))
