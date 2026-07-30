"""malax and skpax, the two audit4 candidates still open.

MALAX. His ALAX card is 圍火取暖 and its other slot is already shipped:
      P'alax -> palah  使人取暖
so the ALAX family IS the modern alah/palah warm-by-the-fire root, and the map
already accepts it for the p-form. malax sits on malax 要放棄 (abandon), which is
a different word. But malax is also a sub of BALAX 更新, where the majority is
barah/embarah/mnbarah/tnbarah -- one key, two cards, so ownership decides.

SKPAX. His K'PAX 工作 card ships qpah/qmpah/mqpah/dmqpah, and even his blind
spkpax got spqpah. Only skpax walked off, to skpax 習慣放鞭炮. Print the whole
card so the s-slot's neighbours are visible.
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
    print("%s%-13s spk %-5d %-36s %s" % (
        pad, w, SPK.get(w, 0),
        " | ".join(dict.fromkeys(OMNI.get(w) or []))[:36] or "-- BLIND --",
        ("<= his " + ",".join(used[:3])) if used else ""))


print("=== warm-by-the-fire: the alah family ===")
for w in ("alah", "malah", "palah", "mnalah", "pnalah", "smalah", "alahan",
          "malax", "mlax", "alax"):
    show(w)
print("   -- every omnibus word glossed with 取暖 --")
for s, w in sorted({(SPK.get(w, 0), w) for w, gs in OMNI.items()
                    for g in gs if "\u53d6\u6696" in g}, reverse=True)[:10]:
    show(w, "      ")

print("\n=== renew (the BALAX majority) ===")
for w in ("barah", "mbarah", "embarah", "smbarah", "pbarah", "mbrah"):
    show(w)

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
print("\n########## every slot spelling 'malax' ##########")
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh"), "hw"), (ent.get("paradigm"), ent.get("zh"), "par")]
    slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh"), "sub")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
    for f, g, kind in slots:
        if any(key(w) == "malax" for w in TOK.findall(f or "")):
            print("   [%-16s] %-4s %-34s %s" % (hw[:16], kind, (f or "")[:34], (g or "")[:44]))

print("\n########## his K'PAX card ##########")
for ent in E:
    hw = (ent.get("hw") or "")
    if not re.match(r"^K'PAX|^KPAX|^SKPAX", hw.upper()):
        continue
    print("--- %s   %s" % (hw, (ent.get("zh") or "")[:70]))
    if ent.get("paradigm"):
        print("    par %s" % ent["paradigm"][:70])
    for s in ent.get("subs", []):
        f = (s.get("form") or "")
        kk = key(TOK.findall(f)[0]) if TOK.findall(f) else ""
        print("    sub %-14s -> %-11s %s" % (f[:14], MAP.get(kk, "(green)"), (s.get("zh") or "")[:44]))
