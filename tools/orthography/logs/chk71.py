"""snax and spax: the two paah slots not yet judged.

snax is shipped as snah, which is charRules output, not a choice. spax is green.
Print his slots, the current values' own attestation, and every s-form of paah on
record, before deciding whether either belongs in batch 63.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


for w in ("snah", "snaah", "sgnaah", "spaah", "pnaah", "sknaah", "gnaah", "knaah"):
    print("   %-10s spk %-5d %s" % (w, SPK.get(w, 0),
          " | ".join(dict.fromkeys(OMNI.get(w) or [])) or "-- BLIND --"))

e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
print("\n=== his PAX cards, every slot ===")
for ent in E:
    hw = ent.get("hw") or ""
    if not hw.lower().startswith("pax"):
        continue
    print("\n--- %s  %s" % (hw, (ent.get("zh") or "")[:90]))
    for s in ent.get("subs", []):
        f = (s.get("form") or "")
        k = key(TOK.findall(f)[0]) if TOK.findall(f) else ""
        print("   sub %-12s -> %-10s  %s" % (f[:12], MAP.get(k, "(green)"),
                                             (s.get("zh") or "")[:44]))
