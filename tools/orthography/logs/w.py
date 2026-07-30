"""Word/gloss probe over the omnibus + speech corpus.

  python w.py word W1 W2 ...     -- exact modern words, with every gloss
  python w.py gloss 新 分離       -- every modern word whose gloss contains the string
"""
import sys, io, json, pickle, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "/tools/orthography/spoken_truku.json", encoding="utf-8"))
BY = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w:
        BY[w.lower()].append(g)

mode, args = sys.argv[1], sys.argv[2:]
if mode == "word":
    for a in args:
        gs = BY.get(a.lower(), [])
        print("%-14s speech %-5s %s" % (a, SPK.get(a.lower(), 0),
                                        " / ".join(gs) if gs else "-- NOT IN OMNIBUS"))
else:
    for a in args:
        hits = [(w, g) for w, g, _ in ROWS if w and a in (g or "")]
        print("=== %s  (%d)" % (a, len(hits)))
        for w, g in hits[:40]:
            print("   %-14s speech %-5s %s" % (w, SPK.get(w.lower(), 0), g))
