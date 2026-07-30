"""The five biggest green CLUSTERS left, by occurrence, not by type.

green6 ranks types; a family of four 2-3x types is worth more than one 4x type and
costs one lookup instead of four. By occurrence the leaders are:
   L'NGUT  lmngut 3 + lngutan 3 + lngut 2 + plngut 2   = 10
   TIPYAQ  tepyaq 4 + pntipyaq 3 + tipyaq 2            =  9
   QODAP   tqodap 3 + ptqodap 2 + kdapan 2             =  7
   Q'TQOT  sq'tqot 3 + q'tqot 2                        =  5
   LIKUT   likut 2 + tnlikut 2                         =  4
For each: his whole card, his keys the map already answered (the half-brown test
-- a family with brown siblings has already had its root decided), and the modern
family by SHAPE and by GLOSS, because the gloss is what finds a word whose shape
his spelling hides.
"""
import io, sys, json, pickle, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)
ALL = sorted(set(OMNI) | set(SPK))
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])

FAM = [
    ("L'NGUT", r"^L'NGUT|^LNGUT", r"lngut|l'ngut",
     r"rngu|lngu|rmngu", ("受孕", "懷孕", "生育")),
    ("TIPYAQ", r"^TIPYAQ|^KUI", r"tipyaq|tepyaq",
     r"tpiyaq|tipiq|tpyaq", ("一點點", "少量", "小份", "蠶", "糞蟲")),
    ("QODAP", r"^QODAP|^KDAPAN", r"qodap|kdapan",
     r"qdapa|kdapa|qudap", ("熄滅", "鰥夫", "寡婦")),
    ("Q'TQOT", r"^Q'TQOT", r"q'tqot|qtqot",
     r"qtut|qqtut|qtqut", ("捆綁", "手銬", "鏈條", "繩索")),
    ("LIKUT", r"^LIKUT", r"likut",
     r"rikut|likut|rkut", ("藉口", "詭計", "推託")),
]

for name, cardpat, keypat, shape, glosses in FAM:
    print("\n" + "=" * 72)
    print("== %s" % name)
    cp = re.compile(cardpat)
    for ent in E:
        if not cp.match((ent.get("hw") or "").upper()):
            continue
        print("   hw %s %s" % (ent.get("hw"), ent.get("tag") or ""))
        print("   zh:", (ent.get("zh") or "-")[:72])
        for x in ent.get("examples", []):
            print("   § %-48s %s" % (x.get("t", "")[:48], (x.get("zh") or "")[:34]))
        for s in ent.get("subs", []):
            print("   - %-16s %s" % (s.get("form", ""), (s.get("zh") or "")[:46]))
            for x in s.get("examples", []):
                print("       § %-44s %s"
                      % (x.get("t", "")[:44], (x.get("zh") or "")[:32]))
    print("   -- his keys the map already answered --")
    kp = re.compile(keypat)
    got = False
    for k in sorted(MAP):
        if kp.search(k):
            print("      %-14s -> %-14s omni %-20s spk %s"
                  % (k, MAP[k], (OMNI.get(MAP[k]) or "-")[:20], SPK.get(MAP[k], 0)))
            got = True
    if not got:
        print("      (none -- the whole family is green)")
    blk = [k for k in LEX if kp.search(k) and not LEX[k]]
    if blk:
        print("      LEXNULL:", blk)
    print("   -- modern by shape /%s/ --" % shape)
    r, n = re.compile(shape), 0
    for w in ALL:
        if r.search(w):
            print("      %-16s %-32s spk %s"
                  % (w, (OMNI.get(w) or "-")[:32], SPK.get(w, 0)))
            n += 1
            if n >= 18:
                print("      ...")
                break
    if not n:
        print("      (nothing)")
    print("   -- modern by gloss %s --" % "/".join(glosses))
    seen = set()
    for w, g, _ in ROWS:
        if w and g and any(z in g for z in glosses) and w.lower() not in seen:
            seen.add(w.lower())
            print("      %-16s %-32s spk %s" % (w, g[:32], SPK.get(w.lower(), 0)))
            if len(seen) >= 18:
                print("      ...")
                break
