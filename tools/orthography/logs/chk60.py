"""Pre-flight for batch 60 -- the word-final -ao residue.

Every proposal here is a CORRECTION of a shipped brown value except pbbagi, which
is green. That raises the bar: a shipped value has already been asserted once, so
replacing it needs the new value priced in both corpora AND the old one shown to
be unattested or in the wrong slot. Print, per key: what table holds it now, the
current value's price, the proposed value's price, the lexical_map veto, and the
whole modern neighbourhood the proposal comes from.

Two of the thirteen -ao oddities are NOT here on purpose: nnamao>nnamu (namu
'yours-pl' 12x, a real -u word) and q'nao>qusul (the tier-X garlic substitution).
Both earn their exception.
"""
import io, sys, json, pickle, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
MAN = json.load(io.open(H + "tools/orthography/manual_map.json", encoding="utf-8"))
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
app = io.open(H + "site/app.js", encoding="utf-8").read()
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def table(n):
    i = app.index("var %s = {" % n)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))


OV, CL = table("WORD_OVERRIDES"), table("CLITIC_FORMS")
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)
ALL = sorted(set(OMNI) | set(SPK))

PROP = [
    ("psqlasao", "psqrasaw", r"qras|qaras"),
    ("pspoxao", "pspuhaw", r"spuh|smapuh"),
    ("ssinao", "ssinaw", r"sinaw"),
    ("mlb'bao", "mrbnaw", r"rbnaw"),
    ("nplb'bao", "nprbnaw", r"rbnaw"),
    ("bubao", "bgbaw", r"bgbag|bgbaw"),
    ("mbubao", "embgbaw", r"bgbag|bgbaw"),
    ("pbubao", "pbgbaw", r"bgbag|bgbaw"),
    ("pbbagi", "pbgbagi", r"bgbag"),
    ("mql'xao", "mkraaw", r"kraaw"),
    ("ql'xao", "kraaw", r"kraaw"),
    ("mdludao", "mdrudaw", r"rudaw"),
]


def price(w):
    return "omni %-26s spk %s" % ((OMNI.get(w) or "-")[:26], SPK.get(w, 0))


for k, new, fam in PROP:
    src = ("OV" if k in OV else "MAP" if k in MAP else
           "CL" if k in CL else "GREEN")
    cur = OV.get(k) or MAP.get(k) or CL.get(k)
    print("\n== %-12s [%s]" % (k, src))
    print("   now  %-14s %s" % (cur or "-", price(cur) if cur else ""))
    print("   prop %-14s %s" % (new, price(new)))
    flags = []
    if k in MAN:
        flags.append("in manual_map (%s)" % MAN[k])
    if k in LEX:
        flags.append("LEXNULL" if not LEX[k] else "lex=%s" % LEX[k])
    if new in MAP.values():
        flags.append("value already used by " +
                     ",".join(x for x in MAP if MAP[x] == new)[:60])
    print("   flags:", "; ".join(flags) or "-")
    r = re.compile(fam)
    n = 0
    for w in ALL:
        if r.search(w):
            print("      %-16s %-34s spk %s"
                  % (w, (OMNI.get(w) or "-")[:34], SPK.get(w, 0)))
            n += 1
            if n >= 16:
                print("      ...")
                break

print("\n-- the -aw hortative slot, family by family --")
for stem in ("qras", "spuh", "sinaw", "rbnaw", "bgba", "raaw", "rudaw"):
    hits = [w for w in ALL if stem[:4] in w and w.endswith("aw")]
    print("   %-8s %s" % (stem, ", ".join(
        "%s(%s)" % (w, SPK.get(w, 0)) for w in hits[:12]) or "-"))
