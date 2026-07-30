"""Close out rows 45-105, and pre-flight the paah family for batch 63.

The block cleared almost entirely, which is itself worth recording:
  tasil   the bare row is one half of a homograph -- tmtasil 專取岩石 shows the
          shape does quarry-rock work. No better candidate; btunux is his own.
  ita     TWO cards, 看-root and inclusive 我們. The loose tokens are almost all
          the pronoun. Flat map, bigger card wins.
  nita    same collision: "Nita ka d'xgal nii" 這塊地是我們的 beside "Nita mo
          balae" 我真的看見了.
  ksa     TWO cards, 行走 and （你）說！ -- and the walk card carries the whole
          shipped paradigm mksa/ksaan/ksaon/pksa. Bigger card wins.
  bbuyo   audit2 quoted a sub's 黑暗; the HEADWORD is 荒地——山野, which is bbuyu
          雜草地/打獵 exactly.
  sinao   answered by pnsinaw/ptgsinaw/ksinaw.
Left over: toxoi, where tuhuy's only omnibus rows are a euphemism cluster.
Ask whether anything else carries 陪 before accepting a regular respelling.

Then the paah family. pax 103x is the highest-frequency wrong brown in the
review: his card 1 is 從——自——由…起, the shipped value is 打人的聲音（擬聲詞）at
spk 0, and pnax>pnaah is ALREADY shipped -- the map accepts the root for the
n-form while leaving the headword on an onomatopoeia.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
MAN = json.load(io.open(H + "tools/orthography/manual_map.json", encoding="utf-8"))
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)

print("=== omnibus words glossed with 陪 (is tuhuy the accompany word?) ===")
hits = sorted({(SPK.get(w, 0), w, " | ".join(dict.fromkeys(gs))[:40])
               for w, gs in OMNI.items() for g in gs if "\u966a" in g}, reverse=True)
for s, w, g in hits[:12]:
    used = [x for x in MAP if MAP[x] == w]
    print("   %-14s spk %-5d %-40s %s" % (w, s, g,
          ("<= his " + ",".join(used[:3])) if used else ""))

print("\n=== the paah family ===")
for w in sorted((w for w in OMNI if "paah" in w or w in ("pah",)),
                key=lambda x: -SPK.get(x, 0))[:14]:
    used = [x for x in MAP if MAP[x] == w]
    print("   %-14s spk %-5d %-40s %s" % (
        w, SPK.get(w, 0), " | ".join(dict.fromkeys(OMNI[w]))[:40],
        ("<= his " + ",".join(used[:3])) if used else ""))

PROP = {"pax": "paah", "npax": "npaah", "mpax": "empaah"}
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
OWN = {k: [] for k in PROP}
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh")), (ent.get("paradigm"), ent.get("zh"))]
    slots += [(x.get("t"), x.get("zh")) for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh")), (s.get("paradigm"), s.get("zh"))]
        slots += [(x.get("t"), x.get("zh")) for x in s.get("examples", [])]
    for f, g in slots:
        for w in TOK.findall(f or ""):
            k = key(w)
            if k in OWN and (hw, (g or "")[:34]) not in OWN[k]:
                OWN[k].append((hw, (g or "")[:34]))


def att(v):
    o, s = OMNI.get(v.lower()), SPK.get(v.lower(), 0)
    return ("OMNI %-24s spk %d" % (" | ".join(dict.fromkeys(o))[:24], s)) if o else \
           ("-- BLIND --%s" % ("  spk %d" % s if s else ""))


print("\n=== pre-flight ===")
for k, v in PROP.items():
    cur = MAP.get(k, "(green)")
    print("\n%-8s %-10s -> %-10s%s" % (k, cur, v,
          "  !!LEXNULL!!" if (k in LEX and not LEX[k]) else ""))
    print("   now  %-10s %s" % (cur, att(cur) if cur != "(green)" else ""))
    print("   prop %-10s %s" % (v, att(v)))
    if k in MAN:
        print("   manual_map already says: %s" % MAN[k])
    other = [x for x in MAP if MAP[x] == v and x != k]
    if other:
        print("   value already used by: %s" % other)
    for hw, g in OWN[k][:7]:
        print("      card [%-14s] %s" % (hw[:14], g))

print("\n-- lexical_map entries on this family --")
for k in sorted(LEX):
    if "pax" in k or "paah" in k:
        print("   %-12s = %s" % (k, json.dumps(LEX[k], ensure_ascii=False)[:300]))
