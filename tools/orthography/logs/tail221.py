# -*- coding: utf-8 -*-
"""[batch 221] Batch 204's different-root test, mechanized over the whole tail.

For each remaining sole-blocker value: reverse it to HIS token (the blocker
ranking reports map VALUES, batch 219), pull HIS Chinese for it -- headword
gloss first, falling back to the example gloss and marked when it does (batch
203: a sentence gloss is not the word's gloss) -- then ask the register for
every word whose gloss shares a Han character with his, and report the one
CLOSEST IN SHAPE to his token.

It rules nothing. It prices the seam: a row whose nearest meaning-carrier is
5+ edits away on a different root is the refusal batch 204 describes, and a row
whose nearest carrier is 0-2 edits away is a question worth a person.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\dev\formosan\seediq\taroko-pecoraro"
ORTH = os.path.join(ROOT, "tools", "orthography")

mp = io.open(os.path.join(ROOT, "site", "modern_map.js"), encoding="utf-8").read()
a = mp.index("window.MODERN_MAP = {")
MM = dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                     mp[a:mp.index("\n};", a) + 2], re.M))
s = io.open(os.path.join(ROOT, "site", "entries.js"), encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])
g = json.load(io.open(os.path.join(ORTH, "attested_gloss.json"), encoding="utf-8"))

TOK = re.compile(r"[A-Za-z\u00c0-\u024f'\u2019\u02bc\"]+")
HAN = re.compile(r"[\u4e00-\u9fff]")


def wordkey(w):                        # app.js wordKey(), exactly
    return re.sub(r'[\u2019\u02bc"\u0294]', "'",
                  (w or "").lower()).replace("\u0142", "l")


def val(raw):
    k = wordkey(raw)
    v = MM.get(k)
    if v is None:
        v = k.replace("o", "u").replace("l", "r").replace("x", "h")
    return v


def G(w):
    v = g.get(w)
    return " ".join(v) if isinstance(v, list) else (v or "")


REG = [(w, set(HAN.findall(G(w)))) for w in sorted(g) if HAN.search(G(w))]


def ed(a, b):
    if abs(len(a) - len(b)) > 6:
        return 99
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


# his token -> (his Chinese, whether it came from the headword or an example)
GLOSS, WHERE = {}, {}


def walk(e, hw):
    f = e.get("hw") or e.get("form") or ""
    zh = (e.get("zh") or "").strip()
    for t in TOK.findall(f):
        k = wordkey(t)
        if zh and k not in GLOSS:
            GLOSS[k], WHERE[k] = zh, "head"
    for x in (e.get("examples") or []):
        xz = (x.get("zh") or "").strip()
        for t in TOK.findall(x.get("t") or ""):
            k = wordkey(t)
            if xz and k not in GLOSS:
                GLOSS[k], WHERE[k] = xz, "EX"
    for sb in (e.get("subs") or []):
        walk(sb, hw)


for e in E:
    walk(e, e.get("hw", "?"))

# every token in the book, so a blocker VALUE can be reversed to his spelling
BACK = {}
for k in list(GLOSS):
    BACK.setdefault(val(k), []).append(k)

WANT = sys.argv[1].split()
print("%-12s %-11s %-4s %s" % ("value", "his token", "src", "nearest register word carrying his Chinese"))
for target in WANT:
    toks = BACK.get(target) or [k for k, v in MM.items() if v == target]
    if not toks:
        print("%-12s (no token in the book -- reverse it by hand)" % target)
        continue
    tok = toks[0]
    zh = GLOSS.get(tok, "")
    chars = set(HAN.findall(zh))
    # drop characters that are pure apparatus, batch 218
    chars -= set("的詞根同上之動形註引申等音義不明")
    if not chars:
        print("%-12s %-11s %-4s (no Chinese of his to test)"
              % (target, tok, WHERE.get(tok, "-")))
        continue
    best = []
    for w, cs in REG:
        if cs & chars:
            best.append((ed(target, w), w, "".join(sorted(cs & chars))))
    best.sort()
    show = "  ".join("%s(%d)%s" % (w, d, sh) for d, w, sh in best[:3]) or "(none)"
    print("%-12s %-11s %-4s %s" % (target, tok, WHERE.get(tok, "-"), show))
