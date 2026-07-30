"""IYUX again: is his -stloong- the SIT root (tluung) or the MEET root (strung)?

pnstrngan 成婚;相遇的地方 18x and pstrung 相遇（結婚;打戰）4x carry his exact sense,
and they carry it on a str- cluster -- which is what charRules already produces from
his stl-. The sit root, which the map writes with the l, carries no marriage sense
anywhere. Print both families in full, plus every one of his own keys holding stlo/
stlng/tloong, so the decision is made on the whole paradigm rather than one slot.
"""
import io, sys, json, pickle, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])

print("-- omnibus: the strung / strng family --")
for w, g, _ in ROWS:
    if w and ("strung" in w.lower() or "strng" in w.lower() or "strngan" in w.lower()):
        print("   %-16s %-42s spk %s" % (w, (g or "-")[:42], SPK.get(w.lower(), 0)))
print("   -- spoken only --")
for w in sorted(SPK):
    if "strung" in w or "strng" in w:
        print("   %-16s spk %s" % (w, SPK[w]))

print("\n-- his keys holding stlo / stlng / stloong --")
for k, v in sorted(MAP.items()):
    if "stlo" in k or "stlng" in k or "stln" in k:
        print("   %-16s -> %-16s omni %-26s spk %s"
              % (k, v, (dict((r[0].lower(), r[1]) for r in ROWS if r[0]).get(v) or "-")[:26],
                 SPK.get(v, 0)))
