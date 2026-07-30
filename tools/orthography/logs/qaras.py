"""QALAS 喜樂 is a half-brown card: the syncopated slots are on `qras`, the
unsyncopated ones are green. Modern spells the full root `qaras` (batch 28 already
used `qnaras` 17x for the kn- infix), so the green half has an answer sitting in
the corpus. Print the whole qaras family, and every green token on the card.
"""
import io, sys, json, pickle, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
app = io.open(H + "site/app.js", encoding="utf-8").read()
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def table(n):
    i = app.index("var %s = {" % n)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))


OV, CL = table("WORD_OVERRIDES"), table("CLITIC_FORMS")
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)

print("-- omnibus + speech: the qaras family --")
for w, g, _ in ROWS:
    if w and "qaras" in w.lower():
        print("   %-16s %-40s spk %s" % (w, (g or "-")[:40], SPK.get(w.lower(), 0)))
print("   -- spoken only --")
for w in sorted(SPK):
    if "qaras" in w and w not in OMNI:
        print("   %-16s spk %s" % (w, SPK[w]))

print("\n-- the QALAS card, token by token --")
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
for ent in E:
    if (ent.get("hw") or "").upper() != "QALAS":
        continue
    forms = [ent.get("hw")] + [s.get("form") for s in ent.get("subs", [])]
    for f in [x for x in forms if x]:
        for w in TOK.findall(f):
            k = key(w)
            if len(k) < 2:
                continue
            src = "OV" if k in OV else ("MAP" if k in MAP else
                                        ("CL" if k in CL else "GREEN"))
            v = OV.get(k) or MAP.get(k) or CL.get(k) or "-"
            print("   %-14s %-6s %-16s omni %-24s spk %s"
                  % (k, src, v, (OMNI.get(v) or "-")[:24], SPK.get(v, 0)))
