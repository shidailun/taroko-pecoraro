"""The next residue the -ao census exposed: brown spans ending in a bare o.

His o is modern u almost everywhere (SPELLING_MAP), so a brown value that KEEPS a
word-final o is either a loan/name frozen on purpose (tiers J and N do that 279
times between them) or a value nobody looked at. Ask the same three questions as
the -ao class: is word-final -o a shape modern Truku writes, which keys produce
these, and what does the family say.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
MAN = json.load(io.open(H + "tools/orthography/manual_map.json", encoding="utf-8"))
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)
ALL = set(OMNI) | set(SPK)

print("-- word-final single vowels across %d modern types --" % len(ALL))
c = collections.Counter(w[-1] for w in ALL if len(w) > 2)
for v in "aeiou":
    toks = sum(SPK.get(w, 0) for w in ALL if w.endswith(v))
    print("   -%s %6d types %8d spoken tokens" % (v, c.get(v, 0), toks))
print("   sample -o types:", sorted(w for w in ALL if w.endswith("o"))[:25])

print("\n-- every mapped value ending in a bare o --")
hits = sorted(k for k, v in MAP.items() if v.endswith("o") and len(v) > 2)
for k in hits:
    v = MAP[k]
    alt = v[:-1] + "u"
    print("   %-14s -> %-12s omni %-20s spk %-4s | %-12s omni %-20s spk %s%s"
          % (k, v, (OMNI.get(v) or "-")[:20], SPK.get(v, 0),
             alt, (OMNI.get(alt) or "-")[:20], SPK.get(alt, 0),
             "  MANUAL" if k in MAN else ""))

print("\n-- their cards --")
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
want = set(hits)
for ent in E:
    def fields(o):
        return [x for x in (o.get("hw"), o.get("form"), o.get("paradigm"),
                            o.get("tag")) if x]
    all_f = fields(ent) + [x.get("t") for x in ent.get("examples", []) if x.get("t")]
    for s in ent.get("subs", []):
        all_f += fields(s) + [x.get("t") for x in s.get("examples", []) if x.get("t")]
    ks = {key(w) for f in all_f for w in TOK.findall(f)}
    hit = ks & want
    if not hit:
        continue
    print("\n== %s %s   [holds %s]" % (ent.get("hw"), ent.get("tag") or "",
                                       ",".join(sorted(hit))))
    print("   zh:", (ent.get("zh") or "-")[:70])
    for x in ent.get("examples", []):
        print("   § %-50s %s" % (x.get("t", "")[:50], (x.get("zh") or "")[:34]))
    for s in ent.get("subs", []):
        print("   - %-18s %s" % (s.get("form", ""), (s.get("zh") or "")[:46]))
        for x in s.get("examples", []):
            print("       § %-46s %s" % (x.get("t", "")[:46], (x.get("zh") or "")[:32]))
