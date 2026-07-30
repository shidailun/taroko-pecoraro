"""Every key/token whose shape contains his g'xal-'gxal' (親戚/伙伴), with its value.

kmttg'xal is the tell: modern Truku writes gxal 親戚, tgxal 團聚, ttgxal -- a real
x, not an h. charRules sweeps his x to h unconditionally, so every unmapped token
of this family prints ghal, which is not a word. Before touching any of them, list
what the family actually contains and what each one currently prints.
"""
import json, io, sys, re, collections
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
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
TOK = re.compile("[A-Za-z\u00c0-\u00ff\u0142\u0141\u0294'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


PAT = sys.argv[1] if len(sys.argv) > 1 else "xal"
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
            if PAT in k:
                cnt[k] += 1
                card.setdefault(k, (ent.get("hw") or "").split(" ")[0])
for k, n in cnt.most_common():
    src = "OV" if k in OV else ("MAP" if k in MAP else ("CL" if k in CL else "GREEN"))
    v = OV.get(k) or MAP.get(k) or CL.get(k) or "-"
    print("%3dx %-16s %-6s %-18s [%s]" % (n, k, src, v, card[k]))
