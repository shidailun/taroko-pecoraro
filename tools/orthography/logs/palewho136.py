# -*- coding: utf-8 -*-
"""For the top pale values: which of HIS tokens produce them, under which TIER,
and what his own entry says about the word. Pale means no modern Truku source
vouches for the value; this asks whether a modern Truku source ever COULD.
"""
import io, json, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")

H = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ORTH = os.path.join(H, "tools", "orthography")
SITE = os.path.join(H, "site")

MM = json.load(io.open(os.path.join(ORTH, "modern_map.json"), encoding="utf-8"))
mp = MM["map"] if "map" in MM else MM
app = io.open(os.path.join(SITE, "app.js"), encoding="utf-8").read()
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')
i = app.index("var WORD_OVERRIDES = {")
ov = dict(PAIR.findall(app[i:app.index("\n  };", i)]))

inv = collections.defaultdict(list)          # modern value -> [(his token, tier)]
for k, rec in mp.items():
    v = rec["modern"] if isinstance(rec, dict) else rec
    if isinstance(v, str):
        inv[v.lower()].append((k, (rec.get("tier") if isinstance(rec, dict) else "?")))
for k, v in ov.items():
    inv[v.lower()].append((k, "OV"))

ent = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
a = ent.index("window.ENTRIES = ") + len("window.ENTRIES = ")
E = json.loads(ent[a:ent.rindex("];") + 1])

pale = json.load(io.open(os.path.join(ORTH, "logs", "pale136.json"), encoding="utf-8"))

def toks(s):
    return set(re.findall(r"[A-Za-z'\"-]+", s or ""))

where = collections.defaultdict(list)
for e in E:
    bag = toks(e.get("hw", ""))
    for s in (e.get("subs") or []):
        bag |= toks(s.get("form", ""))
    for ex in (e.get("examples") or []):
        for f in ("tk", "truku", "tw", "text"):
            bag |= toks(ex.get(f, ""))
    for t in bag:
        where[t.lower()].append(e)

LOAN = re.compile(r"emprunt|japon|chinois|jap\.|chin\.", re.I)
NAMEY = re.compile(r"name \(|nom propre|prénom|\bprenom\b", re.I)

def desc(e):
    s = json.dumps(e, ensure_ascii=False)
    marks = []
    if LOAN.search(s):
        marks.append("LOAN")
    if NAMEY.search(s):
        marks.append("NAME")
    for t in (e.get("tags") or []):
        marks.append(str(t)[:18])
    g = e.get("fr") or ""
    if not g:
        for s2 in (e.get("subs") or []):
            g = s2.get("fr") or ""
            if g:
                break
    return e.get("hw", "?"), ";".join(marks)[:34], g[:38]

tiers = collections.Counter()
print("%-12s %-4s %-22s %-6s %-10s %-30s %s"
      % ("pale", "occ", "his token(s)", "tier", "headword", "marks", "gloss"))
print("-" * 120)
for v, n in list(pale.items())[:45]:
    ks = inv.get(v, [])
    tier = ",".join(sorted({t for _, t in ks})) or "-"
    hits = []
    for k, _ in ks:
        hits += where.get(k.lower(), [])
    seen, ents = set(), []
    for e in hits:
        if id(e) not in seen:
            seen.add(id(e)); ents.append(e)
    hw, marks, gl = desc(ents[0]) if ents else ("?", "", "")
    print("%-12s %-4d %-22s %-6s %-10s %-30s %s"
          % (v, n, ",".join(k for k, _ in ks)[:22], tier, hw[:10], marks, gl))

for v, n in pale.items():
    for _, t in inv.get(v, []):
        tiers[t] += n
print("\n-- pale OCCURRENCES by the tier that proposed the value")
for t, c in tiers.most_common():
    print("   %-4s %6d" % (t, c))
