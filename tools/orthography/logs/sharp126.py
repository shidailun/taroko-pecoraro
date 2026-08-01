# -*- coding: utf-8 -*-
"""The family test, aimed at the PALE half — and with a root-finder that works.

sharp125 killed 500 of 538 dark claims by asking whether the CLAIMED ROOT'S
FAMILY carries his sense rather than whether one gloss of one word does.  Its
family lookup was crude: it stripped a PRE prefix and then took every omnibus
word containing what was left, so it found nothing for rmajing (the -m- is an
INFIX, not a prefix) and passed a claim the family prajing 72x 開始 / psrajing
起火 / mtrajing 青春期 plainly refutes.  roots() here yields every candidate:
prefix-stripped, infix-stripped (C-m-/C-n-), reduplication-stripped.

Aimed at pale, the test reads the other way round and separates the two things
the pale mass is made of:
  family CARRIES his sense  -> the value is probably RIGHT and merely
      unverified.  That is the PAUX shape (paux 6x is glossed 犁田, one
      specialised sense, while mknpaux 反過來 and mspaux 會翻 say the root is
      his 翻轉) and it is a verification question, not a map question.
  family is SILENT          -> the stem is probably WRONG, and if a near-shape
      carries his gloss whole that near-shape is the candidate.
Only the second set can be fixed by editing the map, so only it is printed.
"""
import collections, difflib, io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = r"C:\dev\formosan\seediq\taroko-pecoraro"
D = os.path.join(H, "tools", "orthography")
sys.path.insert(0, D)
sys.path.insert(0, ".")
import tables as T
from inflection import PRE

V = dict((m.group(1), int(m.group(2))) for m in re.finditer(
    r'^  "(.*)": (\d),$', io.open(os.path.join(H, "site", "verified.js"),
                                  encoding="utf-8").read(), re.M))
HAN = re.compile(r"[\u4e00-\u9fff]")
STOP = set("的了是在和與或人事物東西樣子個們不無沒有為之其此")
SPLIT = re.compile(r"[；;，,。．\-—－–、（）()〔〕\[\]？?！!／/：:\s]+")
VOID = re.compile(
    r"^\s*[（(]?\s*(同上|見|參見|同前|詞根不明|參照|＝|=|\?|？|上列|前一詞)")
TAIL = re.compile(r"[的地得者之過了]+$")
NAME = re.compile(r"name|emprunt|nom", re.I)


def han(g):
    return set(HAN.findall(g or "")) - STOP


def segs(g):
    out = set()
    for p in SPLIT.split(g or ""):
        p = p.strip()
        if 2 <= len(p) <= 5 and all(HAN.match(c) for c in p) and han(p):
            b = TAIL.sub("", p)
            if 2 <= len(p) <= 4:
                out.add(p)
            if 2 <= len(b) <= 4 and han(b):
                out.add(b)
    return out


def shares(gs, zhs):
    for g in gs:
        gh = han(g)
        for zh in zhs:
            zc = han(zh)
            if len(gh & zc) >= 2:
                return g
            if gh and len(gh) <= 2 and gh <= zc:
                return g
            for n in range(len(g) - 1):
                if HAN.match(g[n:n + 1]) and g[n:n + 2] in zh:
                    return g
    return None


def val(w):
    k = T.key(w)
    return T.CL.get(k) or T.OV.get(k) or T.MAP.get(k) or T.crule(k)


def roots(v):
    """every string the value could be built on: prefix-, infix- and
    reduplication-stripped, longest first"""
    out = set()
    for p in PRE:
        if p and v.startswith(p) and len(v) - len(p) >= 3:
            out.add(v[len(p):])
    # C-m- / C-n- infix: smriyu -> sriyu, rmajing -> rajing
    for n in (1, 2):
        if len(v) > n + 3 and v[n] in "mn":
            out.add(v[:n] + v[n + 1:])
    # CV- and CVC- reduplication: llabang -> labang, kkbanah -> kbanah
    if len(v) > 4 and v[0] == v[1]:
        out.add(v[1:])
    if len(v) > 5 and v[:2] == v[2:4]:
        out.add(v[2:])
    out.add(v)
    return set(x for x in out if len(x) >= 3)


