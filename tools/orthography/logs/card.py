"""Dump whole entries by headword, with each token's current map value.

Adjudicating a slot means reading his own card: the headword tag (he prints
variants himself -- "KALIP (parfois: QALIP)"), the paradigm line, and the gloss on
the exact sub-entry the green token sits in. This prints all of it, and marks every
token brown/green so the half-mapped slots are visible at a glance.
"""
import json, io, sys, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"

app = io.open(H + "site/app.js", encoding="utf-8").read()


def table(name):
    i = app.index("var %s = {" % name)
    j = app.index("\n  };", i)
    out = {}
    for m in re.finditer(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"', app[i:j]):
        out[m.group(1)] = m.group(2)
    return out


OV, CL = table("WORD_OVERRIDES"), table("CLITIC_FORMS")
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
LX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


def val(w):
    k = key(w)
    if k in OV:
        return OV[k]
    if k in MAP:
        return MAP[k]
    if k in CL:
        return CL[k]
    if k in LX:
        return "<blocked>"
    return None


TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def mark(s):
    out = []
    for w in TOK.findall(s or ""):
        v = val(w)
        out.append("%s[%s]" % (w, v if v else "GREEN"))
    return "  ".join(out)


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
want = [w.lower() for w in sys.argv[1:]]
for ent in E:
    hw = (ent.get("hw") or "")
    if not any(w in hw.lower() or w in key(hw) for w in want):
        continue
    # the tag field is where he prints his own variant spellings -- KALIP carries
    # "(parfois: QALIP)", which decides the q on its own.
    print("\n===== %s %s  %s" % (hw, ent.get("tag") or "",
                                 (ent.get("zh") or ent.get("fr") or "")[:90]))
    if ent.get("paradigm"):
        print("  PARA %s" % mark(ent["paradigm"]))
    for x in ent.get("examples", []):
        print("  ex   %s | %s" % ((x.get("t") or "")[:70], (x.get("zh") or x.get("fr") or "")[:40]))
    for s in ent.get("subs", []):
        print("  -- %-16s %s" % (s.get("form"), (s.get("zh") or s.get("fr") or "")[:70]))
        print("     %s" % mark(s.get("form")))
        if s.get("paradigm"):
            print("     PARA %s" % mark(s["paradigm"]))
        for x in s.get("examples", []):
            print("     ex %s | %s" % ((x.get("t") or "")[:66], (x.get("zh") or x.get("fr") or "")[:36]))
