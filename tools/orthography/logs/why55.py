"""Which n-gram made a value impossible, and what the lexicon writes instead."""
import json, sys, pickle, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
SPK = json.load(open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
O = pickle.load(open("omni.pkl", "rb"))
LEX = set(SPK) | set(w.lower() for w, g, _ in O[0])
NG = collections.Counter()
for w in LEX:
    p = "^" + w + "$"
    for n in (2, 3, 4):
        for i in range(len(p) - n + 1):
            NG[p[i:i + n]] += 1

for v in sys.argv[1:]:
    p = "^" + v + "$"
    dead = [p[i:i + n] for n in (2, 3, 4) for i in range(len(p) - n + 1)
            if NG[p[i:i + n]] == 0]
    print("\n%-12s dead: %s" % (v, dead or "none — licit"))
    for g in dead:
        core = g.strip("^$")
        near = sorted((w for w in LEX if core in w), key=len)[:8]
        print("   %-8s (%d types hold %r)  %s" % (g, len(near), core, near))
