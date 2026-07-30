"""For each dead curated key with a live twin: is the twin already brown?

A dead key whose twin is mapped is bookkeeping -- delete it. A dead key whose twin
is GREEN is the real defect: the word was adjudicated and the page never got it.
Consults all three tables respellable() reads, not just the map.
"""
import json, io, sys, re
sys.stdout.reconfigure(encoding="utf-8")
S = "C:/dev/formosan/seediq/taroko-pecoraro/site/"
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

t = io.open(S + "modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
app = io.open(S + "app.js", encoding="utf-8").read()
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def table(name):
    i = app.index("var %s = {" % name)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))


OV, CL = table("WORD_OVERRIDES"), table("CLITIC_FORMS")
manual = json.load(io.open(H + "manual_map.json", encoding="utf-8"))

PAIRS = [("d'xo'", "d'xo"), ("d'yax", "dyax"), ("dxyaq", "d'xyaq"),
         ("knudus", "kn'udus"), ("mpkuda", "mpkuda'"),
         ("mpkudus", "mpk'udus"), ("pkudus", "pk'udus"),
         ("sa so", "sa'so"), ("sdxyaq", "sd'xyaq"), ("slosi", "sl\u00f6si")]
for dead, live in PAIRS:
    where = ("MAP" if live in MAP else "OVERRIDE" if live in OV
             else "CLITIC" if live in CL else "GREEN")
    print("%-9s -> %-11s | live %-10s %-8s %s"
          % (dead, manual.get(dead, ""), live, where,
             MAP.get(live) or OV.get(live) or CL.get(live) or ""))
