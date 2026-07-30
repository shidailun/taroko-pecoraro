"""mnsa: 53 slots, and the biggest find since pax if it holds.

His MNSA is a sub of his USA card, glossed 已去過 -- the past of GO. The shipped
value mnsa is the past of SAY (如此說…。, spk 72), which in modern Truku is
exactly that shape: msa 說 -> mnsa 說過. His own msa>msa 他這樣說的 is already
shipped for the say verb, so the two are distinct in his dictionary and collide
in the modern one.

Before writing, the risk has to be excluded: if any of the 53 slots is actually
the SAY sense, this is a homograph split and not a defect. So classify all 53 by
whether the Chinese gloss contains a going word or a saying word, and print the
ones that are neither.
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


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])

GO = re.compile("\u53bb|\u5f80|\u524d\u5f80|\u4e0a\u53bb|\u4e0b\u53bb|\u9032|\u5230")
SAY = re.compile("\u8aaa|\u8b1b|\u544a\u8a34|\u7a31")
buckets = collections.Counter()
other = []
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh"), "hw"), (ent.get("paradigm"), ent.get("zh"), "par")]
    slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh"), "sub")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
    for f, g, kind in slots:
        if not any(key(w) == "mnsa" for w in TOK.findall(f or "")):
            continue
        g = g or ""
        go, say = bool(GO.search(g)), bool(SAY.search(g))
        if go and not say:
            buckets["GO only"] += 1
        elif say and not go:
            buckets["SAY only"] += 1
            other.append(("SAY", hw, kind, f, g))
        elif go and say:
            buckets["both words present"] += 1
            other.append(("BOTH", hw, kind, f, g))
        else:
            buckets["neither"] += 1
            other.append(("----", hw, kind, f, g))

print("=== 53 slots spelling mnsa, classified by gloss ===")
for k, v in buckets.most_common():
    print("   %-20s %d" % (k, v))
print("\n=== every slot that is not unambiguously GO ===")
for tag, hw, kind, f, g in other:
    print("  %s [%-13s] %-4s %-30s %s" % (tag, hw[:13], kind, (f or "")[:30], g[:52]))

print("\n=== the go paradigm, for the record ===")
for w in ("musa", "mnusa", "mnsa", "msa", "mha", "wada", "nusa", "smnsa"):
    used = [x for x in MAP if MAP[x] == w]
    print("   %-9s spk %-5d %-32s %s" % (
        w, SPK.get(w, 0), " | ".join(dict.fromkeys(OMNI.get(w) or []))[:32] or "-- BLIND --",
        ("<= his " + ",".join(used[:3])) if used else ""))
