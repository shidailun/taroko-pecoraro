# -*- coding: utf-8 -*-
"""The sharp end of claimaudit2: where the dictionary literally has his word.

boyaq is the shape to look for.  His BOYAQ is 山豬, the map claims buyak
動物肢解, and the omnibus has bowyak glossed 山豬 — 242 spoken.  Not "shares a
character": the same gloss.

So: a LISTED claim whose value's gloss shares nothing with the entry's, where
some attested near-shape carries one of his gloss segments WHOLE (or he carries
its gloss whole), and that word is said.  Segment = split on the punctuation he
and the omnibus both use, so 山豬 out of "山豬。" and 松樹 out of "松樹－富含…".
"""
import collections, difflib, io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = r"C:\dev\formosan\seediq\taroko-pecoraro"
sys.path.insert(0, os.path.join(H, "tools", "orthography"))
sys.path.insert(0, ".")
import tables as T

V = dict((m.group(1), int(m.group(2))) for m in re.finditer(
    r'^  "(.*)": (\d),$', io.open(os.path.join(H, "site", "verified.js"),
                                  encoding="utf-8").read(), re.M))
HAN = re.compile(r"[\u4e00-\u9fff]")
STOP = set("的了是在和與或人事物東西樣子個們不無沒有為之其此")
SPLIT = re.compile(r"[；;，,。．\-—－–、（）()〔〕\[\]？?！!／/：:\s]+")
VOID = re.compile(r"^\s*[（(]?\s*(同上|見|參見|同前|詞根不明|參照|＝|=|\?|？|上列|前一詞)")


def han(g):
    return set(HAN.findall(g or "")) - STOP


TAIL = re.compile(r"[的地得者之過了]+$")


def segs(g):
    """meaning-bearing segments: 2-4 Han characters, nothing else in them.

    His glosses are adjectival where the omnibus's are bare -- SDAMAT is
    思念的 and csdamat is 思念 -- so the whole-segment test failed on one
    trailing 的 and left a dark claim on 菜；菜酥 standing.  Strip his tail and
    keep BOTH forms."""
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

rows = []
for token in sorted(gl):
    v = val(token)
    if not v or len(token) < 4 or V.get(v) != 1:
        continue
    vg = GL.get(v)
    if not vg or shares(vg, sorted(gl[token])):
        continue
    mine = set()
    for zh in gl[token]:
        mine |= segs(zh)
    hits = []
    base = token.replace("'", "")
    for s in mine:
        for w in by_seg.get(s, ()):
            if w == v or w == token:
                continue
            r = difflib.SequenceMatcher(None, base, w).ratio()
            if r >= 0.6:
                hits.append((round(r, 2), T.SPK.get(w, 0), w, s,
                             "; ".join(sorted(GL[w]))[:26]))
    if hits:
        hits.sort(reverse=True)
        rows.append((occ[token], token, v, "; ".join(sorted(vg))[:24],
                     hits[:3], home.get(token), sorted(gl[token])))

rows.sort(key=lambda r: -r[0])
print("%d claims where an attested near-shape carries his gloss WHOLE"
      " (%d occurrences)\n" % (len(rows), sum(r[0] for r in rows)))
for n, token, v, vgl, hits, hw, zhs in rows[:int(sys.argv[1]) if len(sys.argv) > 1 else 40]:
    print("[%d] %-13s @%-11s claims %-12s = %s" % (n, token, (hw or "?")[:11], v, vgl))
    print("     his: %s" % "; ".join(zhs)[:74])
    for r, spk, w, s, g in hits:
        print("     -> %-13s %.2f spk %-4d  «%s»  %s" % (w, r, spk, s, g))
