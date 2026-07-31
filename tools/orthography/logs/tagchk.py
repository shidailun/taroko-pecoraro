"""Adjudicate the tag/paradigm candidates before shipping any of them.

For each: what the map already says about the NEIGHBOURING keys (the
self-contradiction test -- is the right modern word already sitting on his other
spelling of the same word?), his own card and every example that uses it, and a
gloss search of the modern dictionary so the meaning decides rather than the
shape.
"""
import json, sys, pickle, re, io, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
O = pickle.load(open("omni.pkl", "rb"))
OMNI = collections.OrderedDict()
for w, g, _ in O[0]:
    if g:
        OMNI.setdefault(w.lower(), g)
SPK = json.load(open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]

s = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def tk(x):
    return (x.lower().replace("\u2019", "'").replace("\u02bc", "'")
            .replace('"', "'").replace("\u0294", "'").replace("\u0142", "l"))


EX = collections.defaultdict(list)
CARD = {}
for e in E:
    hw, hz = tk(e.get("hw") or ""), (e.get("zh") or "").strip()
    for sb in [e] + e.get("subs", []):
        f = tk(sb.get("form") or sb.get("hw") or "")
        z = (sb.get("zh") or hz).strip()
        if f:
            CARD.setdefault(f, (e.get("hw"), z, e.get("tag") or ""))
        for x in sb.get("examples", []):
            for m in TOK.finditer(x.get("t") or ""):
                EX[tk(m.group(0))].append((x.get("t") or "", x.get("zh") or ""))


def mapline(k):
    v = MM.get(k)
    return "GREEN (no key)" if not v else "%s  [tier %s]" % (v["modern"], v["tier"])


def gloss_search(*pats):
    out = [(SPK.get(w, 0), w, g) for w, g in OMNI.items()
           if any(p in g for p in pats)]
    return sorted(out, reverse=True)[:12]


GROUPS = [
    ("PONGAO / p'ngao", ["p'ngao", "pongao", "pungao", "pngao"],
     ["\u91d1\u9f9c\u5b50", "\u7532\u87f2"]),
    ("QDOAN / qdowan", ["qdowan", "qdoan", "qduan", "qduwan"], ["\u814b\u4e0b"]),
    ("QTQOT family", ["qtqot", "qtqut", "sqtqot", "sqtqut", "qdqut", "qdqdan",
                      "qtqotan", "qmtqot"],
     ["\u9435\u93c8", "\u93c8\u689d", "\u675f\u7e1b", "\u93d0\u929e"]),
    ("SNKAXA / ikaxa", ["ikaxa", "snkaxa", "kaxa", "mkaxa", "kaha", "mkaha",
                        "sngkaxa", "sngkaha"], ["\u524d\u5929", "\u5f8c\u5929"]),
    ("XILWI / silwi", ["silwi", "xilwi", "hilwi", "sirwi"],
     ["\u9435\u7d72", "\u9435"]),
]

for title, keys, pats in GROUPS:
    print("\n" + "=" * 74)
    print(title)
    print("=" * 74)
    for k in keys:
        c = CARD.get(k)
        print(" %-10s map: %-24s %s"
              % (k, mapline(k), ("card %s = %s" % (c[0], c[1][:38])) if c else ""))
        if k in OMNI:
            print("            MODERN: %-4s %s" % (SPK.get(k, ""), OMNI[k][:60]))
        for t, z in EX.get(k, [])[:2]:
            print("            ex: %-46s %s" % (t[:46], z[:32]))
    print("   --- modern words glossed %s ---" % "/".join(pats))
    for n, w, g in gloss_search(*pats):
        print("     %-14s %-4s %s" % (w, n or "", g[:62]))
