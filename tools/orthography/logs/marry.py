"""IYUX's kmstloon/kmpstloong/kmpstlngun are about MARRYING, not sitting.

The map ships kmstloon>kmstruun, an l>r on a stem that looks like his tloong 坐
(= modern tluung 125x, which the map itself already writes with the l). Before
either confirming or fixing the two green siblings, ask the omnibus what 結婚/成婚
actually is, and whether the sit root carries that sense.
"""
import io, sys, json, pickle, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))

print("-- omnibus glosses mentioning 結婚 / 成婚 / 娶 / 嫁 --")
seen = set()
for w, g, _ in ROWS:
    if not w or not g:
        continue
    if any(c in g for c in ("結婚", "成婚", "娶", "嫁", "婚")):
        k = (w.lower(), g)
        if k in seen:
            continue
        seen.add(k)
        print("   %-16s %-40s spk %s" % (w, g[:40], SPK.get(w.lower(), 0)))

print("\n-- anything whose SHAPE holds tluung / stluung / struung --")
for w, g, _ in ROWS:
    if w and ("tluung" in w.lower() or "struung" in w.lower() or "tleeng" in w.lower()):
        print("   %-16s %-40s spk %s" % (w, (g or "-")[:40], SPK.get(w.lower(), 0)))
print("   -- spoken --")
for w in sorted(SPK):
    if "tluung" in w or "struung" in w or "tleeng" in w or "stlung" in w:
        print("   %-16s spk %s" % (w, SPK[w]))
