"""Pre-flight for the -ao residue. Three questions, in order.

(1) Is word-final -ao a thing modern Truku writes AT ALL? Eight of the thirteen are
    identity claims saying it is. Count the modern types, don't assume.
(2) What do the four non-identity oddities' cards actually say -- mdludao>mdrudu,
    pspoxao>pspuhan, nnamao>nnamu, ssinao>ssino. A -ao key landing on -u or -an is
    either a real morphological answer or a slot mismatch.
(3) Every card that holds one, printed whole, with the neighbours' values -- the
    half-brown test, which is what settled QALAS as already-done rather than a
    vein.
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
ALL = set(OMNI) | set(SPK)

print("-- (1) word-final vowel pairs across %d modern types --" % len(ALL))
import collections
c = collections.Counter(w[-2:] for w in ALL if len(w) > 2)
for suf in ("aw", "ao", "au", "ay", "ai", "uy", "ui", "ow", "oo"):
    toks = sum(SPK.get(w, 0) for w in ALL if w.endswith(suf))
    print("   -%-3s %5d types %7d spoken tokens" % (suf, c.get(suf, 0), toks))
print("   the -ao types:", sorted(w for w in ALL if w.endswith("ao"))[:20])

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


TARGETS = ["bubao", "pbubao", "mbubao", "mlb'bao", "nplb'bao", "mql'xao",
           "ql'xao", "ssinao", "psqlasao", "mdludao", "pspoxao", "nnamao"]
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
print("\n-- (2)/(3) the cards --")
for ent in E:
    def fields(o):
        out = [o.get("hw"), o.get("form"), o.get("paradigm"), o.get("tag")]
        return [x for x in out if x]
    all_f = fields(ent) + [x.get("t") for x in ent.get("examples", []) if x.get("t")]
    for s in ent.get("subs", []):
        all_f += fields(s) + [x.get("t") for x in s.get("examples", []) if x.get("t")]
    ks = {key(w) for f in all_f for w in TOK.findall(f)}
    hit = ks & set(TARGETS)
    if not hit:
        continue
    print("\n== %s %s   [holds %s]" % (ent.get("hw"), ent.get("tag") or "",
                                       ",".join(sorted(hit))))
    print("   zh:", (ent.get("zh") or "-")[:66])
    for x in ent.get("examples", []):
        print("   § %-50s %s" % (x.get("t", "")[:50], (x.get("zh") or "")[:32]))
    for s in ent.get("subs", []):
        print("   - %-18s %s" % (s.get("form", ""), (s.get("zh") or "")[:44]))
        for x in s.get("examples", []):
            print("       § %-46s %s" % (x.get("t", "")[:46], (x.get("zh") or "")[:32]))
    print("   values:", ", ".join(
        "%s>%s" % (k, MAP[k]) for k in sorted(ks) if k in MAP))
