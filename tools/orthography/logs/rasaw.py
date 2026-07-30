"""The last -au on the page, and it is brown.

After the charRules -ao rule, exactly ONE span in the whole dictionary still ends
-au: `psqrasau`, the shipped value of his `psqlasao`. A brown -au is a claim that
this word is the one place the orthography does that, against 2,407 modern types
in -aw and 4 in -au. Print the whole qras/qlas family in both corpora, his card,
and every one of his keys holding qlas/qras, before deciding.
"""
import io, sys, json, pickle, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)

print("-- omnibus: anything holding qras / qlas / rasa --")
for w, g, _ in ROWS:
    if w and re.search(r"qras|qlas|rasa|rasaw", w.lower()):
        print("   %-16s %-40s spk %s" % (w, (g or "-")[:40], SPK.get(w.lower(), 0)))
print("   -- spoken only --")
for w in sorted(SPK):
    if re.search(r"qras|qlas|rasaw", w) and w not in OMNI:
        print("   %-16s spk %s" % (w, SPK[w]))

print("\n-- his keys holding qlas / qras --")
for k, v in sorted(MAP.items()):
    if "qlas" in k or "qras" in k:
        print("   %-16s -> %-16s omni %-26s spk %s"
              % (k, v, (OMNI.get(v) or "-")[:26], SPK.get(v, 0)))

print("\n-- his cards --")
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
for ent in E:
    fields = [ent.get("hw"), ent.get("tag"), ent.get("paradigm")]
    fields += [x.get("t") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        fields += [s.get("form"), s.get("paradigm")]
        fields += [x.get("t") for x in s.get("examples", [])]
    blob = " ".join(f for f in fields if f)
    if not re.search(r"qlas|qras", blob, re.I):
        continue
    print("\n== %s  %s" % (ent.get("hw"), ent.get("tag") or ""))
    print("   zh:", (ent.get("zh") or "-")[:70])
    for x in ent.get("examples", []):
        print("   § %-52s %s" % (x.get("t", "")[:52], (x.get("zh") or "")[:34]))
    for s in ent.get("subs", []):
        print("   - %-20s %s" % (s.get("form", ""), (s.get("zh") or "")[:44]))
        for x in s.get("examples", []):
            print("       § %-48s %s" % (x.get("t", "")[:48], (x.get("zh") or "")[:34]))
