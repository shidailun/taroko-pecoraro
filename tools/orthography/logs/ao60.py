"""Batch 60 seed: the -ao keys whose VALUE does not end -aw.

The charRules edit settled the green half of word-final -ao. The brown half is a
different question and the DOM answered part of it: exactly one span on the page
still ends -au, `psqrasau`. Ask the map directly instead -- every key ending -ao,
grouped by what its value ends in -- so the 13 exceptions to the 267 are read as a
list rather than found one at a time. For each, price both endings in both corpora
so an exception that is EARNING its exception can be told from one that is not.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
MAN = json.load(io.open(H + "tools/orthography/manual_map.json", encoding="utf-8"))
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)


def price(w):
    return "omni %-22s spk %s" % ((OMNI.get(w) or "-")[:22], SPK.get(w, 0))


ends = collections.Counter()
odd = []
for k, v in sorted(MAP.items()):
    if not k.endswith("ao"):
        continue
    ends[v[-2:]] += 1
    if not v.endswith("aw"):
        odd.append((k, v))

print("-- what his word-final -ao becomes, over %d keys --" % sum(ends.values()))
for suf, n in ends.most_common():
    print("   -%-6s %4d" % (suf, n))

print("\n-- the %d that are not -aw --" % len(odd))
for k, v in odd:
    alt = v[:-2] + "aw" if len(v) > 2 else v
    print("   %-16s -> %-16s %s" % (k, v, price(v)))
    print("   %-16s    %-16s %s%s%s"
          % ("", alt, price(alt),
             "  MANUAL" if k in MAN else "",
             "  LEXNULL" if k in LEX and not LEX[k] else ""))
