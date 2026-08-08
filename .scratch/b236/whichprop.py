# -*- coding: utf-8 -*-
"""Which sentence-sweep proposal did batch 236 remove?

dom232's sweep iterates over PALE map values. Batch 236 darkened exactly one
previously-pale value (`teumuk` -> `towmuk`), so the 13 -> 12 drop should be
that proposal and nothing else. Re-run the sweep body with PALE pinned to the
single value: a proposal coming back is the count moving for the claimed
reason. Control: run it with PALE empty, which must yield nothing.

Needs no browser -- the sweep's other inputs are the corpus and entries.js.
"""
import collections, os, sys
sys.path.insert(0, os.path.join("tools", "orthography", "logs"))
sys.stdout.reconfigure(encoding="utf-8")
import dom232 as M

HAN, TOK, ed = M.HAN, M.TOK, M.ed
ENT = M.entries_json()
AM = M.sources()[0]
MM, VER = M.modern_map(), M.verified()


def modern(w):
    k = M.re.sub(r"[’ʼ\"ʔ]", "'", w).lower()
    return MM.get(k) or M.char_rules(k)


def sweep(PALE):
    CZ = M.corpus(with_zh=True)
    rows = [(ws, set(HAN.findall(zh))) for ws, zh in CZ if zh and HAN.search(zh)]
    byhan = collections.defaultdict(list)
    for i, (_, hs) in enumerate(rows):
        for h in hs:
            byhan[h].append(i)
    his_rows = []

    def ex(e):
        for x in (e.get("examples") or []):
            t, zh = x.get("t") or "", x.get("zh") or ""
            if t and zh and HAN.search(zh):
                for w in TOK.findall(t):
                    if modern(w) in PALE:
                        his_rows.append((modern(w), set(HAN.findall(zh))))
        for sb in (e.get("subs") or []):
            ex(sb)
    for e in ENT:
        ex(e)
    props = set()
    for val, hs in his_rows:
        if not hs:
            continue
        cand = collections.Counter()
        for h in hs:
            for i in byhan.get(h, ()):
                cand[i] += 1
        best = None
        for i, sh in cand.items():
            if sh < 2:
                continue
            ws, chs = rows[i]
            c = sh / float(min(len(hs), len(chs)))
            if c < 0.60:
                continue
            for w in ws:
                if w == val or w in PALE or w not in AM:
                    continue
                e2 = ed(val, w)
                if e2 > 2 or e2 >= max(2, len(val) - 2):
                    continue
                if best is None or (-e2, c) > best[0]:
                    best = ((-e2, c), val, w)
        if best:
            props.add((best[1], best[2]))
    return props


print("teumuk alone :", sorted(sweep({"teumuk"})))
print("control, none:", sorted(sweep(set())))
print("towmuk now   :", sorted(sweep({"towmuk"})), "(dark, so not swept live)")

# --- isolate batch 236 exactly ------------------------------------------
# PALE offline == map values with no verified.js entry. That is an
# APPROXIMATION of the DOM set (blind to CITE_SPELL and WORD_OVERRIDES,
# batch 230), but both sides use the same approximation, so the DIFF is
# what batch 236 did and nothing else. Validated below by the count.
def pale_of(mm, ver):
    return set(v for v in mm.values() if not all(p in ver for p in v.split()))

now_mm, now_ver = dict(MM), set(VER)
old_mm, old_ver = dict(MM), set(VER)
old_mm["teumuk"] = "teumuk"
old_mm["txoulang"] = "thulang"
old_mm["mpatxoulang"] = "empathulang"
old_ver -= {"empthowlang", "thowlang", "towmuk"}
old_ver |= {"empathulang", "thulang"}

import types
def with_map(mm):
    global MM
    MM = mm
    return sweep(pale_of(mm, old_ver if mm is old_mm else now_ver))

p_now = with_map(now_mm)
p_old = with_map(old_mm)
print()
print("offline props  now=%d  before=%d" % (len(p_now), len(p_old)))
print("  LOST :", sorted(p_old - p_now))
print("  GAINED:", sorted(p_now - p_old))
