"""Batch 62 pre-flight: who OWNS each key, and what the value costs.

The flat map cannot split one key across two cards, so before rewriting a key I
have to know it belongs to the card whose gloss I am reasoning from. slut and
mslut and pslut are the risky ones -- they are short, common shapes, and if some
other card of his spells a fat-word or a blunt-word that way then the value it has
today may be right for THAT card and wrong only for S'LUT.

Prints, per key: every card it occurs on with the gloss, its current value and
that value's own attestation, the proposed value and ITS attestation, whether
lexical_map vetoes it, and who else already points at the proposed value.
"""
import io, sys, json, pickle, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
MAN = json.load(io.open(H + "tools/orthography/manual_map.json", encoding="utf-8"))
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


PROP = {
    "tabe": "sakur", "ptabe": "psakur",
    "ttuun": "ttuun", "ttuon": "ttuun", "ttuan": "ttuan", "t'tuan": "ttuan",
    "ms'lut": "msdlut", "mslut": "msdlut",
    "ps'lut": "psdlut", "pslut": "psdlut",
    "s'lut": "sdlut", "slut": "sdlut",
    "mksia": "msqsiya",
}
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
            if k in OWN and (hw, (g or "")[:30]) not in OWN[k]:
                OWN[k].append((hw, (g or "")[:30]))


def att(v):
    o, s = OMNI.get(v), SPK.get(v, 0)
    return ("OMNI %-22s spk %d" % (o[:22], s)) if o else \
           ("-- BLIND --%s" % ("  spk %d" % s if s else ""))


for k, v in PROP.items():
    cur = MAP.get(k, "(green)")
    veto = "  !!LEXNULL!!" if (k in LEX and not LEX[k]) else ""
    print("\n%-10s %-12s -> %-10s%s" % (k, cur, v, veto))
    print("   now  %-12s %s" % (cur, att(cur) if cur != "(green)" else ""))
    print("   prop %-12s %s" % (v, att(v)))
    if k in MAN:
        print("   manual_map already says: %s" % MAN[k])
    other = [x for x in MAP if MAP[x] == v and x != k]
    if other:
        print("   value already used by: %s" % other)
    for hw, g in OWN[k][:6]:
        print("      card [%-14s] %s" % (hw[:14], g))
    if not OWN[k]:
        print("      (no card found -- CHECK)")

print("\n-- lexical_map entries touching these --")
for k in sorted(LEX):
    if k.lstrip("_") in PROP or k.lstrip("_") in ("tbian", "tbiyan", "tabe"):
        print("   %-12s = %s" % (k, json.dumps(LEX[k], ensure_ascii=False)[:400]))
