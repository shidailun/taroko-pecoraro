# -*- coding: utf-8 -*-
"""Per-item dossier for the 71 informant answers (batch 242).

For each of the 71 raw tokens the translator answered, print: current map
value + source tier, his card's own gloss(es), whether the answer is a listed
modern word, and whether the answer's gloss shares a meaningful character with
his gloss (the batch 204/232 different-root test, stoplist-derived).
"""
import collections
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.abspath(".")
SITE = os.path.join(H, "site")
ORTH = os.path.join(H, "tools", "orthography")


def read(p):
    return io.open(p, encoding="utf-8").read()


def entries_json():
    s = read(os.path.join(SITE, "entries.js"))
    return json.loads(s[s.index("["):s.rindex("]") + 1])


def modern_map():
    t = read(os.path.join(SITE, "modern_map.js"))
    a = t.index("window.MODERN_MAP = {")
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def app_table(name):
    t = read(os.path.join(SITE, "app.js"))
    a = t.index("var " + name + " = {")
    b = t.index("\n  };", a)
    return dict((m.group(1), m.group(2)) for m in
                re.finditer(r'"([^"]+)"\s*:\s*"([^"]*)"', t[a:b]))


GL = [json.load(io.open(os.path.join(ORTH, n), encoding="utf-8"))
      for n in ("attested_gloss.json", "bible_gloss.json", "parquet_gloss.json")]
LEX = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"),
                            encoding="utf-8")))


def glosses(w):
    out = []
    for D in GL:
        g = D.get(w) or []
        for x in (g if isinstance(g, list) else [g]):
            x = str(x).strip()
            if x and x not in out:
                out.append(x)
    return out


ZH = re.compile(r"[㐀-鿿]")
MM = modern_map()
CLI = app_table("CLITIC_FORMS")
OV = app_table("WORD_OVERRIDES")


def wordKey(w):
    return re.sub(r"[’ʼ\"ʔ]", "'", (w or "").lower()).replace("ł", "l")


def charRules(w):
    return wordKey(w).replace("o", "u").replace("l", "r").replace("x", "h")


def val(w):
    k = wordKey(w)
    if k in CLI:
        return k, "clitic"
    if k in OV:
        return OV[k], "override"
    if k in MM:
        return MM[k], "map"
    return charRules(k), "charrule"


# metalinguistic strip, batch 218 (approx: strip common apparatus phrases)
META = [ "的詞根", "…'s root", "的過去式", "參見", "見" ]


def strip_meta(s):
    for m in META:
        s = s.replace(m, "")
    return s


# batch 232's stoplist: commonest Han characters across the register's own
# glosses, cut at the depth that reproduces every character already named as
# noise (著 at rank 26 -> cut 30). Approximate here from GL corpus.
_CHARCOUNT = collections.Counter()
for D in GL:
    for v in D.values():
        for x in (v if isinstance(v, list) else [v]):
            _CHARCOUNT.update(ZH.findall(str(x)))
STOP = set(c for c, _ in _CHARCOUNT.most_common(30))


def shares_char(a, b):
    ca = set(ZH.findall(strip_meta(a))) - STOP
    cb = set(ZH.findall(strip_meta(b))) - STOP
    return ca & cb


# ---- his book ---------------------------------------------------------
ENT = entries_json()
TOK = re.compile(r"[A-Za-zÀ-ÿł'’ʼ\"]+")


def truku_fields(e):
    heads, sents = [], []
    heads.append(e.get("hw") or "")
    for p in (e.get("paradigm") or []):
        heads.append(p if isinstance(p, str) else (p.get("form") or ""))
    for x in (e.get("examples") or []):
        sents.append((x.get("t") or "", x))
    for s in (e.get("subs") or []):
        heads.append(s.get("form") or "")
        for p in (s.get("paradigm") or []):
            heads.append(p if isinstance(p, str) else (p.get("form") or ""))
        for x in (s.get("examples") or []):
            sents.append((x.get("t") or "", x))
    return heads, sents


DEFN = collections.defaultdict(list)   # wordKey -> [(entry, sub or None)]
SEEN = collections.defaultdict(list)

for e in ENT:
    for f, s in ([(e.get("hw"), None)] +
                 [(x.get("form"), x) for x in (e.get("subs") or [])]):
        for t in TOK.findall(f or ""):
            DEFN[wordKey(t)].append((e, s))
    heads, sents = truku_fields(e)
    here = set()
    for f in heads:
        for t in TOK.findall(f):
            here.add(wordKey(t))
    for k in here:
        SEEN[k].append(e)


def gl_of(o):
    g = (o.get("zh") or "").strip()
    return "" if g and not re.sub(r"[?？／\s]", "", g) else g


def card_for(k):
    defs = sorted(DEFN.get(k) or [],
                  key=lambda es: (not gl_of(es[1] or es[0]), es[1] is None))
    if not defs:
        return None
    e, sub = defs[0]
    o = sub or e
    return {
        "name": (o.get("form") if sub else o.get("hw")) or "",
        "parent": e.get("hw") if sub else None,
        "gloss": gl_of(o),
        "tag": (o.get("paradigm") if sub else o.get("tag")) or
               (e.get("tag") if sub else ""),
    }


# ---- the 71 answers -----------------------------------------------------
ANSWERS = json.load(io.open(os.path.join(H, ".scratch", "b242", "answers.json"),
                            encoding="utf-8"))

rows = []
for item in ANSWERS:
    raw = item["raw"]
    ans = item["ans"]
    k = wordKey(raw)
    cur, src = val(raw)
    card = card_for(k)
    ans_words = re.findall(r"[A-Za-zÀ-ÿ'’ʼ]+", ans)
    ans_info = []
    for aw in ans_words:
        awk = wordKey(aw)
        listed = awk in LEX
        gl = glosses(awk)
        ans_info.append({"w": aw, "listed": listed, "gloss": gl})
    rows.append({
        "n": item["n"], "raw": raw, "answer": ans,
        "cur_value": cur, "cur_src": src,
        "card": card, "ans_words": ans_info,
    })

io.open(os.path.join(H, ".scratch", "b242", "dossier.json"), "w",
        encoding="utf-8").write(json.dumps(rows, ensure_ascii=False, indent=1))
print("wrote dossier.json: %d rows" % len(rows))
