"""Attestation + gloss for a list of candidate spellings, and the map's current
value for a list of his keys. Membership is the UNION of the omnibus and the
spoken corpus -- a glossed-only set hides attested forms that carry no gloss."""
import json, io, sys, re, pickle, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"

O = pickle.load(open("omni.pkl", "rb"))
GLOSS = collections.defaultdict(list)
for w, g, _ in O[0]:
    if g:
        GLOSS[w.lower()].append(g)
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
CNT = SPK if isinstance(SPK, dict) else collections.Counter(SPK)
ALL = {w.lower() for w, g, _ in O[0]} | set(CNT)

t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
app = io.open(H + "site/app.js", encoding="utf-8").read()
i = app.index("var WORD_OVERRIDES = {")
OV = dict(re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')
          .findall(app[i:app.index("\n  };", i)]))

mode = "w"
for arg in sys.argv[1:]:
    if arg == "-k":
        mode = "k"
        print("\n--- his keys ---")
        continue
    if arg == "-w":
        mode = "w"
        print("\n--- candidate spellings ---")
        continue
    if arg == "-s":
        mode = "s"
        print("\n--- substring search over the modern lexicon ---")
        continue
    if mode == "k":
        v = OV.get(arg) or MAP.get(arg)
        print("%-14s -> %s" % (arg, v if v else "(GREEN)"))
    elif mode == "s":
        hits = [(w, CNT.get(w, 0), "; ".join(dict.fromkeys(GLOSS.get(w, [])))[:52])
                for w in ALL if arg in w]
        for w, n, g in sorted(hits, key=lambda r: -r[1])[:22]:
            print("   %-16s %5s %s" % (w, n or "", g))
        if not hits:
            print("   (%s: nothing)" % arg)
    else:
        n, g = CNT.get(arg, 0), "; ".join(dict.fromkeys(GLOSS.get(arg, [])))[:64]
        print("%-16s %-6s %-9s %s" % (arg, ("%dx" % n) if n else "0x",
                                      "ATTESTED" if arg in ALL else "--absent--", g))
