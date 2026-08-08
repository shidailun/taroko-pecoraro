# -*- coding: utf-8 -*-
"""Does he write `xx-`, and does modern Truku write `hh-`? Counts only."""
import collections
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORTH = os.path.join(ROOT, "tools", "orthography")

AM = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"),
                           encoding="utf-8")))
AG = json.load(io.open(os.path.join(ORTH, "attested_gloss.json"), encoding="utf-8"))
hh = sorted(w for w in AM if w.startswith("hh"))
print("modern register: %d words start hh-" % len(hh))
for w in hh[:14]:
    g = AG.get(w) or []
    g = g if isinstance(g, list) else [g]
    print("   %-13s %s" % (w, "／".join(g)[:56]))

s = io.open(os.path.join(ROOT, "site", "entries.js"), encoding="utf-8").read()
blob = json.dumps(json.loads(s[s.index("["):s.rindex("]") + 1]), ensure_ascii=False)
TOK = re.compile(u"[A-Za-zçüö’ʼ\"']+")
c = collections.Counter(w.lower() for w in TOK.findall(blob))
xx = {w: n for w, n in c.items() if w.startswith("xx")}
print("\nhis book: %d xx- types, %d occurrences" % (len(xx), sum(xx.values())))
for w, n in sorted(xx.items(), key=lambda r: -r[1])[:14]:
    print("   %-13s %d" % (w, n))

# and the doubled-onset habit generally: how often does he double an initial C?
dbl = {w: n for w, n in c.items()
       if len(w) > 2 and w[0] not in "aeiou'\"" and w[1] == w[0]}
print("\nhis doubled-onset types: %d, occurrences %d"
      % (len(dbl), sum(dbl.values())))
