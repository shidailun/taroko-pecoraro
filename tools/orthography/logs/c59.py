"""Dump every card holding one of the batch-59 candidate tokens, with values.

card.py takes headwords, but a candidate is a token and I do not always know which
headword owns it -- and bash eats the apostrophes and curly quotes in both. So the
token list lives here.
"""
import json, io, sys, re
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


def val(k):
    for T, n in ((OV, "OV"), (MAP, "MAP"), (CL, "CL")):
        if k in T:
            return "%s[%s]" % (T[k], n)
    return "GREEN"


WANT = set(sys.argv[1:]) or {
    "gqoaq", "smt'to", "tbiun", "ptbiun", "tbii", "ptbii", "ktii", "pkloi",
    "mptsadyaq", "siba",
}
for ent in E:
    fs = [ent.get("hw"), ent.get("paradigm")] + [x.get("t") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        fs += [s.get("form"), s.get("paradigm")] + [x.get("t") for x in s.get("examples", [])]
    toks = [key(w) for f in fs if f for w in TOK.findall(f)]
    hit = set(toks) & WANT
    if not hit:
        continue
    print("=====", ent.get("hw"), "|", (ent.get("zh") or "")[:56], "  ->", sorted(hit))
    if ent.get("paradigm"):
        print("   PARA", ent["paradigm"])
    for x in ent.get("examples", [])[:3]:
        print("   ex", x.get("t"), "|", (x.get("zh") or "")[:46])
    for s in ent.get("subs", []):
        print("  --", s.get("form"), (s.get("zh") or "")[:44])
        if s.get("paradigm"):
            print("     PARA", s["paradigm"])
        for x in s.get("examples", [])[:2]:
            print("     ex", x.get("t"), "|", (x.get("zh") or "")[:46])
    print("   VALUES:", "  ".join("%s>%s" % (k, val(k)) for k in sorted(set(toks))
                                  if k in WANT or len(k) > 3)[:700])
