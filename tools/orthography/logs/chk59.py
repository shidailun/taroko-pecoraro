"""Pre-flight for batch 59: every proposed VALUE priced against both corpora.

b58's lesson twice over -- a real word is not yet the right word, and a value the
build will silently discard is worse than no value at all. So this prints, for each
proposed key->value: whether the key is already claimed (and by which table), what
lexical_map.json says about it (a null is a veto the builder applies AFTER the write),
and the omnibus gloss + speech count of the value. Nothing is written.
"""
import json, io, sys, re, pickle
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
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
MAN = json.load(io.open(H + "tools/orthography/manual_map.json", encoding="utf-8"))

ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)

FIX = [
    ("dao", "daaw"), ("dmao", "dmaaw"), ("mdao", "mdaaw"),
    ("spngao", "spngaw"),
    ("ilnabao", "rnabaw"),
    ("gqoaq", "gquwaq"),
    ("mptsadyaq", "emptseejiq"),
    ("pkloi", "pkrui"),
    ("tbiun", "tbiyun"), ("ptbiun", "ptbiyun"),
    ("nsl'lu", "nsleelug"),
    ("bnaxang", "qnbahang"),
    ("mpkuda", "empkudaw"),
    ("ttuun", "ttuun"), ("ttuon", "ttuun"),
    ("ttuan", "ttuan"), ("t'tuan", "ttuan"),
    ("pt'tui", "pteetui"),
    ("kmpstloong", "kmpstruung"), ("kmpstlngun", "kmpstrngun"),
    ("kmttg'xal", "kmttgxal"),
    ("stbako", "slumak"),
    ("patuxun", "peeutuxun"),
    ("dmbasyaq", "dmbasyaq"),
    ("siba", "siba"),
]
for k, v in FIX:
    src = "OV" if k in OV else ("MAP" if k in MAP else ("CL" if k in CL else "green"))
    cur = OV.get(k) or MAP.get(k) or CL.get(k) or "-"
    veto = ""
    if k in LEX:
        veto = "  LEX_BLOCK(null)" if not LEX[k] else "  LEX=%s" % LEX[k]
    man = "  manual=%s" % MAN[k] if k in MAN else ""
    print("%-14s -> %-13s  now %-5s %-14s  omni %-30s spk %-4s%s%s"
          % (k, v, src, cur, (OMNI.get(v) or "-")[:30], SPK.get(v, 0), veto, man))

print("\n-- neighbours worth seeing --")
for w in ["ttui", "ttuy", "tteetu", "teetu", "teetun", "teetuun", "pteetu",
          "pteetui", "pteetuan", "slumak", "lumak", "spajiq", "pkrui", "sprui",
          "krui", "tbiyun", "tbiyan", "quwaq", "gquwaq", "squwaq", "rnabaw",
          "spngaw", "spngan", "daaw", "dmdaaw", "ddaaw", "seejiq", "emptseejiq",
          "kudaw", "empkudaw", "gxal", "tgxal", "ttgxal", "kmstruun",
          "peeutux", "peutuxun", "sleelug", "psleelug", "qnbahang"]:
    print("   %-14s omni %-34s spk %s" % (w, (OMNI.get(w) or "-")[:34], SPK.get(w, 0)))
