"""Every modern word whose gloss contains ANY of the given substrings.

bygloss() in probe.py scores on character overlap with his whole zh field, which
is right for a card but too loose for a single sense -- 希望某人遭殃 pulls in every
word glossed 希望. This asks the narrow question instead: who carries this exact
word?
"""
import io, sys, json, pickle, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
O = pickle.load(open("omni.pkl", "rb"))
GLOSS = collections.defaultdict(list)
for w, g, _ in O[0]:
    if g:
        GLOSS[w.lower()].append(g)
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
CNT = SPK if isinstance(SPK, dict) else collections.Counter(SPK)

for pat in sys.argv[1:]:
    print("\n--- %s ---" % pat)
    hits = [(CNT.get(w, 0), w, "; ".join(dict.fromkeys(gs))[:60])
            for w, gs in GLOSS.items() if any(pat in g for g in gs)]
    for n, w, g in sorted(hits, reverse=True)[:20]:
        print("   %-16s %5s %s" % (w, n or "", g))
    if not hits:
        print("   (nothing)")
