"""Gloss-first lookup for the green tail.

Usage: python look.py TOKEN [TOKEN...]

For each Pecoraro token it prints, in order:
  1. where it lives in the book, with his own Chinese and French definition
  2. the rule-consistent candidate spellings, with omnibus + speech attestation
  3. omnibus words whose CHINESE GLOSS overlaps his, ranked by shape distance
       -- this is the half that matters: search the meaning, not the shape
"""
import sys, json, pickle, re, collections, difflib
sys.stdout.reconfigure(encoding="utf-8")

H = "C:/dev/formosan/seediq/taroko-pecoraro"
O = pickle.load(open("omni.pkl", "rb"))
ROWS = O[0]
SPK = json.load(open(H + "/tools/orthography/spoken_truku.json", encoding="utf-8"))
s = open(H + "/site/entries.js", encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])
t = open(H + "/site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
TOK = re.compile(r"[A-Za-zÀ-ÿłŁʔ'’\"]+")
BY_WORD = collections.defaultdict(list)
for w, g, _ in ROWS:
    BY_WORD[w.lower()].append(g)

def key(w):
    return w.lower().replace('"', "'").replace("\u2019", "'")

# every field that reaches the screen as Truku, with the gloss that governs it
def occurrences(tok):
    out = []
    for e in E:
        zh, fr = e.get("zh") or "", e.get("fr") or ""
        flds = [("hw", e.get("hw"), zh, fr), ("par", e.get("paradigm"), zh, fr),
                ("xref", e.get("crossRef"), zh, fr)]
        flds += [("ex", x.get("t"), x.get("zh") or zh, x.get("fr") or fr)
                 for x in e.get("examples", [])]
        for sb in e.get("subs", []):
            szh, sfr = sb.get("zh") or zh, sb.get("fr") or fr
            flds += [("sub", sb.get("form"), szh, sfr), ("par", sb.get("paradigm"), szh, sfr)]
            flds += [("ex", x.get("t"), x.get("zh") or szh, x.get("fr") or sfr)
                     for x in sb.get("examples", [])]
        for fld, txt, z, f in flds:
            if txt and any(key(m.group(0)) == tok for m in TOK.finditer(txt)):
                out.append((fld, txt, z, f, e.get("hw")))
    return out

# the swaps the book actually attests, applied as alternatives rather than a rule
SWAP = [("o", "u"), ("x", "h"), ("l", "r"), ("ç", "x"), ("k", "q"), ("q", "k"),
        ("e", "i"), ("d", "j"), ("t", "c"), ("ai", "ay"), ("ao", "aw"),
        ("ui", "uy"), ("oa", "uwa")]
def candidates(tok):
    seen = {tok.replace("'", "")}
    frontier = [tok.replace("'", "")]
    for _ in range(3):
        nxt = []
        for w in frontier:
            for a_, b in SWAP:
                if a_ in w:
                    v = w.replace(a_, b)
                    if v not in seen:
                        seen.add(v); nxt.append(v)
        frontier = nxt
    return sorted(seen)

def zh_chars(g):
    return set(re.findall(r"[\u4e00-\u9fff]", g or ""))

def report(tok):
    tok = key(tok)
    print("=" * 72)
    print("TOKEN  %-16s  current: %s" % (tok, MAP.get(tok, "— GREEN")))
    occ = occurrences(tok)
    mine = set()
    for fld, txt, z, f, hw in occ[:6]:
        print("   %-4s %-40s | %-8s %s" % (fld, txt[:40], (hw or "")[:8], (z or "")[:34]))
        mine |= zh_chars(z)
    if len(occ) > 6:
        print("   ... %d occurrences total" % len(occ))
    hit = [(c, BY_WORD.get(c, []), SPK.get(c, 0)) for c in candidates(tok)]
    hit = [h for h in hit if h[1] or h[2]]
    print("  candidates attested:")
    if not hit:
        print("     (none of %d rule-consistent shapes is in any corpus)" % len(candidates(tok)))
    for c, gs, n in sorted(hit, key=lambda x: -(len(x[1]) * 100 + x[2])):
        print("     %-14s omni %-2d %-26s speech %d" % (c, len(gs), (gs[0] if gs else "")[:26], n))
    # gloss-first: what modern word carries his meaning, whatever its shape?
    if mine:
        scored = []
        for w, gs in BY_WORD.items():
            for g in gs:
                ov = zh_chars(g) & mine
                if len(ov) >= 2 and len(ov) / max(1, len(zh_chars(g))) >= 0.34:
                    scored.append((difflib.SequenceMatcher(None, tok.replace("'", ""), w).ratio(),
                                   len(ov), w, g))
        scored.sort(reverse=True)
        print("  modern words whose gloss overlaps his:")
        for r, n, w, g in scored[:8]:
            print("     %-14s %-26s shape %.2f  speech %d" % (w, g[:26], r, SPK.get(w, 0)))
        if not scored:
            print("     (nothing in the omnibus is glossed like it)")

for tok in sys.argv[1:]:
    report(tok)
