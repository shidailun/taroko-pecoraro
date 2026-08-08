# -*- coding: utf-8 -*-
"""batch 219 / 229's dropped-letter class, mechanised.

A pale value that is one INSERTION short of a shape his own family spells:
`tgrgri` beside `tgrgrigun`, `pqeli` beside the `Pxoqel` paradigm's `phqili`.
Both were found by hand. This asks the whole pale-blocker set at once.
"""
import collections, io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.abspath(".")
SITE = os.path.join(H, "site"); ORTH = os.path.join(H, "tools", "orthography")
rd = lambda p: io.open(p, encoding="utf-8").read()

def entries():
    s = rd(os.path.join(SITE, "entries.js"))
    return json.loads(s[s.index("["):s.rindex("]") + 1])

def modern_map():
    t = rd(os.path.join(SITE, "modern_map.js")); a = t.index("window.MODERN_MAP = {")
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$', t[a:t.index("\n};", a) + 2], re.M))

def app_table(name):
    t = rd(os.path.join(SITE, "app.js")); a = t.index("var " + name + " = {")
    return dict((m.group(1), m.group(2)) for m in
                re.finditer(r'"([^"]+)"\s*:\s*"([^"]*)"', t[a:t.index("\n  };", a)]))

MM = modern_map(); CLI = app_table("CLITIC_FORMS"); OV = app_table("WORD_OVERRIDES")
_v = rd(os.path.join(SITE, "verified.js"))
_a = _v.index("window.MODERN_VERIFIED = {")
VER = set(re.findall(r'^  "(.+?)":', _v[_a:], re.M))   # two-space keys (batch 207)
LEX = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"), encoding="utf-8")))
G = {}
for n in ("attested_gloss.json", "bible_gloss.json", "parquet_gloss.json"):
    for k, v in json.load(io.open(os.path.join(ORTH, n), encoding="utf-8")).items():
        G.setdefault(k, []).extend(v if isinstance(v, list) else [v])
KNOWN = LEX | set(G)

wordKey = lambda w: re.sub(r"[’ʼ\"ʔ]", "'", (w or "").lower()).replace("ł", "l")
charRules = lambda w: wordKey(w).replace("o", "u").replace("l", "r").replace("x", "h")
def val(w):
    k = wordKey(w)
    if k in CLI: return k
    if k in OV: return OV[k]
    if k in MM: return MM[k]
    return charRules(k)

E = entries(); TOK = re.compile(r"[A-Za-zÀ-ÿł'’ʼ\"]+")
his_tokens = collections.Counter()
def walk(e):
    yield e.get("hw") or ""
    for p in (e.get("paradigm") or []):
        yield p if isinstance(p, str) else (p.get("form") or "")
    for x in (e.get("examples") or []): yield x.get("t") or ""
    for s in (e.get("subs") or []):
        yield s.get("form") or ""
        for p in (s.get("paradigm") or []):
            yield p if isinstance(p, str) else (p.get("form") or "")
        for x in (s.get("examples") or []): yield x.get("t") or ""
for e in E:
    for f in walk(e):
        for t in TOK.findall(f): his_tokens[wordKey(t)] += 1

# every DARK value his book renders, and the token behind it
DARKVALS = {}
for k in his_tokens:
    v = val(k)
    if all(part in VER for part in v.split()): DARKVALS.setdefault(v, []).append(k)

ROWS = json.load(io.open(os.path.join(H, ".scratch", "b235", "blocked.json"),
                         encoding="utf-8"))
pale = collections.Counter()
for r in ROWS:
    for p in r["pale"]: pale[p] += 1
print("pale blocking types: %d   dark values in the book: %d"
      % (len(pale), len(DARKVALS)))

A = "abcdefghijklmnopqrstuvwxyz'"
hits = []
for p in sorted(pale):
    cands = set()
    for i in range(len(p) + 1):
        for c in A:
            q = p[:i] + c + p[i + 1:] if False else p[:i] + c + p[i:]
            if q == p: continue
            listed = q in KNOWN
            inside = [v for v in DARKVALS if q in v and v != p]
            if listed or inside:
                cands.add((q, listed, tuple(sorted(inside))[:3]))
    if cands: hits.append((p, sorted(cands)))
print("pale values with at least one single-insertion candidate: %d of %d"
      % (len(hits), len(pale)))
tot = sum(len(c) for _, c in hits)
print("candidate shapes in total: %d" % tot)
listed_only = [(p, [c for c in cs if c[1]]) for p, cs in hits]
listed_only = [(p, cs) for p, cs in listed_only if cs]
print("...of which the candidate is a LISTED modern word: %d values, %d shapes"
      % (len(listed_only), sum(len(c) for _, c in listed_only)))
io.open(".scratch/b241/rows.txt", "w", encoding="utf-8").write(
    "\n".join("%-14s %s" % (p, " | ".join("%s%s%s" % (q, "*" if l else "",
              ("<" + ",".join(ins)) if ins else "") for q, l, ins in cs))
              for p, cs in hits))
print("rows written to .scratch/b241/rows.txt")
