"""Did every key in a batch actually land in the BUILT map, with the right value?

manual_map.json is the input, not the artifact. A key can be written there and
never reach site/modern_map.js: a null in lexical_map.json is a standing human
"stay green" decision, it joins lex_block, and `adjudicated` subtracts lex_block
precisely so that a later manual entry cannot quietly overrule it. Verifying the
JSON I just wrote proves nothing about the page.
"""
import json, io, sys, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"
S = "C:/dev/formosan/seediq/taroko-pecoraro/site/"

b = io.open(sys.argv[1], encoding="utf-8").read()
ns = {}
exec(b[b.index("FIX = {"):b.index("\n}\n", b.index("FIX = {")) + 3], ns)
FIX = ns["FIX"]

t = io.open(S + "modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
LEX = json.load(io.open(H + "lexical_map.json", encoding="utf-8"))

bad = []
for k, v in sorted(FIX.items()):
    got = MAP.get(k)
    if got != v:
        why = ("lexical_map null -- a standing stay-green decision"
               if k in LEX and not LEX[k] else
               "in lexical_map as %r" % LEX[k] if k in LEX else "not in the map")
        bad.append((k, v, got, why))
        print("  MISS %-12s want %-12s got %-12s  (%s)" % (k, v, got, why))
print("%d/%d keys landed" % (len(FIX) - len(bad), len(FIX)))
