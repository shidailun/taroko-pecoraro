"""The green list, searched by HIS gloss against the modern lexicon.

For every green token still without a map key, take the Chinese gloss on the slot
he wrote it in, cut it into CJK n-grams, and find every modern word whose own
gloss contains one. Score each candidate on two independent axes -- gloss overlap
and shape against his char-rule form -- and print the ones that score on both.
This is the "look it up in the modern dictionary" pass, run over the whole list at
once instead of a word at a time. Writes nothing; every hit still has to survive a
paradigm read before it earns a manual_map key.
"""
import json, sys, pickle, re, collections, difflib, io
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"

SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
O = pickle.load(open("omni.pkl", "rb"))
OMNI = {}
for w, g, _ in O[0]:
    if g:
        OMNI.setdefault(w.lower(), g)
ROWS = json.load(io.open("green2.json", encoding="utf-8"))
CJK = re.compile(r"[\u3400-\u9fff]+")
STOP = {"一個", "什麼", "自己", "某人", "某物", "的人", "之物", "動詞", "同上",
        "他們", "我們", "你們", "使其", "不要", "可以", "已經", "東西", "地方",
        "形式", "詞根", "參見", "註", "或許", "無疑", "這個", "那個"}

IDX = collections.defaultdict(set)
for w, g in OMNI.items():
    for seg in CJK.findall(g):
        for n in (2, 3, 4):
            for i in range(len(seg) - n + 1):
                z = seg[i:i + n]
                if z not in STOP:
                    IDX[z].add(w)

SM = {"x": "h", "o": "u", "l": "r"}
MARKS = "'\u2019\u02bc\"\u0294"


def cr(w):
    return "".join(SM.get(c, c) for c in re.sub("[" + MARKS + "]", "", w.lower()))


MIN = float(sys.argv[1]) if len(sys.argv) > 1 else 0.55
out = []
for cnt, tok, rendered, tag, gloss in ROWS:
    grams = set()
    for seg in CJK.findall(gloss or ""):
        for n in (2, 3, 4):
            for i in range(len(seg) - n + 1):
                grams.add(seg[i:i + n])
    grams -= STOP
    if not grams:
        continue
    hits = collections.Counter()
    for z in grams:
        for w in IDX.get(z, ()):
            hits[w] += len(z)
    if not hits:
        continue
    mine = cr(tok)
    scored = []
    for w, gs in hits.most_common(400):
        sh = difflib.SequenceMatcher(None, mine, w).ratio()
        if sh >= MIN:
            scored.append((sh, gs, w))
    scored.sort(reverse=True)
    if scored:
        out.append((cnt, tok, rendered, tag, gloss, scored[:4]))

out.sort(reverse=True)
for cnt, tok, rendered, tag, gloss, sc in out:
    print("\n%2dx %-14s (renders %-14s) [%s] %s" % (cnt, tok, rendered, tag, (gloss or "")[:54]))
    for sh, gs, w in sc:
        print("      %-16s %4sx  shape %.2f  %s" % (w, SPK.get(w, 0), sh, (OMNI.get(w) or "")[:42]))
print("\n%d green tokens have a shape+gloss candidate" % len(out))
