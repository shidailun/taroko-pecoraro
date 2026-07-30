"""Second pre-flight: the TLOONG family, and the lexical_map nulls in the way.

kmpstloong/kmpstlngun were on the take-list as confirm-only, i.e. the value equals
what charRules already prints. That is only honest if the char rule is RIGHT, and
CLAUDE.md's batch 24 says TLOONG is the SIT root, whose modern forms keep the l
(tleengan 93x). If so the rule's l>r is wrong here and the claim would ship a fake
word in brown -- the worst state available.
"""
import json, io, sys, re, pickle
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)

print("-- modern SIT family --")
for w in ["tluung", "truung", "tleeng", "tleengan", "tleengun", "tlnga", "tlngi",
          "tlngun", "ptluung", "ptleengan", "kmptluung", "kmptruung", "struung",
          "sruung", "mtluung", "mtruung", "kntluung", "pstluung", "pstruung",
          "kmpstluung", "kmpstruung", "kmpstlngun", "kmpstrngun"]:
    print("   %-14s omni %-34s spk %s" % (w, (OMNI.get(w) or "-")[:34], SPK.get(w, 0)))

print("\n-- what the map already says about his tloong/tlngun keys --")
for k, v in sorted(MAP.items()):
    if "tloong" in k or "tlngun" in k or "tlngan" in k or "tlnge" in k:
        print("   %-16s -> %-16s  omni %-24s spk %s"
              % (k, v, (OMNI.get(v) or "-")[:24], SPK.get(v, 0)))

print("\n-- lexical_map.json --")
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
for k, v in sorted(LEX.items()):
    print("   %-14s %s" % (k, v))
