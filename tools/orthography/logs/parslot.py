# -*- coding: utf-8 -*-
"""How big is the paradigm-only population?

FORMS indexes headwords and sub-forms. A token he prints ONLY in a ° paradigm
line — KUGUS's `kgusi`, `kgusan`, `kgusun` — has no alphabetical slot, no page,
and no way to be looked up. Count them before designing anything for them.
"""
import io, json, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")

H = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
s = io.open(os.path.join(H, "site", "entries.js"), encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])

# app.js: TRUKU_TOKEN_G then wordKey() — letters plus his two elision marks,
# " folded to ', lowercased.
TOK = re.compile(r"[A-Za-z'’ʼʔ\"çÇłöÖäÄ]+")
def keys(t):
    out = []
    for m in TOK.findall(t or ""):
        k = re.sub(r"[’ʼʔ\"]", "'", m).lower().strip("'")
        if len(k) >= 2 and re.search(r"[a-z]", k):
            out.append(k)
    return out

forms, par = collections.defaultdict(set), collections.defaultdict(set)
for i, e in enumerate(E):
    for k in keys(e.get("hw")):
        forms[k].add(i)
    for k in keys(e.get("paradigm")):
        par[k].add(i)
    for sb in e.get("subs") or []:
        for k in keys(sb.get("form")):
            forms[k].add(i)
        for k in keys(sb.get("paradigm")):
            par[k].add(i)

only = {k: v for k, v in par.items() if k not in forms}
print("entries %d" % len(E))
print("paradigm token types %d   of which NO form slot anywhere: %d"
      % (len(par), len(only)))
print("unambiguous (exactly one entry prints it): %d"
      % sum(1 for v in only.values() if len(v) == 1))

# how many of those actually occur in a sentence somewhere in the book?
sent = collections.Counter()
for e in E:
    for x in (e.get("examples") or []):
        for k in set(keys(x.get("t"))):
            sent[k] += 1
    for sb in e.get("subs") or []:
        for x in (sb.get("examples") or []):
            for k in set(keys(x.get("t"))):
                sent[k] += 1
attested = {k: sent[k] for k in only if sent[k]}
print("of those, occur in at least one example sentence: %d  (%d sentence hits)"
      % (len(attested), sum(attested.values())))
print()
print("top 20 by sentence hits:")
for k, n in sorted(attested.items(), key=lambda kv: (-kv[1], kv[0]))[:20]:
    ents = sorted(only[k])
    print("   %-16s %4d   printed by %s"
          % (k, n, ", ".join(E[i]["hw"] for i in ents[:3])))
