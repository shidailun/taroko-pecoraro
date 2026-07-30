"""Pre-flight for batch 64.

alax. His only ALAX card is 圍火取暖, and the map gives the key alax 放棄 spk 25 --
the abandon word. If the key is used ONLY on that card it is wrong the same way
malax is; if it turns up in sentences across the dictionary meaning abandon, it is
a homograph and the majority keeps it. Print every slot.

Also confirm the s-slot of qpah, and that nothing else owns m'alax.
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


def show(w, pad="   "):
    used = [x for x in MAP if MAP[x] == w]
    print("%s%-13s spk %-5d %-34s %s" % (
        pad, w, SPK.get(w, 0),
        " | ".join(dict.fromkeys(OMNI.get(w) or []))[:34] or "-- BLIND --",
        ("<= his " + ",".join(used[:3])) if used else ""))


print("=== the s-slot of work ===")
for w in ("sqpah", "pqpah", "spqpah", "qpah", "qpahun", "qnpahan", "skpax", "sqpahan"):
    show(w)

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
for target in ("alax", "m'alax", "skpax", "p'alax"):
    print("\n########## every slot spelling %r  (now %s) ##########"
          % (target, MAP.get(target, "(green)")))
    n = 0
    for ent in E:
        hw = ent.get("hw") or ""
        slots = [(ent.get("hw"), ent.get("zh"), "hw"), (ent.get("paradigm"), ent.get("zh"), "par")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
        for s in ent.get("subs", []):
            slots += [(s.get("form"), s.get("zh"), "sub")]
            slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
        for f, g, kind in slots:
            if any(key(w) == target for w in TOK.findall(f or "")):
                n += 1
                if n <= 26:
                    print("   [%-15s] %-4s %-30s %s" % (hw[:15], kind, (f or "")[:30], (g or "")[:42]))
    print("   (%d slots)" % n)
