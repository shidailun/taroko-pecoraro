# -*- coding: utf-8 -*-
"""Negative control for `logs/dom231.py` (batch 231).

A log that cannot fail is a list of excuses. Every assertion in dom231 is fed a
tampered world here and required to REFUSE it, plus positive controls that must
still pass: the untampered run, and a run with the ILRDF parquets unplugged
(a missing corpus is a skip, not a failure -- the map is not wrong because a
drive is unmounted).

The DOM is measured ONCE and replayed from cache, so this costs one browser.

    python .scratch/b231/control231.py
"""
import copy
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.join("tools", "orthography", "logs"))
import dom231 as D                                          # noqa: E402

CACHE = os.path.join(".scratch", "b231", "dom231_dom.json")
if os.path.exists(CACHE):
    DOM = json.load(io.open(CACHE, encoding="utf-8"))
else:
    DOM = D.measure()
    json.dump(DOM, io.open(CACHE, "w", encoding="utf-8"))

REAL = {k: getattr(D, k) for k in
        ("measure", "modern_map", "verified", "sources", "entries_strings",
         "his_tokens", "his_headwords", "entries_json", "audio_ids",
         "parquet_counts", "char_rules", "HERE")}
MM0, V0 = D.modern_map(), D.verified()
AM0, AG0, BG0, PG0 = D.sources()
TXT0, CNT0 = D.entries_strings(), D.his_tokens()
HEAD0, ENT0, IDS0 = D.his_headwords(), D.entries_json(), D.audio_ids()
PQ0 = D.parquet_counts()


def run():
    buf = io.StringIO()
    old, sys.stdout = sys.stdout, buf
    try:
        rc = D.main()
    finally:
        sys.stdout = old
    return rc, buf.getvalue()


def case(name, expect_fail=True, **patch):
    for k, v in REAL.items():
        setattr(D, k, v)
    D.measure = lambda: copy.deepcopy(DOM)
    for k, v in patch.items():
        setattr(D, k, v)
    rc, out = run()
    ok = (rc != 0) if expect_fail else (rc == 0)
    line = next((l for l in out.splitlines() if l.startswith("FAIL")), "")
    print("%-4s %-46s %s" % ("ok" if ok else "BAD", name,
                             line[5:100] if expect_fail else
                             out.strip().splitlines()[-1]))
    return ok


def dom(**over):
    d = copy.deepcopy(DOM)
    for k, v in over.items():
        if isinstance(v, dict):
            d[k].update(v)
        else:
            d[k] = v
    return lambda: d


def dom_del(bucket, key):
    d = copy.deepcopy(DOM)
    d[bucket].pop(key, None)
    return lambda: d


def mm(**over):
    m = dict(MM0)
    m.update(over)
    return lambda: m


def ver(drop=(), **over):
    v = dict(V0)
    for k in drop:
        v.pop(k, None)
    v.update(over)
    return lambda: v


def src(am_add=(), gloss=None):
    am = set(AM0) | set(am_add)
    ag = dict(AG0)
    if gloss:
        ag.update(gloss)
    return lambda: (am, ag, BG0, PG0)


def tmp_logs(strip):
    """A copy of the logs dir with a citation string removed."""
    d = os.path.join(".scratch", "b231", "cited_" + str(abs(hash(strip)) % 9999))
    if not os.path.isdir(d):
        os.makedirs(d)
    for b in ("dom219.py", "b57.py"):
        s = io.open(os.path.join(REAL["HERE"], b), encoding="utf-8").read()
        io.open(os.path.join(d, b), "w", encoding="utf-8").write(
            s.replace(strip, "REDACTED"))
    return d


