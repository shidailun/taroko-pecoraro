"""audit2 rows 175-250: eight candidates.

The rest of the block is the three known false-positive classes -- name rows
(walae>waray 線 filed 人名（女）, palas>paras the stinging nettle filed 人名, samao,
tixong), synonym wording, and incomplete omnibus rows (damat 菜餚 filed 恢復原狀,
angal 拿取 filed 生（生產）).

These eight are where the modern word may be a different word entirely. For each:
his gloss, the shipped value's own senses and spoken count, and then every
omnibus word whose gloss carries HIS meaning, so an alternative -- if one exists
-- has to show itself rather than be guessed.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)

# key -> (his gloss in one phrase, regex of the meaning to hunt for)
CASES = [
    ("apo",    "\u67ff\u5b50 persimmon",        "\u67ff"),
    ("lodo",   "\u5de2\u7a9d\u3001\u5200\u9798 nest / sheath", "\u5de2|\u9798"),
    ("leqo",   "\u4ec7\u6068\u61ce\u6068 hatred", "\u6068|\u8a87\u5fcc|\u53a6\u60e1"),
    ("q'l\u00f6t", "\u93ee\u5b50 saw",           "\u93ee"),
    ("kyoxan", "\u5c0d\u5973\u4eba\u5011 to women", "\u5973\u4eba|\u5a66\u5973"),
    ("ngali",  "\u5269\u9918\u591a\u51fa surplus", "\u5269\u9918|\u591a\u51fa"),
    ("btaqan", "\u817f\u3001\u5927\u817f thigh",  "\u5927\u817f"),
    ("stoq",   "\u6298\u65b7\u8131\u843d break off", "\u6298\u65b7|\u65b7\u6389|\u8131\u843d"),
]


def show(w, pad="   "):
    used = [x for x in MAP if MAP[x] == w]
    print("%s%-13s spk %-5d %-38s %s" % (
        pad, w, SPK.get(w, 0),
        " | ".join(dict.fromkeys(OMNI.get(w) or []))[:38] or "-- BLIND --",
        ("<= his " + ",".join(used[:3])) if used else ""))


for k, his, pat in CASES:
    v = MAP.get(k, "(green)")
    print("\n=== %-8s -> %-10s   his: %s %s" % (
        k, v, his, "!!LEXNULL!!" if (k in LEX and not LEX[k]) else ""))
    show(v, "   value  ")
    hits = sorted({(SPK.get(w, 0), w) for w, gs in OMNI.items()
                   for g in gs if re.search(pat, g)}, reverse=True)
    if not hits:
        print("   -- nothing in the omnibus carries his meaning --")
    for s, w in hits[:7]:
        show(w, "   cand   ")
