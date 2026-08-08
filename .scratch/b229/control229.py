# -*- coding: utf-8 -*-
"""Negative control for dom229.py (batch 209's rule: a ledger that cannot fail
is a list of excuses). Measures the page ONCE, then replays it through main()
with one assertion tampered at a time and requires each tamper to FAIL.

    python .scratch/b229/control229.py        # site served at :8765
"""
import copy
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "orthography", "logs"))
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dom229.json")

import dom229 as D  # noqa: E402

if os.path.exists(CACHE):
    BASE = json.load(io.open(CACHE, encoding="utf-8"))
else:
    BASE = D.measure()
    json.dump(BASE, io.open(CACHE, "w", encoding="utf-8"))

REAL = dict(MM=D.modern_map(), V=D.verified(), SRC=D.sources(),
            TXT=D.entries_strings(), IDS=D.audio_ids())
CONST = dict((k, getattr(D, k)) for k in dir(D) if k.isupper())


def run(dom=None, mm=None, v=None, src=None, txt=None, ids=None, **consts):
    for k, val in CONST.items():
        setattr(D, k, copy.deepcopy(val))
    for k, val in consts.items():
        setattr(D, k, val)
    D.measure = lambda: copy.deepcopy(dom or BASE)
    D.modern_map = lambda: copy.deepcopy(mm or REAL["MM"])
    D.verified = lambda: copy.deepcopy(v or REAL["V"])
    D.sources = lambda: copy.deepcopy(src or REAL["SRC"])
    D.entries_strings = lambda: (txt if txt is not None else REAL["TXT"])
    D.audio_ids = lambda: copy.deepcopy(ids or REAL["IDS"])
    out = io.StringIO()
    keep, sys.stdout = sys.stdout, out
    try:
        rc = D.main()
    finally:
        sys.stdout = keep
    return rc, out.getvalue()


def dom_with(**kw):
    d = copy.deepcopy(BASE)
    for k, f in kw.items():
        f(d[k])
    return d


def mm_with(**kw):
    m = copy.deepcopy(REAL["MM"])
    m.update(kw)
    return m


def v_with(drop=(), **kw):
    v = copy.deepcopy(REAL["V"])
    for k in drop:
        v.pop(k, None)
    v.update(kw)
    return v


def src_with(add=(), drop=(), gloss_drop=()):
    AM, AG, BG = copy.deepcopy(REAL["SRC"])
    for w, g in add:
        AM.add(w)
        AG[w] = [g]
    for w in drop:
        AM.discard(w)
    for w in gloss_drop:
        AG.pop(w, None)
        BG.pop(w, None)
    return AM, AG, BG


CASES = [
    ("baseline, untampered", dict(), 0),

    # 1. the metric
    ("denominator moved", dict(DENOM=5430), 1),
    ("floor raised above the measurement", dict(FLOOR=5400), 1),

    # 2. the map
    ("a ruling drifts to a third spelling",
     dict(mm=mm_with(**{"pk'kax": "pkkah"})), 1),
    ("the parenthetical's dark side moves", dict(mm=mm_with(**{"sm'lu": "smlu"})), 1),
    ("a deleted key comes back", dict(mm=mm_with(mman="mman")), 1),
    ("the char-rule assertion is wrong", dict(CHAR_INERT={"mman": "nnan"}), 1),

    # 3. the colours
    ("a ruled value renders pale",
     dict(dom=dom_with(unv=lambda u: u.update({"phqili": 2}))), 1),
    ("a ruled value renders nowhere",
     dict(dom=dom_with(seen=lambda s: s.pop("smalu", None))), 1),
    ("a ruled value still sole-blocks",
     dict(dom=dom_with(sole=lambda s: s.update({"emaan": 3}))), 1),
    ("a ruled value leaves verified.js", dict(v=v_with(drop=("uri",))), 1),
    ("the two-word value loses its joined key", dict(v=v_with(drop=("ini ku",))), 1),

    # 4. the code-6 hand check
    ("pqlqah changes rung", dict(v=v_with(pqlqah=1)), 1),
    ("the rung-6 root loses its gloss", dict(src=src_with(gloss_drop=("qlqah",))), 1),
    ("a ruled value leaves the register", dict(src=src_with(drop=("phqili",))), 1),
    ("sluun loses the second sense", dict(src=src_with(gloss_drop=("sluun",))), 1),

    # 5. the refusal, both halves
    ("the refused word is now listed", dict(src=src_with(add=(("qntqdan", "捆綁"),))), 1),
    ("the refused word goes dark",
     dict(dom=dom_with(unv=lambda u: u.pop("qntqdan", None))), 1),
    ("an -an of the syncopated stem appears",
     dict(src=src_with(add=(("qnstqdan", "x"),))), 1),
    ("the sister slot leaves the register", dict(src=src_with(drop=("qntqitan",))), 1),
    ("his 捆綁 carriers fall below the floor", dict(BKUY_FLOOR=99), 1),
    ("a 捆綁 carrier spells his own stem",
     dict(src=src_with(add=(("qtdun", "捆綁"),))), 1),
    ("his 受苦 family turns up glossed 殺",
     dict(src=src_with(add=(("prqilun", "殺"),))), 1),

    # 6. the reverted freeze
    ("the nguy freeze is back in verified.js", dict(v=v_with(nguy=1)), 1),
    ("nguy renders again",
     dict(dom=dom_with(seen=lambda s: s.update({"nguy": 1}))), 1),

    # 7. the slots that must not move
    ("a HOLD slot is re-ruled", dict(mm=mm_with(nagwi="gneeguy")), 1),
    ("the furniture value turns up in a .truku box",
     dict(dom=dom_with(inTruku=lambda t: t.update({"uru": 1}))), 1),

    # 8. his page
    ("a patched sentence changed",
     dict(txt=REAL["TXT"].replace("ka Wilang mo ole", "ka Wilang mo olo")), 1),
    ("a corrected reading is back in his text",
     dict(txt=REAL["TXT"] + "\nIni ko bi stama ana mman ka yako"), 1),
    ("the spaced-ini-ko count collapses", dict(SPACED_FLOOR=999), 1),
    ("a second joined iniko appears",
     dict(txt=REAL["TXT"] + "\nkika iniko sk'la"), 1),

    # 9. audio
    ("an audio id was minted",
     dict(ids=set(REAL["IDS"]) | {"ex_new_clip"}), 1),
    # re-minting holds the COUNT, so the count assertion cannot see it -- swap
    # rather than drop, or the case is proving the wrong assertion
    ("a corrected example was re-minted (count unchanged)",
     dict(ids=(set(REAL["IDS"]) - {"ex_ini_ko_bi_stama_ana_mman_ka_yako"})
          | {"ex_ini_ko_bi_stama_ana_maan_ka_yako"}), 1),
]

bad = 0
for name, kw, want in CASES:
    rc, out = run(**kw)
    got = "FAIL" if rc else "pass"
    okmark = "ok " if rc == want else "BAD"
    if rc != want:
        bad += 1
    line = [l for l in out.splitlines() if l.startswith("FAIL")]
    print("%s %-48s -> %s   %s" % (okmark, name, got,
                                   (line[0][5:70] if line else "")))

print("\n%d cases, %d wrong" % (len(CASES), bad))
sys.exit(1 if bad else 0)