n = ok = 0
CASES = [
    # --- positive controls
    ("POSITIVE untampered", False, {}),
    ("POSITIVE parquets unplugged -> skip, not fail", False,
     dict(parquet_counts=lambda: None)),

    # --- 1. the rulings themselves
    ("map reverted to his own letters", True,
     dict(modern_map=mm(kasayang="kasayang"))),
    ("map drifted to a third spelling", True,
     dict(modern_map=mm(isoka="isu kaa"))),
    ("value re-joined into one word", True,
     dict(modern_map=mm(kasayang="kasayanga"))),
    ("map entry deleted outright", True,
     dict(modern_map=lambda: dict((k, v) for k, v in MM0.items()
                                  if k != "isoka"))),
    ("a PART of the value left verified.js", True,
     dict(verified=ver(drop=("sayang",)))),
    ("a part demoted to an inferred code", True, dict(verified=ver(isu=7))),
    ("the joined string renders again", True,
     dict(measure=dom(seen={"isuka": 3}))),
    ("char rules stopped spelling the join (no-op pin)", True,
     dict(char_rules=lambda w: "zzz")),

    # --- 2. the colours the ruling bought
    ("the ruled value renders pale", True,
     dict(measure=dom(unv={"ka sayang": 2}))),
    ("the ruled value renders green", True,
     dict(measure=dom(raw={"isu ka": 1}))),
    ("the ruled value sole-blocks again", True,
     dict(measure=dom(sole={"ka sayang": 4}))),
    ("the ruled value is furniture only (no .truku)", True,
     dict(measure=dom_del("inTruku", "isu ka"))),

    # --- 3. his book
    ("his sentence was reworded", True,
     dict(entries_strings=lambda: TXT0.replace("Malu kasayang da", "Malu da"))),
    ("his parenthetical was tidied away", True,
     dict(entries_strings=lambda: TXT0.replace("iso ka (isoka)", "iso ka"))),
    ("a frequency floor FELL", True,
     dict(his_tokens=lambda: dict(CNT0, sayang=9))),
    ("the join stopped being a hapax", True,
     dict(his_tokens=lambda: dict(CNT0, isoka=4))),
    ("a second ka+ join appeared", True,
     dict(his_tokens=lambda: dict(CNT0, kaiso=1, **{"iso": CNT0["iso"]}))),
    ("the card exclusion lost its subject", True,
     dict(his_headwords=lambda: HEAD0 - {"kaya"})),

    # --- 4. the record
    ("dom219's refusal string was deleted", True,
     dict(HERE=tmp_logs('"isuka": "蓋住 is spuy'))),
    ("b57's identity pin was deleted", True,
     dict(HERE=tmp_logs('"kasayang": "kasayang"'))),

    # --- 5. the outside voice
    ("the parquets now carry the JOINED form", True,
     dict(parquet_counts=lambda: dict(PQ0 or {}, kasayang=2))),
    ("the split count fell below its floor", True,
     dict(parquet_counts=lambda: dict(PQ0 or {}, **{"ka sayang": 12}))),
    ("his own frame vanished from the corpus", True,
     dict(parquet_counts=lambda: dict(PQ0 or {}, frame=0))),

    # --- 6. the refusals
    ("a refused word went dark with nobody ruling it", True,
     dict(measure=dom_del("unv", "yianu"))),
    ("sruweq stopped being green (a map entry appeared)", True,
     dict(measure=dom_del("raw", "sruweq"))),
    ("his Yamo was remapped", True, dict(modern_map=mm(yamo="yianu"))),
    ("a y..nu form entered the register", True,
     dict(sources=src(am_add=("yianu",)))),
    ("a 2pl form left the register", True,
     dict(sources=lambda: (AM0 - {"jyamu"}, AG0, BG0, PG0))),
    ("週期 acquired a carrier", True,
     dict(sources=src(gloss={"qqrus": ["週期性的"]}))),
    ("a 反覆 carrier came within reach of urang", True,
     dict(sources=src(gloss={"urung": ["反覆發生"]}))),

    # --- 7. the unglossed limit
    ("SLOWEQ acquired a gloss", True,
     dict(entries_json=lambda: [dict(e, fr="Fatigue.") if e.get("hw") == "SLOWEQ"
                                else e for e in ENT0])),
    ("the unglossed class changed size", True,
     dict(entries_json=lambda: [dict(e, fr="??") if e.get("hw") == "PARO"
                                else e for e in ENT0])),
    ("sruweq's price changed", True, dict(measure=dom(sole={"sruweq": 5}))),

    # --- 8. the metric and the audio
    ("the metric FELL below the floor", True,
     dict(measure=dom(ok=DOM["ok"] - 1))),
    ("the denominator moved", True, dict(measure=dom(tot=DOM["tot"] + 3))),
    ("an audio id was re-minted", True,
     dict(audio_ids=lambda: set(list(IDS0)[:-1]))),
]

for name, ef, patch in CASES:
    n += 1
    ok += case(name, ef, **patch)

print("\n%d/%d controls behaved (%d tampers refused, 2 positive)"
      % (ok, n, n - 2))
sys.exit(0 if ok == n else 1)
