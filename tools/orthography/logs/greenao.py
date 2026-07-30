"""Every green token whose shape the map already decides 267 times out of 280.

His final -ao is -aw in 267 of the 280 mapped keys that end in it. charRules does
NOT know that: it only does x>h, o>u, l>r, so a green -ao token prints -au, a shape
the modern orthography does not use word-finally. Every green -ao token is therefore
printing a fake word, and the fix is the same one the map has already made 267 times.

Prints each with its count, its card, and whether -aw is attested anywhere.
"""
import json, io, sys, re, collections, pickle
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
app = io.open(H + "site/app.js", encoding="utf-8").read()
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def table(n):
    i = app.index("var %s = {" % n)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))


OV, CL = table("WORD_OVERRIDES"), table("CLITIC_FORMS")
PROSE = set()
for n in ("FORM_PROSE", "TAG_PROSE"):
    i = app.index("var %s = {}" % n)
    for s in re.findall(r'"([^"]*)"', app[i:app.index('.split(" ")', i)]):
        PROSE |= set(s.split())
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])

ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)

TOK = re.compile("[A-Za-z\u00c0-\u00ff\u0142\u0141\u0294'\u2019\u02bc\"]+")
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


SUF = sys.argv[1] if len(sys.argv) > 1 else "ao"
NEW = sys.argv[2] if len(sys.argv) > 2 else "aw"
cnt, card = collections.Counter(), {}
for ent in E:
    fs = [ent.get("hw"), ent.get("paradigm")] + [x.get("t") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        fs += [s.get("form"), s.get("paradigm")] + [x.get("t") for x in s.get("examples", [])]
    for f in fs:
        if not f:
            continue
        for w in TOK.findall(f):
            k = key(w)
            if len(k) > 1 and k.endswith(SUF) and k not in MAP and k not in OV \
                    and k not in CL and k not in PROSE:
                cnt[k] += 1
                card.setdefault(k, (ent.get("hw") or "").split(" ")[0])
print("green types ending -%s: %d   (%d occurrences)" % (SUF, len(cnt), sum(cnt.values())))
for k, n in cnt.most_common():
    v = k[:-len(SUF)] + NEW
    g = OMNI.get(v)
    print("%3dx %-14s -> %-14s [%s]  omni %-28s speech %s"
          % (n, k, v, card[k], (g or "-")[:28], SPK.get(v, 0)))
