"""What does the built map say about every token on a given card?

  python fam.py BALAX BOLOX
"""
import sys, io, json, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
app = io.open(H + "site/app.js", encoding="utf-8").read()
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def table(n):
    i = app.index("var %s = {" % n)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))


OV, CL = table("WORD_OVERRIDES"), table("CLITIC_FORMS")
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
SM = {"x": "h", "o": "u", "l": "r"}
TOK = re.compile("[A-Za-z\u00c0-\u00ff\u0142\u0141\u0294'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


def val(w):
    k = key(w)
    for tb, n in ((OV, "OV"), (MAP, "MAP"), (CL, "CL")):
        if k in tb:
            return tb[k], n
    return "".join(SM.get(c, c) for c in re.sub("['\u2019\u02bc\"\u0294]", "", k)), "GREEN"


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
for ent in E:
    hw = ent.get("hw") or ""
    if hw.split()[0] not in sys.argv[1:]:
        continue
    fs = [ent.get("hw"), ent.get("paradigm")]
    fs += [x.get("t") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        fs += [s.get("form"), s.get("paradigm")]
        fs += [x.get("t") for x in s.get("examples", [])]
    seen = {}
    for f in fs:
        if not f:
            continue
        for w in TOK.findall(f):
            k = key(w)
            if len(k) > 1 and k not in seen:
                seen[k] = val(w)
    print("=== %s" % hw)
    for k, (v, src) in sorted(seen.items()):
        print("   %-14s %-14s %s" % (k, v, src))
