# -*- coding: utf-8 -*-
"""Systematic stem-shape variants, probed against the corpus.

KLUI is the shape.  Batch 19 pinned kluyun / skluyun / pskluyun to identity on
the finding that "there is no modern -un form of any -uwi root on record, so
pskluwiun would be an invention".  The finding was wrong, and wrong in an
instructive way: THE STEM SHORTENS BEFORE THE SUFFIX.  kluwi + un is not
kluwiun, it is klwiun (1x), and sklwiun is 22x 奇妙.  Nobody found them because
everybody searched for the long stem.

So the probe: for every value on screen that no corpus vouches for, apply a
short list of mechanical stem alternations and ask whether the RESULT is
attested.  No glosses involved — this is a spelling question, and the gloss is
only printed so the hit can be read.
"""
import collections, io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = r"C:\dev\formosan\seediq\taroko-pecoraro"
D = os.path.join(H, "tools", "orthography")
sys.path.insert(0, D)
sys.path.insert(0, ".")
import tables as T

V = dict((m.group(1), int(m.group(2))) for m in re.finditer(
    r'^  "(.*)": (\d),$', io.open(os.path.join(H, "site", "verified.js"),
                                  encoding="utf-8").read(), re.M))
NAME = re.compile(r"name|emprunt|nom", re.I)


def val(w):
    k = T.key(w)
    return T.CL.get(k) or T.OV.get(k) or T.MAP.get(k) or T.crule(k)


def variants(v):
    """mechanical stem alternations, each named so a hit can be judged"""
    out = []
    # the KLUI shape: a shortening stem before a suffix
    for a, b in (("uy", "wi"), ("oy", "wi"), ("uwi", "wi"), ("uwa", "wa"),
                 ("owa", "wa"), ("uwu", "wu"), ("iya", "ya"), ("iyu", "yu")):
        if a in v:
            out.append((v.replace(a, b, 1), "%s>%s" % (a, b)))
    # the reverse: a stem that keeps its vowel where we dropped it
    for a, b in (("wi", "uwi"), ("wa", "uwa"), ("ya", "iya")):
        if a in v:
            out.append((v.replace(a, b, 1), "%s>%s" % (a, b)))
    # medial schwa, written and unwritten
    for n in range(1, len(v) - 1):
        if v[n] == "e":
            out.append((v[:n] + v[n + 1:], "drop e@%d" % n))
    for n in range(1, len(v) - 1):
        if v[n] not in "aeiou" and v[n + 1] not in "aeiou":
            out.append((v[:n + 1] + "e" + v[n + 1:], "add e@%d" % n))
    return out


gl = collections.defaultdict(set)
occ = collections.Counter()
home, tag = {}, {}
for e in T.entries():
    tg, hw, ezh = (e.get("tag") or ""), e.get("hw") or "?", e.get("zh") or ""
    slots = [(e.get("hw"), ezh), (e.get("paradigm"), ezh)]
    for s in e.get("subs") or []:
        slots += [(s.get("form"), s.get("zh") or ezh),
                  (s.get("paradigm"), s.get("zh") or ezh)]
    for txt, zh in slots:
        for m in T.TOK.finditer(txt or ""):
            k = T.key(m.group(0))
            home.setdefault(k, hw)
            tag.setdefault(k, tg)
            if zh:
                gl[k].add(zh)
    f = [e.get("hw"), e.get("paradigm"), e.get("tag")]
    for x in e.get("examples") or []:
        f.append(x.get("t"))
    for s in e.get("subs") or []:
        f += [s.get("form"), s.get("paradigm")]
        for x in s.get("examples") or []:
            f.append(x.get("t"))
    for y in f:
        for m in T.TOK.finditer(y or ""):
            occ[T.key(m.group(0))] += 1

MIN = int(sys.argv[2]) if len(sys.argv) > 2 else 3
rows = []
for tok in sorted(occ):
    if len(tok) < 4 or NAME.search(tag.get(tok) or ""):
        continue
    v = val(tok)
    if not v or V.get(v):
        continue                       # already vouched: nothing to fix
    if T.SPK.get(v, 0) or T.OMNI.get(v):
        continue                       # has a witness of its own
    hits = []
    for cand, how in variants(v):
        if cand == v:
            continue
        spk = T.SPK.get(cand, 0)
        if spk >= MIN or (T.OMNI.get(cand) and spk >= 1):
            hits.append((spk, cand, how, (T.OMNI.get(cand) or "-")[:34]))
    if hits:
        hits.sort(reverse=True)
        rows.append((occ[tok], tok, v, hits[:2], home.get(tok),
                     sorted(gl.get(tok, ()))[:1]))

rows.sort(key=lambda r: -r[0])
print("%d pale-with-no-witness values one mechanical stem alternation away "
      "from an attested word (%d occurrences)\n"
      % (len(rows), sum(r[0] for r in rows)))
lim = int(sys.argv[1]) if len(sys.argv) > 1 else 40
for n, tok, v, hits, hw, zhs in rows[:lim]:
    print("[%d] %-14s @%-11s -> %-14s  %s"
          % (n, tok, (hw or "?")[:11], v, (zhs[0] if zhs else "")[:40]))
    for spk, cand, how, g in hits:
        print("     %-14s spk %-4d  [%s]  %s" % (cand, spk, how, g))
