# -*- coding: utf-8 -*-
"""sharp124, but judged against the claimed word's FAMILY.

Batch 124 hand-rejected five of seven new claims and they were all one shape:
THE OMNIBUS'S GLOSS FOR A BARE ROOT RECORDS A HOMONYM OR A NARROW SENSE, NOT THE
ROOT'S MEANING.  banah is glossed 人名（男）while embanah 183x is 紅色的; narux is
心傷 while mnarux 271x is 生病；病痛; mgealu is 像…延長線一樣 while gnealu 50x is
恩典慈愛.  Comparing his Chinese with ONE gloss of ONE word therefore produces a
false alarm whenever the lexicographer's pick for the bare form was not the
sense he meant.

So the test moves up a level: a claim is only suspicious if NOTHING IN THE
CLAIMED ROOT'S WHOLE FAMILY carries his sense.  That kills the five for free and
buys the room to drop the near-shape threshold from 0.60 to 0.55, which the old
filter could not afford.

Prints, for every survivor, the family size that was searched — so a claim
resting on a one-word family can be read for what it is.
"""
import collections, difflib, io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = r"C:\dev\formosan\seediq\taroko-pecoraro"
sys.path.insert(0, os.path.join(H, "tools", "orthography"))
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

# every omnibus word indexed by the substrings of length >= 4 it contains,
# so a root's family can be pulled without knowing where the seam is
SUB = collections.defaultdict(set)
for w in GL:
    for n in range(len(w) - 3):
        for m in range(n + 4, len(w) + 1):
            SUB[w[n:m]].add(w)


def core(v):
    """the longest PRE-strip that still leaves something root-shaped"""
    best = v
    for p in sorted(PRE, key=len, reverse=True):
        if p and v.startswith(p) and len(v) - len(p) >= 4:
            return v[len(p):]
    return best


def family(v):
    c = core(v)
    fam = set(SUB.get(c, ()))
    fam |= set(SUB.get(v, ()))
    fam.add(v)
    return fam


gl = collections.defaultdict(set)
occ = collections.Counter()
home = {}
for e in T.entries():
    tag = (e.get("tag") or "").lower()
    hw = e.get("hw") or "?"
    ezh = e.get("zh") or ""
    frozen = "name" in tag or "emprunt" in tag
    slots = [(e.get("hw"), ezh), (e.get("paradigm"), ezh)]
    for s in e.get("subs") or []:
        slots += [(s.get("form"), s.get("zh") or ezh),
                  (s.get("paradigm"), s.get("zh") or ezh)]
    for txt, zh in slots:
        if not txt:
            continue
        for m in T.TOK.finditer(txt):
            k = T.key(m.group(0))
            if frozen or not zh or VOID.match(zh) or len(han(zh)) < 2:
                continue
            gl[k].add(zh)
            home.setdefault(k, hw)
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

RATIO = float(sys.argv[2]) if len(sys.argv) > 2 else 0.55
rows = []
killed = 0
for token in sorted(gl):
    v = val(token)
    if not v or len(token) < 4 or V.get(v) != 1:
        continue
    vg = GL.get(v)
    if not vg or shares(vg, sorted(gl[token])):
        continue
    fam = family(v)
    famgl = set()
    for w in fam:
        famgl |= GL.get(w, set())
    if shares(famgl, sorted(gl[token])):
        killed += 1
        continue                       # the root's family DOES carry his sense
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
print("%d claims survive the FAMILY test (%d occurrences); %d killed because "
      "the claimed root's own family carries his sense\n"
      % (len(rows), sum(r[0] for r in rows), killed))
lim = int(sys.argv[1]) if len(sys.argv) > 1 else 40
for n, tok, v, hits, hw, zhs, fs in rows[:lim]:
    print("[%d] %-14s @%-11s claims %-12s = %s   (family %d)"
          % (n, tok, (hw or "?")[:11], v,
             "; ".join(sorted(GL.get(v, ["-"])))[:26], fs))
    print("     his: %s" % "; ".join(zhs)[:76])
    for r, spk, w, s, g in hits:
        print("     -> %-14s %.2f spk %-4d «%s» %s" % (w, r, spk, s, g))