GL = collections.defaultdict(set)
for w, g in T.OMNI.items():
    if g:
        GL[w].add(g)
by_seg = collections.defaultdict(set)
for w, gs in GL.items():
    if T.SPK.get(w, 0) < 3:
        continue
    for g in gs:
        for s in segs(g):
            by_seg[s].add(w)

SUB = collections.defaultdict(set)
for w in GL:
    for n in range(len(w) - 2):
        for m in range(n + 3, len(w) + 1):
            SUB[w[n:m]].add(w)


def family(v):
    fam = set()
    for r in roots(v):
        fam |= SUB.get(r, set())
    fam.add(v)
    return fam


gl = collections.defaultdict(set)
occ = collections.Counter()
home, tag = {}, {}
for e in T.entries():
    tg = (e.get("tag") or "")
    hw = e.get("hw") or "?"
    ezh = e.get("zh") or ""
    slots = [(e.get("hw"), ezh), (e.get("paradigm"), ezh)]
    for s in e.get("subs") or []:
        slots += [(s.get("form"), s.get("zh") or ezh),
                  (s.get("paradigm"), s.get("zh") or ezh)]
    for txt, zh in slots:
        if not txt:
            continue
        for m in T.TOK.finditer(txt):
            k = T.key(m.group(0))
            home.setdefault(k, hw)
            tag.setdefault(k, tg)
            if not zh or VOID.match(zh) or len(han(zh)) < 2:
                continue
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

RATIO = float(sys.argv[2]) if len(sys.argv) > 2 else 0.6
rows = []
vouched = 0
for token in sorted(gl):
    if NAME.search(tag.get(token) or ""):
        continue
    v = val(token)
    if not v or len(token) < 4 or V.get(v):
        continue                       # dark: sharp125's territory
    fam = family(v)
    famgl = set()
    for w in fam:
        famgl |= GL.get(w, set())
    if shares(famgl, sorted(gl[token])):
        vouched += 1
        continue                       # PAUX shape: right stem, unverified
    mine = set()
    for zh in gl[token]:
        mine |= segs(zh)
    hits = []
    base = token.replace("'", "")
    for s in mine:
        for w in by_seg.get(s, ()):
            if w == v or w == token or w in fam:
                continue
            r = difflib.SequenceMatcher(None, base, w).ratio()
            if r >= RATIO:
                hits.append((round(r, 2), T.SPK.get(w, 0), w, s,
                             "; ".join(sorted(GL[w]))[:26]))
    if hits:
        hits.sort(reverse=True)
        seen, keep = set(), []
        for h in hits:
            if h[2] in seen:
                continue
            seen.add(h[2])
            keep.append(h)
        rows.append((occ[token], token, v, keep[:3], home.get(token),
                     sorted(gl[token]), len(fam)))

rows.sort(key=lambda r: -r[0])
print("%d PALE values whose stem's family is SILENT on his sense, with a "
      "near-shape that carries it (%d occurrences)" % (len(rows),
                                                       sum(r[0] for r in rows)))
print("%d other pale values ARE vouched by their own family — the PAUX shape, "
      "a verification question not a map question\n" % vouched)
lim = int(sys.argv[1]) if len(sys.argv) > 1 else 40
for n, tok, v, hits, hw, zhs, fs in rows[:lim]:
    print("[%d] %-14s @%-11s pale on %-13s (family %d, silent)"
          % (n, tok, (hw or "?")[:11], v, fs))
    print("     his: %s" % "; ".join(zhs)[:76])
    for r, spk, w, s, g in hits:
        print("     -> %-14s %.2f spk %-4d «%s» %s" % (w, r, spk, s, g))
